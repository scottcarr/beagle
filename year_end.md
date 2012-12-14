#Fall 2012 End of Semester

Gustavo and Scott went to PCSI to do a data collection.  We were aiming
to do the first collection with all three blades at the same time.  Unfortunately,
there is a problem with one of the I2C channels are we were able to collect
two out of three.  Scott will investigate this problem.

One key issue is the mounting of the BeagleBone and sensors.  There is a cap
on the turbine blades in the middle of the hub.  The BeagleBone can
fit in the in this space.  Stronger mounting that will resist vibration
will be a next step.

![beagle mounting ](https://github.com/scottcarr/beagle/blob/master/beagle.JPG?raw=true)

We attached the sensors similarly to how the accelerometers were attached
to the original turbine.  The sensors are taped to the blade and the wires
themselves are also taped to stop them from moving as the blade spins.  A next
step for this is mounting the sensors with a more permanent method to minimize
any movement relative to the blade.  We also need to mount them at a specific
distance for measurements consistent with the original turbine setup.

![sensors on blade](https://github.com/scottcarr/beagle/blob/master/blade.JPG?raw=true)

We collected 10,000 samples per sensor with the wind tunnel running.  We
observed that the speed of the front turbine was fluctuating during the
collection.  The cause of this is unknown because the other turbine was
rotating more consistently.

The data is below:

![Accelerometer Data](https://github.com/scottcarr/beagle/blob/master/accel.png?raw=true)

![FFT](https://github.com/scottcarr/beagle/blob/master/fft.png?raw=true)

Here we can see the fluctuation in the speed of rotation.  The sensor is
configured for +/-2g range for maximum sensitivity, so the lines go off
the graph at the beginning when it was spinning fastest.

In order to validate the data, the next step will be to put out accelerometer
on the same blade as the original accelerometers and compare the two.

PCSI also has a calibrator for low frequency acceleration that we will try
next semester as well.
