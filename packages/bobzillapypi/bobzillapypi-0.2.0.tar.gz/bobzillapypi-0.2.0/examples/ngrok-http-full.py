#!/usr/bin/env python

import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import io
from bobzillapypi import NgrokSessionBuilder, log_level
import os
import socket
import socketserver
import threading
import time

UNIX_SOCKET = "/tmp/http.socket"

# enable logging
FORMAT = '%(asctime)-15s %(levelname)s %(name)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(5)
# log_level("TRACE")

def on_stop():
  print("on_stop")

def on_restart():
  print("on_restart")

def on_update(version, permit_major_version):
  print("on_update, version: {}, permit_major_version: {}".format(version, permit_major_version))

async def create_tunnel():
  # create builder
  builder = NgrokSessionBuilder()
  # create session
  session = (
    await builder.authtoken_from_env()
    .handle_stop_command(on_stop)
    .handle_restart_command(on_restart)
    .handle_update_command(on_update)
    .connect()
  )
  print("session: {}".format(session))

  # create tunnel
  # tunnel = await session.tcp_endpoint().metadata("python tun meta").remote_addr("n.tcp.ngrok.io:nnnnn").listen()
  tunnel = await session.http_endpoint().metadata("python tun meta").listen()
  print("tunnel: {}".format(tunnel.url()))

  # res = await tunnel.forward_tcp("localhost:9000")
  res = await tunnel.forward_pipe(UNIX_SOCKET)
  print("res: {}".format(res))

class HelloHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    body = bytes("<html><body>Hello</body></html>", "utf-8")
    self.protocol_version = "HTTP/1.1"
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.send_header("Content-Length", len(body))
    self.end_headers()
    self.wfile.write(body)

def start_http_server():
  httpd = HTTPServer(('localhost', 9000), HelloHandler)
  thread = threading.Thread(target=httpd.serve_forever, daemon=True)
  thread.start()

class UnixSocketHttpServer(socketserver.UnixStreamServer):
    def get_request(self):
        request, client_address = super(UnixSocketHttpServer, self).get_request()
        return (request, ["local", 0])

def start_unix_http_server():
  if os.path.exists(UNIX_SOCKET):
    os.remove(UNIX_SOCKET)
  httpd = UnixSocketHttpServer((UNIX_SOCKET), HelloHandler)
  thread = threading.Thread(target=httpd.serve_forever, daemon=True)
  thread.start()

# start_http_server()
start_unix_http_server()
loop = asyncio.new_event_loop()
loop.run_until_complete(create_tunnel())
loop.close()

print("shutting down")
