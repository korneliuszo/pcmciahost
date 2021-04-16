
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
        self.s.flush()
        time.sleep(0.2)
        self.s.reset_input_buffer()
    
    def ping(self,val):
        self.s.write(struct.pack(">BB",0x05,val))
        return self.s.read(1)[0]

    def ready(self):
        self.s.write(struct.pack(">B",0x06))
        return self.s.read(1)[0]

    def reset(self):
        self.s.write(b"\x02\x01")
        self.s.flush()
        time.sleep(0.2)
        self.s.write(b"\x02\x00")
        self.s.flush()
        time.sleep(0.2)
        while not self.ready():
            pass
    
    def readattr(self,addr):
        self.s.write(struct.pack(">BL",0x03,addr))
        return self.s.read(1)[0]

    def readattrit(self):
        addr = 0
        while True:
            yield self.readattr(addr)
            addr +=2
