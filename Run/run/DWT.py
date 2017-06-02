"""Functions to compute the discrete wavelet transform of the signals"""

import math, numpy, os
from obspy.core import read, Stream, Trace

from inversion_parameters import nrec, dt_ref, nt_ref
from user_parameters import nvm

def compute_DWT(isource, j):
	"""Read the results of the simulation in SU file
	and compute the wavelet transform

	Input:
	isource = index of the source
	j = scale at which we run the inversion process"""

	namedir1 = 'Source_' + str(isource + 1)
	os.chdir(namedir1)

	filename_d = '../../Data/data_shot' + str(isource + 1) + '.su'
	filename_s = 'OUTPUT_FILES/Up_file_single.su'
	stream_d = read(filename_d, format='SU')
	stream_s = read(filename_s, format='SU')

	stream_d_DWT = Stream()
	stream_s_DWT = Stream()
	for irec in range(0, nrec):
		trace_d = stream_d[irec].copy()
		trace_s = stream_s[irec].copy()
		# Interpolation: We need the same sampling rate to carry out the DWT
		trace_d.interpolate(sampling_rate=1.0 / dt_ref, starttime=trace_d.stats.starttime, npts=nt_ref)
		trace_s.interpolate(sampling_rate=1.0 / dt_ref, starttime=trace_s.stats.starttime, npts=nt_ref)
		# Discrete Wavelet Transform
		data = trace_d.data
		synthetics = trace_s.data
		(data_DWT, NA_d) = WT(data, nt_ref, j)
		(synthetics_DWT, NA_s) = WT(synthetics, nt_ref, j)
		trace_d_DWT = Trace(data=data_DWT, header=trace_d.stats)
		trace_s_DWT = Trace(data=synthetics_DWT, header=trace_s.stats)
		trace_d_DWT.data = numpy.require(trace_d_DWT.data, dtype=numpy.float32)
		trace_s_DWT.data = numpy.require(trace_s_DWT.data, dtype=numpy.float32)
		stream_d_DWT.append(trace_d_DWT)
		stream_s_DWT.append(trace_s_DWT)
	stream_d_DWT.write('OUTPUT_FILES/data_DWT.su', format='SU', byteorder='<')
	stream_s_DWT.write('OUTPUT_FILES/synthetics_DWT.su', format='SU', byteorder='<')
	os.chdir('..')

def WT(seism, NSTEP, level):
	"""Compute the DWT of the signal with Daubechies wavelet

	Input:
	seism = signal to be reconstructed at scale level
	NSTEP = number of time steps in the signal
	level = scale of the reconstruction

	Output:
	seism = signal reconstructed
	NA = length of the wavelet"""

	NA = 0
	if level > 0:
   		if level == 12:
			NA = 45046
   		if level == 11:
			NA = 22518
   		if level == 10:
			NA = 11254   
   		if level == 9:
			NA = 5622
   		if level == 8:
			NA = 2806
   		if level == 7:
			NA = 1398
   		if level == 6:
			NA = 694  
   		if level == 5:
			NA = 342 
   		if level == 4:
			NA = 166
   		if level == 3:
			NA = 78
   		if level == 2:
			NA = 34
   		if level == 1:
			NA = 12

	if level > 0 and NA > 0:
   		nonzero_basis = numpy.zeros(NA)
		basis = numpy.zeros(NSTEP)
		seism_WT = numpy.zeros(NSTEP)

		fname = 'scale_basis_Daubechies' + str(nvm) + '_scale' + str(level)
		filename = '../../WT_basis/' + fname + '.dat'
		nonzero_basis = numpy.loadtxt(filename)

		# initialization
		iend = 1
		istart = 1 - NA
		# find shifted basis 
		while istart < NSTEP:
    			basis[:] = 0.0
			j = 0
			for i in range(istart, iend):
				if i >= 0 and i < NSTEP:
					basis[i] = nonzero_basis[j]
				j = j + 1
			# WT
			wc = numpy.dot(seism, basis)
			# inverse wavelet transform to construct data
			seism_WT = seism_WT + wc * basis
			iend = iend + int(math.pow(2.0, level))
			istart = istart + int(math.pow(2.0, level))
		seism = seism_WT
	return (seism, NA)

