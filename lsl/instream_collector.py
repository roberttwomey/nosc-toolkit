import os
import threading
import socket
import argparse
import math
import time
import cv2
import numpy as np
from pylsl import StreamInlet, resolve_stream

WC_WIDTH = 640
WC_HEIGHT = 480
WC_CHNS = 3

# find stream
print("Resolving streams...")

stream_names = ['Muse', 'Webcam', 'HRV']

stream_inlets = []

# create stream inlets
print("Creating stream inlets")
for name in stream_names:
    stream = resolve_stream('name', name))
    stream_inlets.append(StreamInlet(stream[0]))


cv2.namedWindow("preview")

while True:
    # retreive new sample
    sample_muse, timestamp_muse = inlet_muse.pull_sample()
  #  sample_hrv, timestamp_hrv = inlet_hrv.pull_sample()
    sample_webcam, timestamp_webcam = inlet_webcam.pull_sample()
    
    print("Sample muse", timestamp_muse, sample_muse)
   # print("Sample hrv", timestamp_hrv, sample_hrv)
    frame = np.reshape(sample_webcam, (WC_HEIGHT, WC_WIDTH, WC_CHNS)).astype(np.uint8)
    print(frame)
    cv2.imshow("preview", frame)
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyWindow("preview")
