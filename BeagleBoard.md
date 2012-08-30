# Documentation for hooking up the 
# Sparkfun IMU Digital Combo Board 6 Degrees of Freedom ITG3200 / ADXL345

Wiring
------

All the wiring is done with the beagle bone proto cape

Breakout board pin / beagle bone  pin
GND /  GND (on proto cape)
3.3V / 3.3V (on proto cape)
SCL / I2C2_SCL (P9 expansion header - pin 19)
SDA / I2C2_SDA (P9 expansion header - pin 20)
INT0 / no connect
INT1 / no connect

Software
--------

Strangely, the I2C2_XXX hardware pins map to I2C bus 3 in Angstrom Linux.  I don't
understand the mapping scheme.  This is something to keep in mind if we add
more sensors to other buses.

The command i2cdetect -r 3 probes every address on the bus:

    root@beaglebone:~# i2cdetect -r 3
    WARNING! This program can confuse your I2C bus, cause data loss and worse!
    I will probe file /dev/i2c-3 using read byte commands.
    I will probe address range 0x03-0x77.
    Continue? [Y/n] Y
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- UU -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- 53 UU UU UU UU -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- -- 

0x53 is the address of the ADXL345 Accelerometer

0x68 is the address of the ITG-3200 gyro 

Notice they show up at the corresponding cells in the table above.  If they
were not connected the table would look like:

         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- UU -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- UU UU UU UU -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- -- 

'UU' means in use by some over device/process

