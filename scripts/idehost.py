#!/usr/bin/env python3
import pcmciaconn
import printattr
import funcconfregs
from whynotinpython import templatematch
import time
import struct

class IdeConn():
    def __init__(self,port):
        self.p = pcmciaconn.PcmciaConn(port)
        self.p.sync()
        self.p.reset()
        _, self.attr = printattr.parse_iterator(self.p.readattrit())
        self.fcr = funcconfregs.FuncConfRegs(self.p,self.attr)
        if self.attr["FUNCID"]["FUNCTION"] != "Fixed Disk":
            raise Exception("Not Disk card")
        selconf = None
        attrdict = {
                "IO_RANGE" : {
                    0 : {
                        "ADDR" : 0x1f0,
                        "LEN" : 8,
                    },
                    1 : {
                        "ADDR" : 0x3f6,
                        "LEN" : 2,
                    }
                }
            }
        for confid,conft in self.attr["CFTABLE"].items():
            for confd in conft:
                if templatematch(attrdict,confd):
                    selconf = confid
                    break
            if selconf is not None:
                break
        self.fcr.CONFIG_OPTION = selconf | (1<<6)
        print("Config:",hex(self.fcr.CONFIG_OPTION))
        self.fcr.SOCKET_COPY = 0

    def prop(addr):
        return property(lambda self : self.p.readio(addr), lambda self, val : self.p.writeio(addr, val))

    DATA = prop(0x1f0+0)
    ERROR_FEATURES = prop(0x1f0+1)
    SECT_COUNT = prop(0x1f0+2)
    SECT_NO = prop(0x1f0+3)
    CYL_LO = prop(0x1f0+4)
    CYL_HI = prop(0x1f0+5)
    SELC_H = prop(0x1f0+6)
    STAT_CMD = prop(0x1f0+7)
    ALTS_DEVCTRL = prop(0x3f6+0)
    DRV_ADDR = prop(0x3f6+1)

class IdeHigh():
    def __init__(self,port):
        self.i = IdeConn(port)
        self.i.ALTS_DEVCTRL = 4
        time.sleep(0.000005)
        self.i.ALTS_DEVCTRL = 0
        self.busypoll()
        self.i.SELC_H = 0xA0
        self.i.STAT_CMD = 0xEC
        self.busypoll()
        self.identity = { "RAW" : [] }
        for i in range(256):
            cl=self.i.DATA
            ch=self.i.DATA
            self.identity["RAW"].append(ch <<8 | cl)
        if self.identity["RAW"][0] != 0x848A:
            raise Exception("Uh, no valid magic number")
        self.identity["SN"] = self.idtoascii(self.identity["RAW"][10:20])
        self.identity["FW"] = self.idtoascii(self.identity["RAW"][23:27])
        self.identity["MN"] = self.idtoascii(self.identity["RAW"][27:47])
        self.identity["LBA"] = bool(self.identity["RAW"][49]&(1<<9))
        if not self.identity["LBA"]:
            raise Exception("We don't support non LBA")
        if self.capacity() > 0x0FFFFFFF:
            raise Exception("We don't support disks bigger than 128GB")

    def capacity(self):
        return (self.identity["RAW"][7] << 16) | self.identity["RAW"][8]

    def idtoascii(self,vals):
        ret = b""
        for i in vals:
            ret+=struct.pack(">H",i)
        return ret

    def busypoll(self):
        time.sleep(0.0000004)
        while self.i.ALTS_DEVCTRL & 0xc0 != 0x40:
            pass
    
    def setaddr(self,lba):
        self.i.SECT_COUNT = 1
        self.i.SECT_NO = (lba & 0x00000FF)>> 0
        self.i.CYL_LO = (lba & 0x000FF00)>> 8
        self.i.CYL_HI = (lba & 0x0FF0000)>>16
        self.i.SELC_H = (lba & 0xF000000)>>24 | 0xE0

    def read(self,addr):
        self.setaddr(addr)
        self.i.STAT_CMD = 0x20
        ret = b""
        for i in range(256):
            self.busypoll()            
            ret+=self.i.DATA.to_bytes(1,'little')
            ret+=self.i.DATA.to_bytes(1,'little')
        return ret

    def write(self,addr,data):
        self.setaddr(addr)
        self.i.STAT_CMD = 0x30
        ret = b""
        for i in data:
            self.busypoll()                        
            self.i.DATA = i
        self.busypoll()
        return 

if __name__ == '__main__':
    i = IdeHigh("/dev/ttyACM0")
    print(i.identity)
    print(i.capacity())
    print(i.read(0))
    sect= bytearray(i.read(1))
    print(sect)
    for idx, v in enumerate(sect):
        sect[idx] = 0xFF & ~v
    i.write(1,sect)
    print(i.read(1))


