#include <sys/ioctl.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <stdio.h>
#include <string.h>

char get_whoami();
void open_mpu6050();
void dump_fifo();
unsigned int get_fifo_count();
void write_i2c(char reg, char* buff, unsigned int n);
void enable_fifo();
unsigned int read_fifo(char *buff);
void set_sample_div();
void read_sample(char *buff);
