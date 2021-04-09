#!/usr/bin/env python3

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


knownid = {
        0x01 : lambda t: CISTPL_DEVICE(t),
        0x1C : lambda t: CISTPL_DEVICE_OC(t),
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
