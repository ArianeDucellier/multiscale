# Multiscale velocity inversion with SPECFEM2D
import numpy, os

from create_functions import *
from DWT import *
from launch_run import *
from optimization import *
from preprocess import *

from inversion_parameters import nsource

# ---------------------------------------------------------------
# Step 1 - Define a wavelet and the maximal decomposition scale J
# ---------------------------------------------------------------
from inversion_parameters import J

# Create input files and directories
j = J
#create_dir(j)

# OR Full loop:
#print '----- Multiscale velocity inversion -----'
#for j in range(0, J + 1):
#	print("Create directories for scale {}".format(j))
#	create_dir(j)

# --------------------------------------------------------------
# Step 2 - Start with j = J (or j = j - 1 if coming from step 4)
# --------------------------------------------------------------
j = J
namedir0 = 'Scale_' + str(j)
os.chdir(namedir0)

# OR Full loop:
#j = J
#while j >= 0:
#	namedir0 = 'Scale_' + str(j)
#	os.chdir(namedir0)
#	print("Begin inversion at scale {}".format(j))

# -------------------------------------------------------
# Step 3 - Carry out a full waveform inversion at scale j
# -------------------------------------------------------

iiter = 0	
iiter += 1

# OR Full loop:
#iiter = 0
#while iiter < 10: # What is the good criterion here?
#	iiter += 1

# ---------------------------------------------------------------------------------------------------
# Step a - Compute forward simulation with the current model with the spectral element code SPECFEM2D
# ---------------------------------------------------------------------------------------------------
#copy_model(j, iiter)
#create_forward()
#launch_forward()

misfit = numpy.zeros(nsource)

for isource in range(0, nsource):
	# --------------------------------------------------------------------------------------------------------
	# Step b - Apply wavelet transform to the data obtained from the forward simulations and to the synthetics
	# --------------------------------------------------------------------------------------------------------
#	compute_DWT(isource, j)
	# Preprocessing of the signal
#	process(isource, j)
	# ------------------------------------------------------------------------------------------------------------------------------------------------
	# Step c - Compute the difference between the data obtained from the forward simulations and the synthetics for the time window chosen for scale j
	# ------------------------------------------------------------------------------------------------------------------------------------------------
	misfit[isource] = time_difference(isource, j)

#print("Misfit at iteration {}: {}".format(iiter, numpy.sum(misfit)))

#old
#misfit = sum_misfit(j)

# -----------------------------------------------------------------------------------------------------------------------
# Step d - Carry out an adjoint wavefield simulation with the spectral element code to compute the gradient of the misfit
# -----------------------------------------------------------------------------------------------------------------------
#create_adjoint()
#launch_adjoint()

# Step e - Choose a search direction by conjugate gradient

# Step f - Obtain the scalar step size that minimizes the misfit

# Create directory for the new model at the end of the current iteration
#namedir1 = 'iteration_' + str(iiter)
#if not os.path.exists(namedir1):
#	os.makedirs(namedir1)

# ----------------------------------------------
# Step g - Update the model and return to step a
# ----------------------------------------------

# ---------------------------------------------------------------
# Step 4 - When the previous loop has converged, return to step 2
# ---------------------------------------------------------------

# OR Full loop:
#	os.chdir('..')
#	print("End of inversion at scale {}".format(j))
#	j = j - 1

# --------------------------------------------------
# Step 5 - Continue until convergence at scale j = 0
# --------------------------------------------------

# OR Full loop:
#print '----- END -----'

