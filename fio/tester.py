import serial
import time
import struct

class FioComm:
    def __init__(self):

        # constants
        self.CMD_ID_WRITE = 0x01
        self.CMD_ID_READ = 0x02
        self.CARRIAGE_RETURN = 0x0A
        self.RESPONSE_OK = "OK\r\n"
        self.MPU6050_ADDR = 0x68
        self.BITS_PER_G = 16384.0
        self.BITS_PER_DEG_PER_S = 131.0

        # registers
        self.MPU6050_REG_WHOAMI = 0x75
        self.MPU6050_REG_FIFO_EN = 0x23
        self.MPU6050_REG_INT_ENABLE = 0x38
        self.MPU6050_REG_GYRO_XOUT_H = 0x43
        self.MPU6050_REG_GYRO_XOUT_L = 0x44
        self.MPU6050_REG_GYRO_YOUT_H = 0x45
        self.MPU6050_REG_GYRO_YOUT_L = 0x46
        self.MPU6050_REG_GYRO_ZOUT_H = 0x47
        self.MPU6050_REG_GYRO_ZOUT_L = 0x48
        self.MPU6050_REG_ACCEL_XOUT_H = 0x3B
        self.MPU6050_REG_ACCEL_XOUT_L = 0x3C
        self.MPU6050_REG_ACCEL_YOUT_H = 0x3D
        self.MPU6050_REG_ACCEL_YOUT_L = 0x3E
        self.MPU6050_REG_ACCEL_ZOUT_H = 0x3F
        self.MPU6050_REG_ACCEL_ZOUT_L = 0x40
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
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_XOUT_H, 1)
        xh = ord(resp[0])
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_XOUT_L, 1)
        xl = ord(resp[0])
        x = self.convert_from_twos_comp(xh, xl) / self.BITS_PER_DEG_PER_S
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_YOUT_H, 1)
        yh = ord(resp[0])
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_YOUT_L, 1)
        yl = ord(resp[0])
        y = self.convert_from_twos_comp(yh, yl) / self.BITS_PER_DEG_PER_S
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_ZOUT_H, 1)
        zh = ord(resp[0])
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_GYRO_ZOUT_L, 1)
        zl = ord(resp[0])
        z = self.convert_from_twos_comp(zh, zl) / self.BITS_PER_DEG_PER_S
        return x, y, z

    def convert_from_twos_comp(self, hi, lo):
        val = hi*2**8 + lo
        if hi > 127:
            val = val - 2**16
        return val

    def read_accel(self):
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_XOUT_H, 1)
        xh = ord(resp[0])
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_XOUT_L, 1)
        xl = ord(resp[0])
        x = self.convert_from_twos_comp(xh, xl) / self.BITS_PER_G
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_YOUT_H, 1)
        yh = ord(resp[0])
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_YOUT_L, 1)
        yl = ord(resp[0])
        y = self.convert_from_twos_comp(yh, yl) / self.BITS_PER_G
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_ZOUT_H, 1)
        zh = ord(resp[0])
        resp = self.readI2C(self.MPU6050_ADDR, self.MPU6050_REG_ACCEL_ZOUT_L, 1)
        zl = ord(resp[0])
        z = self.convert_from_twos_comp(zh, zl) / self.BITS_PER_G
        return x, y, z

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
    #fm.print_reg_contents()
    #print fm.wake_up()
    x, y, z = fm.read_accel()
    #x, y, z = fm.read_gyro()
    print x, y, z
