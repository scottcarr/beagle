import serial
import time

USB_FILE = '/dev/tty.usbserial-AE01A6ZM'

def write_something():
    ser.write(bytearray([0x01, 0x68, 0x75, 0x01, 0x0A]))
    print ser.read(4)

def read_whoami():
    ser.write(bytearray([0x02, 0x68, 0x75, 0x01, 0x0A]))
    rv = ser.read(2)
    print "WHOAMI: {0}".format(hex(ord(rv[0])))

if __name__ == '__main__':
    ser = serial.Serial(USB_FILE)
    if not ser.isOpen():
        print "Port failed to open"
    ser.baudrate = 57600
    write_something()
    read_whoami()
    ser.close()
