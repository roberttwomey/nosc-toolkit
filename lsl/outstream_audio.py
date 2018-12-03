from pylsl import StreamInfo, StreamOutlet
import time
import struct
import matplotlib.pyplot as plt
import pyaudio
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 * 4
SAMPLE_RATE = 10

# Create audio object
audio = pyaudio.PyAudio()

# Create stream
stream = audio.open(format=FORMAT, 
        channels=CHANNELS,
        rate=RATE, 
        input=True,
        output=True,
        frames_per_buffer=CHUNK)

# Setup outlet stream infos
stream_info_audio = StreamInfo('Audio', 'Experimental', CHANNELS, SAMPLE_RATE, 'int32', 'audioid_1')
channels = stream_info_audio.desc().append_child("channels")
channels.append_child('amplitude')

# Create outlets
outlet_audio = StreamOutlet(stream_info_audio)

print("Outlets created")

# Setup plots for visuals
fig, ax = plt.subplots()
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))
ax.set_ylim(0, 255)
ax.set_xlim(0, CHUNK)
plt.show(block=False)

# Continuosly read in chunks
while True:
    data = stream.read(CHUNK)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype=np.uint8)[::2] + 127
    print(data_int[0])
    outlet_audio.push_sample([data_int[0]])

    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(1.0 / SAMPLE_RATE)    

