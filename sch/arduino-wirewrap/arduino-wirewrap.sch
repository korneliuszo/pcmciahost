EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L arduino:Arduino_Mega2560_Shield XA1
U 1 1 6002D235
P 3500 4250
F 0 "XA1" H 3500 1869 60  0000 C CNN
F 1 "Arduino_Mega2560_Shield" H 3500 1763 60  0000 C CNN
F 2 "Arduino:Arduino_Mega2560_Shield" H 4200 7000 60  0001 C CNN
F 3 "https://store.arduino.cc/arduino-mega-2560-rev3" H 4200 7000 60  0001 C CNN
	1    3500 4250
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x34_Top_Bottom J1
U 1 1 60055BC4
P 6150 4600
F 0 "J1" H 6200 6417 50  0000 C CNN
F 1 "Conn_02x34_Top_Bottom" H 6200 6326 50  0000 C CNN
F 2 "pcmcia:10118309" H 6150 4600 50  0001 C CNN
F 3 "~" H 6150 4600 50  0001 C CNN
	1    6150 4600
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR02
U 1 1 6005C0B4
P 2200 6100
F 0 "#PWR02" H 2200 5950 50  0001 C CNN
F 1 "+5V" V 2215 6228 50  0000 L CNN
F 2 "" H 2200 6100 50  0001 C CNN
F 3 "" H 2200 6100 50  0001 C CNN
	1    2200 6100
	0    -1   -1   0   
$EndComp
$Comp
L power:+5V #PWR03
U 1 1 6005E82D
P 2200 6200
F 0 "#PWR03" H 2200 6050 50  0001 C CNN
F 1 "+5V" V 2215 6328 50  0000 L CNN
F 2 "" H 2200 6200 50  0001 C CNN
F 3 "" H 2200 6200 50  0001 C CNN
	1    2200 6200
	0    -1   -1   0   
$EndComp
$Comp
L power:+5V #PWR04
U 1 1 6005EB8D
P 2200 6300
F 0 "#PWR04" H 2200 6150 50  0001 C CNN
F 1 "+5V" V 2215 6428 50  0000 L CNN
F 2 "" H 2200 6300 50  0001 C CNN
F 3 "" H 2200 6300 50  0001 C CNN
	1    2200 6300
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR01
U 1 1 60061423
P 2000 5800
F 0 "#PWR01" H 2000 5550 50  0001 C CNN
F 1 "GND" H 2005 5627 50  0000 C CNN
F 2 "" H 2000 5800 50  0001 C CNN
F 3 "" H 2000 5800 50  0001 C CNN
	1    2000 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 5800 2200 5800
Wire Wire Line
	2200 5800 2200 5700
Connection ~ 2200 5800
Connection ~ 2200 5600
Wire Wire Line
	2200 5600 2200 5500
Connection ~ 2200 5700
Wire Wire Line
	2200 5700 2200 5600
Wire Wire Line
	2200 5900 2200 5800
$Comp
L power:GND #PWR05
U 1 1 6006400E
P 5950 3000
F 0 "#PWR05" H 5950 2750 50  0001 C CNN
F 1 "GND" V 5955 2872 50  0000 R CNN
F 2 "" H 5950 3000 50  0001 C CNN
F 3 "" H 5950 3000 50  0001 C CNN
	1    5950 3000
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR07
U 1 1 60065E36
P 6450 3000
F 0 "#PWR07" H 6450 2750 50  0001 C CNN
F 1 "GND" V 6455 2872 50  0000 R CNN
F 2 "" H 6450 3000 50  0001 C CNN
F 3 "" H 6450 3000 50  0001 C CNN
	1    6450 3000
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR06
U 1 1 600664BE
P 5950 6300
F 0 "#PWR06" H 5950 6050 50  0001 C CNN
F 1 "GND" H 5955 6127 50  0000 C CNN
F 2 "" H 5950 6300 50  0001 C CNN
F 3 "" H 5950 6300 50  0001 C CNN
	1    5950 6300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR08
