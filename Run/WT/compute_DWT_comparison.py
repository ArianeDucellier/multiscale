"""File to compute the DWT of the data"""

import math, matplotlib, numpy, pylab
import matplotlib.pyplot as plt
from scipy import interpolate

from functions import *

dirname0 = '/home/alcd/Documents/Data/data' # name of the directory where we find the data
dirname1 = '../source401_25m_potential'     # name of the directory where we find the synthetics
dirname2 = '../source401_25m_smooth_potential' # name of the directory where we find the synthetics
dirname3 = '../source401_25m_smooth2_potential' # name of the directory where we find the synthetics
filename0 = 'data_shot401.bin'              # name of the binary file where we find the data
filename1 = 'Up_file_single.bin'            # name of the binary file where we find the synthetics
filename2 = 'Up_file_single.bin'            # name of the binary file where we find the synthetics
filename3 = 'Up_file_single.bin'            # name of the binary file where we find the synthetics
nr = 321                                    # number of receivers
nt0 = 2001                                  # number of time steps for the data
nt1 = 16001                                 # number of time steps for the synthetics
nt2 = 16001                                 # number of time steps for the synthetics
nt3 = 16001                                 # number of time steps for the synthetics
nt_ref = 40001                              # number of time steps for the DWT
dt0 = 0.004                                 # time step for the data
dt1 = 0.0005                                # time step for the synthetics
dt2 = 0.0005                                # time step for the synthetics
dt3 = 0.0005                                # time step for the synthetics
dt_ref = 0.0002                             # time step for the DWT
x0 = 11000.0                                # position of the first receiver
dx = 25.0                                   # spacing between two receivers
NL = 12                                     # number of levels for DWT

fv0 = numpy.fromfile(dirname0 + '/' + filename0, 'f4')
fv1 = numpy.fromfile(dirname1 + '/OUTPUT_FILES/' + filename1, 'f4')
fv2 = numpy.fromfile(dirname2 + '/OUTPUT_FILES/' + filename2, 'f4')
fv3 = numpy.fromfile(dirname3 + '/OUTPUT_FILES/' + filename3, 'f4')
v0 = numpy.reshape(fv0, (nr, nt0))
v1 = numpy.reshape(fv1, (nr, nt1))
v2 = numpy.reshape(fv2, (nr, nt2))
v3 = numpy.reshape(fv3, (nr, nt3))
t0 = pylab.arange(0.0, nt0 * dt0, dt0)
t1 = pylab.arange(0.0, nt1 * dt1, dt1)
t2 = pylab.arange(0.0, nt2 * dt2, dt2)
t3 = pylab.arange(0.0, nt3 * dt3, dt3)
t_ref = pylab.arange(0.0, nt_ref * dt_ref, dt_ref)
f_ref = pylab.arange(0.0, (0.5 * (nt_ref - 1) + 1) / ((nt_ref - 1) * dt_ref), 1.0 / ((nt_ref - 1) * dt_ref))

# Loop on receivers
for i in range(0, nr):
	seism0 = v0[i, :]
	seism1 = -50.0 * v1[i, :]
	seism2 = -50.0 * v2[i, :]
	seism3 = -50.0 * v3[i, :]
	f0 = interpolate.interp1d(t0, seism0)
	f1 = interpolate.interp1d(t1, seism1)
	f2 = interpolate.interp1d(t2, seism2)
	f3 = interpolate.interp1d(t3, seism3)
	seism_inter0 = f0(t_ref)
	seism_inter1 = f1(t_ref)
	seism_inter2 = f2(t_ref)
	seism_inter3 = f3(t_ref)
	seism_WT0 = numpy.zeros((nt_ref, NL))
	seism_WT1 = numpy.zeros((nt_ref, NL))
	seism_WT2 = numpy.zeros((nt_ref, NL))
	seism_WT3 = numpy.zeros((nt_ref, NL))
	seism_WT_fft0 = numpy.zeros((int(0.5 * (nt_ref - 1) + 1), NL))
	seism_WT_fft1 = numpy.zeros((int(0.5 * (nt_ref - 1) + 1), NL))
	seism_WT_fft2 = numpy.zeros((int(0.5 * (nt_ref - 1) + 1), NL))
	seism_WT_fft3 = numpy.zeros((int(0.5 * (nt_ref - 1) + 1), NL))
# Computation of scaled signals
	for j in range(0, NL):
		seism_WT0[:, j] =  preprocess(seism_inter0, nt_ref, dt_ref, j + 1)
		seism_WT1[:, j] =  preprocess(seism_inter1, nt_ref, dt_ref, j + 1)
		seism_WT2[:, j] =  preprocess(seism_inter2, nt_ref, dt_ref, j + 1)
		seism_WT3[:, j] =  preprocess(seism_inter3, nt_ref, dt_ref, j + 1)
		seism_WT_fft0[:, j] = dt_ref * numpy.fft.rfft(seism_WT0[:, j])
		seism_WT_fft1[:, j] = dt_ref * numpy.fft.rfft(seism_WT1[:, j])
		seism_WT_fft2[:, j] = dt_ref * numpy.fft.rfft(seism_WT2[:, j])
		seism_WT_fft3[:, j] = dt_ref * numpy.fft.rfft(seism_WT3[:, j])

