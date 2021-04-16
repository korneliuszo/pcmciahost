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
        self.fcr.CONFIG_OPTION = selconf
        print("Config:",self.fcr.CONFIG_OPTION)


if __name__ == '__main__':
    i = IdeConn("/dev/ttyACM0")
