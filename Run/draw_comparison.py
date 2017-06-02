"""File to draw a picture of the seismic wave"""

import matplotlib, numpy, pylab
import matplotlib.pyplot as plt

dirname1 = 'source401_50m_potential'        # name of the directory where we find the synthetics
dirname2 = 'source401_25m_potential'        # name of the directory where we find the synthetics
dirname3 = 'source401_10m_potential'        # name of the directory where we find the synthetics
dirname0 = '/home/alcd/Documents/Data/data' # name of the directory where we find the data
filename1 = 'Up_file_single.bin'            # name of the binary file of the synthetics
filename2 = 'Up_file_single.bin'            # name of the binary file of the synthetics
filename3 = 'Up_file_single.bin'            # name of the binary file of the synthetics
filename0 = 'data_shot401.bin'              # name of the binary file of the data
nr = 321                                    # number of receivers
nt1 = 8001                                  # number of time steps for the synthetics
nt2 = 16001                                 # number of time steps for the synthetics
nt3 = 40001                                 # number of time steps for the synthetics
nt0 = 2001                                  # number of time steps for the data
dt1 = 0.001                                 # time step for the synthetics
dt2 = 0.0005                                # time step for the synthetics
dt3 = 0.0002                                # time step for the synthetics
dt0 = 0.004                                 # time step for the data
x0 = 11000.0                                # position of the first receiver
dx = 25.0                                   # spacing between two receivers

fv1 = numpy.fromfile(dirname1 + '/OUTPUT_FILES/' + filename1, 'f4')
fv2 = numpy.fromfile(dirname2 + '/OUTPUT_FILES/' + filename2, 'f4')
fv3 = numpy.fromfile(dirname3 + '/OUTPUT_FILES/' + filename3, 'f4')
fv0 = numpy.fromfile(dirname0 + '/' + filename0, 'f4')
v1 = numpy.reshape(fv1, (nr, nt1))
v2 = numpy.reshape(fv2, (nr, nt2))
v3 = numpy.reshape(fv3, (nr, nt3))
v0 = numpy.reshape(fv0, (nr, nt0))
t1 = pylab.arange(0.0, nt1 * dt1, dt1)
t2 = pylab.arange(0.0, nt2 * dt2, dt2)
t3 = pylab.arange(0.0, nt3 * dt3, dt3)
t0 = pylab.arange(0.0, nt0 * dt0, dt0)
f1 = pylab.arange(0.0, (0.5 * (nt1 - 1) + 1) / ((nt1 - 1) * dt1), 1.0 / ((nt1 - 1) * dt1))
f2 = pylab.arange(0.0, (0.5 * (nt2 - 1) + 1) / ((nt2 - 1) * dt2), 1.0 / ((nt2 - 1) * dt2))
f3 = pylab.arange(0.0, (0.5 * (nt3 - 1) + 1) / ((nt3 - 1) * dt3), 1.0 / ((nt3 - 1) * dt3))
f0 = pylab.arange(0.0, (0.5 * (nt0 - 1) + 1) / ((nt0 - 1) * dt0), 1.0 / ((nt0 - 1) * dt0))

for i in range(0, nr):
	fig = plt.figure(i) # time
	vt1 = -50.0 * v1[i, :]
	vt2 = -50.0 * v2[i, :]
        vt3 = -50.0 * v3[i, :]
        vt0 = v0[i, :]
        plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
        pylab.plot(t0, vt0, 'black', label='data')
	pylab.plot(t1, vt1, 'skyblue', label='ds = 50 m')
	pylab.plot(t2, vt2, 'red', label='ds = 25 m')
	pylab.plot(t3, vt3, 'lime', label='ds = 10 m')
        pylab.legend(loc='upper right')
	pylab.xlabel('Time (s)')
	pylab.ylabel('Potential (m2/s)')
	pylab.title('Potential at x = ' + str(x0 + i * dx) + ' m')
	pylab.savefig('OUTPUT_FILES/timestep/time/v' + str(i + 1) + '.png')
	plt.close(fig)

	fig = plt.figure(nr + i) # frequency (1)
	vfft1 = dt1 * numpy.fft.rfft(vt1)
	vfft2 = dt2 * numpy.fft.rfft(vt2)
	vfft3 = dt3 * numpy.fft.rfft(vt3)
        vfft0 = dt0 * numpy.fft.rfft(vt0)
	plt.xlim(0, 100)
        pylab.plot(f0, numpy.sqrt(numpy.real(vfft0 * numpy.conj(vfft0))), 'black', label='data')
	pylab.plot(f1, numpy.sqrt(numpy.real(vfft1 * numpy.conj(vfft1))), 'skyblue', label='ds = 50 m')
	pylab.plot(f2, numpy.sqrt(numpy.real(vfft2 * numpy.conj(vfft2))), 'red', label='ds = 25 m')
	pylab.plot(f3, numpy.sqrt(numpy.real(vfft3 * numpy.conj(vfft3))), 'lime', label='ds = 10 m')
        pylab.legend(loc='upper right')
	pylab.xlabel('Frequency (Hz)')
	pylab.ylabel('Fourier transform')
	pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m')
	pylab.savefig('OUTPUT_FILES/timestep/frequency/v' + str(i + 1) + '.png')
	plt.close(fig)

