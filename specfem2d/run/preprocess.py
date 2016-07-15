"""Functions to carry out the preprocessing"""

import numpy, obspy, os
from obspy.core import read, Stream, Trace
from obspy.signal.invsim import cosine_sac_taper
#from obspy.signal.util import _npts2nfft

from inversion_parameters import nrec, tstart, tend, sstart, send, filt_freq

def process(isource, j):
	"""Read the DWT results in SU file
	and apply preprocessing

	Input:
	isource = index of the source
	j = scale at which we run the inversion process"""

	namedir1 = 'Source_' + str(isource + 1)
	os.chdir(namedir1)

	stream_d = read('OUTPUT_FILES/data_DWT.su', format='SU', byteorder='<')
	stream_s = read('OUTPUT_FILES/synthetics_DWT.su', format='SU', byteorder='<')

	stream_d_new = Stream()
	stream_s_new = Stream()
	for irec in range(0, nrec):
		trace_d = stream_d[irec].copy()
		trace_s = stream_s[irec].copy()
		# Window
		starttime = tstart[j - 1] + irec * 25.0 * sstart[j - 1]
		endtime = tend[j - 1] + irec * 25.0 * send[j - 1]
		cut_func(trace_d, starttime, endtime)
		cut_func(trace_s, starttime, endtime)
		# Tapering
		trace_d.taper(max_percentage=0.8, type="hann")
		trace_s.taper(max_percentage=0.8, type="hann")
		# Filtering
		filter_synt(trace_d, filt_freq)
		filter_synt(trace_s, filt_freq)
		# Tapering
		trace_d.taper(max_percentage=0.8, type="hann")
		trace_s.taper(max_percentage=0.8, type="hann")
		trace_d.data = numpy.require(trace_d.data, dtype=numpy.float32)
		trace_s.data = numpy.require(trace_s.data, dtype=numpy.float32)
		stream_d_new.append(trace_d)
		stream_s_new.append(trace_s)
	stream_d_new.write('OUTPUT_FILES/data_process.su', format='SU', byteorder='<')
	stream_s_new.write('OUTPUT_FILES/synthetics_process.su', format='SU', byteorder='<')
	os.chdir('..')

def cut_func(st, cut_start, cut_end, dynamic_length=10.0):
	t1 = cut_start - dynamic_length
	t2 = cut_start + dynamic_length
	if isinstance(st, obspy.Trace):
		return flex_cut_trace(st, t1, t2)
	elif isinstance(st, obspy.Stream):
		tr_list = []
		for tr in st:
			tr_list.append(flex_cut_trace(tr, t1, t2))
		return obspy.Stream(traces=tr_list)
	else:
		raise ValueError("cut_func method only accepts obspy.Trace or obspy.Stream as the first Argument")

def filter_synt(tr, pre_filt):
	"""Perform a frequency domain taper like during the response removal just without an actual response..."""

	data = tr.data.astype(numpy.float64)
	# Smart calculation of nfft dodging large primes
#	nfft = _npts2nfft(len(data))
	nfft = int(0.5 * (data.size - 1) + 1)
	fy = 1.0 / (tr.stats.delta * 2.0)
#	freqs = numpy.linspace(0, fy, nfft // 2 + 1)
	freqs = numpy.linspace(0, fy, nfft) 
	# Transform data to frequency domain
#	data = numpy.fft.rfft(data, n=nfft)
	data = numpy.fft.rfft(data)
	data *= cosine_sac_taper(freqs, flimit=pre_filt)
	data[-1] = abs(data[-1]) + 0.0j
	# Transform data back into the time domain
#	data = numpy.fft.irfft(data)[0:len(data)]
	data = numpy.fft.irfft(data, int((nfft - 1) * 2.0 + 1))
	# Assign processed data and store processing information
	tr.data = data

def flex_cut_trace(tr, cut_starttime, cut_endtime):
	# not cut strictly, but also based on the original trace length
	if not isinstance(tr, obspy.Trace):
		raise ValueError("cut_trace method only accepts obspy.Trace as the first argument")
	starttime = tr.stats.starttime
	endtime = tr.stats.endtime
	cut_starttime = max(starttime, cut_starttime)
	cut_endtime = min(endtime, cut_endtime)
	if cut_starttime > cut_endtime:
		raise ValueError("Cut starttime is larger than cut endtime")
	return tr.slice(cut_starttime, cut_endtime)

