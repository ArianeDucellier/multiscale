"""File to compute the DWT of the data"""

import math, matplotlib, numpy, pylab
import matplotlib.pyplot as plt
from scipy import interpolate

from functions import *

dirname = '../source401_25m_smooth2_potential' # name of the directory where we find the synthetics
dirname0 = '/home/alcd/Documents/Data/data' # name of the directory where we find the data
filename = 'Up_file_single.bin'             # name of the binary file of the synthetics
filename0 = 'data_shot401.bin'              # name of the binary file of the data
nr = 321                                    # number of receivers
nt = 16001                                  # number of time steps for the synthetics
nt0 = 2001                                  # number of time steps for the data
nt_ref = 40001                              # number of time steps for the DWT
dt = 0.0005                                 # time step for the synthetics
dt0 = 0.004                                 # time step for the data
dt_ref = 0.0002                             # time step for the DWT
x0 = 11000.0                                # position of the first receiver
dx = 25.0                                   # spacing between two receivers
NL = 12                                     # number of levels for DWT

fv = numpy.fromfile(dirname + '/OUTPUT_FILES/' + filename, 'f4')
fv0 = numpy.fromfile(dirname0 + '/' + filename0, 'f4')
v = numpy.reshape(fv, (nr, nt))
v0 = numpy.reshape(fv0, (nr, nt0))
t = pylab.arange(0.0, nt * dt, dt)
t0 = pylab.arange(0.0, nt0 * dt0, dt0)
t_ref = pylab.arange(0.0, nt_ref * dt_ref, dt_ref)
f_ref = pylab.arange(0.0, (0.5 * (nt_ref - 1) + 1) / ((nt_ref - 1) * dt_ref), 1.0 / ((nt_ref - 1) * dt_ref))

# Loop on receivers
for i in range(0, nr):
#	seism = 1000000.0 * v[i, :]
#	seism = 0.001 * v[i, :]
	seism = -50.0 * v[i, :]
	seism0 = v0[i, :]
	f = interpolate.interp1d(t, seism)
	f0 = interpolate.interp1d(t0, seism0)
	seism_inter = f(t_ref)
	seism_inter0 = f0(t_ref)
	seism_WT = numpy.zeros((nt_ref, NL))
	seism_WT0 = numpy.zeros((nt_ref, NL))
	seism_WT_fft = numpy.zeros((int(0.5 * (nt_ref - 1) + 1), NL))
	seism_WT_fft0 = numpy.zeros((int(0.5 * (nt_ref - 1) + 1), NL))
# Computation of scaled signals
	for j in range(0, NL):
		seism_WT[:, j] =  preprocess(seism_inter, nt_ref, dt_ref, j + 1)
		seism_WT0[:, j] =  preprocess(seism_inter0, nt_ref, dt_ref, j + 1)
		seism_WT_fft[:, j] = dt_ref * numpy.fft.rfft(seism_WT[:, j])
		seism_WT_fft0[:, j] = dt_ref * numpy.fft.rfft(seism_WT0[:, j])

# Figure of the data
        fig = plt.figure(i, figsize=(16, 12)) # time 1-4
	for j in range(0, 4):
		plt.subplot(2, 2, j + 1)    
   		plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
		pylab.plot(t_ref, seism_WT[:, j], 'b', label='synthetics')
        	pylab.plot(t_ref, seism_WT0[:, j], 'r', label='data')
		pylab.xlabel('Time (s)')
#		pylab.ylabel('Z Displacement (m)')
#		pylab.ylabel('Pressure (Pa)')
		pylab.ylabel('Potential (m2/s)')
#		pylab.title('Z displacement at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
#		pylab.title('Pressure at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.title('Potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig(dirname + '/DWT/time/v' + str(i + 1) + '_scale1_4.png')
	plt.close(fig)
        fig = plt.figure(nr + i, figsize=(16, 12)) # time 5-8
	for j in range(4, 8):
		plt.subplot(2, 2, j - 3)    
		plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
		pylab.plot(t_ref, seism_WT[:, j], 'b', label='synthetics')
        	pylab.plot(t_ref, seism_WT0[:, j], 'r', label='data')
		pylab.xlabel('Time (s)')
#		pylab.ylabel('Z Displacement (m)')
#		pylab.ylabel('Pressure (Pa)')
		pylab.ylabel('Potential (m2/s)')
#		pylab.title('Z displacement at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
#		pylab.title('Pressure at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.title('Potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig(dirname + '/DWT/time/v' + str(i + 1) + '_scale5_8.png')
	plt.close(fig)
        fig = plt.figure(2 * nr + i, figsize=(16, 12)) # time 9-12
	for j in range(8, 12):
		plt.subplot(2, 2, j - 7)    
		plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
		pylab.plot(t_ref, seism_WT[:, j], 'b', label='synthetics')
        	pylab.plot(t_ref, seism_WT0[:, j], 'r', label='data')
		pylab.xlabel('Time (s)')
#		pylab.ylabel('Z Displacement (m)')
#		pylab.ylabel('Pressure (Pa)')
		pylab.ylabel('Potential (m2/s)')
#		pylab.title('Z displacement at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
#		pylab.title('Pressure at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.title('Potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig(dirname + '/DWT/time/v' + str(i + 1) + '_scale9_12.png')
	plt.close(fig)
	fig = plt.figure(3 * nr + i, figsize=(16, 12)) # frequency 1-4
	for j in range(0, 4):
		plt.subplot(2, 2, j + 1)    
		plt.xlim(0, 60)
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft[:, j] * numpy.conj(seism_WT_fft[:, j]))), 'b', label='synthetics')
		pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft0[:, j] * numpy.conj(seism_WT_fft0[:, j]))), 'r', label='data')
		pylab.xlabel('Frequency (Hz)')
		pylab.ylabel('Fourier transform')
#		pylab.title('FFT at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
#		pylab.title('FFT of pressure at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig(dirname + '/DWT/frequency/v' + str(i + 1) + '_scale1_4.png')
	plt.close(fig)
	fig = plt.figure(4 * nr + i, figsize=(16, 12)) # frequency 5-8
	for j in range(4, 8):
		plt.subplot(2, 2, j - 3)    
		plt.xlim(0, 60)
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft[:, j] * numpy.conj(seism_WT_fft[:, j]))), 'b', label='synthetics')
		pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft0[:, j] * numpy.conj(seism_WT_fft0[:, j]))), 'r', label='data')
		pylab.xlabel('Frequency (Hz)')
		pylab.ylabel('Fourier transform')
#		pylab.title('FFT at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
#		pylab.title('FFT of pressure at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig(dirname + '/DWT/frequency/v' + str(i + 1) + '_scale5_8.png')
	plt.close(fig)
	fig = plt.figure(5 * nr + i, figsize=(16, 12)) # frequency 9-12
	for j in range(8, 12):
		plt.subplot(2, 2, j - 7)    
		plt.xlim(0, 20)
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft[:, j] * numpy.conj(seism_WT_fft[:, j]))), 'b', label='synthetics')
		pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft0[:, j] * numpy.conj(seism_WT_fft0[:, j]))), 'r', label='data')
		pylab.xlabel('Frequency (Hz)')
		pylab.ylabel('Fourier transform')
#		pylab.title('FFT at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
#		pylab.title('FFT of pressure at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig(dirname + '/DWT/frequency/v' + str(i + 1) + '_scale9_12.png')
	plt.close(fig)

