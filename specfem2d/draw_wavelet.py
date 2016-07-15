"""File to draw a picture of the wavelet"""

import matplotlib, numpy, pylab
import matplotlib.pyplot as plt

filename = 'DATA/both_10m/source.txt' # name of the file to read
nt       = 40001                      # Number of time steps
dt       = 0.0002                     # Time step

fw = numpy.loadtxt(filename)
f = pylab.arange(0.0, (0.5 * (nt - 1) + 1) / ((nt - 1) * dt), 1.0 / ((nt - 1) * dt))
wfft = dt * numpy.fft.rfft(fw[:,1])

fig = plt.figure(0) # time
plt.xlim(0, 0.7)
plt.ylim(-40.0, 30.0)
plt.plot(fw[:,0], fw[:,1], 'b-', label='Initial')
plt.xlabel('Time (s)')
plt.ylabel('Wavelet')
plt.title('Wavelet source')
plt.savefig('DATA/both_10m/Source_time.eps')
plt.close(fig)

fig = plt.figure(1) # frequency (1)
plt.xlim(0, 100)
plt.ylim(0, 1)
plt.plot(f, numpy.sqrt(numpy.real(wfft * numpy.conj(wfft))), 'b-', label='Initial')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Fourier transform')
plt.title('Wavelet source')
plt.savefig('DATA/both_10m/Source_frequency_1.eps')
plt.close(fig)

fig = plt.figure(2) # frequency (2)
plt.xlim(0, 2500)
plt.ylim(0, 0.005)
plt.plot(f, numpy.sqrt(numpy.real(wfft * numpy.conj(wfft))), 'b-', label='Initial')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Fourier transform')
plt.title('Wavelet source')
plt.savefig('DATA/both_10m/Source_frequency_2.eps')
plt.close(fig)
