#!/usr/bin/env python

import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import bobzillapypi
import os
import socket
import socketserver
import threading
import time

UNIX_SOCKET = "/tmp/http.socket"

async def create_tunnel():
  # still alive?
  alive_task = loop.create_task(alive())

  # create session
  f = bobzillapypi.connect(metadata="python ses meta")
  await f
  session = f.result()
  print("session: {}".format(session))

  # create tunnel
  # f2 = session.start_tunnel(metadata="python tun meta", remote_addr="n.tcp.ngrok.io:nnnnn")
  f2 = session.start_tunnel(metadata="python tun meta")
  await f2
  tunnel = f2.result()
  print("tunnel: {}".format(tunnel))

  # f3 = tunnel.forward_tcp("localhost:9999")
  f3 = tunnel.forward_unix(UNIX_SOCKET)
  # await python_accept_loop(tunnel)
  await f3
  res = f3.result()
  print("res: {}".format(res))

async def alive():
  while (True):
    await asyncio.sleep(5)
    print("asyncio is alive")

async def python_accept_loop(tunnel):
  # accept loop
  while (True):
    # accept a new connection
    f3 = tunnel.accept()
    await f3
    conn = f3.result()
    print("conn: {}".format(conn))
  
    loop.create_task(async_wire_to_http(conn))
    # buffered_io(conn)
    # raw_io(conn)

async def async_wire_to_http(conn):
  # https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-client
  transport, protocol = await loop.create_connection(
    lambda: ClientProtocol(conn),
    "localhost", 9999)

  await wire_conn_reader(conn, transport)

class ClientProtocol(asyncio.Protocol):
  def __init__(self, conn):
    self.conn = conn

  def connection_made(self, transport):
    print("connection made")

  def data_received(self, data):
    print('Data received: {!r}'.format(data.decode()))
    self.conn.write(bytearray(data))

  def connection_lost(self, exc):
    print('The server closed the connection')

async def wire_conn_reader(conn, s):
  while (True):
    f = conn.recv(10)
    await f
    data = f.result()
    print("conn_read: {}: {}".format(len(data), data))
    if not data:
      print("wire_conn_reader: read channel closed")
      break
    size = s.write(bytes(data))
    if size == 0:
      print("wire_conn_reader: write channel closed")
      break

def buffered_io(conn):
  # The issue with Buffered*er is they use 'memoryview' which isn't implemented by pyo3.
  # Someone is trying to add it, but the maintainers don't sound super positive on it.
  # This month: https://github.com/PyO3/pyo3/pull/2792
  # Older: https://github.com/PyO3/pyo3/issues/617
  reader = io.BufferedReader(conn)
  writer = io.BufferedWriter(conn)
  while (True):
    data = reader.read1(10)
    print("data: {}: {}".format(type(data), data))
    writer.write(data)
    writer.flush()
    if not data:
      break

# Conn implements the RawIOBase interface:
#   https://docs.python.org/3/library/io.html#io.RawIOBase
# Might be useful to implement the Stream*er interfaces:
#   https://docs.python.org/3/library/asyncio-stream.html#streamreader
def raw_io(conn):
  while (True):
    read_buffer = bytearray(10)
    size = conn.readinto(read_buffer)
    print("read: {} buffer: {}".format(size, read_buffer))
    if size == 0:
      break

    write_buffer = bytearray()
    write_buffer.extend(read_buffer[:size])
    conn.write(write_buffer)

def start_http_server():
  httpd = HTTPServer(('localhost', 9999), BaseHTTPRequestHandler)
  # The issue with Conn pretending to be an INET socket is having a file descriptor
  # that the select loop can select on. possibly use an actual unix socket instead.
  # httpd.socket = tunnel 
  thread = threading.Thread(target=httpd.serve_forever, daemon=True)
  thread.start()

class UnixSocketHttpServer(socketserver.UnixStreamServer):
    def get_request(self):
        request, client_address = super(UnixSocketHttpServer, self).get_request()
        return (request, ["local", 0])

def start_unix_http_server():
  if os.path.exists(UNIX_SOCKET):
    os.remove(UNIX_SOCKET)
  httpd = UnixSocketHttpServer((UNIX_SOCKET), BaseHTTPRequestHandler)
  thread = threading.Thread(target=httpd.serve_forever, daemon=True)
  thread.start()

# start_http_server()
start_unix_http_server()
loop = asyncio.new_event_loop()
loop.run_until_complete(create_tunnel())
loop.close()

print("shutting down")