U 1 1 60066A04
P 6450 6300
F 0 "#PWR08" H 6450 6050 50  0001 C CNN
F 1 "GND" H 6455 6127 50  0000 C CNN
F 2 "" H 6450 6300 50  0001 C CNN
F 3 "" H 6450 6300 50  0001 C CNN
	1    6450 6300
	1    0    0    -1  
$EndComp
Text HLabel 4800 3300 2    50   Input ~ 0
PA0_OE
Text HLabel 5950 3800 0    50   Input ~ 0
PA0_OE
Text HLabel 4800 3400 2    50   Input ~ 0
PA1_WE
Text HLabel 5950 4400 0    50   Input ~ 0
PA1_WE
Text HLabel 4800 3500 2    50   Input ~ 0
PA2_CE1
Text HLabel 4800 3600 2    50   Input ~ 0
PA3_CE2
Text HLabel 4800 3700 2    50   Input ~ 0
PA4_READY_IREQ
Text HLabel 4800 3800 2    50   Input ~ 0
PA5_INPACK
Text HLabel 4800 3900 2    50   Input ~ 0
PA6_IOIS16_WP
Text HLabel 4800 4000 2    50   Input ~ 0
PA7_WAIT
Text HLabel 5950 3600 0    50   Input ~ 0
PA2_CE1
Text HLabel 6450 3700 2    50   Input ~ 0
PA3_CE2
Text HLabel 5950 4500 0    50   Input ~ 0
PA4_READY_IREQ
Text HLabel 6450 5500 2    50   Input ~ 0
PA5_INPACK
Text HLabel 5950 6200 0    50   Input ~ 0
PA6_IOIS16_WP
Text HLabel 6450 5400 2    50   Input ~ 0
PA7_WAIT
Text HLabel 4800 6400 2    50   Input ~ 0
PB0_A16
Text HLabel 4800 6300 2    50   Input ~ 0
PB1_A17
Text HLabel 4800 6200 2    50   Input ~ 0
PB2_A18
Text HLabel 4800 6100 2    50   Input ~ 0
PB3_A19
Text HLabel 4800 2900 2    50   Input ~ 0
PB4_A20
Text HLabel 4800 3000 2    50   Input ~ 0
PB5_A21
Text HLabel 4800 3100 2    50   Input ~ 0
PB6_A22
Text HLabel 4800 3200 2    50   Input ~ 0
PB7_A23
Text HLabel 5950 4800 0    50   Input ~ 0
PB0_A16
Text HLabel 6450 4100 2    50   Input ~ 0
PB1_A17
Text HLabel 6450 4200 2    50   Input ~ 0
PB2_A18
Text HLabel 6450 4300 2    50   Input ~ 0
PB3_A19
Text HLabel 6450 4400 2    50   Input ~ 0
PB4_A20
Text HLabel 6450 4500 2    50   Input ~ 0
PB5_A21
Text HLabel 6450 4800 2    50   Input ~ 0
PB6_A22
Text HLabel 6450 4900 2    50   Input ~ 0
PB7_A23
Text HLabel 4800 4800 2    50   Input ~ 0
PC0_A8
Text HLabel 4800 4700 2    50   Input ~ 0
PC1_A9
Text HLabel 4800 4600 2    50   Input ~ 0
PC2_A10
Text HLabel 4800 4500 2    50   Input ~ 0
PC3_A11
Text HLabel 4800 4400 2    50   Input ~ 0
PC4_A12
Text HLabel 4800 4300 2    50   Input ~ 0
PC5_A13
Text HLabel 4800 4200 2    50   Input ~ 0
PC6_A14
Text HLabel 4800 4100 2    50   Input ~ 0
PC7_A15
Text HLabel 5950 4100 0    50   Input ~ 0
PC0_A8
Text HLabel 5950 4000 0    50   Input ~ 0
PC1_A9
Text HLabel 5950 3700 0    50   Input ~ 0
PC2_A10
Text HLabel 5950 3900 0    50   Input ~ 0
PC3_A11
Text HLabel 5950 5000 0    50   Input ~ 0
PC4_A12
Text HLabel 5950 4200 0    50   Input ~ 0
PC5_A13
Text HLabel 5950 4300 0    50   Input ~ 0
PC6_A14
Text HLabel 5950 4900 0    50   Input ~ 0
PC7_A15
Text HLabel 2200 3000 0    50   Input ~ 0
PD0_A24
Text HLabel 2200 2900 0    50   Input ~ 0
PD1_A25
Text HLabel 2200 2300 0    50   Input ~ 0
PD2_REG
Text HLabel 2200 2400 0    50   Input ~ 0
PD3_IORD
Text HLabel 4800 4900 2    50   Input ~ 0
PD7_IOWR
Text HLabel 6450 5000 2    50   Input ~ 0
PD0_A24
Text HLabel 6450 5100 2    50   Input ~ 0
PD1_A25
Text HLabel 6450 5600 2    50   Input ~ 0
PD2_REG
Text HLabel 6450 3900 2    50   Input ~ 0
PD3_IORD
Text HLabel 6450 4000 2    50   Input ~ 0
PD7_IOWR
Text HLabel 4800 2400 2    50   Input ~ 0
PE3_RESET
Text HLabel 4800 2100 2    50   Input ~ 0
PE4_BVD1
Text HLabel 4800 2200 2    50   Input ~ 0
PE5_BVD2
Text HLabel 6450 5700 2    50   Input ~ 0
PE4_BVD1
Text HLabel 6450 5800 2    50   Input ~ 0
PE5_BVD2
Text HLabel 2200 3400 0    50   Input ~ 0
PF0_A0
Text HLabel 2200 3500 0    50   Input ~ 0
PF1_A1
Text HLabel 2200 3600 0    50   Input ~ 0
PF2_A2
Text HLabel 2200 3700 0    50   Input ~ 0
PF3_A3
Text HLabel 2200 3800 0    50   Input ~ 0
PF4_A4
Text HLabel 2200 3900 0    50   Input ~ 0
PF5_A5
Text HLabel 2200 4000 0    50   Input ~ 0
PF6_A6
Text HLabel 2200 4100 0    50   Input ~ 0
PF7_A7
Text HLabel 5950 5800 0    50   Input ~ 0
PF0_A0
Text HLabel 5950 5700 0    50   Input ~ 0
PF1_A1
Text HLabel 5950 5600 0    50   Input ~ 0
PF2_A2
Text HLabel 5950 5500 0    50   Input ~ 0
PF3_A3
Text HLabel 5950 5400 0    50   Input ~ 0
PF4_A4
Text HLabel 5950 5300 0    50   Input ~ 0
PF5_A5
Text HLabel 5950 5200 0    50   Input ~ 0
PF6_A6
Text HLabel 5950 5100 0    50   Input ~ 0
PF7_A7
Text HLabel 2200 4200 0    50   Input ~ 0
PK0_D8
Text HLabel 2200 4300 0    50   Input ~ 0
PK1_D9
Text HLabel 2200 4400 0    50   Input ~ 0
PK2_D10
Text HLabel 2200 4500 0    50   Input ~ 0
PK3_D11
Text HLabel 2200 4600 0    50   Input ~ 0
PK4_D12
Text HLabel 2200 4700 0    50   Input ~ 0
PK5_D13
Text HLabel 2200 4800 0    50   Input ~ 0
PK6_D14
Text HLabel 2200 4900 0    50   Input ~ 0
PK7_D15
Text HLabel 6450 5900 2    50   Input ~ 0
PK0_D8
Text HLabel 6450 6000 2    50   Input ~ 0
PK1_D9
Text HLabel 6450 6100 2    50   Input ~ 0
PK2_D10
Text HLabel 6450 3200 2    50   Input ~ 0
PK3_D11
Text HLabel 6450 3300 2    50   Input ~ 0
PK4_D12
Text HLabel 6450 3400 2    50   Input ~ 0
PK5_D13
Text HLabel 6450 3500 2    50   Input ~ 0
PK6_D14
Text HLabel 6450 3600 2    50   Input ~ 0
PK7_D15
Text HLabel 6450 5300 2    50   Input ~ 0
PE3_RESET
Text HLabel 2200 2500 0    50   Input ~ 0
PH0_CD1
Text HLabel 2200 2600 0    50   Input ~ 0
PH1_CD2
Text HLabel 4800 2500 2    50   Input ~ 0
PH3_VS1
Text HLabel 4800 2600 2    50   Input ~ 0
PH4_VS2
Text HLabel 6450 3100 2    50   Input ~ 0
PH0_CD1
Text HLabel 6450 3800 2    50   Input ~ 0
PH3_VS1
Text HLabel 6450 5200 2    50   Input ~ 0
PH4_VS2
Text HLabel 6450 6200 2    50   Input ~ 0
PH1_CD2
$Comp
L power:+5V #PWR0101
U 1 1 600D787A
P 5950 4600
F 0 "#PWR0101" H 5950 4450 50  0001 C CNN
F 1 "+5V" V 5965 4728 50  0000 L CNN
F 2 "" H 5950 4600 50  0001 C CNN
F 3 "" H 5950 4600 50  0001 C CNN
	1    5950 4600
	0    -1   -1   0   
