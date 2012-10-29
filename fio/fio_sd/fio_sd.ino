#include <Wire.h>
#include <SD.h>

#define PACKET_SIZE     (5)
#define CMD_ID_WRITE    (0x01)
#define CMD_ID_READ     (0x02)

#define MPU6050_ADDR    (0x68)

#define INTERRUPT_PIN_D2    (0) // for whatever reason, D2 maps to int 0

// register addr
#define MPU6050_REG_USER_CTRL       (0x6A)
#define MPU6050_REG_WHOAMI          (0x75)
#define MPU6050_REG_FIFO_EN         (0x23)
#define MPU6050_REG_INT_ENABLE      (0x38)
#define MPU6050_REG_GYRO_XOUT_H     (0x43)
#define MPU6050_REG_GYRO_XOUT_L     (0x44)
#define MPU6050_REG_GYRO_YOUT_H     (0x45)
#define MPU6050_REG_GYRO_YOUT_L     (0x46)
#define MPU6050_REG_GYRO_ZOUT_H     (0x47)
#define MPU6050_REG_GYRO_ZOUT_L     (0x48)
#define MPU6050_REG_ACCEL_XOUT_H    (0x3B)
#define MPU6050_REG_ACCEL_XOUT_L    (0x3C)
#define MPU6050_REG_ACCEL_YOUT_H    (0x3D)
#define MPU6050_REG_ACCEL_YOUT_L    (0x3E)
#define MPU6050_REG_ACCEL_ZOUT_H    (0x3F)
#define MPU6050_REG_ACCEL_ZOUT_L    (0x40)
#define MPU6050_REG_SMPLRT_DIV      (0x19)
#define MPU6050_REG_CONFIG          (0x1A)
#define MPU6050_REG_GYRO_CONFIG     (0x1B)
#define MPU6050_REG_ACCEL_CONFIG    (0x1C)
#define MPU6050_REG_PWR_MGMT_1      (0x6B)
#define MPU6050_REG_PWR_MGMT_2      (0x6C)
#define MPU6050_REG_FIFO_COUNT_H    (0x72)
#define MPU6050_REG_FIFO_COUNT_L    (0x73)
#define MPU6050_REG_FIFO_R_W        (0x74)

// register values
#define MPU6050_INT_ENABLE_FIFO_OFLOW   (0x10)
#define MPU6050_INT_DATA_RDY            (0x01)
#define MPU6050_FIFO_ENABLE_ACCEL_GYRO   (0x78) 
#define MPU6050_FIFO_EN                 (0x40)


#define N_SAMPLES (1000)

unsigned char hi,lo;
int samples = 0;
File data;

void writeToI2C(char chip_addr, char reg_addr, unsigned char value)
{
    Wire.beginTransmission(chip_addr);
    Wire.write(reg_addr);
    Wire.write(value);
    Wire.endTransmission();
}

void readFromI2C(char chip_addr, char reg_addr, unsigned int num, unsigned char* buff) 
{
    Wire.beginTransmission(chip_addr);
    Wire.write(reg_addr);
    Wire.endTransmission();
    Wire.beginTransmission(chip_addr);
    Wire.requestFrom(chip_addr, num); 
    int i;
    for (i = 0; i < num; i++) {
        while(!Wire.available()); // wait for recv
        buff[i++] = Wire.read();
    }
    Wire.endTransmission();
}

//void handleInterrupt()
//{
//    isr = true;
//}

void wake_up()
{
    writeToI2C(MPU6050_ADDR, MPU6050_REG_PWR_MGMT_1, 0);
}

//void enableFIFO() 
//{
//    writeToI2C(MPU6050_ADDR, MPU6050_REG_USER_CTRL, MPU6050_FIFO_EN);
//    writeToI2C(MPU6050_ADDR, MPU6050_REG_FIFO_EN, MPU6050_FIFO_ENABLE_ACCEL_GYRO);
//}

