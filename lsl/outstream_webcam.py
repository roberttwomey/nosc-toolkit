import cv2
from pylsl import StreamInfo, StreamOutlet
import numpy as np

WC_WIDTH = 160
WC_HEIGHT = 120
WC_CHNS = 3
SAMPLE_RATE = 10

# create a video capture object
vc = cv2.VideoCapture(0)

# stream from camera 1
# vc = cv2.VideoCapture(1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

print("Connected to video device...")

# create lsl stream info
stream_info_webcam = StreamInfo('Webcam', 'Experiment', WC_WIDTH * WC_HEIGHT * WC_CHNS, SAMPLE_RATE, 'int32', 'webcamid_1')

# create the stream
outlet_webcam = StreamOutlet(stream_info_webcam)

print("Streaming data...")

# while there are still frames being read
while rval:
    # resize and flatten the image into a 1d array 
    frame = cv2.resize(frame, (WC_WIDTH, WC_HEIGHT))
    outlet_webcam.push_sample(frame.flatten())
    # print(frame)

    # read in new frame
    rval, frame = vc.read()
    key = cv2.waitKey(SAMPLE_RATE)

    if key == 27: # exit on ESC
        break
vc.release()
