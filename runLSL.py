#!/c/Users/Robert/AppData/Local/Programs/Python/Python37-32/python

# This file is to run the corresponding bat, exe and python files
import subprocess
import os

hrDeviceName = "Polar H7"

current_dir = os.getcwd()

# Run the Muse EEG
print("========== Connecting to Muse EEG... ==========")
# p1 = subprocess.Popen(current_dir + "\muse\StreamMuse.bat")
musecmd = "muse-io --osc-bp-urls osc.udp://127.0.0.1:6000/muse/elements/ --osc-battery-urls osc.udp://127.0.0.1:6000/muse/batt/"

p1 = subprocess.Popen(musecmd)
stdout, stderr = p1.communicate()

# return 0 if success
if p1.returncode == 0:
    print("========== Muse EEG connected! ==========")
os.system('python lsl/outstream_muse.py')

# Run Polar HR/HVR device
print("========== Connecting to Polar HR/HVR device... ==========")
p2 = subprocess.Popen(current_dir + "\\ble\BLEPolarDirect\\bin\Debug\BLEPolarDirect.exe" + " \"" + hrDeviceName+"\"")

stdout, stderr = p2.communicate()
# return 0 if success
if p2.returncode == 0:
    print("========== Polar HR/HVR device connected! ==========")

# Run Shadow Suit applications
# Make sure having MuseLab under C:\Program Files (x86)\Muse
print("========== Connecting to Shadow Suit... ==========")
p3 = subprocess.Popen("C:\Program Files\Motion\Shadow.exe")
stdout, stderr = p3.communicate()
# return 0 if success
if p3.returncode == 0:
    print("========== Shadow Suit connected! ==========")
os.system('python lsl/outstream_shadowsuit.py')

# Run Webcam applications
print("========== Connecting to Webcam... ==========")
os.system('python lsl/outstream_webcam.py')

print("========== Done! ==========")

