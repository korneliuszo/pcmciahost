
import serial
import time
import struct

class PcmciaConn():
    def __init__(self,port):
        self.s=serial.Serial()
        self.s.port = port
        self.s.baudrate = 76800
        self.s.setDTR(False)
        self.s.open()
        time.sleep(1)

    def sync(self):
        self.s.write(b"\x00\x00\x00\x00\x00\x00")
    
    def ping(self,val):
        self.s.write(struct.pack(">BB",0x05,val))
        return self.s.read(1)[0]
    
    def reset(self):
        self.s.write(b"\x02\x01")
        self.s.flush()
        time.sleep(0.2)
        self.s.write(b"\x02\x00")
        self.s.flush()
        time.sleep(0.2)
    
    def readattr(self,addr):
        self.s.write(struct.pack(">BL",0x03,addr))
        return self.s.read(1)[0]
