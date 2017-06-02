import math, numpy

from user_parameters import *

def preprocess(d, NSTEP, deltat, Wscale, t0=0.0, f0=1.0, is_laplace=0, dis_sr=0.0, S_x=1.0, S_t=1.0, is_window=0, window_type=1, V_slow=1.0, V_fast=1.0, mute_near=0, offset_near=0.0, mute_far=0, offset_far=0.0):
	"""Process the signal (including DWT)"""

	istart = 0
	iend = NSTEP - 1

	# mute
	if mute_near == 1 and dis_sr <= offset_near:
		d[:] = 0.0
		istart = NSTEP
		iend = 0
	if mute_far == 1 and dis_sr >= offset_far:
		d[:] = 0.0
		istart = NSTEP
		iend = 0

	# laplace damping spatially and temporally 
	if is_laplace == 1 and istart < iend:
		# spatial
		d = d * exp(- dis_sr * S_x)
		# temporal
		for itime in range(0, NSTEP):
			d[itime] = d[itime] * exp(- itime * deltat * S_t)

	# dip-window using slopes 
	if is_window == 1 and istart < iend:
		# estimate surface-wave arrivals
		istart = max(int((dis_sr / V_fast + t0 - 1.2 / f0) / deltat), istart)
		iend = min(int((dis_sr / V_slow + 3.0 / f0 + t0 + 1.2 / f0) / deltat), iend)
		if istart < iend: 
			# window
			tas = taper(NSTEP, istart, iend, window_type)
			d = d * tas

	# WT filtering
	if Wscale > 0 and istart < iend:
		(d, NA) = WT(d, NSTEP, Wscale)
		istart = max(istart - NA, 0)
		iend = min(iend + NA, NSTEP - 1)
	return d 

def taper(npts, istart, iend, window_type):
	"""Taper function
	Input:
		- npts: number of time steps in the signal
		- istart: time step where we begin tapering
		- iend: time step where we end tapering
		- window_type: Type of tapering
	Output:
		- tas: multiplying factor for tapering"""

	nlen = iend - istart + 1

	# some constants
	sfac1 = math.pow(2.0 / nlen, 2.0) # for Welch taper
	ipwr_t = 10.0                     # for time-domain cosine taper

	# initialization
	tas = numpy.zeros(npts)
	fac = numpy.zeros(nlen)

	for i in range(0, nlen):
		if window_type == 2:
			fac[i] = 1.0 - sfac1 * math.pow(i - nlen / 2.0, 2.0)
		elif window_type == 3:
			fac[i] = 1.0 - math.pow(math.cos(PI * i / (nlen - 1)), ipwr_t)
		elif window_type == 4:
			fac[i] = 0.5 - 0.5 * math.cos(TWOPI * i / (nlen - 1))
		else:
			fac[i] = 1.0 # boxcar window

	tas[istart:iend] = fac[0:nlen]
	return tas

def WT(seism, NSTEP, level):
	"""Compute the DWT of the signal with Daubechies wavelet
	Input:
		- seism: signal to be reconstructed at scale level
		- NSTEP: number of time steps in the signal
		- level: scale of the reconstruction
	Output:
		- seism: signal reconstructed
		- NA: length of the wavelet"""

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
		filename = 'WT_basis/' + fname + '.dat'
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

