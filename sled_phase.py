#!/usr/bin/python
import sys, time, signal
import math
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

client.sendCommand("Lights On")

#open txt file
file = open('Sled_phase3.txt','a')

#go to -0.15
t_position = client.goto(-0.15)
time.sleep(2.5)

# Getting the current position
position = client.getPosition()
print "Getting position ({} meter)".format(position[0][0,0])

# Sinusoidal motion
client.sendCommand("Sinusoid Start 0.15 1.6")

start_time = client.time()
file.write(str(start_time)+'\n')

T = 1.6
trials = 1

while 1:
    
    #Since it starts at -.15, sled goes to the right side
    LED = 1 #Right turning point
    print "LED = RIGHT"
    time.sleep(.4)
    
    #Get time
    time_now = client.time() - start_time
    print "Time ({}seconds)".format(time_now)
    #claculate where in the cycle we are
    time_cycle = time_now/T
    mantissa = math.floor(time_cycle)
    fraction = time_cycle - mantissa
    
    if fraction < 0.5:
        time_wait = (mantissa)*T + 0.8 - time_now
    elif fraction > 0.5:
        time_wait = (mantissa + 1)*T + 0.8 - time_now
        
    time.sleep(time_wait)
    # Getting the current position
    while 1:
        position = client.getPosition()
        #print "position ({}seconds)".format(position[0][0,0])
        if position[0][0,0] > 0.14990:
            time_stim = client.time() - start_time
            print "Position ({} meter)".format(position[0][0,0])
            file.write(str(position[0][0,0])+'\t'+str(time_stim)+'\n')
            break
    
    LED = 2 #Left turning point
    print "LED = LEFT"
    time.sleep(.4)
    
    #Get time
    time_now = client.time() - start_time
    print "Time ({}seconds)".format(time_now)
    #claculate where in the cycle we are
    time_cycle = time_now/T
    mantissa = math.floor(time_cycle)
    fraction = time_cycle - mantissa
    
    if fraction < 0.5:
        time_wait = (mantissa)*T + 1.6 - time_now
    elif fraction > 0.5:
        time_wait = (mantissa + 1)*T - time_now
        
    time.sleep(time_wait)
    # Getting the current position
    while 1:
        position = client.getPosition()
        if position[0][0,0] < -0.14990:
            time_stim = client.time() - start_time
            print "Position ({} meter)".format(position[0][0,0])
            file.write(str(position[0][0,0])+'\t'+str(time_stim)+'\n')
            break
        
    trials += 1 
        
    if trials > 25:
        #position = client.getPosition(client.time())
        #if position > 0.14:
        break
        

client.sendCommand("Sinusoid Stop")
time.sleep(1.0)
file.close()

# Shutdown
client.sendCommand("Bye")
client.__del__()

