#!/usr/bin/env python3
import struct
import itertools
import copy

def CISTPL_DEVICE(t,pdict):
    ret = "CISTPL_DEVICE " + str(t) + "\n"
    i=2
    leaf = {}
    ret += DEVICE_INFO(t[i:],leaf)
    pdict["DEVICE"]=leaf
    return ret

def CISTPL_DEVICEA(t,pdict):
    ret = "CISTPL_DEVICEA " + str(t) + "\n"
    i=2
    leaf = {}
    ret += DEVICE_INFO(t[i:],leaf)
    pdict["DEVICEA"]=leaf
    return ret

def CISTPL_DEVICEOA(t,pdict):
    ret = "CISTPL_DEVICEOA " + str(t) + "\n"
    i=2
    leaf = {}
    ret += DEVICE_INFO(t[i:],leaf)
    pdict["DEVICEOA"]=leaf
    return ret

def DEVICE_INFO(t,leaf):
    ret = ""
    i = 0
    leaf["DeviceInfo"]=[]
    while t[i] != 0xff:
        leaf2={}
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
                0 : ("DSPEED_NULL",None),
                1 : ("DSPEED_250NS",250e-9),
                2 : ("DSPEED_200NS",200e-9),
                3 : ("DSPEED_150NS",150e-9),
                4 : ("DSPEED_100NS",100e-9),
                7 : ("DSPEED_EXT",None),
            }
        ret += " " + device_type[t[i]>>4] + (" WEN " if t[i]&0x08 else " WP ") + device_speed[t[i]&0x7][0] +"\n"
        leaf2["Dtype"] = device_type[t[i]>>4]
        leaf2["WEN"] = bool(t[i]&0x08)
        leaf2["Speed"] = device_speed[t[i]&0x7][1]
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
            speed= device_speed_mantisa[(t[i+off]&0x78)>>4] * device_speed_exponent[(t[i+off]&0x07)]
            ret += "  EXTENDED DEV_SPEED: " + "{:.1e}\n".format(speed)
            leaf2["Speed"] = speed

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
        leaf["DeviceInfo"].append(leaf2)
    return ret

def CISTPL_DEVICE_OC(t,pdict):
    ret = "CISTPL_DEVICE_OC " + str(t) + "\n"
    i=2
    VCC_DICT = { 0: "5V", 1:"3.3V",2: "X.XV", 3:"Y.YV"}
    leaf = {}
    leaf["OtherCondidions"] = []
    while True:
        ret+=" VCC " + VCC_DICT[(t[i]>>1)&0x3] + (" MWAIT" if t[i]&0x01 else " NOMWAIT") + "\n"
        leaf["OtherCondidions"].append({
                "VCC" :  VCC_DICT[(t[i]>>1)&0x3],
                "MWAIT" : bool(t[i]&0x01),
            }) 
        i+=1
        if not t[i-1]&0x80:
            break
    ret+=DEVICE_INFO(t[i:],leaf)
    pdict["DEVICE_OC"]=leaf    
    return ret

def CISTPL_JEDEC_C(t,pdict):
    ret = "CISTPL_DEVICE_JEDEC_C " + str(t) + "\n"
    i=2
    leaf=[]
    for mfg,cid in zip(t[i::2], t[i+1::2]):
        ret+=" MFG: " + hex(mfg) + " ID: " + hex(cid) + "\n"
        leaf.append({
            "MFG" : mfg,
            "ID" : cid,
        })
    pdict["JEDEC"] = leaf
    return ret

def CISTPL_JEDEC_A(t,pdict):
    ret = "CISTPL_DEVICE_JEDEC_A " + str(t) + "\n"
    i=2
    leaf=[]
    for mfg,cid in zip(t[i::2], t[i+1::2]):
        ret+=" MFG: " + hex(mfg) + " ID: " + hex(cid) + "\n"
        leaf.append({
            "MFG" : mfg,
            "ID" : cid,
        })
    pdict["JEDEC_A"] = leaf
    return ret


def CISTPL_MANFID(t,pdict):
    pdict.setdefault("MANFID",[])
    ret = "CISTPL_MANFID " + str(t) + "\n"
    manf,card = struct.unpack("<HH",bytes(t[2:6]))
    ret += " MANF: " + hex(manf) + " CARD: " + hex(card) +"\n"
    pdict["MANFID"].append({ "MANF" : manf, "CARD" : card})
    return ret


