# This file is to run the corresponding bat, exe and python files
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
import subprocess
import os, sys, time, threading
from multiprocessing import Process

hrDeviceName = "Polar H7"

current_dir = os.getcwd()

# Run the Muse EEG
print("=== Opening muse\StreamMuse.bat ===")
p1 = subprocess.Popen(current_dir + "\muse\StreamMuse.bat", creationflags=CREATE_NEW_CONSOLE)
time.sleep(3.0)
cmd_muse = "lsl/outstream_muse.py"
p2 = subprocess.Popen(["python", cmd_muse], creationflags=CREATE_NEW_CONSOLE)
print("=== Done with muse! ===")

# Run Polar HR/HVR device
print("=== Opening BLEPolarDirect ===")
p3 = subprocess.Popen(current_dir + "\\ble\BLEPolarDirect\\bin\Debug\BLEPolarDirect.exe" + " \"" + hrDeviceName+"\"")
print("=== Done with BLEPolarDirect! ===")

# Run Shadow Suit applications
# Make sure having MuseLab under C:\Program Files\Motion\Shadow.exe
print("=== Opening Shadow Suit ===")
p4 = subprocess.Popen("C:\Program Files\Motion\Shadow.exe")
time.sleep(3.0)
cmd_shadow = "lsl/outstream_shadowsuit.py"
p5 = subprocess.Popen(["python", cmd_shadow], creationflags=CREATE_NEW_CONSOLE)
print("=== Done with shadow Suit! ===")

# Run Webcam applications
print("=== Opening Webcam ===")
cmd_webcam = "lsl/outstream_webcam.py"
p6 = subprocess.Popen(["python", cmd_webcam], creationflags=CREATE_NEW_CONSOLE)
print("=== Done with Webcam! ===")