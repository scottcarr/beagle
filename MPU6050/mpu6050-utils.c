#include "mpu6050-utils.h"

int file;
char get_whoami() {
    char whoami = 0x75;
    char buff;
    if(write(file, &whoami, 1) != 1) {
        printf("i2c write failed: %i\n", errno);
        return -1;
    }
    if(read(file, &buff, 1) != 1) {
        printf("i2c read failed: %i\n", errno);
        return -1;
    } else {
        return buff;
    }
}

void open_mpu6050()
{
    char *filename = "/dev/i2c-3";
    int addr = 0x68;
    file = open(filename, O_RDWR);
    if (file < 0) {
        printf("Opening i2c failed\n");
    } 

    if (ioctl(file, I2C_SLAVE, addr) < 0) {
        printf("Failed to set i2c slave device\n");
    }
}

void dump_fifo()
{
    int n = 1024;
    char fifo = 0x74;
    char buff[1024];
    if(write(file, &fifo, 1) != 1) {
        printf("i2c write failed: %i\n", errno);
    }
    if(read(file, &buff, n) != n) {
        printf("i2c read failed: %i\n", errno);
    }
}

unsigned int get_fifo_count()
{
    char fifo = 0x72;
    char buff[2];
    if(write(file, &fifo, 1) != 1) {
        printf("i2c write failed: %i\n", errno);
        return -1;
    }
    if(read(file, &buff, 2) != 2) {
        printf("i2c read failed: %i\n", errno);
        return -1;
    }
    return (buff[0] << 8) | buff[1]; 
}

void wake_up()
{
    char val = 0;
    write_i2c(0x6B, &val, 1);
}

void write_i2c(char reg, char *buff, unsigned int n)
{
    char out[n+1];
    out[0] = reg;
    memcpy(out+1, buff, n);
    if(write(file, &out, n+1) != n+1) {
        printf("i2c write failed: %i\n", errno);
    }
}

void enable_fifo()
{
    char addr = 0x23;
    char val = 0x00;
    write_i2c(addr, &val, 1);
}

unsigned int read_fifo(char *buff)
{
    unsigned int n = get_fifo_count();
    char reg = 0x74;
    if(write(file, &reg, 1) != 1) {
        printf("error writing fifo addr\n");
        return -1;
    } else {
        if(read(file, buff, n) != n) {
            printf("error reading fifo\n");
            return -1;
        } else {
            return n;
        }
    }
    
}

void set_sample_div()
{
    char addr = 0x19;
    unsigned char val = 0x00;
    write_i2c(addr, &val, 1);
}

void sleep()
{
    char val = 0x40;
    write_i2c(0x6B, &val, 1);
}

void read_sample(char *buff)
{
    char reg = 0x3B;
    unsigned int n = 14;
    if(write(file, &reg, 1) != 1) {
        printf("i2c write failed\n");
    } else {
        if (read(file, buff, n) != n) {
            printf("i2c read failed\n");
        }
    }
}


