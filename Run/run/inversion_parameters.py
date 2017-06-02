"""Parameters used during the inversion process"""

# Number of processors
nproc = 256

# Maximum decomposition scale
J = 9

# Properties to invert
Rho = True
Vp = True
Vs = True

# Number of sources
nsource = 2

# Number of receivers
nrec = 321

# Number of time steps
nt_d = 2001       # for the data
nt_s = 16001      # for the synthetics
nt_ref = 40001    # as reference signal (for DWT)

# Time step
dt_d = 0.004      # for the data
dt_s = 0.0005     # for the synthetics
dt_ref = 0.0002   # as reference signal (for DWT)

# Choice of time window for the misfit for each scale
tstart = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
tend = [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0]
sstart = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
send = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Choice of frequencies for filtering
filt_freq = [2,4,20,25]

# Choice of receivers included in the misfit
rstart = 1
rend = 321

# Factor to multiply the synthetics
f = -50.0

# Trial step lengths
gamma = [1.0, 2.0]