def CISTPL_VERS_1(t,pdict):
    leaf = {}
    ret = "CISTPL_VERS_1 " + str(t) + "\n"
    ret += " MAJOR: " + str(t[2]) + " MINOR: " + str(t[3]) + "\n"
    leaf["MAJOR"] = t[2]
    leaf["MINOR"] = t[3]
    i = iter(t[4:])
    for info in ("PRODUCT", "NAME", "ADD1", "ADD2"):
        st=next(i)
        if st == 0xff:
            pdict["VERS"] = leaf
            return ret
        if st == 0:
            string = ""
        else:
            string=chr(st) + bytes(itertools.takewhile(int(0).__ne__,i)).decode("ascii")
        ret+=" " + info + ": " + string + "\n"
        leaf[info] = string
    pdict["VERS"] = leaf
    return ret

def CISTPL_FUNCID(t,pdict):
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
    pdict["FUNCID"] = {}
    pdict["FUNCID"]["FUNCTION"] = functiondict[t[2]]
    pdict["FUNCID"]["ROM"] =  bool(t[3]&0x02)
    pdict["FUNCID"]["POST"] =  bool(t[3]&0x01)
    return ret

def CISTPL_FUNCE(t,pdict):
    pdict.setdefault("FUNCE",[])
    def FUNCE_ATA(t,leaf):
        ret = " FUNCE_ATA\n"
        leaf["TYPE"] = "ATA"
        return ret
    def FUNCE_ATA2(t,leaf):
        ret = " FUNCE_ATA2\n"
        leaf["TYPE"] = "ATA2"
        bitdict = {
            "V"  : bool((t[3]&0x03)>>0),
            "S"  : bool((t[3]&0x04)>>2),
            "U"  : bool((t[3]&0x08)>>3),
            "D"  : bool((t[3]&0x10)>>4),
            "P0" : bool((t[4]&0x01)>>0),
            "P1" : bool((t[4]&0x02)>>1),
            "P2" : bool((t[4]&0x04)>>2),
            "P3" : bool((t[4]&0x08)>>3),
            "N"  : bool((t[4]&0x10)>>4),
            "E"  : bool((t[4]&0x20)>>5),
            "I"  : bool((t[4]&0x40)>>6),
        }
        for key,val in bitdict.items():
            ret += "  " + key + "=" + str(val) + "\n"
            leaf[key] = val
        return ret

    def FUNCE_LAN_TECH(t,leaf):
        ret = " FUNCE_LAN_TECH\n"
        leaf["TYPE"] = "LAN_TECH"
        techdict = {
                1 : "Arcnet",
                2 : "Ethernet",
                3 : "Token Ring",
                4 : "Local Talk",
                5 : "FDDI/CDDI",
                6 : "ATM",
                7 : "Wireless",
            }
        tech = techdict[t[3]]
        ret += "  TECH: " + tech + "\n"
        leaf["TECH"] = tech
        return ret

    def FUNCE_LAN_SPEED(t,leaf):
        ret = " FUNCE_LAN_SPEED\n"
        leaf["TYPE"] = "LAN_SPEED"
        tech = struct.unpack("<L",bytes(t[3:7]))[0]
        ret += "  SPEED: " + str(tech) + "\n"
        leaf["SPEED"] = tech
        return ret

    def FUNCE_LAN_MEDIA(t,leaf):
        ret = " FUNCE_LAN_MEDIA\n"
        leaf["TYPE"] = "LAN_MEDIA"
        mediadict = {
                1 : "Unshielded twisted pair",
                2 : "Shielded twisted pair",
                3 : "Thin coax",
                4 : "Thick coax",
                5 : "Fiber",
                6 : "Spread spectrum radio 902-928 MHz",
                7 : "Spread spectrum radio 2.4 GHz",
                8 : "Spread spectrum radio 5.4 GHz",
                9 : "Diffuse infra red",
                10 : "Point to point infra red",
            }
        media = mediadict[t[3]]
        ret += "  MEDIA: " + media + "\n"
        leaf["MEDIA"] = media
        return ret

    def FUNCE_LAN_NID(t,leaf):
        ret = " FUNCE_LAN_NID\n"
        leaf["TYPE"] = "LAN_NID"
        nid = ':'.join('%02x' % b for b in t[4:4+t[3]])
        ret += "  NID: " + nid + "\n"
        leaf["NID"] =nid
        return ret

    def FUNCE_LAN_CONN(t,leaf):
        ret = " FUNCE_LAN_CONN\n"
        leaf["TYPE"] = "LAN_CONN"
        conn = "Closed connector standard" if t[3] else "Open connector standard"
        ret += "  Conn: " + conn + "\n"
        leaf["CONN"] = conn
        return ret

    def FUNCE_SIO_USB(t, leaf):      
        ret = " FUNCE_SIO)USB\n"
        leaf["TYPE"] = "SIO_USB"
        typed = {
            0x00 : "USB/OHCI",
            0x01 : "USB/Universal",
            0x02 : "NHCI"
            }
        ret += "  TYPE: " + typed[t[3]] + "\n"
        leaf["TYPE"] = typed[t[3]]
        powerd = {
            0x00 : "Self Powered",
            0x01 : "Bus Powered",
            0x02 : "100mA",
            0x03 : "500mA",
            }
        ret += "  POWER: " + powerd[t[4]] + "\n"
        leaf["POWER"] = powerd[t[4]]
        speed = struct.unpack("<H",bytes(t[5:7]))[0]
        ret += "  SPEED: " + str(speed) + "\n"
        leaf["SPEED"] = speed
        return ret

    ret = "CISTPL_FUNCE " + str(t) + "\n"
    knownfunc = {
            "Fixed Disk" : {
                0x01 : FUNCE_ATA,
                0x02 : FUNCE_ATA2,
            },
            "Network Adapter" : {
                0x01 : FUNCE_LAN_TECH,
                0x02 : FUNCE_LAN_SPEED,
                0x03 : FUNCE_LAN_MEDIA,
                0x04 : FUNCE_LAN_NID,
                0x05 : FUNCE_LAN_CONN,
            },
            "Serial I/O Bus Adapter" : {
                0x02 : FUNCE_SIO_USB,
            }
        }
    if pdict["FUNCID"]["FUNCTION"] in knownfunc.keys():
        if t[2] in knownfunc[pdict["FUNCID"]["FUNCTION"]].keys():
            leaf = {}
            ret += knownfunc[pdict["FUNCID"]["FUNCTION"]][t[2]](t,leaf)
            pdict["FUNCE"].append(leaf)
            return ret
        else:
            return ret + " UNKNOWN" + "\n"
    else:
        return ret + " UNKNOWN" + "\n"

