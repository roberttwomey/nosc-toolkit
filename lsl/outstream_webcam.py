import cv2
from pylsl import StreamInfo, StreamOutlet
import numpy as np

# video capture size and channels
WC_WIDTH = 160
WC_HEIGHT = 120
WC_CHNS = 3

# video capture sample intervals in ms
HIGH_FRAMERATE = 33
LOW_FRAMERATE = 1000

# initial conditions, capture at high frame rate
SAMPLE_RATE = HIGH_FRAMERATE
DURATION_HIGH_FRAMERATE_MS = (1.0 / SAMPLE_RATE) * 30.0 * 1000

# create a video capture object
vc = cv2.VideoCapture(0)

# vc.set(cv2.CV_CAP_PROP_FPS,SAMPLE_RATE)

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

framecount = 0

# while there are still frames being read
while rval:
    # resize and flatten the image into a 1d array 
    frame = cv2.resize(frame, (WC_WIDTH, WC_HEIGHT))
    outlet_webcam.push_sample(frame.flatten())
    # print(frame)

    # read in new frame
    rval, frame = vc.read()

    framecount = framecount + 1
    if framecount > DURATION_HIGH_FRAMERATE and SAMPLE_RATE == HIGH_FRAMERATE:
        SAMPLE_RATE = LOW_FRAMERATE
        print("{} frames elapsed.".format(framecount))
        print("Switching to low framerate...")
    # with opencv 3.4, you can not change capture framerate directly
    # you control fps by changing a waitkey delay to set frame rate
    # see here: https://stackoverflow.com/questions/52068277/change-frame-rate-in-opencv-3-4-2
    key = cv2.waitKey(SAMPLE_RATE) ## why is SAMPLE_RATE here?

    if key == 27: # exit on ESC
        break
vc.release()
