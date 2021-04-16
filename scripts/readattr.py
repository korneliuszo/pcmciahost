#!/usr/bin/env python3

import pcmciaconn
import sys

p=pcmciaconn.PcmciaConn("/dev/ttyACM0")
print("sync")
p.sync()
print("Ping:", p.ping(34))
print("reset")
p.reset()
print("read")

f=open(sys.argv[1],"wb")
it = p.readattrit()
while True:
    t=[]
    t.append(next(it))
    if t[0]==0xff:
        f.write(bytes(t))
        break
    l=next(it)
    t.append(l)
    for a in range(l):
        t.append(next(it))
    f.write(bytes(t))

