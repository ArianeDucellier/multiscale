"""Functions to carry out the optimization"""

import numpy, os
from obspy.core import read, Stream, Trace

from inversion_parameters import nrec, dt_ref, dt_s, nt_ref, nt_s, tstart, sstart, rstart, rend, f

def time_difference(isource, j):
	"""Compute the time difference between data and synthetics

	Input:
	isource = index of the source
	j = scale at which we run the inversion process"""

	namedir1 = 'Source_' + str(isource + 1)
	os.chdir(namedir1)

	filename_d = 'OUTPUT_FILES/data_process.su'
	filename_s = 'OUTPUT_FILES/synthetics_process.su'
	filename_i = 'OUTPUT_FILES/Up_file_single.su'
	stream_d = read(filename_d, format='SU', byteorder='<')
	stream_s = read(filename_s, format='SU', byteorder='<')
	stream_i = read(filename_i, format='SU')

	misfit = 0.0
	stream_adj = Stream()
	for irec in range(0, nrec):
		adj = numpy.zeros(nt_s)
		trace_i = stream_i[irec].copy()
		if irec >= rstart - 1 and irec <= rend - 1:
			trace_d = stream_d[irec].copy()
			trace_s = stream_s[irec].copy()
			if trace_d.data.size != trace_s.data.size:
				raise ValueError("Data and synthetic signals should have the same length")
			nstep = trace_s.data.size
			adj_temp = numpy.zeros(nt_ref)
			starttime = tstart[j - 1] + irec * 25.0 * sstart[j - 1]
			istart = int(starttime / dt_ref)
			for it in range(0, nstep):
				misfit += 0.5 * numpy.power(f * trace_s.data[it] - trace_d.data[it], 2.0)
				adj_temp[istart + it] = f * trace_s.data[it] - trace_d.data[it]
			trace_adj = Trace(data=adj_temp, header=trace_s.stats)
			trace_adj.interpolate(sampling_rate=1.0 / dt_s, starttime=trace_adj.stats.starttime, npts=nt_s)
		else:
			trace_adj = Trace(data=adj, header=trace_i.stats)
		trace_adj.data = numpy.require(trace_adj.data, dtype=numpy.float32)
		stream_adj.append(trace_adj)
	stream_adj.write('SEM/Up_file_single.su.adj', format='SU')
	os.chdir('..')

	return misfit

def search_step():
	"""Function to find the appropriate step length for the conjugate gradient
	"""

	# Save current model into intermediate files
	for isource in range(0, nsource):
		namedir1 = 'Source_' + str(isource + 1)
		os.chdir(namedir1)
		for iproc in range(0, nproc):
			if iproc < 10:
				filename1 = 'DATA/proc00000' + str(iproc) + '_model_velocity.dat_input'
				filename2 = 'DATA/proc00000' + str(iproc) + '_model_velocity.save'
			elif proc < 100:
				filename1 = 'DATA/proc0000' + str(iproc) + '_model_velocity.dat_input'
				filename2 = 'DATA/proc0000' + str(iproc) + '_model_velocity.save'
			else:
				filename1 = 'DATA/proc000' + str(iproc) + '_model_velocity.dat_input'
				filename2 = 'DATA/proc000' + str(iproc) + '_model_velocity.save'
			shutil.copy (filename1, filename2)
		os.chdir('..')

	# Get the gradient direction

	# Loop on step length
	for i in range(0, len(gamma)):
		for isource in range(0, nsource):
			namedir1 = 'Source_' + str(isource + 1)
			os.chdir(namedir1)
			# Modify the model
			for iproc in range(0, nproc):
				if iproc < 10:
					filename1 = 'DATA/proc00000' + str(iproc) + '_model_velocity.save'
					filename2 = 'DATA/proc00000' + str(iproc) + '_model_velocity.dat_input'
				elif proc < 100:
					filename1 = 'DATA/proc0000' + str(iproc) + '_model_velocity.save'
					filename2 = 'DATA/proc0000' + str(iproc) + '_model_velocity.dat_input'
				else:
					filename1 = 'DATA/proc000' + str(iproc) + '_model_velocity.save'
					filename2 = 'DATA/proc000' + str(iproc) + '_model_velocity.dat_input'
				model = numpy.loadtxt(filename1)

