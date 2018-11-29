# NOSC Toolkit

A collection of tools for capturing and visualizing non-ordinary states of consciousness and their precipitating contexts. Developed for the Arthur C. Clarke Center for Human Imagination and the Center for Human Transformation. 

## Technological Overview

Currently this project interfaces with the following sensors:

* motion capture - Motion Studio Shadow suits
* EEG - muse
* HR/HVR - Polar H7 or H10
* webcam (reference video)
* breath

Data is captured using LabRecorder from the [Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) project.

Data are visualized in Unity. 

## Capturing Data

Assumes you have done all software setup below. 

### Start the LabRecorder app.

Run the LabRecorder app. 

After starting each of the individual data streams below, hit "update" in the LabRecorder "Record from Streams" window to refresh to list of available data streams. 

### Capture from Muse EEG

Pair the Muse with your computer, wear the device, and start the oustream software. 

In a command prompt, run: [muse/StreamLSLMuseData.bat](muse/StreamLSLMuseData.bat)

### Capture from Polar HR/HVR device

Put on the Polar H10 monitor and start the data outstream software. 

In a command prompt, run: [ble/ble-polar-direct/BLEConsole/bin/Debug/BLEConsole.exe](ble/ble-polar-direct/BLEConsole/bin/Debug/BLEConsole.exe)

### Capture from Shadow Suit

Put on the Shadow Suit and power it on. 

Once the indicator light is pulsing a slow blue, connect to the available ```Shadow1``` WiFi network from your laptop. 

In git bash, run the shadow outstream software. 

From the [lsl/flow-lsl-interface](lsl/flow-lsl-interface) directory in git bash, run:
```
python outstream_shadowsuit.py
```

### Capture from Webcam

Plug in the webcam to your USB port.

In git bash, run the webcam oustream software.

From the [lsl/flow-lsl-interface](lsl/flow-lsl-interface) directory in git bash, run:
```
python oustream_webcam.py
```

### Record with Lab Recorder

If you now update the lis of available streams in labrecorder, you should see the Polar, Muse, Webcam, and Mocap/Shadow Suit. Click the checkbox next to each of these you wish to record to. 

Set a storage location for your data using the "Browse" button. I suggest using the [data/](data/) directory. Give your file/take a meaningful name.  

Use the "Start" and "Stop" buttons under Recording Control to make your recordings.

### Cleanup

When you are finished recording, you can quit out of all of the oustream softwares started above. Check your recordings using the ```gui.py``` software below.

## Browse your Recorded Data

Our main software for browsing the recorded data is ```gui.py``` found in [lsl/flow-lsl-interface](lsl/flow-lsl-interface)

Run the program from git bash. From the [lsl/flow-lsl-interface](lsl/flow-lsl-interface) directory, run:

```
python gui.py your_data_file.xdf
```
Replace ```your_data_file.xdf``` with the name of the file you wish to preview.

## Playback LSL Data to Unity

Coming soon. 

## Live Stream LSL Data to Unity

Coming soon. 

## Initial Setup

### Install the Shadow Suit software (Motion)

download and install:

[https://www.motionshadow.com/software/5753105639538688](https://www.motionshadow.com/software/5753105639538688)

### Install LabRecorder

download LabRecorder-1.13.zip from here: 

[ftp://sccn.ucsd.edu/pub/software/LSL/Apps/](ftp://sccn.ucsd.edu/pub/software/LSL/Apps/)

### Install Unity

We are currently testing with 2018.2.15f1

[https://unity3d.com/get-unity/download](https://unity3d.com/get-unity/download)

### Setup the python lsl interface software

Do the necessary python installation for the flow-lsl-interface submodule. See [lsl/flow-lsl-interface/readme.md](lsl/flow-lsl-interface/readme.md).