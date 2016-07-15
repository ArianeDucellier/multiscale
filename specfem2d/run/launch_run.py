"""Functions to launch the computations"""

import os, subprocess

from inversion_parameters import nsource

def create_forward():
	"""Function to modify the Par_file before forward computation
	"""

	for isource in range(0, nsource):
		namedir1 = 'Source_' + str(isource + 1)
		os.chdir(namedir1)
		f = open('DATA/Par_file', 'r')
		lines = f.readlines()
		lines[7] = 'SIMULATION_TYPE                 = 1  # 1 = forward, 3 = adjoint + kernels; 2 is purposely UNUSED (for compatibility with the numbering of our 3D codes)\n'
		lines[9] = 'SAVE_FORWARD                    = .true. # save the last frame, needed for adjoint simulation\n'
		f.close()
		f = open('DATA/Par_file', 'w')
		for item in lines:
			f.write("%s" % item)
		f.close()
		os.chdir('..')

def launch_forward():
	"""Function to launch the forward computation
	"""

	for isource in range(0, nsource):
		namedir1 = 'Source_' + str(isource + 1)
		os.chdir(namedir1)
		print '---------------------------------'
		print ' Source {0}: forward simulation'.format(isource + 1)
		print '---------------------------------'
		print 'meshing and computing'
		os.system('srun ./xmeshfem2D')
		os.system('srun ./xspecfem2D')
		os.chdir('..')

def create_adjoint():
	"""Function to modify the Par_file before adjoint computation
	"""

	for isource in range(0, nsource):
		namedir1 = 'Source_' + str(isource + 1)
		os.chdir(namedir1)
		f = open('DATA/Par_file', 'r')
		lines = f.readlines()
		lines[7] = 'SIMULATION_TYPE                 = 3  # 1 = forward, 3 = adjoint + kernels; 2 is purposely UNUSED (for compatibility with the numbering of our 3D codes)\n'
		lines[9] = 'SAVE_FORWARD                    = .false. # save the last frame, needed for adjoint simulation\n'
		f.close()
		f = open('DATA/Par_file', 'w')
		for item in lines:
			f.write("%s" % item)
		f.close()
		os.chdir('..')

def launch_adjoint():
	"""Function to launch the adjoint computation
	"""

	for isource in range(0, nsource):
		namedir1 = 'Source_' + str(isource + 1)
		os.chdir(namedir1)
		print '---------------------------------'
		print ' Source {0}: adjoint simulation'.format(isource + 1)
		print '---------------------------------'
		print 'meshing and computing'
		os.system('srun ./xmeshfem2D')
		os.system('srun ./xspecfem2D')
		os.chdir('..')

