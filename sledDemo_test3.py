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
print " "

#open txt file
file = open('Sled_test8.txt','a')

client.sendCommand("Lights On")

#go to -0.15
t_position = client.goto(-0.15)
time.sleep(2)

# Getting the current position
position = client.getPosition()
print "Getting position ({} meter)".format(position[0][0,0])
p = client.getPositionAndTime()
print "Getting time ({} sec)".format(p[0])
print "Getting time ({} sec)".format(p[1][0,0])

# Sinusoidal motion
client.sendCommand("Sinusoid Start 0.15 1.6")
start_time = client.time()
start_comp_time = time.time()

    
file.write(str(start_time)+'\t'+str(start_comp_time)+'\n')
print "start time: ({} seconds)".format(start_time)

while client.time()-start_time < 50:
    
   
    # Getting the current position
    position = client.getPosition()
    pos_time = client.time()
    comp_time = time.time()
       
    file.write(str(position[0][0,0])+'\t'+str(pos_time-start_time)+'\t'+str(comp_time-start_comp_time)+'\n')
        #print "Getting position ({} meter)".format(position)
        #print "client time: ({} seconds)".format(client.time())
        #time.sleep(.8)

client.sendCommand("Sinusoid Stop")
time.sleep(1)

file.close()


# Shutdown
client.sendCommand("Bye")
client.__del__()

