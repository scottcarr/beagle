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

        # registers
        self.MPU6050_REG_WHOAMI = 0x75
        self.MPU6050_REG_FIFO_EN = 0x23
        self.MPU6050_REG_INT_ENABLE = 0x38
        self.MPU6050_REG_GYRO_XOUT_H = 0x43
        self.MPU6050_REG_ACCEL_XOUT_H = 0x3B
        self.MPU6050_REG_SMPLRT_DIV = 0x19
        self.MPU6050_REG_CONFIG = 0x1A
        self.MPU6050_REG_GYRO_CONFIG = 0x1B
        self.MPU6050_REG_ACCEL_CONFIG = 0x1C
        self.MPU6050_REG_PWR_MGMT_1 = 0x6B
        self.MPU6050_REG_PWR_MGMT_2 = 0x6C

        # register values
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
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_WHOAMI, 1) 
        return ord(resp[0])

    def enable_int_fifo_oflow(self):
        return self.writeI2C(self.MPU6050_ADDR, self.MPU6050_REG_INT_ENABLE,\
                self.MPU6050_INT_ENABLE_FIFO_OFLOW)

    def read_gyro(self):
        return self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_XOUT_H, 6)

    def read_accel(self):
        return self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_XOUT_H, 6)

    def read_sample_rate(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_SMPLRT_DIV, 1)
        return ord(resp[0])

    def read_config(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_CONFIG, 1)
        return ord(resp[0])

    def read_gyro_config(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_CONFIG, 1)
        return ord(resp[0])

    def read_accel_config(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_CONFIG, 1)
        return ord(resp[0])

    def read_fifo_en(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_FIFO_EN, 1)
        return ord(resp[0])

    def read_pwr_mgmt_1(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_PWR_MGMT_1, 1)
        return ord(resp[0])

    def read_pwr_mgmt_2(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_PWR_MGMT_2, 1)
        return ord(resp[0])

    def print_reg_contents(self):
        print "Who am i: {0}".format(hex(fm.read_whoami()))
        print "Sample rate: {0}".format(hex(fm.read_sample_rate()))
        print "Config: {0}".format(hex(fm.read_config()))
        print "Gyro config: {0}".format(hex(fm.read_gyro_config()))
        print "Accel config: {0}".format(hex(fm.read_accel_config()))
        print "FIFO enable: {0}".format(hex(fm.read_fifo_en()))
        print "Power management 1: {0}".format(hex(fm.read_pwr_mgmt_1()))
        print "Power management 2: {0}".format(hex(fm.read_pwr_mgmt_2()))

    def wake_up(self):
        return self.writeI2C(self.MPU6050_ADDR, self.MPU6050_REG_PWR_MGMT_1, 0)

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    fm = FioComm()
    #print fm.enable_fifo(XG_FIFO_EN = True, YG_FIFO_EN = True,\
    #        ZG_FIFO_EN = True, ACCEL_FIFO_EN = True)
    #print fm.enable_int_fifo_oflow()
    #while True:
    #    print fm.ser.read()
    #g =  fm.read_gyro()
    #gx = ord(g[0])*2**16 + ord(g[1])
    #gy = ord(g[2])*2**16 + ord(g[3])
    #gz = ord(g[4])*2**16 + ord(g[5])
    #print "gyro X: {0}".format(hex(gx))
    #print "gyro Y: {0}".format(hex(gy))
    #print "gyro Z: {0}".format(hex(gz))
    #a = fm.read_accel()
    #ax = ord(a[0])*2**16 + ord(a[1])
    #ay = ord(a[2])*2**16 + ord(a[3])
    #az = ord(a[4])*2**16 + ord(a[5])
    #print "accel X: {0}".format(hex(ax))
    #print "accel Y: {0}".format(hex(ay))
    #print "accel Z: {0}".format(hex(az))
    #print g
    #print a
    fm.print_reg_contents()
    print fm.wake_up()
