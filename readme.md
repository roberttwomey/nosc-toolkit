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

In a command prompt, run: [muse/StreamMuseOSC.bat](muse/StreamMuseOSC.bat)

Open the git bash application. 

Change the the nosc project directory, and navigate to [lsl/](lsl/).

Run the oustream muse program:

```
python oustream_muse.py
```

### Capture from Polar HR/HVR device

Put on the Polar H10 monitor and start the data outstream software. 

In a command prompt, run: [ble/ble-polar-direct/BLEPolarDirect/bin/Debug/BLEPolarDirect.exe](ble/ble-polar-direct/BLEPolarDirect/bin/Debug/BLEPolarDirect.exe)

### Capture from Shadow Suit

Start the Shadow desktop app. (Called "Shadow")

Put on the Shadow Suit and power it on. (See the video tutorial [here](https://www.motionshadow.com/setup))

Once the indicator light is pulsing a slow blue, connect to the available ```Shadow1``` WiFi network from your laptop. (SSID: "Shadow1", pwd: 2062012708). In the Shadow app you should see the live skeleton.

Open the git bash application. 

Change to the nosc project directory, and navigate to [lsl/](lsl/). 

Run the outstream shadowsuit software:

```
python outstream_shadowsuit.py
```

### Capture from Webcam

Plug in the webcam to your USB port.

Open the git bash application. 

Change to the nosc project directory, and navigate to [lsl](lsl). 

Run the oustream webcam software:

```
python outstream_webcam.py
```

If you need to switch what camera you are recording from, open ```oustream_webcam.py``` in a text editor. 

Change the following line to select a different camera number:

```
vc = cv2.VideoCapture(0)
```

For instance to use the external webcam instead of the built-in camera on your laptop, write:

```
vc = cv2.VideoCapture(1)
```

### Record with Lab Recorder

If you now update the list of available streams in labrecorder, you should see the Polar, Muse, Webcam, and Mocap/Shadow Suit. Click the checkbox next to each of these you wish to record to. 

Set a storage location for your data using the "Browse" button. I suggest using the [data/](data/) directory in the nosc directory. Give your file/take a meaningful name.  

Use the "Start" and "Stop" buttons under Recording Control to make your recordings.

### Cleanup

When you are finished recording, you can quit out of all of the oustream softwares started above. Check your recordings using the ```gui.py``` software below.

## Preview your Recorded Data

Our main software for previewing the recorded data is ```gui.py``` found in [lsl/](lsl)

Run the program from git bash. From the [lsl](lsl) directory, run:

```
python gui.py your_data_file.xdf
```
Replace ```your_data_file.xdf``` with the name of the file you wish to preview.


## Live Stream  Data in Unity

More coming soon. For now we have very preliminary visualization in Unity. 

### Shadow/MoCap Data in Unity

Start the Shadow desktop app. Wear the shadow suit. Connect your laptop to the shadow WiFi network. You should see the shadow suit in the shadow software.

With Unity, open the [unity/shadow-unity-test](unity/shadow-unity-test) project. 

Play **SampleScene**. 

You should see the rigged skeleton follow the motions of your shadow suit.

### LSL Data in Unity

Wear the Polar sensor and start the BLEPolarDirect program. 

With Unity, open the [unity/unity LSL test](unity/unity%20LSL%20test) project. 

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

Do the necessary python installation for the flow-lsl-interface submodule. See [lsl/flow-lsl-interface/readme.md](lsl/flow-lsl-interface/readme.md).