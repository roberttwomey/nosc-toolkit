import tkinter as tk
import numpy as np
import xdf
import sys
import cv2
from PIL import Image, ImageTk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from matplotlib import colors as mcolors

matplotlib.use('TkAgg')

# how many samples should be drawn at once
SAMPLE_FREQ = 1000
TICK_FREQ = 10

VIDEO_WIDTH = 160 #320
VIDEO_HEIGHT = 120 #240

def fig2rgb_array(fig):
    fig.canvas.draw()
    buf = fig.canvas.tostring_rgb()
    ncols, nrows = fig.canvas.get_width_height()
    return np.fromstring(buf, dtype=np.uint8).reshape(nrows, ncols, 3)


# find nearest item
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

# get the time in in the format 'hh:mm:ss'
def convert_time(seconds_total):
    seconds = int(seconds_total % 60)
    minutes = int(seconds_total / 60) % 60
    hours = int(seconds_total / (60 * 60))
    
    return '{}:{}:{}'.format(hours, minutes, seconds)

# create vectorized function so it can be applied across array elements
convert_time_v = np.vectorize(convert_time)

def nothing(x):
    pass

# retrieve a particular data stream from xdf file given index
def retrieve_stream_data(stream, i):
    samples = stream[0][i]["time_series"]
    samples = np.array(samples)
    timestamps = stream[0][i]["time_stamps"]

    return samples, timestamps

