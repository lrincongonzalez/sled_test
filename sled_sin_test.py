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



client.sendCommand("Lights On")

Period = 1.2,1.0
Repetitions = [02]


#loop starts here
#go to -0.15


for i in range(len(Repetitions)):
    for j in range(len(Period)):
        rep = Repetitions[i]
        T = Period[j]
        
        t_position = client.goto(-0.15)
        time.sleep(2)
        #open txt file
        file = open('sin{:03}rep{:02}.txt'.format(T,rep),'a')
        client.sendCommand("Sinusoid Start 0.15 {:03}".format(T))
        tstart = time.time()
        tzero = None
        while (time.time() - tstart) < 200.0:
            p = client.getPositionAndTime()

            if tzero is None:
                tzero = p[0]
            file.write(str(p[0] - tzero) + '\t' + str(p[1][0,0]) + '\n')
            time.sleep(0.001)
        
        print "Period {}, rep {}, Ran for {} ".format(T , rep , p[0] - tzero)

        client.sendCommand("Sinusoid Stop")
        time.sleep(2.0)
        file.close()
        
    


# Shutdown
client.sendCommand("Bye")
client.__del__()

