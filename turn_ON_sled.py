#!/usr/bin/python
import sys, time, signal

sys.path.append('C:/Users/DCC-User/Documents/GitHub/Rudolph')
from sledclient import SledClient

# Set connection details
host = "sled"
port = 3375

# Establish connection
client = SledClient()
client.connect(host, port)

# Start streaming positions
client.startStream()
time.sleep(1)

while 1:
    ri = raw_input("Press 1:Lights ON, 2:Lights OFF, 3:Sled ON, 4:Sled OFF, 5:Go to, 8:esc")

    if ri == '1':
        client.sendCommand("Lights On")
        print "Lights ON"
    if ri == '2':
        client.sendCommand("Lights Off")
        print "Lights Off"
    if ri == '3':
        client.sendCommand("Sinusoid Start 0.15 1.6")
        print "Sled ON"
    if ri == '4':
        client.sendCommand("Sinusoid Stop")
        print "Sled OFF"
    if ri == '5':
        goto_sled = raw_input("go where?")
        client.goto(goto_sled)
        print "go to"
        time.sleep(3)
    if ri == '8':
        break;



# Shutdown
client.sendCommand("Bye")
client.__del__()

