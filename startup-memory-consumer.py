#!/usr/bin/env python3
"""
Usage:

    startup-memory-consumer [port]

Will listen on port 8080 if not specified.   

Use the following environment variables to configure startup
consumption behavior.

    STARTUP_CONSUME_MEBIBYTES
    STARTUP_CONSUME_SECONDS
    RUNTIME_CONSUME_MEBIBYTES
    RUNTIME_CONSUME_SECONDS

To consume memory on-demand, POST a payload such as the following.

    curl http://localhost:8080 -X POST -d '{"mebibytes": 1, "seconds": 3}'

"""
import os
import sys
import time
import ctypes
import gc
import logging
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread, Event


def consume_mem(number_of_bytes: int, seconds: int | None = None):
    logging.info(f"Consuming {number_of_bytes} bytes for {seconds} seconds...")
    buffer = ctypes.create_string_buffer(int(number_of_bytes))
    if seconds is None:
      Event().wait() # Wait forever
    time.sleep(seconds)
    buffer = None
    gc.collect(generation=0)
    logging.info(f"Consuming {number_of_bytes} bytes for {seconds} seconds...DONE")


def mebibytes_to_bytes(mebibytes: int) -> int:
    return mebibytes * 1024 * 1024


class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_response
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        try:
            post = json.loads(post_data)
            args_tuple=(mebibytes_to_bytes(post["mebibytes"]), post["seconds"])
            Thread(target=consume_mem, args=args_tuple).start()
        except:
            logging.error("Failed to consume memory!")
            pass

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def startup_consume() -> int:
    config = {
      "st_mib": os.getenv("STARTUP_CONSUME_MEBIBYTES", default="64"),
      "st_sec": os.getenv("STARTUP_CONSUME_SECONDS",   default="1"),
      "rt_mib": os.getenv("RUNTIME_CONSUME_MEBIBYTES", default="4"),
      "rt_sec": os.getenv("RUNTIME_CONSUME_SECONDS",   default=None),
    }
    for key, val in config.items():
        try:
            config[key] = float(val)
        except:
            config[key] = None
    Thread(target=consume_mem, args=(mebibytes_to_bytes(config["st_mib"]), config["st_sec"])).start()
    Thread(target=consume_mem, args=(mebibytes_to_bytes(config["rt_mib"]), config["rt_sec"])).start()


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting startup and base memory consumption...\n')
    startup_consume()
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        logging.info('Stopping httpd...\n')
        # TODO: implement clean termination
        os.kill(os.getpid(), 9)


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
