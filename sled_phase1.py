#!/usr/bin/python
import sys, time, signal
import sledclient
import math

# there was a drift in the position values

#sys.path.append()
#to append Wilbert 


# Set connection details
host = "sled"
port = 3375

# Establish connection
client = sledclient.SledClient(verbose = 0, nBuffer = 5)
client.connect(host, port)

# Start streaming positions
client.startStream()
time.sleep(2)

client.sendCommand("Lights On")

#open txt file
file = open('Sled_phase3.txt','a')

#go to -0.15
t_position = client.goto(-0.15)
time.sleep(2.5)

# Getting the current position
position = client.getPosition(client.time())
print "Getting position ({} meter)".format(position[0][0])

# Sinusoidal motion
client.sendCommand("Sinusoid Start 0.15 1.6")

start_time = client.time()
file.write(str(start_time)+'\n')

T = 1.6
trials = 1

while 1:
    
    #Since it starts at -.15, sled goes to the right side
    LED = 1 #Right turning point
    
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
        
    time_2_stim = time_wait + client.time()
    while 1:
        if client.time()>time_2_stim:
            break
        
    # Getting the current position
    position = client.getPosition(client.time())
    time_stim = client.time() - start_time
    print "Position ({} meter)".format(position[0][0])
    file.write(str(position[0][0])+'\t'+str(time_stim)+'\n')
    
    LED = 2 #Left turning point
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
        
    time_2_stim = time_wait + client.time()
    while 1:
        if client.time()>time_2_stim:
            break
    # Getting the current position
    position = client.getPosition(client.time())
    time_stim = client.time() - start_time
    print "Position ({} meter)".format(position[0][0])
    file.write(str(position[0][0])+'\t'+str(time_stim)+'\n')
        
    trials += 1 
        
    if trials > 100:
        #position = client.getPosition(client.time())
        #if position > 0.14:
        break
        

client.sendCommand("Sinusoid Stop")
time.sleep(1.0)
file.close()

# Shutdown
client.sendCommand("Bye")
client.__del__()

