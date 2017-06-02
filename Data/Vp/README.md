# Vp

This repository contains the following files:
- bathymetry.dat: Two colums (x and z(x)). Sea floor elevation computed with create_model.m from the P-wave velocity file from the Chevron dataset
- create_model.m: Create bathymetry file and input model for SPECFEM2D from the P-wave velocity file from the Chevron dataset
- create_model_smooth.m: Same as create_model.m, but smoothes the velocity contrast around the low velocity layer
- draw_bathymetry.py: Python routine to make a figure of the bathymetry
- draw_vp_compare.py: Python routine to make a figure of the 1D P-wave velocity models (from the input files for SPECFEM2D)
- draw_vp.py: Python routine to make a figure of the 1D P-wave velocity model (from the P-wave velocity file from the Chevron dataset)
- figure_geometry: GMT routine to make a figure of the geometry of the problem
- figure_model: GMT routine to make a figure of the geometry of the first numerical simulation
- sources.data: Two columns (x and z). Coordinates of the 1600 sources in the Chevron dataset
- stations.dat: Two columns (x and z). Coordinates of the 321 receivers in the Chevron dataset, corresponding to the source located at 11 km from the left boundary of the model
