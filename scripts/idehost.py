#!/usr/bin/env python3
import pcmciaconn
import printattr
import funcconfregs
from whynotinpython import templatematch
import time

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

    def busypoll(self):
        time.sleep(0.0000004)
        while self.i.ALTS_DEVCTRL & 0xc0 != 0x40:
            pass

if __name__ == '__main__':
    i = IdeHigh("/dev/ttyACM0")

