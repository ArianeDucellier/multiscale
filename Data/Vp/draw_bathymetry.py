"""File to draw a picture of the bathymetry"""

import matplotlib, numpy, pylab
import matplotlib.pyplot as plt

filename = 'bathymetry.dat' # name of the ascii file to read

b = numpy.loadtxt(filename)
x = b[:, 0]
z = b[:, 1]

fig = plt.figure(0)
pylab.plot(x, z)
pylab.xlabel('Distance (m)')
pylab.ylabel('Height (m)')
pylab.title('Bathymetry')
pylab.savefig("bathymetry.eps")
plt.close(fig)