def CISTPL_CONFIG(t,pdict):
    ret = "CISTPL_CONFIG " + str(t) + "\n"
    tpcc_rmsz = ((t[2] & 0x3C)>>2) + 1
    tpcc_rasz = ((t[2] & 0x03)>>0) + 1
    ret += " TPCC_LAST: " + str(t[3]) + "\n"
    n=0
    TPCC_RADR = 0
    for val in t[4:4+tpcc_rasz]:
        TPCC_RADR |= val << n
        n+=8
    ret += " TPCC_RADR: " + hex(TPCC_RADR) + "\n"
    n=0
    TPCC_RMSK = 0
    for val in t[4+tpcc_rasz:4+tpcc_rasz+tpcc_rmsz]:
        TPCC_RMSK |= val << n
        n+=8
    ret += " TPCC_RMSK: " + hex(TPCC_RMSK) + "\n"
    pdict["CONFIG"] = {
            "TPCC_LAST" : t[3],
            "TPCC_RADR" : TPCC_RADR,
            "TPCC_RMSK" : TPCC_RMSK,
        }
    return ret

def CISTPL_CFTABLE_ENTRY(t,pdict):
    ret = "CISTPL_CFTABLE_ENTRY " + str(t) + "\n"
    ret += " CONF_ENTRY_NUMBER: " + str(t[2]&0x3f) + (" (DEFAULT)\n" if t[2]&0x40 else "\n")
    idx = t[2]&0x3f
    pdict.setdefault("CFTABLE",{})
    pdict["CFTABLE"].setdefault(idx,[])
    leaf = copy.deepcopy(pdict["CFTABLE"][idx][-1]) if len(pdict["CFTABLE"][idx]) else {}
    leaf["DEFAULT"] = bool(t[2]&0x40)
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
        leaf["IF_TYPE"] = ift[t[reg]&0x0f]
        tpce_if_fields = {
                "BVDs" : bool(t[reg]&0x10),
                "WP"  : bool(t[reg]&0x20),
                "READY" : bool(t[reg]&0x40),
                "M Wait" : bool(t[reg]&0x80),
            }
        for key,val in tpce_if_fields.items():
            ret += " " + key + " Active=" + str(val) + "\n"
            leaf["IF_"+key] = val
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
        leaf.setdefault(pd,{})
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
            leaf[pd]["V_Norm"] = val
        if TPCE_PD & 0x02:
            val,reg = to_int(t,reg,100)
            ret += "  Min V: " + val + "V\n"
            leaf[pd]["V_Min"] = val
        if TPCE_PD & 0x04:
            val,reg = to_int(t,reg,100)
            ret += "  Max V: " + val + "V\n"
            leaf[pd]["V_Max"] = val
        if TPCE_PD & 0x08:
            val,reg = to_int(t,reg,1)
            ret += "  Static I: " + val + "A\n"
            leaf[pd]["I_Static"] = val
        if TPCE_PD & 0x10:
            val,reg = to_int(t,reg,1)
            ret += "  Avg I: " + val + "A\n"
            leaf[pd]["I_Avg"] = val
        if TPCE_PD & 0x20:
            val,reg = to_int(t,reg,1)
            ret += "  Peak I: " + val + "A\n"
            leaf[pd]["I_Peak"] = val
        if TPCE_PD & 0x40:
            val,reg = to_int(t,reg,1)
            ret += "  PDwn I: " + val + "A\n"
            leaf[pd]["I_PDwn"] = val
    if TPCE_FS & 0x04:
        TPCE_TD = t[reg]
        reg+=1
        ret += " WAIT Scale: " + str((TPCE_TD&0x03)>>0) + "\n"
        leaf["TD_WAIT"] = (TPCE_TD&0x03)>>0
        ret += " READY Scale: " + str((TPCE_TD&0x1C)>>2) + "\n"
        leaf["TD_READY"] = (TPCE_TD&0x1C)>>2
    if TPCE_FS & 0x08:
        TPCE_IO = t[reg]
        reg+=1
        bust = {
                0 : "Reserved",
                1 : "8bit only",
                2 : "16bit only",
                3 : "8/16bit",
                }
        ret += " " + bust[(TPCE_IO&0x60)>>5] + "\n"
        leaf["IO_TYPE"] = bust[(TPCE_IO&0x60)>>5]
        ret += " IOAddrLines: " + str(TPCE_IO&0x1F) + "\n"
        leaf["IO_AddrLines"] = TPCE_IO&0x1F
        if TPCE_IO & 0x80:
            leaf["IO_RANGE"] = {}
            IO_RANGE = t[reg]
            reg+=1
            for i in range((IO_RANGE&0x0f)+1):
                ret += " Range: " + str(i) + "\n"
                leaf["IO_RANGE"][i] = {}
                addr = 0
                for n in range((IO_RANGE&0x20)>>4):
                    addr |= t[reg] << (n*8)
                    reg+=1
                ret += "  Address: " + hex(addr) + "\n"
                leaf["IO_RANGE"][i]["ADDR"] = addr
                length = 0
                for n in range((IO_RANGE&0xC0)>>6):
                    length |= t[reg] << (n*8)
                    reg+=1
                ret += "  Length: " + hex(length+1) + "\n"
                leaf["IO_RANGE"][i]["LEN"] = length+1
    if TPCE_FS & 0x10:
        TPCE_IRQ = t[reg]
        reg+=1
        ret += " IRQ Share=" +str(bool(TPCE_IRQ&0x80)) + "\n"
        leaf["IRQ_Share"] = bool(TPCE_IRQ&0x80)
        ret += " IRQ Pulse=" +str(bool(TPCE_IRQ&0x40)) + "\n"
        leaf["IRQ_Pulse"] = bool(TPCE_IRQ&0x40)
        ret += " IRQ Level=" +str(bool(TPCE_IRQ&0x20)) + "\n"
        leaf["IRQ_Level"] = bool(TPCE_IRQ&0x20)
        if not TPCE_IRQ&0x10:
            ret += " IRQ Line=" +str(TPCE_IRQ&0x0F) + "\n"
            leaf["IRQ_Line"] = TPCE_IRQ&0x0F
        else:
            ret += " IRQ VEND=" +str(bool(TPCE_IRQ&0x08)) + "\n"
            leaf["IRQ_VEND"] = bool(TPCE_IRQ&0x08)
            ret += " IRQ BERR=" +str(bool(TPCE_IRQ&0x04)) + "\n"
            leaf["IRQ_BERR"] = bool(TPCE_IRQ&0x04)
            ret += " IRQ IOCK=" +str(bool(TPCE_IRQ&0x02)) + "\n"
            leaf["IRQ_IOCK"] = bool(TPCE_IRQ&0x02)
            ret += " IRQ NMI=" +str(bool(TPCE_IRQ&0x01)) + "\n"
            leaf["IRQ_NMI"] = bool(TPCE_IRQ&0x01)
            mask = t[reg] | (t[reg+1]<<8)
            reg+=2
            ret += " IRQ Mask=" + hex(mask) + "\n"
            leaf["IRQ_Mask"] = mask
    if (TPCE_FS & 0x60)>>5 == 0:
        pass
    if (TPCE_FS & 0x60)>>5 == 1:
        length = (t[reg] | (t[reg+1]<<8))*256
        reg+=2
        ret += " Memory Length: " + str(length) + "\n"
        leaf["MEM_RANGE"] = {0:{}}
        leaf["MEM_RANGE"][0]["Addr"] = 0
        leaf["MEM_RANGE"][0]["Len"] = length
        leaf["MEM_RANGE"][0]["Host_Addr"] = 0
    if (TPCE_FS & 0x60)>>5 == 2:
        length = (t[reg] | (t[reg+1]<<8))*256
        addr = (t[reg+2] | (t[reg+3]<<8))*256
        reg+=4
        ret += " Memory Address: " + hex(addr) + "\n"
        ret += " Memory Length: " + str(length) + "\n"
        leaf["MEM_RANGE"] = {0:{}}
        leaf["MEM_RANGE"][0]["MEM_Addr"] = addr
        leaf["MEM_RANGE"][0]["MEM_Len"] = length
        leaf["MEM_RANGE"][0]["Host_Addr"] = 0
    if (TPCE_FS & 0x60)>>5 == 3:
        TPCE_MS = t[reg]
        reg+=1
        leaf["MEM_RANGE"] = {}
        for i in range((TPCE_MS&0x07)+1):
            leaf["MEM_RANGE"][i] = {}
            ret += " Range: " + str(i) + "\n"
            length = 0
            for n in range((TPCE_MS&0x18)>>3):
                length |= t[reg] << (n*8)
                reg+=1
            ret += "  Length: " + hex(length*256) + "\n"
            leaf["MEM_RANGE"][i]["MEM_Len"] = length*256          
            addr = 0
            for n in range((TPCE_MS&0x60)>>5):
                addr |= t[reg] << (n*8)
                reg+=1
            ret += "  Address: " + hex(addr*256) + "\n"
            leaf["MEM_RANGE"][i]["MEM_Addr"] = addr*256
            leaf["MEM_RANGE"][i]["Host_Addr"] = 0
            if TPCE_MS&0x80:
                haddr = 0
                for n in range((TPCE_MS&0x60)>>5):
                    haddr |= t[reg] << (n*8)
                    reg+=1
                ret += "  Host Address: " + hex(haddr*256) + "\n"
                leaf["MEM_RANGE"][i]["Host_Addr"] = haddr*256
    if TPCE_FS & 0x80:
        TPCE_MI = t[reg]
        reg+=1
        ret += " Max Twin Cards: " + str(TPCE_MI&0x7) + "\n"
        leaf["FS_TwinCards"] = TPCE_MI&0x7
        ret += " Audio: " + str(bool(TPCE_MI&0x8)) + "\n"
        leaf["FS_Audio"] = bool(TPCE_MI&0x8)
        ret += " Read only: " + str(bool(TPCE_MI&0x10)) + "\n"
        leaf["FS_RO"] = bool(TPCE_MI&0x10)
        ret += " Pwr Down: " + str(bool(TPCE_MI&0x20)) + "\n"
        leaf["FS_PWRDWN"] = bool(TPCE_MI&0x20)
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
            leaf["FS_DMA_PIN"] = dmadict[(TPCE_MI2&0x0C)>>2]
            ret += " Dma: " + ("16bit" if (TPCE_MI2&0x10) else "8bit") + "\n"
            leaf["FS_DMA_Width"] = 16 if (TPCE_MI2&0x10) else 8
            if TPCE_MI2&0x80:
                ret += " TH: " + str(t[reg]) + "." + str(t[reg+1]) + "\n"
                leaf["FS_TH"] = str(t[reg]) + "." + str(t[reg+1])
                reg+=2
    pdict["CFTABLE"][idx].append(leaf)
    return ret

