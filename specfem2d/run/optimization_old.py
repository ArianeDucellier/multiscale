"""Functions to carry out the optimization"""

import numpy, os
from scipy import interpolate

import DWT
from inversion_parameters import nsource, nrec, nt_d, nt_s, nt_ref, dt_d, dt_s, dt_ref, tstart, tend, sstart, send, rstart, rend, f, gamma

def sum_misfit(j):
	"""Function to sum the misfit from all sources

	Input:
	j = scale at which we run the inversion process
	"""

	misfit = 0.0
	for isource in range(0, nsource):
		misfit_int = compute_misfit(isource, j)

def compute_misfit(isource, j):
	"""Function to compute the misfit

	Input:
	isource = index of the source
	j = scale at which we run the inversion process
	"""

	namedir1 = 'Source_' + str(isource + 1)
	os.chdir(namedir1)

	dirname_d = '../../Data/'
	dirname_s = 'OUTPUT_FILES/'
	filename_d = 'data_shot' + str(isource + 1) + '.bin'

	t_d = numpy.arange(0.0, nt_d * dt_d, dt_d)
	t_s = numpy.arange(0.0, nt_s * dt_s, dt_s)
	t_ref = numpy.arange(0.0, nt_ref * dt_ref, dt_ref)

	fv_d = numpy.fromfile(dirname_d + filename_d, 'f4')
	v_d = numpy.reshape(fv_d, (nrec, nt_d))

	misfit = 0.0
	adj = numpy.zeros(nt_ref)
	for irec in range(rstart - 1, rend):
		d = v_d[irec, :]
		if irec + 1 < 10:
			prefix = 'AA.S000' + str(irec + 1)
		elif irec + 1 < 100:
			prefix = 'AA.S00' + str(irec + 1)
		else:
			prefix = 'AA.S0' + str(irec + 1)
#		filename_s = prefix + '.BXZ.semd'
		filename_s = prefix + '.PRE.semp'
		fv_s = numpy.loadtxt(dirname_s + filename_s)
		s = f * fv_s[:, 1]
		istart = int((tstart + irec * 25.0 * sstart) / dt_ref)
		iend = int((tend + irec * 25.0 * send) / dt_ref)
		f_d = interpolate.interp1d(t_d, d)
		f_s = interpolate.interp1d(t_s, s)
		d_inter = f_d(t_ref)
		s_inter = f_s(t_ref)
		(d_WT, NA_d) = DWT.WT(d_inter, nt_ref, j)
		(s_WT, NA_s) = DWT.WT(s_inter, nt_ref, j)
		for it in range(0, nt_ref + 1):
			if it >= istart and it <= iend:			
				misfit += 0.5 * numpy.power(s_WT[it] - d_WT[it], 2.0)
				adj[it] = s_WT[it] - d_WT[it]
		f_a = interpolate.interp1d(t_ref, adj)
		adj_int = f_a(t_s)
#		filename_x = 'SEM/' + prefix + '.BXX.adj'
#		filename_y = 'SEM/' + prefix + '.BXY.adj'
#		filename_z = 'SEM/' + prefix + '.BXZ.adj'
#		filename_p = 'SEM/' + prefix + '.PRE.adj'
		filename_p = 'SEM/' + prefix + '.POT.adj'
#		source_x = numpy.ndarray((nt_s, 2))
#		source_y = numpy.ndarray((nt_s, 2))
#		source_z = numpy.ndarray((nt_s, 2))
		source_p = numpy.ndarray((nt_s, 2))
#		source_x[:, 0] = t_s
#		source_y[:, 0] = t_s
#		source_z[:, 0] = t_s
		source_p[:, 0] = t_s
#		source_x[:, 1] = adj_int
#		source_y[:, 1] = numpy.zeros(nt_s)
#		source_z[:, 1] = numpy.zeros(nt_s)
		source_p[:, 1] = adj_int
#		numpy.savetxt(filename_x, source_x)
#		numpy.savetxt(filename_y, source_y)
#		numpy.savetxt(filename_z, source_z)
		numpy.savetxt(filename_p, source_p)
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
				