# Figure of the data
        fig = plt.figure(i, figsize=(16, 12)) # time 1-4
	for j in range(0, 4):
		plt.subplot(2, 2, j + 1)    
		plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
        	pylab.plot(t_ref, seism_WT0[:, j], 'black', label='data')
		pylab.plot(t_ref, seism_WT1[:, j], 'skyblue', label='initial')
		pylab.plot(t_ref, seism_WT2[:, j], 'red', label='smooth 1')
		pylab.plot(t_ref, seism_WT3[:, j], 'lime', label='smooth 2')
		pylab.xlabel('Time (s)')
		pylab.ylabel('Potential (m2/s)')
		pylab.title('Potential at at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig('../OUTPUT_FILES/DWT/model/time/v' + str(i + 1) + '_scale1_4.png')
	plt.close(fig)
        fig = plt.figure(nr + i, figsize=(16, 12)) # time 5-8
	for j in range(4, 8):
		plt.subplot(2, 2, j - 3)    
		plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
        	pylab.plot(t_ref, seism_WT0[:, j], 'black', label='data')
		pylab.plot(t_ref, seism_WT1[:, j], 'skyblue', label='initial')
		pylab.plot(t_ref, seism_WT2[:, j], 'red', label='smooth 1')
		pylab.plot(t_ref, seism_WT3[:, j], 'lime', label='smooth 2')
		pylab.xlabel('Time (s)')
		pylab.ylabel('Potential (m2/s)')
		pylab.title('Potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig('../OUTPUT_FILES/DWT/model/time/v' + str(i + 1) + '_scale5_8.png')
	plt.close(fig)
        fig = plt.figure(2 * nr + i, figsize=(16, 12)) # time 9-12
	for j in range(8, 12):
		plt.subplot(2, 2, j - 7)    
		plt.xlim(0.01 * i, 1.0 + 0.0175 * i)
        	pylab.plot(t_ref, seism_WT0[:, j], 'black', label='data')
		pylab.plot(t_ref, seism_WT1[:, j], 'skyblue', label='initial')
		pylab.plot(t_ref, seism_WT2[:, j], 'red', label='smooth 1')
		pylab.plot(t_ref, seism_WT3[:, j], 'lime', label='smooth 2')
		pylab.xlabel('Time (s)')
		pylab.ylabel('Potential (m2/s)')
		pylab.title('Potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig('../OUTPUT_FILES/DWT/model/time/v' + str(i + 1) + '_scale9_12.png')
	plt.close(fig)
	fig = plt.figure(3 * nr + i, figsize=(16, 12)) # frequency 1-4
	for j in range(0, 4):
		plt.subplot(2, 2, j + 1)    
		plt.xlim(0, 60)
		pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft0[:, j] * numpy.conj(seism_WT_fft0[:, j]))), 'black', label='data')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft1[:, j] * numpy.conj(seism_WT_fft1[:, j]))), 'skyblue', label='initial')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft2[:, j] * numpy.conj(seism_WT_fft2[:, j]))), 'red', label='smooth 1')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft3[:, j] * numpy.conj(seism_WT_fft3[:, j]))), 'lime', label='smooth 2')
		pylab.xlabel('Frequency (Hz)')
		pylab.ylabel('Fourier transform')
		pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig('../OUTPUT_FILES/DWT/model/frequency/v' + str(i + 1) + '_scale1_4.png')
	plt.close(fig)
	fig = plt.figure(4 * nr + i, figsize=(16, 12)) # frequency 5-8
	for j in range(4, 8):
		plt.subplot(2, 2, j - 3)    
		plt.xlim(0, 60)
		pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft0[:, j] * numpy.conj(seism_WT_fft0[:, j]))), 'black', label='data')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft1[:, j] * numpy.conj(seism_WT_fft1[:, j]))), 'skyblue', label='initial')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft2[:, j] * numpy.conj(seism_WT_fft2[:, j]))), 'red', label='smooth 1')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft3[:, j] * numpy.conj(seism_WT_fft3[:, j]))), 'lime', label='smooth 2')
		pylab.xlabel('Frequency (Hz)')
		pylab.ylabel('Fourier transform')
		pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig('../OUTPUT_FILES/DWT/model/frequency/v' + str(i + 1) + '_scale5_8.png')
	plt.close(fig)
	fig = plt.figure(5 * nr + i, figsize=(16, 12)) # frequency 9-12
	for j in range(8, 12):
		plt.subplot(2, 2, j - 7)    
		plt.xlim(0, 20)
		pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft0[:, j] * numpy.conj(seism_WT_fft0[:, j]))), 'black', label='data')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft1[:, j] * numpy.conj(seism_WT_fft1[:, j]))), 'skyblue', label='initial')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft2[:, j] * numpy.conj(seism_WT_fft2[:, j]))), 'red', label='smooth 1')
	        pylab.plot(f_ref, numpy.sqrt(numpy.real(seism_WT_fft3[:, j] * numpy.conj(seism_WT_fft3[:, j]))), 'lime', label='smooth 2')
		pylab.xlabel('Frequency (Hz)')
		pylab.ylabel('Fourier transform')
		pylab.title('FFT of potential at x = ' + str(x0 + i * dx) + ' m (Level ' + str(j + 1) + ')')
		pylab.legend(loc='upper right')
	pylab.savefig('../OUTPUT_FILES/DWT/model/frequency/v' + str(i + 1) + '_scale9_12.png')
	plt.close(fig)

