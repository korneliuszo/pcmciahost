#!/usr/bin/env python3
import struct
import itertools

def CISTPL_DEVICE(t):
    ret = "CISTPL_DEVICE " + str(t) + "\n"
    i=2
    ret += DEVICE_INFO(t[i:])
    return ret

def DEVICE_INFO(t):
    ret = ""
    i = 0
    while t[i] != 0xff:
        device_type = {
                0 : "DTYPE_NULL",
                1 : "DTYPE_ROM",
                2 : "DTYPE_OTPROM",
                3 : "DTYPE_EPROM",
                4 : "DTYPE_EEPROM",
                5 : "DTYPE_FLASH",
                6 : "DTYPE_SRAM",
                7 : "DTYPE_DRAM",
                0xd: "DTYPE_FUNCSPEC",
                0xe: "DTYPE_EXTEND",
            }
        device_speed = {
                0 : "DSPEED_NULL",
                1 : "DSPEED_250NS",
                2 : "DSPEED_200NS",
                3 : "DSPEED_150NS",
                4 : "DSPEED_100NS",
                7 : "DSPEED_EXT",
            }
        ret += " " + device_type[t[i]>>4] + (" WEN " if t[i]&0x08 else " WP ") + device_speed[t[i]&0x7] +"\n"
        off=0
        if t[i]&0x7 == 0x7:
            off+=1
            device_speed_mantisa = {
                    0x1: 1.0,
                    0x2: 1.2,
                    0x3: 1.3,
                    0x4: 1.5,
                    0x5: 2.0,
                    0x6: 2.5,
                    0x7: 3.0,
                    0x8: 3.5,
                    0x9: 4.0,
                    0xa: 4.5,
                    0xb: 5.0,
                    0xc: 5.5,
                    0xd: 6.0,
                    0xe: 7.0,
                    0xf: 8.0,
                }
            device_speed_exponent = {
                    0: 1e-9,
                    1: 10e-9,
                    2: 100e-9,
                    3: 1e-6,
                    4: 10e-6,
                    5: 100e-6,
                    6: 1e-3,
                    7: 10e-3,
                }
            ret += "  EXTENDED DEV_SPEED: " + "{:.1e}\n".format(
                    device_speed_mantisa[(t[i+off]&0x78)>>4] *
                    device_speed_exponent[(t[i+off]&0x07)])
            while t[i+off] &0x80:
                ret += "  EXTENDED DEV_SPEED: " + hex(t[i+off])+"\n"
                off+=1

        if t[i]&0xf0 == 0xe0:        
            off+=1
            ret += "  EXTENDED DEV_ID: " + hex(t[i+off])+"\n"
            while t[i+off] &0x80:
                ret += "  EXTENDED DEV_ID: " + hex(t[i+off])+"\n"
                off+=1
        i+=off+1
    return ret

def CISTPL_DEVICE_OC(t):
    ret = "CISTPL_DEVICE_OC " + str(t) + "\n"
    i=2
    VCC_DICT = { 0: "5V", 1:"3.3V",2: "X.XV", 3:"Y.YV"}

    while True:
        ret+=" VCC " + VCC_DICT[(t[i]>>1)&0x3] + (" MWAIT" if t[i]&0x01 else " NOMWAIT") + "\n"
        i+=1
        if not t[i-1]&0x80:
            break
    ret+=DEVICE_INFO(t[i:])
    return ret

def CISTPL_JEDEC_C(t):
    ret = "CISTPL_DEVICE_JEDEC_C " + str(t) + "\n"
    i=2
    for mfg,cid in zip(t[i::2], t[i+1::2]):
        ret+=" MFG: " + hex(mfg) + " ID: " + hex(cid) + "\n"
    return ret

def CISTPL_MANFID(t):
    ret = "CISTPL_MANFID " + str(t) + "\n"
    manf,card = struct.unpack("<HH",bytes(t[2:]))
    ret += " MANF: " + hex(manf) + " CARD: " + hex(card) +"\n"
    return ret


def CISTPL_VERS_1(t):
    ret = "CISTPL_VERS_1 " + str(t) + "\n"
    ret += " MAJOR: " + str(t[2]) + " MINOR: " + str(t[3]) + "\n"
    i = iter(t[4:])
    for info in ("PRODUCT: ", "NAME: ", "ADD1: ", "ADD2: "):
        st=next(i)
        if st == 0xff:
            return ret
        if st == 0:
            string = ""
        else:
            string=chr(st) + bytes(itertools.takewhile(int(0).__ne__,i)).decode("ascii")
        ret+=" " + info + string + "\n"
    return ret

