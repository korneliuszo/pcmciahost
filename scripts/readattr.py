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
addr=0
while True:
    t=[]
    t.append(p.readattr(addr))
    if t[0]==0xff:
        f.write(bytes(t))
        break
    l=p.readattr(addr+2)
    t.append(l)
    for a in range(addr+4,addr+4+l*2,2):
        t.append(p.readattr(a))
    f.write(bytes(t))
    addr+=4+l*2

