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

knownid = {
        0x01 : CISTPL_DEVICE,
        0x1C : CISTPL_DEVICE_OC,
        0x18 : CISTPL_JEDEC_C,
        0x20 : CISTPL_MANFID,
        0x15 : CISTPL_VERS_1,
        0x21 : CISTPL_FUNCID,
        0x22 : CISTPL_FUNCE,
        0x1A : CISTPL_CONFIG,
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