def CISTPL_FUNCID(t):
    ret = "CISTPL_FUNCID " + str(t) + "\n"
    functiondict = {
            0x00: "Multi-Function",
            0x01: "Memory",
            0x02: "Serial Port",
            0x03: "Parallel Port",
            0x04: "Fixed Disk",
            0x05: "Video Adapter",
            0x06: "Network Adapter",
            0x07: "AIMS",
            0x08: "SCSI",
            0x09: "Security",
            0x0A: "Instrument",
            0x0B: "Serial I/O Bus Adapter",
            0xFE: "Vendor-Specific",
            0xFF: "Do Not Use",
        }
    ret += " FUNCTION: " + functiondict[t[2]] + "\n"
    ret += " " + ("ROM" if t[3]&0x02 else "NOROM") + " " + ("POST" if t[3]&0x01 else "NOPOST") + "\n"
    return ret

def CISTPL_FUNCE(t):
    def FUNCE_ATA(t):
        ret = " FUNCE_ATA\n"
        return ret
    def FUNCE_ATA2(t):
        ret = " FUNCE_ATA2\n"
        ret += "  V=" + str((t[3]&0x03)>>0) + "\n"
        ret += "  S=" + str((t[3]&0x04)>>2) + "\n"
        ret += "  U=" + str((t[3]&0x08)>>3) + "\n"
        ret += "  D=" + str((t[3]&0x10)>>4) + "\n"
        ret += "  P0=" + str((t[4]&0x01)>>0) + "\n"
        ret += "  P1=" + str((t[4]&0x02)>>1) + "\n"
        ret += "  P2=" + str((t[4]&0x04)>>2) + "\n"
        ret += "  P3=" + str((t[4]&0x08)>>3) + "\n"
        ret += "  N=" + str((t[4]&0x10)>>4) + "\n"
        ret += "  E=" + str((t[4]&0x20)>>5) + "\n"
        ret += "  I=" + str((t[4]&0x40)>>6) + "\n"
        return ret

    ret = "CISTPL_FUNCE " + str(t) + "\n"
    knownfunc = {
            0x01 : FUNCE_ATA,
            0x02 : FUNCE_ATA2,
        }
    if t[2] in knownfunc.keys():
        return ret + knownfunc[t[2]](t)
    else:
        return ret + " UNKNOWN"

def CISTPL_CONFIG(t):
    ret = "CISTPL_CONFIG " + str(t) + "\n"
    tpcc_rmsz = ((t[2] & 0x3C)>>2) + 1
    tpcc_rasz = ((t[2] & 0x03)>>0) + 1
    ret += " TPCC_LAST: " + str(t[3]) + "\n"
    n=0
    TPC_RADR = 0
    for val in t[4:4+tpcc_rasz]:
        TPC_RADR |= val << n
        n+=8
    ret += " TPC_RADR: " + hex(TPC_RADR) + "\n"
    n=0
    TPC_RMSK = 0
    for val in t[4+tpcc_rasz:4+tpcc_rasz+tpcc_rmsz]:
        TPC_RMSK |= val << n
        n+=8
    ret += " TPC_RMSK: " + hex(TPC_RMSK) + "\n"
    return ret

