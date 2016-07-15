"""File to draw a picture of the P-wave velocity log"""

import matplotlib, numpy, pylab
import matplotlib.pyplot as plt

filename = 'Vp.bin' # name of the binary file to read
nx = 3820 # number of points in the x direction
nz = 1200 # number of points in the z direction
dz = 5.0 # spacing in the z direction

fp = numpy.fromfile(filename, 'f4')
vp = numpy.reshape(fp, (nx, nz))
vplog = vp[0, :]
z = pylab.arange((nz - 1) * dz, -dz, -dz)

fig = plt.figure(0)
pylab.plot(vplog, z)
pylab.xlabel('P-wave velocity (m/s)')
pylab.ylabel('Depth (m)')
pylab.title('Initial P-wave velocity log')
pylab.savefig("Vp.eps")
plt.close(fig)

