# simulate 3D printer. Create virtual serial port and respond over port as a 
# printer would. For now just respond with "ok"

import subprocess
import serial
import os
import time

privend = "./priv"
pubend = "./pub"
killed = 0
baud = 115200
serial_timeout = 1

socat_p = subprocess.Popen(["socat", "PTY,link=%s" % privend, "PTY,link=%s" % pubend])
while not os.path.exists(privend) or not os.path.exists(pubend):
    time.sleep(0.1)
port = serial.Serial(privend, baudrate = baud, timeout = serial_timeout)

while not killed:
    input = port.readline()
    if input == b"":
        continue
    print(input)
    port.write(b'ok\n')

socat_p.terminate()