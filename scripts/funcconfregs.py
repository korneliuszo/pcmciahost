class FuncConfRegs():
    def __init__(self,conn,attr):
        self.conn = conn
        self.base = attr["CONFIG"]["TPCC_RADR"]
        self.mask = attr["CONFIG"]["TPCC_RMSK"]

    def isrange(self,offset):
        return self.mask & (1<<(offset//2))
    def getp(self, offset):
        if self.isrange(offset):
            return self.conn.readattr(self.base+offset)
        else:
            return None
    def setp(self, offset, val):
        if self.isrange(offset):
            return self.conn.writeattr(self.base+offset, val)

    def prop(offset):
        return property(lambda self : self.getp(offset), lambda self, val : self.setp(offset, val))

    CONFIG_OPTION = prop(0)
