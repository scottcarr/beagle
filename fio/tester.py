import serial
import time

class FioComm:
    def __init__(self):

        # constants
        self.CMD_ID_WRITE = 0x01
        self.CMD_ID_READ = 0x02
        self.CARRIAGE_RETURN = 0x0A
        self.RESPONSE_OK = "OK\r\n"
        self.MPU6050_ADDR = 0x68
        self.MPU6050_REG_WHOAMI = 0x75
        self.MPU6050_REG_FIFO_EN = 0x23
        self.MPU6050_REG_INT_ENABLE = 0x38
        self.MPU6050_INT_ENABLE_FIFO_OFLOW = 0x10

        USB_FILE = '/dev/tty.usbserial-AE01A6ZM'
        BAUDRATE = 57600

        self.ser = serial.Serial(USB_FILE, rtscts=True)
        if not self.ser.isOpen():
            print "Port failed to open"
        self.ser.baudrate = BAUDRATE
        time.sleep(1) # it takes a second for the port to wake up

    def enable_fifo(self,\
            TEMP_FIFO_EN = False,\
            XG_FIFO_EN = False,\
            YG_FIFO_EN = False,\
            ZG_FIFO_EN = False,\
            ACCEL_FIFO_EN = False,\
            SLV2_FIFO_EN = False,\
            SLV1_FIFO_EN = False,\
            SLV0_FIFO_EN = False):

        fifo_en = 0
        if TEMP_FIFO_EN:
            fifo_en |= 0x80
        if XG_FIFO_EN:
            fifo_en |= 0x40
        if YG_FIFO_EN:
            fifo_en |= 0x20
        if ZG_FIFO_EN:
            fifo_en |= 0x10
        if ACCEL_FIFO_EN:
            fifo_en |= 0x08
        if SLV2_FIFO_EN:
            fifo_en |= 0x04
        if SLV1_FIFO_EN:
            fifo_en |= 0x02
        if SLV0_FIFO_EN:
            fifo_en |= 0x01

        return self.writeI2C(self.MPU6050_ADDR, self.MPU6050_REG_FIFO_EN, fifo_en)

    def readI2C(self, chip_addr, reg_addr, num):
        cmd_array = bytearray(
                [self.CMD_ID_READ, chip_addr, reg_addr, num, self.CARRIAGE_RETURN])
        self.ser.write(cmd_array)
        return self.ser.read(num+1)

    def writeI2C(self, chip_addr, reg_addr, value):
        cmd_array = bytearray(
                [self.CMD_ID_WRITE, chip_addr, reg_addr, value, self.CARRIAGE_RETURN])
        self.ser.write(cmd_array)
        return self.ser.read(4)

    def write_something(self):
        return self.writeI2C(self.MPU6050_ADDR, 0x01, 0x00)

    def read_whoami(self):
        return self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_WHOAMI, 1) 

    def enable_int_fifo_oflow(self):
        return self.writeI2C(self.MPU6050_ADDR, self.MPU6050_REG_INT_ENABLE,\
                self.MPU6050_INT_ENABLE_FIFO_OFLOW)

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    fm = FioComm()
    print hex(ord(fm.read_whoami()[0]))
    print fm.enable_fifo(XG_FIFO_EN = True, YG_FIFO_EN = True,\
            ZG_FIFO_EN = True, ACCEL_FIFO_EN = True)
    print fm.enable_int_fifo_oflow()
    while True:
        print fm.ser.read()

