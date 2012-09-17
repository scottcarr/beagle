#!/usr/bin/python

import subprocess
import serial
import time

UART4_RX_conf = "/sys/kernel/debug/omap_mux/gpmc_wait0"
UART4_TX_conf = "/sys/kernel/debug/omap_mux/gpmc_wpn" 

UART4_RX_val = 26
UART4_TX_val = 6

subprocess.call(['echo', str(UART4_RX_val), '>', UART4_RX_conf])
subprocess.call(['echo', str(UART4_TX_val), '>', UART4_TX_conf])

print "echo 'UART 4 (TX):'"
subprocess.call(['cat', UART4_TX_conf])
print ""

print 'echo "UART 4 (RX):"'
subprocess.call(['cat', UART4_RX_conf])
print ""

# open serial port
ser = serial.Serial('/dev/ttyO4')
ser.baudrate = 9600

# go into configure mode
ser.write('+++')
time.sleep(1)
print ser.read() # should see 'O'
print ser.read() # should see 'K'
