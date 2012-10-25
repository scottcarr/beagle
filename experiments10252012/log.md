#Experimentation 10 Oct 2012

With the SD logging application complete, I went to PCSI for further testing.

First, I setup one Xbee radio as a programmer and one as the programee.  See
[XBee Tips](http://wind.cs.purdue.edu/doc/xbee_tips.html) for more information.

Then, I attached the Fio, battery, MPU6050, and SD card to the uninstrumented
turbine blade.

<img src="https://github.com/scottcarr/beagle/raw/master/experiments10252012/tape.JPG">

The MPU6050 is mounted:

(I don't know the appropriate terms, so here is my best approximation)

Accelerometer
<table>
<tr><td>Axis</td><td>description</td></tr>
<tr><td>Positive Z</td><td>into the wind</td></tr>
<tr><td>Positive Y</td><td>towards the blade tip</td></tr>
<tr><td>Positive X</td><td>towards the blade edge</td></tr>
</table>

Gyro
<table>
<tr><td>Z</td><td>rotation in the same plane as the blades rotate</td></tr>
<tr><td>X</td><td>rotation is rotating in the same plane as rotating around the post</td></tr>
<tr><td>Y</td><td>rotation around the blade axis</td></tr>
</table>

I connected the Xbee explorer and programmer radio to my laptop.

<img src="https://github.com/scottcarr/beagle/raw/master/experiments10252012/laptop.JPG">


I programmed the Fio [SD logger app](http://wind.cs.purdue.edu/doc/sd_logger_app.html) 
 using the Arduino application.  The programming was done over the Xbee radio
wirelessly.  The laptop was about 30 feet from the turbine.

<img src="https://github.com/scottcarr/beagle/raw/master/experiments10252012/distance.JPG">

Wireless programming from this distance (and through the wind tunnel walls)
 only worked intermitently.  The first time I tried programming it worked.
The second time I had to go into the wind tunnel.  The reliability and
distance capability of the Xbee radios is an ongoing concern/issue.

To do a data collection, I started the program and then spun the turbine blades by hand.

The Fio collected 1000 data points from the Accelerometer and Gyro (X,Y,Z for both).

<img src="https://raw.github.com/scottcarr/beagle/master/experiments10252012/accel1.png">
<img src="https://raw.github.com/scottcarr/beagle/master/experiments10252012/gyro1.png">

[Raw Data file 1](https://raw.github.com/scottcarr/beagle/master/experiments10252012/DATA.CSV)

Note: to read the data, you need to use [data_reader.py](https://github.com/scottcarr/beagle/blob/master/fio/data_reader.py)
