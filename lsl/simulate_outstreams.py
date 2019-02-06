"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover)
info = StreamInfo('Muse', 'EEG', 8, 100, 'float32', 'myuid34234')

# next make an outlet
outlet = StreamOutlet(info)

# StreamInfo and Outlet for HRV data
hrv_info = StreamInfo('Polar', 'HRV', 3, 70, 'float32', 'myuid3')

# next make an outlet
hrv_outlet = StreamOutlet(hrv_info)

# StreamInfo and Outlet for Shadow Data
mocap_channels = 32
mocap_sample_size = 8
stream_info_mocap = StreamInfo('ShadowSuit', 'MOCAP', mocap_channels * mocap_sample_size, 200)
channels = stream_info_mocap.desc().append_child("channels")
	
channel_list = ["lq0", "lq1", "lq2", "lq3",
		"c0", "c1", "c2", "c3"]

for c in channel_list:
	channels.append_child(c) 

# Create outlets
mocap_outlet = StreamOutlet(stream_info_mocap)


print("now sending data...")
while True:
	# make a new random 8-channel sample; this is converted into a
	# pylsl.vectorf (the data type that is expected by push_sample)
	mysample = [rand(), rand(), rand(), rand(), rand(), rand(), rand(), rand()]
	# now send it and wait for a bit
	outlet.push_sample(mysample)

	myhrvsample = [rand(), rand(), rand()]
	hrv_outlet.push_sample(myhrvsample)

	# fill mocap sample with random data
	mymocapsample = []

	for i in range(0,mocap_channels*mocap_sample_size):
		x = rand()
		mymocapsample.append(x)

	mocap_outlet.push_sample(mymocapsample)
	
	# changes sample rate
	time.sleep(0.01)