import os
import threading
import socket
import argparse
import math
import time
import json
from pythonosc import dispatcher
from pythonosc import osc_server
from pylsl import StreamInfo, StreamOutlet
from http.server import HTTPServer, BaseHTTPRequestHandler

IP_HRV = "127.0.0.1"
PORT_HRV = 80
CHNS_HRV = 1
SAMPLE_RATE = 10

# create seperate thread class for server processes
class ServerThreadHRV(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    
    def run(self):
        print("Starting server thread", self.threadID)
        
        httpd = HTTPServer(("132.239.235.116", PORT_HRV), ServerHRV)
        httpd.serve_forever()
        

class ServerHRV(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Received GET")
    
    def do_POST(self):
        print(self.headers)
        body_json = self.rfile.read(int(self.headers['Content-Length']))
        body = json.loads(body_json)
        new_sample = [body['logs'][0]['rr']]
        print(body)
        print("SAMPLE:", new_sample)
        outlet_hrv.push_sample(new_sample)
        global rr_init, rr_min, rr_max, rr_last 
        if (not rr_init):
            rr_min = body['logs'][0]['rr']
            rr_max = rr_min
            rr_init = True

        for sample in body['logs']:
            if (sample['rr'] < rr_min):
                self.rr_min = sample['rr']
            if (sample['rr'] > rr_max):
                rr_max = sample['rr']
            rr_last = sample['rr']
        

        client.send('{},{},{}'.format(rr_min, rr_max, rr_last).encode('utf-8'));


rr_init = False

# Setup outlet stream infos
stream_info_hrv = StreamInfo('HRV', 'EEG', CHNS_HRV, SAMPLE_RATE, 'float32', 'hrvid_1')
channels = stream_info_hrv.desc().append_child("channels")
channels.append_child('rr')

# Create outlets
outlet_hrv = StreamOutlet(stream_info_hrv)

print("Outlets created")

# Connect as a client to Unity tcp server
# UNCOMMENT WHEN USING IN UNITY
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP_HRV, 12346))

# Start listening for data
server_thread_hrv = ServerThreadHRV(2)
server_thread_hrv.daemon = True
server_thread_hrv.start()

print("Listening for data")

while True:
    continue
