from pylab import *
import numpy as np
import scipy.fftpack as sf

x = np.loadtxt("beagle_data2.csv", delimiter=',')
ion()
figure(1)
clf()
t0 = x[0,0]
plot(x[:,0] - t0, x[:,1], 'b-x')
plot(x[:,0] - t0, x[:,2], 'g-x')
plot(x[:,0] - t0, x[:,3], 'r-x')
legend(['x', 'y', 'z'])
ylabel('accel (g)')
xlabel('time(s)')

figure(2)
clf()
s = sf.fft(x[:,3])
freqs = sf.fftfreq(s.size, mean(np.diff(x[:,0])))
zero = len(freqs)/2
plot(freqs[:zero], abs(s[:zero]))
xlabel('freq (Hz)')
m = np.argmax(abs(s[:zero]))
title("Peak @ {0}".format(freqs[m]))

#t0 = x[0,0]
#plot(x[:,0] - t0, x[:,1], 'b-x')
#plot(x[:,0] - t0, x[:,2], 'g-x')
#plot(x[:,0] - t0, x[:,3], 'r-x')
#legend(['x', 'y', 'z'])
#ylabel('accel (g)')
#xlabel('time(s)')
