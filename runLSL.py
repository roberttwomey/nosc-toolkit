# This file is to run the corresponding bat, exe and python files
import subprocess
import os

# Run the Muse EEG
current_dir = os.getcwd()
#p1 = subprocess.Popen(current_dir + "\muse\StreamMuse.bat")
#os.system('python lsl/outstream_muse.py')

# Run Polar HR/HVR device
p2 = subprocess.Popen(current_dir + "\\ble\BLEPolarDirect\\bin\Debug\BLEPolarDirect.exe")
#stdout, stderr = p2.communicate()
#print("Polar HR/HVR device return code: ", p2.returncode) # return 0 if success

# Run Shadow Suit applications
# Make sure having MuseLab under C:\Program Files (x86)\Muse
p3 = subprocess.Popen("C:\Program Files\Motion\Shadow.exe")
#stdout, stderr = p3.communicate()
#print("Shadow Suit return code: ", p3.returncode) # return 0 if success
#call(["python", "lsl/outstream_shadow.py"])
os.system('python lsl/outstream_shadow.py')

# Run Webcam applications
#call(["python", "lsl/outstream_webcam.py"])
os.system('python lsl/outstream_webcam.py')

