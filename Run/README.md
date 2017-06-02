# Run

This repository contains the following files:
- create_source.m: Interpolate the source function from the Chevron dataset to get the source input file for SPECFEM2D
- draw_comparison.py: Python routine to make a figure of the seismograms with different mesh grid spacings and compare with data from the Chevron dataset
- draw_wave.py: Python routine to make a figure of the seismograms and compare with data from the Chevron dataset
- draw_wavelet.py: Python routine to make a figure of the source time function in both the time and the frequency domains
- Wavelet.txt: Source function from the Chevron dataset (without the header)

This repository contains the following directories:
- DATA: Matlab routine to create the input file for SPECFEM2D and source time functions for SPECFEM2D
- run: Python routines to carry out multiscale inversion analysis
- WT: Python routines to compute DWT and make figures of the seismograms