//void enableINT()
//{
//    pinMode(2,INPUT);
//    attachInterrupt(INTERRUPT_PIN_D2, handleInterrupt, RISING); 
//    writeToI2C(MPU6050_ADDR, MPU6050_REG_INT_ENABLE, MPU6050_INT_ENABLE_FIFO_OFLOW);
//    //writeToI2C(MPU6050_ADDR, MPU6050_REG_INT_ENABLE, MPU6050_INT_DATA_RDY);
//}

void setup()
{
    Serial.begin(57600);
    Wire.begin();
    wake_up();
    int chipSelect = 10;
    pinMode(chipSelect, OUTPUT);
    if(!SD.begin(chipSelect)) {
        while (1) {
            Serial.println("SD card failed.");
        }
    } else {
        Serial.println("SD card initialized.");
    }
    if (SD.exists("data.csv")) {
        SD.remove("data.csv");
    }
    data = SD.open("data.csv", FILE_WRITE);
    //enableFIFO();
    //enableINT();

}

//int getFIFOCount() 
//{
//    int fifo_count;
//    unsigned char fifo_count_l, fifo_count_h;
//    readFromI2C(MPU6050_ADDR, MPU6050_REG_FIFO_COUNT_H, 1, &fifo_count_h); 
//    readFromI2C(MPU6050_ADDR, MPU6050_REG_FIFO_COUNT_L, 1, &fifo_count_l); 
//    fifo_count = (fifo_count_h << 8) + fifo_count_l;    
//    return fifo_count;
//}
//
//void readFIFO(unsigned char *buff, unsigned int count) 
//{
//   readFromI2C(MPU6050_ADDR, MPU6050_REG_FIFO_R_W, count, buff);
//}

void collect_sample()
{
    data.print(millis());
    data.print(',');

    readFromI2C(MPU6050_ADDR, MPU6050_REG_ACCEL_XOUT_H, 1, &hi);
    readFromI2C(MPU6050_ADDR, MPU6050_REG_ACCEL_XOUT_L, 1, &lo);
    data.print(hi, HEX);
    data.print(' ');
    data.print(lo, HEX);
    data.print(',');

    readFromI2C(MPU6050_ADDR, MPU6050_REG_ACCEL_YOUT_H, 1, &hi);
    readFromI2C(MPU6050_ADDR, MPU6050_REG_ACCEL_YOUT_L, 1, &lo);
    data.print(hi, HEX);
    data.print(' ');
    data.print(lo, HEX);
    data.print(',');

    readFromI2C(MPU6050_ADDR, MPU6050_REG_ACCEL_ZOUT_H, 1, &hi);
    readFromI2C(MPU6050_ADDR, MPU6050_REG_ACCEL_ZOUT_L, 1, &lo);
    data.print(hi, HEX);
    data.print(' ');
    data.print(lo, HEX);
    data.print(',');

    readFromI2C(MPU6050_ADDR, MPU6050_REG_GYRO_XOUT_H, 1, &hi);
    readFromI2C(MPU6050_ADDR, MPU6050_REG_GYRO_XOUT_L, 1, &lo);
    data.print(hi, HEX);
    data.print(' ');
    data.print(lo, HEX);
    data.print(',');

    readFromI2C(MPU6050_ADDR, MPU6050_REG_GYRO_YOUT_H, 1, &hi);
    readFromI2C(MPU6050_ADDR, MPU6050_REG_GYRO_YOUT_L, 1, &lo);
    data.print(hi, HEX);
    data.print(' ');
    data.print(lo, HEX);
    data.print(',');

    readFromI2C(MPU6050_ADDR, MPU6050_REG_GYRO_ZOUT_H, 1, &hi);
    readFromI2C(MPU6050_ADDR, MPU6050_REG_GYRO_ZOUT_L, 1, &lo);
    data.print(hi, HEX);
    data.print(' ');
    data.print(lo, HEX);
    data.print('\n');
}

void do_collection()
{
    for(samples = 0; samples < N_SAMPLES; samples++) {
        collect_sample();
    }
    data.close();
    Serial.println("done.");
}

void loop()
{
    while(!Serial.available());
    Serial.println("starting collection");
    Serial.read();
    do_collection();
    //Serial.println("hello world");
    //delay(500);
}
