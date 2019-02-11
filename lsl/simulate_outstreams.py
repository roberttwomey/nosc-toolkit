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

stream_info_muse = StreamInfo('Muse', 'EEG', 8, 100, 'float32', 'myuid34234')
channels = stream_info_muse.desc().append_child("channels")
channel_list = [ "ar0", "ar1", "ar2", "ar3",
        "br0", "br1", "br2", "br3",
        "gr0", "gr1", "gr2", "gr3",
        "tr0", "tr1", "tr2", "tr3",
        "dr0", "dr1", "dr2", "dr3",
        "mellow", "concentration"]

for c in channel_list:
    channels.append_child(c) 

# next make an outlet
muse_outlet = StreamOutlet(stream_info_muse)

# StreamInfo and Outlet for HRV data
stream_info_hrv = StreamInfo('Polar', 'HRV', 3, 70, 'float32', 'myuid3')
channels = stream_info_hrv.desc().append_child("channels")
# channels.append_child('rr')
channel_list = ["bpm", "rr", "hrv"]
for c in channel_list:
	channels.append_child(c)

# next make an outlet
hrv_outlet = StreamOutlet(stream_info_hrv)

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

	# send fake Muse/EEG data

	# make a new random 8-channel sample; this is converted into a
	# pylsl.vectorf (the data type that is expected by push_sample)
	mymusesample = [rand(), rand(), rand(), rand(), rand(), rand(), rand(), rand()]
	# now send it and wait for a bit
	muse_outlet.push_sample(mymusesample)

	# send fake HRV data
	myhrvsample = [rand(), rand(), rand()]
	hrv_outlet.push_sample(myhrvsample)

	# send fake MoCap data
	mymocapsample = []

	for i in range(0,mocap_channels*mocap_sample_size):
		x = rand()
		mymocapsample.append(x)

	mocap_outlet.push_sample(mymocapsample)
	
	
	# changes sample rate
	time.sleep(0.01)