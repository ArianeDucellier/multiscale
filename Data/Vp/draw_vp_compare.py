"""File to draw a picture of the P-wave velocity log"""

import matplotlib, numpy, pylab
import matplotlib.pyplot as plt

filename1 = 'input_model.dat'         # name of the ascii file to read
filename2 = 'input_model_smooth.dat'  # name of the ascii file to read
filename3 = 'input_model_smooth2.dat' # name of the ascii file to read
nx = 3820 # number of points in the x direction
nz = 1200 # number of points in the z direction

fp1 = numpy.loadtxt('../../specfem2d/specfem2d/EXAMPLES/chevron/DATA/' + filename1)
fp2 = numpy.loadtxt('../../specfem2d/specfem2d/EXAMPLES/chevron/DATA/' + filename2)
fp3 = numpy.loadtxt('../../specfem2d/specfem2d/EXAMPLES/chevron/DATA/' + filename3)
z1 = fp1[:, 1]
z2 = fp2[:, 1]
z3 = fp3[:, 1]
vp1 = fp1[:, 3]
vp2 = fp2[:, 3]
vp3 = fp3[:, 3]
zm1 = numpy.reshape(z1, (nz, nx), 'F')
zm2 = numpy.reshape(z2, (nz, nx), 'F')
zm3 = numpy.reshape(z3, (nz, nx), 'F')
vpm1 = numpy.reshape(vp1, (nz, nx), 'F')
vpm2 = numpy.reshape(vp2, (nz, nx), 'F')
vpm3 = numpy.reshape(vp3, (nz, nx), 'F')

fig = plt.figure(0)
pylab.plot(vpm1[:, 0], zm1[:, 0], 'b', label='initial')
pylab.plot(vpm2[:, 0], zm2[:, 0], 'r', label='smooth 1')
pylab.plot(vpm3[:, 0], zm3[:, 0], 'g', label='smooth 2')
pylab.legend(loc='upper right')
pylab.xlabel('P-wave velocity (m/s)')
pylab.ylabel('Depth (m)')
pylab.title('P-wave velocity log')
pylab.savefig("Vp_compare.eps")
plt.close(fig)

