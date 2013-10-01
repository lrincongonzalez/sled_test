import numpy as np
import matplotlib.pyplot as pl

import time
import sys

sys.path.append('C:/Users/DCC-User/Documents/GitHub/Rudolph')
from sledclient import SledClient

client = SledClient()
client.connect('sled', 3375)

client.startStream()

client.sendCommand("Profile 40 Set Table 2 Abs -0.15 1.5")
client.sendCommand("Profile 40 Execute")
time.sleep(1.6)

client.sendCommand("Sinusoid Start 0.15 1.6")

#client.sendCommand("Profile 41 Set Table 0 Abs 0.15 0.8 Next 42")
#client.sendCommand("Profile 42 Set Table 0 Abs -0.15 0.8 Next 41")
#client.sendCommand("Profile 42 Execute")

#time.sleep(3.2)

#for i in range(0, 10):
# client.sendCommand("Profile {} Set Table 0 Abs -0.15 1.6".format(i))
# client.sendCommand("Profile {} Execute".format(i))



d_time = list()
d_position = list()

tstart = time.time()
tzero = None
while (time.time() - tstart) < 12.0:
  p = client.getPositionAndTime()

  if tzero is None:
    tzero = p[0]
    print "TZero is {}".format(tzero)

  d_time.append(p[0] - tzero)
  d_position.append(p[1][0, 0])
  time.sleep(0.001)

print "Ran for {} ".format(p[0] - tzero)

client.sendCommand("Sinusoid Stop")
time.sleep(2.0)


# Make plot

f = 1.0/1.6
pi = 3.1415926

T = np.array(d_time)
X = np.transpose( np.vstack((np.sin(2.0 * pi * f * T), np.cos(2.0 * pi * f * T))) )
Y = np.transpose(np.array(d_position)[np.newaxis])

out = np.linalg.lstsq(X, Y)
s = out[0][0]
c = out[0][1]
Yhat = np.sin(2.0 * pi * f * T) * s + np.cos(2.0 * pi * f * T) * c

Yhat = Yhat - np.mean(Yhat) + np.mean(Y)

print "SSE: ", np.sqrt(np.sum((Y - Yhat) ** 2))

pl.plot(T, Y)
pl.plot(T, Yhat)
pl.show()