$EndComp
$Comp
L power:+5V #PWR0102
U 1 1 600D891D
P 6450 4600
F 0 "#PWR0102" H 6450 4450 50  0001 C CNN
F 1 "+5V" V 6465 4728 50  0000 L CNN
F 2 "" H 6450 4600 50  0001 C CNN
F 3 "" H 6450 4600 50  0001 C CNN
	1    6450 4600
	0    1    1    0   
$EndComp
Text HLabel 4800 6000 2    50   Input ~ 0
PL0_D0
Text HLabel 4800 5900 2    50   Input ~ 0
PL1_D1
Text HLabel 4800 5800 2    50   Input ~ 0
PL2_D2
Text HLabel 4800 5700 2    50   Input ~ 0
PL3_D3
Text HLabel 4800 5600 2    50   Input ~ 0
PL4_D4
Text HLabel 4800 5500 2    50   Input ~ 0
PL5_D5
Text HLabel 4800 5400 2    50   Input ~ 0
PL6_D6
Text HLabel 4800 5300 2    50   Input ~ 0
PL7_D7
Text HLabel 5950 5900 0    50   Input ~ 0
PL0_D0
Text HLabel 5950 6000 0    50   Input ~ 0
PL1_D1
Text HLabel 5950 6100 0    50   Input ~ 0
PL2_D2
Text HLabel 5950 3100 0    50   Input ~ 0
PL3_D3
Text HLabel 5950 3200 0    50   Input ~ 0
PL4_D4
Text HLabel 5950 3300 0    50   Input ~ 0
PL5_D5
Text HLabel 5950 3400 0    50   Input ~ 0
PL6_D6
Text HLabel 5950 3500 0    50   Input ~ 0
PL7_D7
$Comp
L power:+5V #PWR?
U 1 1 6004D8C5
P 5950 4700
F 0 "#PWR?" H 5950 4550 50  0001 C CNN
F 1 "+5V" V 5965 4828 50  0000 L CNN
F 2 "" H 5950 4700 50  0001 C CNN
F 3 "" H 5950 4700 50  0001 C CNN
	1    5950 4700
	0    -1   -1   0   
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 6004DD98
P 6450 4700
F 0 "#PWR?" H 6450 4550 50  0001 C CNN
F 1 "+5V" V 6465 4828 50  0000 L CNN
F 2 "" H 6450 4700 50  0001 C CNN
F 3 "" H 6450 4700 50  0001 C CNN
	1    6450 4700
	0    1    1    0   
$EndComp
$EndSCHEMATC
