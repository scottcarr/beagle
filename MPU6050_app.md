#Building and running the MPU6050 application

The poky build process could have built the application for us and included it in
the root file system image.  However, I'm not sure how to set that up right now.

For now, lets build the application on the beaglebone.

You need to have an MPU6050 wired to I2C 3 for the application to work.  Assuming 
you've got a beaglebone proto cape, pin 19 on the P9 expansion
header is SCL, pin 20 is SDA.  (The I2C2 on the P9 expansion is really
I2C 3 in software.)  The MPU6050 breakout board also needs power (3.3V), 
ground, and a jumper between power and VIO.

Build the application:

    git clone https://github.com/scottcarr/beagle.git
    cd beagle/MPU6050
    make

The executable is called mpu6050.  It takes 1000 samples and dumps everything to
stdout.  It's plain CSV ASCII, so you can plot it however you'd like.  I use
Python.  You can use the script I wrote under beagle/fio/read_beagle.py.  It
requires numpy, scipy and matplotlib.  You can install those with your package
manager if you're running Linux like:

    sudo apt-get install python-numpy python-scipy python-matplotlib

On Mac or Windows it's a bit complicated.  Maybe try [EPD Free](http://www.enthought.com/products/epd_free.php)
