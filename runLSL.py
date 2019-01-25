# This file is to run the corresponding bat, exe and python files
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE
import subprocess
import os, sys, time, threading
from multiprocessing import Process

hrDeviceName = "Polar H7"

current_dir = os.getcwd()

# Run the Muse EEG
# print("=== Opening muse\StreamMuse.bat ===")
# p1 = subprocess.Popen(current_dir + "\muse\StreamMuse.bat", creationflags=CREATE_NEW_CONSOLE)

# os.system('python lsl/outstream_muse.py')
# print("=== Opened oustream_muse.py ===")

# # Run Polar HR/HVR device
# p2 = subprocess.Popen(current_dir + "\\ble\BLEPolarDirect\\bin\Debug\BLEPolarDirect.exe" + " \"" + hrDeviceName+"\"")
# print("=== Opened BLEPolarDirect ===")

# Run Shadow Suit applications
# Make sure having MuseLab under C:\Program Files\Motion\Shadow.exe
p3 = subprocess.Popen("C:\Program Files\Motion\Shadow.exe")
time.sleep(5.0)

print("=== Opened Motion Shadow Suit ===")
os.system('python lsl/outstream_shadowsuit.py')

# Run Webcam applications
os.system('python lsl/outstream_webcam.py')
