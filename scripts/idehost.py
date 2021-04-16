#!/usr/bin/env python3
import pcmciaconn
import printattr
import funcconfregs
from whynotinpython import templatematch

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
        self.DATA = self.prop(0x1f0+0)
        self.ERROR_FEATURES = self.prop(0x1f0+1)
        self.SECT_COUNT = self.prop(0x1f0+2)
        self.SECT_NO = self.prop(0x1f0+3)
        self.CYL_LO = self.prop(0x1f0+4)
        self.CYL_HI = self.prop(0x1f0+5)
        self.SELC_H = self.prop(0x1f0+6)
        self.STAT_CMD = self.prop(0x1f0+7)
        self.ALTS_DEVCTRL = self.prop(0x3f6+0)
        self.DRV_ADDR = self.prop(0x3f6+1)

    def prop(self,addr):
        return property(lambda self : self.conn.readio(offset), lambda self, val : self.conn.writeio(offset, val))


if __name__ == '__main__':
    i = IdeConn("/dev/ttyACM0")
    i.SECT_NO = 0xAA
    print("SECT_NO:", hex(i.SECT_NO))