# fill subplot with data stream content
def create_wave_plot(ax, samples, timestamps, channels):

    num_samples = len(samples)
    num_channels = len(samples[0])
    print(timestamps)

    # get only some samples since it will be too slow if there are too many data points
    samples_index = np.linspace(0, num_samples, num=SAMPLE_FREQ, endpoint=False).astype(int)
    samples_loc = np.array(timestamps[samples_index.tolist()]) - timestamps[0]
    samples_used = samples[samples_index.tolist()]
    
    # convert the time to more familiar format
    timestamp_index = np.linspace(0, num_samples, num=TICK_FREQ, endpoint=False).astype(int)
    timestamp_loc = np.array(timestamps[timestamp_index.tolist()]) - timestamps[0]
    timestamp_labels = convert_time_v(timestamp_loc)

    ticklocs = []
    
    # set the time stamps
    ax.set_xlim(samples_loc[0], samples_loc[-1])
    ax.set_xticks(timestamp_loc)
    ax.set_xticklabels(timestamp_labels)
    
    # calculate the height for each channel to vary in
    dmin = samples.min()
    dmax = samples.max()
    dr = (dmax - dmin) * 0.7  # Crowd them a bit.
    
    y0 = dmin
    y1 = (num_channels - 1) * dr + dmax

    ax.set_ylim(y0, y1)

    segs = []
    for i in range(num_channels):
        segs.append(np.hstack((samples_loc[:, np.newaxis], samples_used[:, i, np.newaxis])))
        ticklocs.append(i * dr)
    
    offsets = np.zeros((num_channels, 2), dtype=float)
    offsets[:, 1] = ticklocs
    
    colors = [mcolors.to_rgba(c)
                  for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    
    # create the lines
    lines = LineCollection(segs, transOffset=None, offsets=offsets, linewidths=.5, colors=colors)
    ax.add_collection(lines)

    # Set the yticks to use axes coordinates on the y axis
    ax.set_yticks(ticklocs)
    ax.set_yticklabels(channels)

# places the track line onto the graphs
def place_trackline(ax, trackline, pos):
    if (trackline is not None):
        trackline.remove()

    trackline = ax.axvline(x=pos, linewidth=0.5, color='k')
    return trackline

# buffers avi video into memory
def buffer_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_buffer = []

    while(cap.isOpened()):
        ret, frame = cap.read()
        if (frame is None):
            break

        frame_buffer.append(frame)
    cap.release()
    return frame_buffer

# the app class that contains the code to run the GUI
class App():

    def __init__(self, file_path):
        # create frames for the gui
        self.root = tk.Tk()

        # quit button
        # self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy).pack()
        # self.quit_button = tk.Button(self.root, text="Quit", command=sys.exit()).pack()

        # the video frame
        self.frame_video = tk.Frame(self.root)
        self.frame_video.pack(side=tk.LEFT)

        # the plots frame
        self.frame_wave_plots = tk.Frame(self.root)
        self.frame_wave_plots.pack(side=tk.RIGHT)

        # the sliders frame
        self.frame_slider = tk.Frame(self.root)
        self.frame_slider.pack(side=tk.TOP)

        # retrieve xdf data
        stream = xdf.load_xdf(file_path)

        self.data_all = []
        
        
        # for astream in stream:
            # print(astream)
        # print(stream[1])
        # exit()
            
        # fill the above list with necessay data to build the graphs
        for sub_stream in stream[0]:
            print(sub_stream['info']['name'])
            print(sub_stream['time_stamps'])

            # buffer video or plot data
            if (sub_stream['info']['name'][0] == 'Webcam'):
                self.data_video = sub_stream['time_series']
                continue
            self.data_all.append((
                sub_stream['time_series'], 
                sub_stream['time_stamps'], 
                sub_stream['info']['desc'][0]['channels'][0].keys()))

        # exit()

        # create plots
        self.fig, self.axes = plt.subplots(len(self.data_all), 1, figsize=(15, 10))
        if len(self.data_all) > 1:
            self.axes = self.axes.ravel()
        elif len(self.data_all) == 1:
            self.axes = [self.axes]
        
        # add the fig to the gui
        self.w_canvas = FigureCanvasTkAgg(self.fig, self.frame_wave_plots)
        self.w_canvas.get_tk_widget().pack()

        # fill the plots with data
        for i, sub_stream in enumerate(self.data_all):
            print(i, sub_stream)
            create_wave_plot(self.axes[i], sub_stream[0], sub_stream[1], sub_stream[2])
        
        # create the slider plots
        self.slider_scale_ax = self.fig.add_axes([0.1, 0.04, 0.8, 0.02])
        self.slider_scale = Slider(self.slider_scale_ax, 'scale', 0.0, 1.0, valinit=1.0)
        self.slider_scale.on_changed(self.handle_slider_scale)

        self.slider_window_ax = self.fig.add_axes([0.1, 0.02, 0.8, 0.02])
        self.slider_window = Slider(self.slider_window_ax, 'window', 0.0, 1.0, valinit=0.0)
        self.slider_window.on_changed(self.handle_slider_window)
       
        self.scale = 1.0
        self.window_start = 0.0
       
        # place initial tracklines
        self.tracklines = []
        for ax in self.axes:
            self.tracklines.append(place_trackline(ax, None, 0))

        '''
        Create video objects
        '''

        # buffer video
        self.frame_buffer = np.uint8(np.array(self.data_video).reshape(-1, VIDEO_HEIGHT, VIDEO_WIDTH, 3))
        print("VIDEO LEN " + str(len(self.frame_buffer)))
        # initilize video vars
        self.len_buffer = len(self.frame_buffer)
        self.frame_index = 0
        self.play = False
        self.frame_delay = 100

        # create video widget
        self.w_video = tk.Label(self.frame_video)
        self.w_video.pack(side=tk.TOP)
        
        # create frame within video frame to hold buttons and progress slider
        self.frame_video_buttons = tk.Frame(self.frame_video)
        self.frame_video_buttons.pack(side=tk.TOP)
        
        self.frame_video_progress = tk.Frame(self.frame_video)
        self.frame_video_progress.pack(side=tk.TOP)

        # create buttons for video control
        self.w_video_play = tk.Button(self.frame_video_buttons, text='Play', command=self.handle_video_play)
        self.w_video_play.pack(side=tk.LEFT)

        self.w_video_pause = tk.Button(self.frame_video_buttons, text='Pause', command=self.handle_video_pause)
        self.w_video_pause.pack(side=tk.LEFT)

        self.w_video_restart = tk.Button(self.frame_video_buttons, text='Restart', command=self.handle_video_restart)
        self.w_video_restart.pack(side=tk.LEFT)

        # create progress slider for video
        self.w_video_progress = tk.Scale(self.frame_video_progress, from_=0, to=100, orient=tk.HORIZONTAL, command=self.handle_progress_change, length=400)
        self.w_video_progress.pack(side=tk.LEFT)

        # set first frame
        self.update_frame()

        # start video frame update coroutine
        self.update_video_frame()

    ## COROUTINE UPDATES
    
    # updates the current video frame to the next
    def update_video_frame(self):
        if self.play and self.frame_index < self.len_buffer - 1:
            self.frame_index += 1
            self.update_frame()
        else:
            pass

        # here's where the coroutine recalls itself to execute periodically
        self.job_update_video_frame = self.root.after(self.frame_delay, self.update_video_frame)

    ## GUI HANDLERS

    def handle_video_play(self):
        self.play = True

    def handle_video_pause(self):
        self.play = False

    def handle_video_restart(self):
        self.frame_index = 0
        self.update_frame()

    def handle_progress_change(self, event):
        # cancel the update frame job since we are changing the video's location
        if (self.job_update_video_frame):
            self.root.after_cancel(self.job_update_video_frame)

        # make sure the index doesnt go out of bounds
        self.frame_index = np.clip(int(self.len_buffer * self.w_video_progress.get() / 100), 0, self.len_buffer - 1)

        # now update the frame
        self.update_frame()

        # start the coroutine again
        self.update_video_frame()

    def handle_slider_scale(self, val):
        # get the new value
        self.scale = self.slider_scale.val

        # after the sliders have changed, we want to modify the plot's x and y size
        for i, sub_stream in enumerate(self.data_all):
            len_sub_stream = len(sub_stream[0])

            # get the new parameters for the x axis
            window_size = np.clip(int(len_sub_stream * self.scale), 1, None)
            start_index = np.clip(int(len_sub_stream * self.window_start), 0, len_sub_stream - window_size)
            end_index = np.clip(start_index + window_size - 1, window_size - 1, len_sub_stream - 1)

            # finding the index of data in the streams to plot
            if (end_index - start_index + 1 <= SAMPLE_FREQ):
                sample_index = np.arange(start_index, end_index + 1)
            else:
                sample_index = np.linspace(start_index, end_index, num=SAMPLE_FREQ, endpoint=True).astype(int)

            sample_locations = np.array(sub_stream[1][sample_index.tolist()]) - sub_stream[1][0]

            # getting the respective timestamps
            timestamp_index = np.linspace(start_index, end_index, num=TICK_FREQ, endpoint=True).astype(int)
            timestamp_ticks = np.array(sub_stream[1][timestamp_index.tolist()]) - sub_stream[1][0]
            timestamp_labels = convert_time_v(timestamp_ticks)

            # set the new labels down 
            self.axes[i].set_xlim(sample_locations[0], sample_locations[-1])
            self.axes[i].set_xticks(timestamp_ticks)
            self.axes[i].set_xticklabels(timestamp_labels)
            self.fig.canvas.draw_idle()

    def handle_slider_window(self, val):
        self.window_start = self.slider_window.val

        for i, sub_stream in enumerate(self.data_all):
            len_sub_stream = len(sub_stream[0])

            window_size = np.clip(int(len_sub_stream * self.scale), 1, None)
            start_index = np.clip(int(len_sub_stream * self.window_start), 0, len_sub_stream - window_size)
            end_index = np.clip(start_index + window_size - 1, window_size - 1, len_sub_stream - 1)

            # finding the index of data in the streams to plot
            if (end_index - start_index + 1 <= SAMPLE_FREQ):
                sample_index = np.arange(start_index, end_index + 1)
            else:
                sample_index = np.linspace(start_index, end_index, num=SAMPLE_FREQ, endpoint=True).astype(int)

            sample_locations = np.array(sub_stream[1][sample_index.tolist()]) - sub_stream[1][0]

            # getting the respective timestamps
            timestamp_index = np.linspace(start_index, end_index, num=TICK_FREQ, endpoint=True).astype(int)
            timestamp_ticks = np.array(sub_stream[1][timestamp_index.tolist()]) - sub_stream[1][0]
            timestamp_labels = convert_time_v(timestamp_ticks)

            # set the new labels down 
            self.axes[i].set_xlim(sample_locations[0], sample_locations[-1])
            self.axes[i].set_xticks(timestamp_ticks)
            self.axes[i].set_xticklabels(timestamp_labels)
            self.fig.canvas.draw_idle()

    ## HELPERS

    def output_current_data(self, video_time):

        # after the sliders have changed, we want to modify the plot's x and y size
        for i, sub_stream in enumerate(self.data_all):
            len_sub_stream = len(sub_stream[0])

            # get the new parameters for the x axis
            window_size = np.clip(int(len_sub_stream * self.scale), 1, None)
            start_index = np.clip(int(len_sub_stream * self.window_start), 0, len_sub_stream - window_size)
            end_index = np.clip(start_index + window_size - 1, window_size - 1, len_sub_stream - 1)

            # finding the index of data in the streams to plot
            if (end_index - start_index + 1 <= SAMPLE_FREQ):
                sample_index = np.arange(start_index, end_index + 1)
            else:
                sample_index = np.linspace(start_index, end_index, num=SAMPLE_FREQ, endpoint=True).astype(int)

            sample_locations = np.array(sub_stream[1][sample_index.tolist()]) - sub_stream[1][0]

            # find sample closest to current video frame
            nearest_time = nearest(sample_locations, video_time)
            nearest_index = sample_locations.tolist().index(nearest_time)
            nearest_value = sub_stream[0][nearest_index]

            # output substream values at nearest time
            print(video_time, nearest_time, nearest_index, nearest_value)   

    def update_frame(self):

        # handle video and progress bar update
        frame = self.frame_buffer[self.frame_index]
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame = ImageTk.PhotoImage(image=frame)

        self.video_current_frame = frame
        self.w_video.configure(image=self.video_current_frame)
        self.w_video.image = self.video_current_frame

        self.w_video_progress.set(100 * self.frame_index / self.len_buffer)

        # handle plot line update
        line_loc = self.data_all[0][1][int(self.frame_index / self.len_buffer * len(self.data_all[0][1]))] - self.data_all[0][1][0]
        for i in range(len(self.axes)):
            self.tracklines[i] = place_trackline(self.axes[i], self.tracklines[i], line_loc)
        
        # print(self.frame_index)
        self.output_current_data(line_loc)

        self.fig.canvas.draw_idle()

        return frame


if __name__ == "__main__":
    newApp = App(sys.argv[1])
    tk.mainloop()
