# NOSC Toolkit

A collection of tools for capturing and visualizing non-ordinary states of consciousness and their precipitating contexts. Developed for the Arthur C. Clarke Center for Human Imagination and the Center for Human Transformation. 

## Technological Overview

Currently this project interfaces with the following sensors:

* motion capture - Motion Studio Shadow suits
* EEG - muse
* HR/HVR - Polar H7 or H10
* webcam (reference video)
* breath (not yet implemented)

Data is captured using LabRecorder from the [Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) project.

Data are visualized in Unity. 

## Capturing Data

Assumes you have done all software setup below. 

### Start the LabRecorder app.

We are currently using LabRecorder from the LSL project to record data. You can get the LabRecorder app here: LabRecorder-1.13.zip [ftp://sccn.ucsd.edu/pub/software/LSL/Apps/](ftp://sccn.ucsd.edu/pub/software/LSL/Apps/)

Start LabRecorder.exe.

As you start each of the individual data streams below, hit "update" in the LabRecorder "Record from Streams" window to refresh to list of available data streams. 

### Capture from Muse EEG

Pair the Muse with your computer, wear the device, and start the oustream software. 

In a command prompt, run: [muse/StreamMuse.bat](muse/StreamMuse.bat)

In Windows Explorer, navigate to ```lsl/flow-lsl-interface``` and run [lsl/flow-lsl-interface/outstream_muse.py](outstream_muse.py).

You should now see the Muse as a data source in LabRecorder. 

### Capture from Polar HR/HVR device

Put on the Polar H10 monitor and start the data outstream software. 

In Windows Explorer, navigate to ```ble/ble-polar-direct/BLEPolarDirect/bin/Debug/``` and run [ble/ble-polar-direct/BLEPolarDirect/bin/Debug/BLEPolarDirect.exe](ble/ble-polar-direct/BLEPolarDirect/bin/Debug/BLEPolarDirect.exe)

You should now see the Polar as a data source in LabRecorder.

### Capture from Shadow Suit

Start the Shadow desktop app. (Called "Shadow")

Put on the Shadow Suit and power it on. (See the video tutorial [here](https://www.motionshadow.com/setup))

Once the indicator light is pulsing a slow blue, connect to the available ```Shadow1``` WiFi network from your laptop. (SSID: "Shadow1", pwd: 2062012708). In the Shadow app you should see the live skeleton.

In Windows Explorer, navigate to ```lsl/flow-lsl-interface``` and run [lsl/flow-lsl-interface/outstream_shadow.py](outstream_shadow.py). 

You should now see the shadowsuit as a data source in LabRecorder.

### Capture from Webcam

Plug in the webcam to your USB port.

In Windows Explorer, navigate to ```lsl/flow-lsl-interface``` and run [lsl/flow-lsl-interface/outstream_webcam.py](lsl/flow-lsl-interface/outstream_webcam.py). 

You should now see the Webcam as a data source in LabRecorder.

### Record with Lab Recorder

If you now update the lis of available streams in labrecorder, you should see the Polar, Muse, Webcam, and Mocap/Shadow Suit. Click the checkbox next to each of these you wish to record to. 

Set a storage location for your data using the "Browse" button. I suggest using the [data/](data/) directory. Give your file/take a meaningful name.  

Use the "Start" and "Stop" buttons under Recording Control to make your recordings.

## Preview Data

Our main software for previewing the recorded data is ```gui.py``` found in [lsl/flow-lsl-interface](lsl/flow-lsl-interface)

Run the program from git bash. From the [lsl/flow-lsl-interface](lsl/flow-lsl-interface) directory, run:

```
python gui.py your_data_file.xdf
```

Replace ```your_data_file.xdf``` with the name of the file you wish to preview.


## Live Stream Data in Unity

More coming soon. For now we have very preliminary visualization in Unity. 

### Shadow/MoCap Data in Unity

Start the Shadow desktop app. Wear the shadow suit. Connect your laptop to the shadow WiFi network. You should see the shadow suit in the shadow software.

With Unity, open the [unity/shadow-unity-test](unity/shadow-unity-test) project. 

Play **SampleScene**. 

You should see the rigged skeleton follow the motions of your shadow suit.

### LSL Data in Unity

Wear the Polar sensor and start the BLEPolarDirect program. 

With Unity, open the [unity/unity%20LSL%20test](unity/unity%20LSL%20test) project. 

Play the **lsl to unity test** scene. 

The floating text panel in the scene should show the current polar readings. 

## Playback LSL Data to Unity

Coming soon.

## Initial Setup

### Install the Muse-IO software

Download the Muse SDK:

[http://storage.googleapis.com/ix_downloads/musesdk-3.4.1/musesdk-3.4.1-windows-installer.exe](http://storage.googleapis.com/ix_downloads/musesdk-3.4.1/musesdk-3.4.1-windows-installer.exe)

or on Khan: 

[Khan\Assembly\Dependencies\musesdk-3.4.1-windows-installer.exe](
Khan\Assembly\Dependencies\musesdk-3.4.1-windows-installer.exe)

Pair the Muse headset:

* Hold Muse On button for 6 seconds.
* Open Control Panel --> Add A device
* Choose yes that you see the pairing code.

### Install the Shadow Suit software (Motion)

Download and install the Shadow desktop app. 

[https://www.motionshadow.com/software/5753105639538688](https://www.motionshadow.com/software/5753105639538688)

#### How to Wear the Shadow Suit

For help on how to put on the shadow suit, see the video tutorial [here](https://www.motionshadow.com/setup)).

### Install LabRecorder

Download LabRecorder-1.13.zip from here: 

[ftp://sccn.ucsd.edu/pub/software/LSL/Apps/](ftp://sccn.ucsd.edu/pub/software/LSL/Apps/)

### Install Unity

We are currently testing with 2018.2.15f1

[https://unity3d.com/get-unity/download](https://unity3d.com/get-unity/download)

### Setup the python lsl interface software

Do the necessary python installation for the python lsl software. See [lsl/readme.md](lsl/readme.md).

### Install Github Desktop

Download github desktop for windows and install: https://desktop.github.com/


# TODO
* textually annotate data
* unity playback of LSL data
* exploratory data analysis in python with scikitlearn, matplotlib, other tools
* use the hrv analysis package: [https://github.com/rhenanbartels/hrv](https://github.com/rhenanbartels/hrv)
* manual, then automatic classification of peak moments/NOSC
