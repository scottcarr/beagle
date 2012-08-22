#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <errno.h>
#include <fcntl.h>

int main() 
{
    int file;
    int adapter_num = 1;  // which i2c adapter
    int base_addr = 0x40;  // the address of the chip on the i2c bus
    char filename[20];

    // setup file name
    snprintf(filename, 19, "/dev/i2c-%d", adapter_num);

    // open file handle to i2c device
    file = open(filename, O_RDWR);
    if (file < 0) {
        // failed to open i2c device
        int err_id = errno;
        printf("Failed to open %s, errno: %i", filename, err_id); 
        exit(err_id);
    }

    // set the mode and address of the chip we want to talk to
    if (ioctl(file, I2C_SLAVE, base_addr) < 0) {
        // failed to open i2c device
        int err_id = errno;
        printf("Failed to set I2C_SLAVE for addr:  %i, errno: %i", 
                base_addr, err_id); 
        exit(err_id);
    }

    // ready to communicate
    /* example commands:
    unsigned char register = 0x10; // the device register you want to access
    char buf[10];

    // using i2c:
    buf[0] = register;
    buf[1] = 0x33;
    buf[2] = 0x31;
    if (write(file, buf, 3) != 3) {
        // error handling
    }

    if (read(file, buf, 1) != 1) {
        // error handling
    } else {
        // buf[0] contains the read byte
    }
    
    // using smbus (preferred)
    int res;
    res = i2c_smbus_read_word_data(file, register);
    if (rev < 0) {
        // error handling
    } else {
        // res contains the read word
    }

    res = i2c_smbus_write_word_data(file, register, buf+1);
    if (rev < 0) {
        // error handling
    } else {
        // res contains the read word
    }

    end example commands */
}
