import cv2
from pylsl import StreamInfo, StreamOutlet
import numpy as np
import sys

# video capture size and channels
WC_WIDTH = 160
WC_HEIGHT = 120
WC_CHNS = 3

# video capture sample intervals in ms
HIGH_FRAMERATE = 33
LOW_FRAMERATE = 1000

# initial conditions, capture at high frame rate
SAMPLE_RATE = HIGH_FRAMERATE
DURATION_HIGH_FRAMERATE_SEC = 30.0
DURATION_HIGH_FRAMERATE = (1.0 / SAMPLE_RATE) * DURATION_HIGH_FRAMERATE_SEC * 1000

print("\n=== outstream_webcam.py ===\n")

sys.stdout.write("Opening video device...")
sys.stdout.flush()

# create a video capture object
vc = cv2.VideoCapture(0)

# vc.set(cv2.CV_CAP_PROP_FPS,SAMPLE_RATE)

# stream from camera 1
# vc = cv2.VideoCapture(1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
    sys.stdout.write("opened.\n")
else:
    rval = False
    sys.stdout.write("failed.\n Exiting\n")
    exit()

sys.stdout.flush()


sys.stdout.write("Creating LSL outlets...")
sys.stdout.flush()

# create lsl stream info
stream_info_webcam = StreamInfo('Webcam', 'Experiment', WC_WIDTH * WC_HEIGHT * WC_CHNS, SAMPLE_RATE, 'int32', 'webcamid_1')

# create the stream
outlet_webcam = StreamOutlet(stream_info_webcam)


framecount = 0

sys.stdout.write("streaming.\n")
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
        sys.stdout.write("{} frames elapsed.\n".format(framecount))
        sys.stdout.write("Switching to low framerate...\n")
        SAMPLE_RATE = LOW_FRAMERATE
      
    # with opencv 3.4, you can not change capture framerate directly
    # you control fps by changing a waitkey delay to set frame rate
    # see here: https://stackoverflow.com/questions/52068277/change-frame-rate-in-opencv-3-4-2
    key = cv2.waitKey(SAMPLE_RATE) ## why is SAMPLE_RATE here?

    if key == 27: # exit on ESC
        break
    if framecount % 30 == 0:
        sys.stdout.write(".")
        sys.stdout.flush()

vc.release()
print("exiting.")