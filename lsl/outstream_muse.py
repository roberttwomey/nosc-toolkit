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

# server params
IP_MUSE = "127.0.0.1"
PORT_MUSE = 6000
CHNS_MUSE = 22
SAMPLE_RATE = 10

# ocs callback handlers
def handle_all(address, *args):
    base = os.path.basename(address)
    if base in current_sample.keys():
        current_sample[base] = list(args)

# create seperate thread class for server processes
class ServerThreadMuse(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    
    def run(self):
        print("Starting server thread", self.threadID)
        
        # specify handlers
        disp = dispatcher.Dispatcher()
        disp.set_default_handler(handle_all)
        #dispatcher.map("/muse/elements/gamma_relative", handle_gamma_relative)

        # create server and begin to listen for data
        server = osc_server.ThreadingOSCUDPServer(
          (IP_MUSE, PORT_MUSE), disp)
        print("Serving on {}".format(server.server_address))
        server.serve_forever() 

# hold timed samples here
current_sample = {
        'alpha_relative': None,
        'beta_relative': None,
        'gamma_relative': None,
        'theta_relative': None,
        'delta_relative': None,
        'mellow': None,
        'concentration': None,
}


# Setup outlet stream infos
stream_info_muse = StreamInfo('Muse', 'EEG', CHNS_MUSE, SAMPLE_RATE, 'float32', 'museid_1')
channels = stream_info_muse.desc().append_child("channels")
channel_list = ["ar0", "ar1", "ar2", "ar3",
        "br0", "br1", "br2", "br3",
        "gr0", "gr1", "gr2", "gr3",
        "tr0", "tr1", "tr2", "tr3",
        "dr0", "dr1", "dr2", "dr3",
        "mellow", "concentration"]

for c in channel_list:
    channels.append_child(c) 

# Create outlets
outlet_muse = StreamOutlet(stream_info_muse)

print("Outlets created")

# create server thread
server_thread_muse = ServerThreadMuse(1)
server_thread_muse.daemon = True
server_thread_muse.start()

print("Listening for data")

# pushes updated sample through the outlet
while True:
    new_sample = []
    for key in current_sample.keys():
        if current_sample[key] is None:
            #print("CONT 1")
            continue

        for element in current_sample[key]:
            if math.isnan(element):
                element = 0.0
            new_sample.append(element)
    
    if (len(new_sample) is not CHNS_MUSE):
        time.sleep(1.0/SAMPLE_RATE)
        #print("CONT 2")
        continue

    outlet_muse.push_sample(new_sample)
    
    # print("Sample sent")
    # print(new_sample)
    # print("")
    # print(".")
    time.sleep(1.0/SAMPLE_RATE)

