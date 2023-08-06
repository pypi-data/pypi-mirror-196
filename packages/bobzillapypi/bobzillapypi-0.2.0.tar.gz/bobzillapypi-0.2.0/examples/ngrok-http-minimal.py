#!/usr/bin/env python

import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from bobzillapypi import NgrokSessionBuilder
import threading

async def create_tunnel():
  session = await NgrokSessionBuilder().authtoken_from_env().connect()
  tunnel = await session.http_endpoint().listen()
  print("tunnel: {}".format(tunnel.url()))
  res = await tunnel.forward_tcp("localhost:9000")

class HelloHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    body = bytes("Hello", "utf-8")
    self.protocol_version = "HTTP/1.1"
    self.send_response(200)
    self.send_header("Content-Length", len(body))
    self.end_headers()
    self.wfile.write(body)

def start_http_server():
  httpd = HTTPServer(('localhost', 9000), HelloHandler)
  thread = threading.Thread(target=httpd.serve_forever, daemon=True)
  thread.start()

start_http_server()
loop = asyncio.new_event_loop()
loop.run_until_complete(create_tunnel())
loop.close()
