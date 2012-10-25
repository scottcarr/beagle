#Experimentation 10 Oct 2012

With the SD logging application complete, I went to PCSI for further testing.

First, I setup one Xbee radio as a programmer and one as the programee.  See
[XBee Tips](http://wind.cs.purdue.edu/doc/xbee_tips.html) for more information.

Then, I attached the Fio, battery, MPU6050, and SD card to the uninstrumented
turbine blade.

<img src="tape.jpg">

I connected the Xbee explorer and programmer radio to my laptop.

<img src="laptop">

I programmed the Fio [SD logger app](http://wind.cs.purdue.edu/doc/sd_logger_app.html) 
 using the Arduino application.

I started the program and then spun the turbine blades by hand.

The Fio collected 1000 data points from the Accelerometer and Gyro (X,Y,Z for both).

<img src="accel1.png"
<img src="gyro1.png"
