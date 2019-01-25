#!/c/Users/Robert/AppData/Local/Programs/Python/Python37-32/python

# This file is to run the corresponding bat, exe and python files
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
import subprocess
import os, sys, time, threading
from multiprocessing import Process

hrDeviceName = "Polar H7"

current_dir = os.getcwd()

# Run the Muse EEG
p1 = subprocess.Popen(current_dir + "\muse\StreamMuse.bat", creationflags=CREATE_NEW_CONSOLE)
os.system('python lsl/outstream_muse.py')

# Run Polar HR/HVR device
p2 = subprocess.Popen(current_dir + "\\ble\BLEPolarDirect\\bin\Debug\BLEPolarDirect.exe" + " \"" + hrDeviceName+"\"")

# Run Shadow Suit applications
# Make sure having MuseLab under C:\Program Files\Motion\Shadow.exe
p3 = subprocess.Popen("C:\Program Files\Motion\Shadow.exe")
os.system('python lsl/outstream_shadowsuit.py')

# Run Webcam applications
os.system('python lsl/outstream_webcam.py')