def CISTPL_NO_LINK(t,pdict):
    ret = "CISTPL_NO_LINK "  + str(t) + "\n"
    return ret

def CISTPL_VENDOR(t,pdict):
    ret = "CISTPL_VENDOR "  + str(t) + "\n"
    pdict.setdefault("VENDOR_"+hex(t[0]),[])
    pdict["VENDOR_"+hex(t[0])].append(bytes(t[2:]))
    return ret

def CISTPL_DATE(t,pdict):
    ret = "CISTPL_DATETIME "  + str(t) + "\n"
    import datetime
    s = t[2]&0x1f
    m = ((t[2]&0xE0)>>5) + (t[3]&0x07)*10
    h = (t[3]&0xF8)>>3
    d = t[4]&0x1F
    m = ((t[4]&0xE0)>>5) + (t[5]&0x01)*10
    y = ((t[5]&0xFE)>>1) + 1980
    date = datetime.datetime(y,m,d,h,m,s)
    ret += " " + date.isoformat() + "\n"
    pdict["DATE"] = date
    return ret

def CISTPL_CHECKSUM(t,pdict):
    ret = "CISTPL_CHECKSUM "  + str(t) + "\n"
    addr, length, checksum = struct.unpack("<hHB",bytes(t[2:7]))
    ret += " Addr: " + str(addr) + " Len: " + str(length) + " Checksum: " + str(checksum) + "\n"
    pdict["CHECKSUM"] = {}
    pdict["CHECKSUM"]["ADDR"] = addr
    pdict["CHECKSUM"]["LEN"] = length
    pdict["CHECKSUM"]["CHECKSUM"] = checksum
    return ret


