"""File to draw a picture of the seismic wave"""

import matplotlib, numpy, pylab
import matplotlib.pyplot as plt

dirname = 'source401_25m_smooth2_potential' # name of the directory where we find the synthetics
dirname0 = '/home/alcd/Documents/Data/data' # name of the directory where we find the data
filename = 'Up_file_single.bin'             # name of the binary file of the synthetics
filename0 = 'data_shot401.bin'              # name of the binary file of the data
nr = 321                                    # number of receivers
nt = 16001                                  # number of time steps for the synthetics
nt0 = 2001                                  # number of time steps for the data
dt = 0.0005                                 # time step for the synthetics
dt0 = 0.004                                 # time step for the data
x0 = 11000.0                                # position of the first receiver
dx = 25.0                                   # spacing between two receivers
factor = -50.0                              # factor to multiply the synthetics (-50.0 for potential, 1000000.0 for displacement)

fv = numpy.fromfile(dirname + '/OUTPUT_FILES/' + filename, 'f4')
fv0 = numpy.fromfile(dirname0 + '/' + filename0, 'f4')
v = numpy.reshape(fv, (nr, nt))
v0 = numpy.reshape(fv0, (nr, nt0))
t = pylab.arange(0.0, nt * dt, dt)
t0 = pylab.arange(0.0, nt0 * dt0, dt0)
f = pylab.arange(0.0, (0.5 * (nt - 1) + 1) / ((nt - 1) * dt), 1.0 / ((nt - 1) * dt))
f0 = pylab.arange(0.0, (0.5 * (nt0 - 1) + 1) / ((nt0 - 1) * dt0), 1.0 / ((nt0 - 1) * dt0))

for i in range(0, nr):
	fig = plt.figure(i, figsize=(8, 6)) # time
	vt = factor * v[i, :]
        vt0 = v0[i, :]
        plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
	pylab.plot(t, vt, 'b', label='synthetics')
        pylab.plot(t0, vt0, 'r', label='data')
        pylab.legend(loc='upper right')
	pylab.xlabel('Time (s)')
	pylab.ylabel('Potential (m2/s)')
	pylab.title('Potential at x = ' + str(x0 + i * dx) + ' m')
	pylab.savefig(dirname + '/time/v' + str(i + 1) + '.png')
	plt.close(fig)

	fig = plt.figure(nr + i, figsize=(8, 6)) # frequency
	vfft = dt * numpy.fft.rfft(vt)
        vfft0 = dt0 * numpy.fft.rfft(vt0)
	plt.xlim(0, 60)
	pylab.plot(f, numpy.sqrt(numpy.real(vfft * numpy.conj(vfft))), 'b', label='synthetics')
        pylab.plot(f0, numpy.sqrt(numpy.real(vfft0 * numpy.conj(vfft0))), 'r', label='data')
        pylab.legend(loc='upper right')
	pylab.xlabel('Frequency (Hz)')
	pylab.ylabel('Fourier transform')
	pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m')
	pylab.savefig(dirname + '/frequency/v' + str(i + 1) + '.png')
	plt.close(fig)

