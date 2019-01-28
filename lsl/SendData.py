"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
from random import random as rand
from random import uniform as randf

from pylsl import StreamInfo, StreamOutlet

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover)
info = StreamInfo('Polar', 'HRV', 3, 65, 'float32', 'myuid34234')
info_muse = StreamInfo('Muse', 'EEG', 22, 100, 'float32', 'myuid344')

# next make an outlet
outlet = StreamOutlet(info)

outlet_muse = StreamOutlet(info_muse)

print("now sending data...")
while True:
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
	
	# three samples for Heart monitor:
	#   1. HR beats per minute (50-140 bpm)
	#   2. r-r interval in milliseconds (7 ms/beat - 20 ms/beat)
	#   3. heart rate variability (HRV, measures as std. dev., or pNN50, not sure of range) *** important ***

	# Muse EEG amy channels
	#   1. concentration score (normalized, 0.0 - 1.0) *** important ***
	#   2. mellow score (normalized, 0.0 - 1.0) 
	#   ... two more aggregate scores and a number of individual channels

    mysample = [randf(50.0, 140.0), randf(7.0, 20.0), rand()]

    muse_sample = [rand(), rand(), rand(), rand(), 
				rand(), rand(), rand(), rand(),
				rand(), rand(), rand(), rand(),
				rand(), rand(), rand(), rand(),
				rand(), rand(), rand(), rand(),
				rand(), rand()]

	# additional stream to add would be motion capture


    # now send it and wait for a bit
    outlet.push_sample(mysample)
    outlet_muse.push_sample(muse_sample)

	# this sleep statement sets sample rate, 100Hz
    time.sleep(0.01)