knownid = {
        0x01 : CISTPL_DEVICE,
        0x17 : CISTPL_DEVICEA,
        0x1C : CISTPL_DEVICE_OC,
        0X1D : CISTPL_DEVICEOA,
        0x18 : CISTPL_JEDEC_C,
        0x19 : CISTPL_JEDEC_A,
        0x20 : CISTPL_MANFID,
        0x15 : CISTPL_VERS_1,
        0x21 : CISTPL_FUNCID,
        0x22 : CISTPL_FUNCE,
        0x1A : CISTPL_CONFIG,
        0x1B : CISTPL_CFTABLE_ENTRY,
        0x14 : CISTPL_NO_LINK,
        0x44 : CISTPL_DATE,
        0x10 : CISTPL_CHECKSUM,
        }
for i in range(0x80, 0x90):
    knownid[i] = CISTPL_VENDOR

def pprinter(t,pdict):
    if t[0] in knownid.keys():
        return knownid[t[0]](t,pdict)
    else:
        return "UNKNOWN\n " + str(bytes(t)) + "\n " + str(t) + "\n"

def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break

def parse_iterator(it):
    parseddict = {}
    ret = ""
    while True:
        t=[]
        t.append(next(it))
        if t[0]==0xff:
            break
        l=next(it)
        t.append(l)
        for a in range(l):
            t.append(next(it))
        ret+=pprinter(t,parseddict)
    return ret, parseddict


if __name__ == '__main__':
    import sys
    it=bytes_from_file(sys.argv[1])
    ret, parseddict = parse_iterator(it)
    print(ret)
    import yaml
    print(yaml.dump(parseddict, default_flow_style=False))
