#include <stdlib.h>
#include <stdio.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <sys/stat.h>


int main() {
    int file;
    int adapter_nr = 3; /* probably dynamically determined */
    char filename[20];

    snprintf(filename, 19, "/dev/i2c-%d", adapter_nr);
    file = open(filename, O_RDWR);
    if (file < 0) {
        printf("Opening i2c failed.\n");
        exit(1);
    }

    int addr = 0x53 ; /* The I2C address */
    if (ioctl(file, I2C_SLAVE, addr) < 0) {
        /* ERROR HANDLING; you can check errno to see what went wrong */
        exit(1);
    }

    char reg = 0x10;
    int res;
    char buf[10];
    buf[0] = 0x00;

    if (write(file,buf, 1) != 1) {
        // error
        printf("Reading i2c failed\n");
    }

    if (read(file,buf, 1) != 1) {
        // error
        printf("Reading i2c failed\n");
    } else {
        printf("Dev ID: %x\n", buf[0]);
    }

    return 0;
}
