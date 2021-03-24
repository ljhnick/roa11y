import os
import json

import httplib2

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()


class RFID:
    # Reads the ID of the card uploaded to the server by the ESP
    def read_card(self):
        read_addr = "/read_card"                    # Address of the page with the javascript function that returns the ID 
        url = self.url + read_addr
        response, content = self.http.request(url, "GET")
        print(content)                              # Prints the content of the response
        return content
    
    # Pushes the data stored in "data.txt" to the server
    def push_data(self):
        write_addr = "/push_data"
        url = self.url + write_addr
        with open('data.txt') as json_file:
            data = json.load(json_file)
        response, content = self.http.request(url, "POST", headers=self.headers, body=json.dumps(data))
            
	
    def __init__(self):
        self.http = httplib2.Http()
        # self.url = "http://192.168.97.62:1880"      # Replace this with the URL of the node-red server (if running locally, you can use http://localhost:1880).
        self.url = "http://192.168.86.246:1880"
        self.headers = {"Content-Type": "application/json; charset=UTF-8"}


test = RFID()
print(test.url)
test.push_data()
test.read_card()
