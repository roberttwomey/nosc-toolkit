import os
import numpy as np
import pandas as pd
import xdf
import cv2

# returns a list of all the streams in the file
def get_streams(file_path):
    streams = xdf.load_xdf(file_path)

    return streams[0]

# create a dataframe object from a substream, where the columns of the dataframe are the 
# channels
def convert_to_df(substream):
    # seperate into the data, timestamps, and channels
    data = np.array(substream['time_series'])
    timestamps = substream['time_stamps']
    channels = list(substream['info']['desc'][0]['channels'][0].keys())
    
    # create the dataframe
    df = pd.DataFrame(data, index=timestamps, columns=channels)
    df.index.name = "time_stamps"

    return df

# extract data from the path
filepath = 'data/alldatatest.xdf'
filename_strip = os.path.basename(filepath).split('.')[0]
outpath = 'data'

# get the streams
substreams = get_streams(filepath)

# loop through each stream and put the data in a df, from which a csv is made
for substream in substreams:
    # get the name of the stream
    substream_name = substream['info']['name'][0]

    # create a .avi video instead of a csv
    if (substream_name == 'Webcam'):
        # save video as avi
        v_stream = substream['time_series']
        v_stream = np.array(v_stream).reshape(-1, 480, 640, 3)

        # v_stream = v_stream / 255.
        
        # create an output stream
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        v_out = cv2.VideoWriter(os.path.join(outpath, '{}_{}.avi'.format(filename_strip, substream_name)), fourcc, 10, (640, 480))
        
        # write each frame to the output
        for i in range(len(v_stream)):
            v_out.write(np.uint8(v_stream[i]))
        v_out.release()

    else:
        # create dataframe
        df_stream = convert_to_df(substream)
        df_stream.to_csv(os.path.join(outpath, '{}_{}.csv'.format(filename_strip, substream_name)))
