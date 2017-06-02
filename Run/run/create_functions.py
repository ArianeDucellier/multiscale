"""Functions to prepare appropriate files and directories before running the computations"""

import os
import shutil

from inversion_parameters import J, nproc, nsource

def create_dir(j):
	"""Function to create the directories for each source

	Input:
	j = scale at which we run the inversion process
	"""

	# Create directory for current scale
	namedir0 = 'Scale_' + str(j)
	if not os.path.exists(namedir0):
    		os.makedirs(namedir0)
	os.chdir(namedir0)
	for isource in range(0, nsource):
		# Create directory for current source
		namedir1 = 'Source_' + str(isource + 1)
		if not os.path.exists(namedir1):
    			os.makedirs(namedir1)
		os.chdir(namedir1)
		# Copy source file and exe files
		filename1 = '../../input_files/source.txt'
		filename2 = 'source.txt'
		shutil.copy (filename1, filename2)
		filename1 = '../../input_files/xmeshfem2D'
		filename2 = 'xmeshfem2D'
		shutil.copy (filename1, filename2)
		filename1 = '../../input_files/xspecfem2D'
		filename2 = 'xspecfem2D'
		shutil.copy (filename1, filename2)
		# Create directories
		namedir2 = 'DATA'
		if not os.path.exists(namedir2):
    			os.makedirs(namedir2)
		namedir3 = 'OUTPUT_FILES'
		if not os.path.exists(namedir3):
    			os.makedirs(namedir3)
		namedir4 = 'SEM'
		if not os.path.exists(namedir4):
    			os.makedirs(namedir4)
		# Copy input files into DATA directory
		filename1 = '../../input_files/interfaces.dat'
		filename2 = 'DATA/interfaces.dat'
		shutil.copy (filename1, filename2)
		filename1 = '../../input_files/Par_file'
		filename2 = 'DATA/Par_file'
		shutil.copy (filename1, filename2)
		filename1 = '../../input_files/SOURCE'
		filename2 = 'DATA/SOURCE'
		shutil.copy (filename1, filename2)
		# Modify file Par_file (locations of the receivers)
		f = open('DATA/Par_file', 'r')
		lines = f.readlines()
		lines[77] = 'xdeb                            = ' + str(1000 + isource * 25) + '.         # first receiver x in meters\n'
		lines[79] = 'xfin                            = ' + str(9000 + isource * 25) + '.         # last receiver x in meters (ignored if only one receiver)\n'
		f.close()
		f = open('DATA/Par_file', 'w')
		for item in lines:
			f.write("%s" % item)
		f.close()
		# Modify file SOURCE (location of the source)
		f = open('DATA/SOURCE', 'r')
		lines = f.readlines()
		lines[3] = 'xs                              = ' + str(1000 + isource * 25) + '.         # source location x in meters\n'
		f.close()
		f = open('DATA/SOURCE', 'w')
		for item in lines:
			f.write("%s" % item)
		f.close()
		os.chdir('..')
	os.chdir('..')

def copy_model(j, iiter):
	"""Function to copy the current velocity model into each of the source directories

	Input:
	j = scale at which we run the inversion process
	iiter = index of the iteration
	"""

	if iiter == 1:
		if j == J:
			# Copy initial model into source directories
			pathname = '../../input_files/proc000'
		else:
			# Copy model from the last iteration of the previous scale into source directories
			pathname = '../../output_files/scale' + str(j + 1) + '/proc000'
	else:
		# Copy model from the previous iteration into source directories
		pathname = '../iteration' + str(iiter - 1) + '/proc000'
	for isource in range(0, nsource):
		namedir1 = 'Source_' + str(isource + 1)
		os.chdir(namedir1)
		for iproc in range(0, nproc):
			if iproc < 10:
				filename1 = pathname + '00' + str(iproc) + '_model_velocity.dat_input'
				filename2 = 'DATA/proc00000' + str(iproc) + '_model_velocity.dat_input'
			elif iproc < 100:
				filename1 = pathname + '0' + str(iproc) + '_model_velocity.dat_input'
				filename2 = 'DATA/proc0000' + str(iproc) + '_model_velocity.dat_input'
			else:
				filename1 = pathname + str(iproc) + '_model_velocity.dat_input'
				filename2 = 'DATA/proc000' + str(iproc) + '_model_velocity.dat_input'
			shutil.copy (filename1, filename2)
		os.chdir('..')

