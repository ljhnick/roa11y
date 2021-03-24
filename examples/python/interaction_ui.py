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

    def actuate(self, flag=None, u=0):
        actuate_addr = "/actuate"
        url = self.url + actuate_addr

        if u >= 0:
            speed = 1023*u
        elif u < 0:
            speed = -u*1023 + 1023
        else:
            speed = 0

        if flag == 1:
            data = {"id":"5", "speed":"1023"}
        elif flag == 2:
            data = {"id": "5", "speed": "2047"}
        elif flag == 0:
            data = {"id": "5", "speed": str(speed)}
        else:
            data = {"id":"5", "speed":"0"}

        response, content = self.http.request(url, "POST", headers=self.headers, body=json.dumps(data))
        print(response)

        return response

    def control_profile(self, profile):
        u_t = json.loads(profile)
        num = len(u_t)
        i = 0
        while i < num-1:
            t0 = u_t[i]["x"]
            t1 = u_t[i+1]["x"]

            t = t1-t0
            u = u_t[i]["y"]
            self.actuate(0, u)
            time.sleep(t)
            i += 1

        self.actuate(0, 0)
        time.sleep(1)
        self.actuate(0, 0)

    def actuate_object(self):
        object_rfid = RFID()
        object = object_rfid.read_card()
        object = json.loads(object)['ID']

        profile_str = json.loads(object_rfid.control_profile)

        object_profile = profile_str[object]
        # object_profile = None #to be updated
        self.control_profile(object_profile)


    def __init__(self):
        self.http = httplib2.Http()
        self.url = "http://192.168.86.22"
        # self.url = "http://192.168.86.246:1880"
        self.headers = {"Content-Type": "application/json; charset=UTF-8"}

class RFID:
    # Reads the ID of the card uploaded to the server by the ESP
    def read_card(self):
        # read_addr = "/read_card"  # Address of the page with the javascript function that returns the ID
        read_addr = "/detect"
        url = self.url + read_addr
        response, content = self.http.request(url, "GET")
        print(content)  # Prints the content of the response
        return content

    # Pushes the data stored in "data.txt" to the server
    def push_data(self):
        write_addr = "/push_data"
        url = self.url + write_addr
        with open('data.txt') as json_file:
            data = json.load(json_file)
        response, content = self.http.request(url, "POST", headers=self.headers, body=json.dumps(data))

    def save_data(self, data):
        # here data is a stringified JSON
        object_id = self.read_card()
        object_id = json.loads(object_id)['ID']
        if object_id is not None:
            # self.object_data = {'id': object_id, 'data': data}
            existing_data = open("data.txt", "r").read()
            try:
                new_data = json.loads(existing_data)
                new_data[object_id] = data
            except:
                new_data = {object_id: {'data': data}}

            with open('data.txt', 'w') as outfile:
                json.dump(new_data, outfile)

    def send_data(self):
        object_id = self.read_card()
        object_id = json.loads(object_id)['ID']
        if object_id is not None:
            existing_data = open("data.txt", "r").read()
            dataJSON = json.loads(existing_data)
            data = dataJSON[object_id]
            return json.dumps(data)

    def __init__(self):
        self.http = httplib2.Http()
        # self.url = "http://192.168.97.62:1880"      # Replace this with the URL of the node-red server (if running locally, you can use http://localhost:1880).
        # self.url = "http://192.168.86.246:1880"
        self.url = "http://192.168.86.22"
        self.headers = {"Content-Type": "application/json; charset=UTF-8"}
        self.control_profile = open("data.txt", "r").read()

class CORSRequestHandler(SimpleHTTPRequestHandler):

    gripper = Gripper()
    rfid = RFID()

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
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_str = self.rfile.read(content_length)

        if post_str.split('|')[0] == 'test':
            self.gripper.control_profile(post_str.split('|')[1])
        elif post_str.split('|')[0] == 'save':
            self.rfid.save_data(post_str.split('|')[1])
        elif post_str.split('|')[0] == 'read':
            data_to_send = self.rfid.send_data()
            self.wfile.write(data_to_send)
        print(post_str)
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