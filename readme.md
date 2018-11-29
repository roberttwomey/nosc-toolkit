# NOSC Toolkit

A collection of tools for capturing and visualizing non-ordinary states of consciousness and their precipitating contexts. Developed for the Arthur C. Clarke Center for Human Imagination and the Center for Human Transformation. 

## Technological Overview

Currently this project interfaces with the following sensors:

* motion capture - Motion Studio Shadow suits
* EEG - muse
* HR/HVR - Polar H7 or H10
* webcam (reference video)
* breath

Data is captured using the LabRecorder from the [Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) project.

Data are visualized in Unity. 

## Capturing Data

Assumes you have done all software setup below. 


## Software Setup Setup

1. Install the Shadow Suit software (Motion)

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