def CISTPL_CFTABLE_ENTRY(t):
    ret = "CISTPL_CFTABLE_ENTRY " + str(t) + "\n"
    ret += " CONF_ENTRY_NUMBER: " + str(t[2]&0x3f) + (" (DEFAULT)\n" if t[2]&0x40 else "\n")
    reg = 3
    if t[2]&0x80:
        ift = {
                0 : "Memory",
                1 : "IO and Memory",
                4 : "Custom interface 0",
                5 : "Custom interface 1",
                6 : "Custom interface 2",
                7 : "Custom interface 3",
            }
        ret += " " + ift[t[reg]&0x0f] + "\n"
        ret += " " + "BVDs Active=" + str(bool(t[reg]&0x10)) + "\n"
        ret += " " + "WP Active=" + str(bool(t[reg]&0x20)) + "\n"
        ret += " " + "READY Active=" + str(bool(t[reg]&0x40)) + "\n"
        ret += " " + "M Wait Active=" + str(bool(t[reg]&0x80)) + "\n"
        reg+=1

    TPCE_FS = t[reg]
    reg+=1
    pd_dict = {
            0 : [],
            1 : ["Vcc"],
            2 : ["Vcc","Vpp"],
            3 : ["Vcc","Vpp1","Vpp2"],
        }
    for pd in pd_dict[TPCE_FS&0x03>>0]:
        TPCE_PD = t[reg]
        reg+=1
        ret += " " + pd + "\n"
        def to_int(t,reg, exps):
            mantisa = {
                    0 : 1.0,
                    1 : 1.2,
                    2 : 1.3,
                    3 : 1.5,
                    4 : 2.0,
                    5 : 2.5,
                    6 : 3.0,
                    7 : 3.5,
                    8 : 4.0,
                    9 : 4.5,
                    10 : 5.0,
                    11 : 5.5,
                    12 : 6.0,
                    13 : 7.0,
                    14 : 8.0,
                    15 : 9.0,
                }
            PD1 = t[reg]
            reg+=1
            val = mantisa[(PD1&0x78)>>3]
            ext = 0.01
            exps *= 10**((PD1&0x7)-7)
            PDX = PD1
            while PDX & 0x80:
                PDX = t[reg]
                reg+=1
                if (PDX&0x7F) == 0x7D:
                    return reg, str(val*exps)+"NC"
                if (PDX&0x7F) == 0x7E:
                    return reg, "ZERO"
                if (PDX&0x7F) == 0x7F:
                    return reg, "NC REQ"
                if (PDX&0x7F) < 100:
                    val += (PDX&0x7f)*ext
                    ext /= 100
            return str(val*exps),reg
        if TPCE_PD & 0x01:
            val,reg = to_int(t,reg,100)
            ret += "  Norm V: " + val + "V\n"
        if TPCE_PD & 0x02:
            val,reg = to_int(t,reg,100)
            ret += "  Min V: " + val + "V\n"
        if TPCE_PD & 0x04:
            val,reg = to_int(t,reg,100)
            ret += "  Max V: " + val + "V\n"
        if TPCE_PD & 0x08:
            val,reg = to_int(t,reg,1)
            ret += "  Static I: " + val + "A\n"
        if TPCE_PD & 0x10:
            val,reg = to_int(t,reg,1)
            ret += "  Avg I: " + val + "A\n"
        if TPCE_PD & 0x20:
            val,reg = to_int(t,reg,1)
            ret += "  Peak I: " + val + "A\n"
        if TPCE_PD & 0x40:
            val,reg = to_int(t,reg,1)
            ret += "  PDwn I: " + val + "A\n"
    if TPCE_FS & 0x04:
        TPCE_TD = t[reg]
        reg+=1
        ret += " WAIT Scale: " + str(TPCE_TD&0x03>>0) + "\n"
        ret += " READY Scale: " + str(TPCE_TD&0x1C>>2) + "\n"
    if TPCE_FS & 0x08:
        TPCE_IO = t[reg]
        reg+=1
        bust = {
                1 : "8bit only",
                2 : "16bit only",
                3 : "8/16bit",
                }
        ret += " " + bust[(TPCE_IO&0x60)>>5] + "\n"
        ret += " IOAddrLines: " + str(TPCE_IO&0x1F) + "\n"
        if TPCE_IO & 0x80:
            IO_RANGE = t[reg]
            reg+=1
            for i in range((IO_RANGE&0x0f)+1):
                ret += " Range: " + str(i) + "\n"
                addr = 0
                for n in range((IO_RANGE&0x20)>>4):
                    addr |= t[reg] << (n*8)
                    reg+=1
                ret += "  Address: " + hex(addr) + "\n"
                length = 0
                for n in range((IO_RANGE&0xC0)>>6):
                    length |= t[reg] << (n*8)
                    reg+=1
                ret += "  Length: " + hex(length+1) + "\n"
    if TPCE_FS & 0x10:
        TPCE_IRQ = t[reg]
        reg+=1
        ret += " IRQ Share=" +str(bool(TPCE_IRQ&0x80)) + "\n"
        ret += " IRQ Pulse=" +str(bool(TPCE_IRQ&0x40)) + "\n"
        ret += " IRQ Level=" +str(bool(TPCE_IRQ&0x20)) + "\n"
        if not TPCE_IRQ&0x10:
            ret += " IRQ Line=" +str(TPCE_IRQ&0x0F) + "\n"
        else:
            ret += " IRQ VEND=" +str(bool(TPCE_IRQ&0x08)) + "\n"
            ret += " IRQ BERR=" +str(bool(TPCE_IRQ&0x04)) + "\n"
            ret += " IRQ IOCK=" +str(bool(TPCE_IRQ&0x02)) + "\n"
            ret += " IRQ NMI=" +str(bool(TPCE_IRQ&0x01)) + "\n"
            mask = t[reg] | (t[reg+1]<<8)
            reg+=2
            ret += " IRQ Mask=" + hex(mask) + "\n"
    if (TPCE_FS & 0x60)>>5 == 0:
        pass
    if (TPCE_FS & 0x60)>>5 == 1:
        length = (t[reg] | (t[reg+1]<<8))*256
        reg+=2
        ret += " Memory Length: " + str(length) + "\n"
    if (TPCE_FS & 0x60)>>5 == 2:
        length = (t[reg] | (t[reg+1]<<8))*256
        addr = (t[reg+2] | (t[reg+3]<<8))*256
        reg+=4
        ret += " Memory Address: " + hex(addr) + "\n"
        ret += " Memory Length: " + str(length) + "\n"
    if (TPCE_FS & 0x60)>>5 == 3:
        TPCE_MS = t[reg]
        reg+=1
        for i in range((TPCE_MS&0x07)+1):
            ret += " Range: " + str(i) + "\n"
            length = 0
            for n in range((TPCE_MS&0x18)>>3):
                length |= t[reg] << (n*8)
                reg+=1
            ret += "  Length: " + hex(length*256) + "\n"
            addr = 0
            for n in range((TPCE_MS&0x60)>>5):
                addr |= t[reg] << (n*8)
                reg+=1
            ret += "  Address: " + hex(addr*256) + "\n"
            if TPCE_MS&0x80:
                haddr = 0
                for n in range((TPCE_MS&0x60)>>5):
                    haddr |= t[reg] << (n*8)
                    reg+=1
                ret += "  Host Address: " + hex(addr*256) + "\n"
    if TPCE_FS & 0x80:
        TPCE_MI = t[reg]
        reg+=1
        ret += " Max Twin Cards: " + str(TPCE_MI&0x7) + "\n"
        ret += " Audio: " + str(bool(TPCE_MI&0x8)) + "\n"
        ret += " Read only: " + str(bool(TPCE_MI&0x10)) + "\n"
        ret += " Pwr Down: " + str(bool(TPCE_MI&0x20)) + "\n"
        if TPCE_MI&0x80:
            TPCE_MI2 = t[reg]
            reg+=1
            dmadict = {
                    0 : "None",
                    1 : "SPKR",
                    2 : "IOIS16",
                    3 : "INPACK",
                }
            ret += " Dma: " + dmadict[(TPCE_MI2&0x0C)>>2] + "\n"
            ret += " Dma: " + ("16bit" if (TPCE_MI2&0x10) else "8bit") + "\n"
            if TPCE_MI2&0x80:
                ret += " TH: " + str(t[reg]) + "." + str(t[reg+1]) + "\n"
                reg+=2
    return ret

knownid = {
        0x01 : CISTPL_DEVICE,
        0x1C : CISTPL_DEVICE_OC,
        0x18 : CISTPL_JEDEC_C,
        0x20 : CISTPL_MANFID,
        0x15 : CISTPL_VERS_1,
        0x21 : CISTPL_FUNCID,
        0x22 : CISTPL_FUNCE,
        0x1A : CISTPL_CONFIG,
        0x1B : CISTPL_CFTABLE_ENTRY,
        }

def pprinter(t):
    if t[0] in knownid.keys():
        return knownid[t[0]](t)
    else:
        return str(bytes(t)) + "\n" + str(t)

if __name__ == '__main__':
    f=open("attr.bin","rb")
    while True:
        t=[]
        t.append(f.read(1)[0])
        if t[0]==0xff:
            break
        l=f.read(1)[0]
        t.append(l)
        for a in range(l):
            t.append(f.read(1)[0])
        print(pprinter(t))
