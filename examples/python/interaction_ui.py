import os
from dynamixel_sdk import *
import time
import json
import numpy as np
import math
import httplib2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()

class Gripper:

    def detach(self):
        detach_addr = "/detach"
        url = self.url + detach_addr
        response, content = self.http.request(url, "GET")
        return response

    def actuate(self, flag=None):
        actuate_addr = "/actuate"
        url = self.url + actuate_addr

        if flag == 1:
            data = {"id":"5", "speed":"1023"}
        elif flag == 2:
            data = {"id": "5", "speed": "2047"}
        else:
            data = {"id":"5", "speed":"0"}

        response, content = self.http.request(url, "POST", headers=self.headers, body=json.dumps(data))

        return response

    def __init__(self):
        self.http = httplib2.Http()
        self.url = "http://192.168.86.22"
        self.headers = {"Content-Type": "application/json; charset=UTF-8"}

class CORSRequestHandler(SimpleHTTPRequestHandler):

    gripper = Gripper()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        return


def run(server_class=HTTPServer, handler_class=CORSRequestHandler, port=8090):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

    # BaseHTTPServer.test(handler_class, server_class)

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()