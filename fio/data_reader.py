import numpy as np
from pylab import *

BITS_PER_G = 16384.0
BITS_PER_DEG_PER_S = 131.0

#DATAFILE = "../experiments10252012/1.CSV"
DATAFILE = "DATA.CSV"

def convert_from_twos_comp(hi, lo):
    val = hi*2**8 + lo
    if hi > 127:
        val = val - 2**16
    return val

def convert_to_ints():
    f = open(DATAFILE)
    int_form = []
    for line in f:
        isFirst = True
        for part in line.split(','):
            if isFirst:
                # TODO add time
                pass
                isFirst = False
            else:
                hi, lo = part.split(' ')
                hi = int(hi, 16)
                lo = int(lo, 16)
                #print convert_from_twos_comp(hi, lo)
                int_form.append(convert_from_twos_comp(hi, lo))
    return int_form

def sort_columns(ints_list):
    n = len(ints_list)/6
    m = 6
    data = np.zeros((n, m))
    for j in range(m):
        for i in range(n):
            data[i,j] = ints_list[i*m+j]
    accel = np.zeros((n,3), dtype='double')
    gyro = np.zeros((n,3), dtype='double')
    accel = data[:,0:3] / BITS_PER_G
    gyro = data[:,3:] / BITS_PER_DEG_PER_S
    return accel, gyro

if __name__ == '__main__':
    ion()
    ints = convert_to_ints()
    accel, gyro = sort_columns(ints)
    figure(1); clf();
    plot(accel)
    title('accel')
    ylabel('G')
    legend(['x', 'y', 'z'])
    figure(2); clf();
    plot(gyro)
    title('gyro')
    ylabel('degree / s')
    legend(['x', 'y', 'z'])

     
                
