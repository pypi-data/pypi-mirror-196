# -*- coding: utf-8 -*-
# Minor change based on the example from hyper h2 server
# https://github.com/python-hyper/h2/blob/master/examples/asyncio/asyncio-server.py

"""
asyncio-server.py
~~~~~~~~~~~~~~~~~

A fully-functional HTTP/2 server using asyncio. Requires Python 3.5+.

This example demonstrates handling requests with bodies, as well as handling
those without. In particular, it demonstrates the fact that DataReceived may
be called multiple times, and that applications must handle that possibility.
"""
import asyncio
import io
import json
import ssl
import time
import os
import collections
from typing import List, Tuple

from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.events import (
    ConnectionTerminated, DataReceived, RemoteSettingsChanged,
    RequestReceived, StreamEnded, StreamReset, WindowUpdated
)
from h2.errors import ErrorCodes
from h2.exceptions import ProtocolError, StreamClosedError
from h2.settings import SettingCodes


RequestData = collections.namedtuple('RequestData', ['headers', 'data'])


class H2Protocol(asyncio.Protocol):
    def __init__(self):
        config = H2Configuration(client_side=False, header_encoding='utf-8')
        self.conn = H2Connection(config=config)
        self.transport = None
        self.stream_data = {}
        self.flow_control_futures = {}
        self.file_path = None
        self.num_sentence_received = {}
        self.raw_headers = None
        self.download_test_length = 2500000000
        self.out_bytes_per_second = 900

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        self.conn.initiate_connection()
        self.transport.write(self.conn.data_to_send())

    def connection_lost(self, exc):
        for future in self.flow_control_futures.values():
            future.cancel()
        self.flow_control_futures = {}

    def data_received(self, data: bytes):
        try:
            events = self.conn.receive_data(data)
        except ProtocolError as e:
            self.transport.write(self.conn.data_to_send())
            self.transport.close()
        else:
            self.transport.write(self.conn.data_to_send())
            for event in events:
                if isinstance(event, RequestReceived):
                    self.request_received(event.headers, event.stream_id)
                elif isinstance(event, DataReceived):
                    self.receive_data(event.data, event.stream_id)
                elif isinstance(event, StreamEnded):
                    self.stream_complete(event.stream_id)
                elif isinstance(event, ConnectionTerminated):
                    self.transport.close()
                elif isinstance(event, StreamReset):
                    self.stream_reset(event.stream_id)
                elif isinstance(event, WindowUpdated):
                    self.window_updated(event.stream_id, event.delta)
                elif isinstance(event, RemoteSettingsChanged):
                    if SettingCodes.INITIAL_WINDOW_SIZE in event.changed_settings:
                        self.window_updated(None, 0)

                self.transport.write(self.conn.data_to_send())

    def request_received(self, headers: List[Tuple[str, str]], stream_id: int):
        self.raw_headers = headers
        headers = collections.OrderedDict(headers)
        path = headers[':path']
        method = headers[':method']
        if method == "PUT" or method == "POST":
            self.file_path = os.path.join(os.path.curdir, path[1:])
            if os.path.exists(self.file_path):
                os.remove(self.file_path)

        # Store off the request data.
        request_data = RequestData(headers, io.BytesIO())
        self.stream_data[stream_id] = request_data

    def handle_request_echo(self, stream_id: int, request_data: RequestData):
        response_headers = [(':status', '200')]
        for i in self.raw_headers:
            # Response headers back and exclude pseudo headers
            if i[0][0] != ':':
                response_headers.append(i)
        body = request_data.data.getvalue().decode('utf-8')
        data = json.dumps(
            {"body": body}, indent=4
        ).encode("utf8")
        self.conn.send_headers(stream_id, response_headers)
        asyncio.ensure_future(self.send_data(data, stream_id))

    def stream_complete(self, stream_id: int):
        """
        When a stream is complete, we can send our response.
        """
        try:
            request_data = self.stream_data[stream_id]
        except KeyError:
            # Just return, we probably 405'd this already
            return

        path = request_data.headers[':path']
        method = request_data.headers[':method']
        if method == "PUT" or method == "POST":
            self.conn.send_headers(stream_id, [(':status', '200')])
            asyncio.ensure_future(self.send_data(
                str(self.num_sentence_received[stream_id]).encode(), stream_id))
        elif path == '/echo':
            self.handle_request_echo(stream_id, request_data)
        elif path == '/downloadTest':
            length = self.download_test_length
            self.conn.send_headers(
                stream_id, [(':status', '200'), ('content-length', str(length))])
            asyncio.ensure_future(self.send_repeat_data(length, stream_id))
        elif path == '/slowConnTest':
            length = int(self.download_test_length/1000)
            self.conn.send_headers(
                stream_id, [(':status', '200'), ('content-length', str(length))])
            asyncio.ensure_future(
                self.send_slow_repeat_data(length, stream_id))
        else:
            self.conn.send_headers(stream_id, [(':status', '404')])
            asyncio.ensure_future(self.send_data(b"Not Found", stream_id))

    def receive_data(self, data: bytes, stream_id: int):
        """
        We've received some data on a stream. If that stream is one we're
        expecting data on, save it off. Otherwise, reset the stream.
        """
        try:
            stream_data = self.stream_data[stream_id]
        except KeyError:
            self.conn.reset_stream(
                stream_id, error_code=ErrorCodes.PROTOCOL_ERROR
            )
        else:
            method = stream_data.headers[':method']
            if method == "PUT" or method == "POST":
                if stream_id in self.num_sentence_received:
                    self.num_sentence_received[stream_id] = self.num_sentence_received[stream_id] + \
                        len(data)
                else:
                    self.num_sentence_received[stream_id] = len(data)
                # update window for stream
                if len(data) > 0:
                    self.conn.increment_flow_control_window(len(data))
                    self.conn.increment_flow_control_window(
                        len(data), stream_id)
            else:
                stream_data.data.write(data)

    def stream_reset(self, stream_id):
        """
        A stream reset was sent. Stop sending data.
        """
        if stream_id in self.flow_control_futures:
            future = self.flow_control_futures.pop(stream_id)
            future.cancel()

    async def send_data(self, data, stream_id):
        """
        Send data according to the flow control rules.
        """
        while data:
            while self.conn.local_flow_control_window(stream_id) < 1:
                try:
                    await self.wait_for_flow_control(stream_id)
                except asyncio.CancelledError:
                    return

            chunk_size = min(
                self.conn.local_flow_control_window(stream_id),
                len(data),
                self.conn.max_outbound_frame_size,
            )

            try:
                self.conn.send_data(
                    stream_id,
                    data[:chunk_size],
                    end_stream=(chunk_size == len(data))
                )
            except (StreamClosedError, ProtocolError):
                # The stream got closed and we didn't get told. We're done
                # here.
                break

            self.transport.write(self.conn.data_to_send())
            data = data[chunk_size:]

    async def send_repeat_data(self, length, stream_id):
        """
        Send data with length according to the flow control rules.
        """
        while length > 0:
            while self.conn.local_flow_control_window(stream_id) < 1:
                try:
                    await self.wait_for_flow_control(stream_id)
                except asyncio.CancelledError:
                    return

            chunk_size = min(
                self.conn.local_flow_control_window(stream_id),
                length,
                self.conn.max_outbound_frame_size,
            )
            repeated = b"This is CRT HTTP test."
            data = int(chunk_size/len(repeated)) * repeated + \
                repeated[:chunk_size % len(repeated)]

            try:
                self.conn.send_data(
                    stream_id,
                    data,
                    end_stream=(chunk_size == length)
                )
            except (StreamClosedError, ProtocolError):
                # The stream got closed and we didn't get told. We're done
                # here.
                break

            self.transport.write(self.conn.data_to_send())
            length = length - chunk_size

    async def send_slow_repeat_data(self, length, stream_id):
        """
        Send data with length slowly (less than 1000 bytes per second)
        """
        while length > 0:
            while self.conn.local_flow_control_window(stream_id) < 1:
                try:
                    await self.wait_for_flow_control(stream_id)
                except asyncio.CancelledError:
                    return

            chunk_size = min(
                self.conn.local_flow_control_window(stream_id),
                length,
                self.conn.max_outbound_frame_size,
                self.out_bytes_per_second
            )
            repeated = b"This is CRT HTTP test."
            data = int(chunk_size/len(repeated)) * repeated + \
                repeated[:chunk_size % len(repeated)]

            try:
                # Sleep for a sec to make the out bytes per second slower than the expected
                time.sleep(1)
                self.conn.send_data(
                    stream_id,
                    data,
                    end_stream=(chunk_size == length)
                )
            except (StreamClosedError, ProtocolError):
                # The stream got closed and we didn't get told. We're done
                # here.
                break

            self.transport.write(self.conn.data_to_send())
            length = length - chunk_size

    async def wait_for_flow_control(self, stream_id):
        """
        Waits for a Future that fires when the flow control window is opened.
        """
        f = asyncio.Future()
        self.flow_control_futures[stream_id] = f
        await f

    def window_updated(self, stream_id, delta):
        """
        A window update frame was received. Unblock some number of flow control
        Futures.
        """
        if stream_id and stream_id in self.flow_control_futures:
            f = self.flow_control_futures.pop(stream_id)
            f.set_result(delta)
        elif not stream_id:
            for f in self.flow_control_futures.values():
                f.set_result(delta)

            self.flow_control_futures = {}


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.options |= (ssl.OP_NO_COMPRESSION)
ssl_context.load_cert_chain(
    certfile="../resources/unittests.crt", keyfile="../resources/unittests.key")
ssl_context.set_alpn_protocols(["h2"])

loop = asyncio.new_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(H2Protocol, '127.0.0.1', 3443, ssl=ssl_context)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
