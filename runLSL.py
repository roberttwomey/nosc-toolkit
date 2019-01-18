# This file is to run the corresponding bat and python files
import subprocess
import os

# Run the Muse EEG
current_dir = os.getcwd()
print("=============",current_dir + "\muse\StreamMuse.bat")
p1 = subprocess.Popen(current_dir + "\muse\StreamMuse.bat")
stdout, stderr = p1.communicate()
print("Muse EEG return code: ", p1.returncode) # return 0 if success
call(["python", "lsl/outstream_muse.py"])

# Run Polar HR/HVR device
p2 = Popen("ble/BLEPolarDirect/bin/Debug/BLEPolarDirect.exe")
stdout, stderr = p2.communicate()
print("Polar HR/HVR device return code: ", p2.returncode) # return 0 if success

# Run Shadow Suit applications
# Make sure having MuseLab under C:\Program Files (x86)\Muse
p3 = Popen("C:\Program Files\Motion\Shadow.exe")
stdout, stderr = p3.communicate()
print("Shadow Suit return code: ", p3.returncode) # return 0 if success
call(["python", "lsl/outstream_shadow.py"])

# Run Webcam applications
call(["python", "lsl/outstream_webcam.py"])

