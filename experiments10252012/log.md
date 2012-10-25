#Experimentation 10 Oct 2012

With the SD logging application complete, I went to PCSI for further testing.

First, I setup one Xbee radio as a programmer and one as the programee.  See
[XBee Tips](http://wind.cs.purdue.edu/doc/xbee_tips.html) for more information.

Then, I attached the Fio, battery, MPU6050, and SD card to the uninstrumented
turbine blade.

<img src="https://github.com/scottcarr/beagle/raw/master/experiments10252012/tape.JPG">

I connected the Xbee explorer and programmer radio to my laptop.

<img src="https://github.com/scottcarr/beagle/raw/master/experiments10252012/laptop.JPG">

I programmed the Fio [SD logger app](http://wind.cs.purdue.edu/doc/sd_logger_app.html) 
 using the Arduino application.

I started the program and then spun the turbine blades by hand.

The Fio collected 1000 data points from the Accelerometer and Gyro (X,Y,Z for both).

<img src="https://raw.github.com/scottcarr/beagle/master/experiments10252012/accel1.png"
<img src="https://raw.github.com/scottcarr/beagle/master/experiments10252012/gyro1.png">

[Raw Data file 1](https://raw.github.com/scottcarr/beagle/master/experiments10252012/DATA.CSV)

Note: to read the data, you need to use [data_reader.py](https://github.com/scottcarr/beagle/blob/master/fio/data_reader.py)
