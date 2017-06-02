# run

This repository contains the following files:
- Several Python files to run the inversion analysis:
    - create_functions.py
    - DWT.py
    - launch_run.py
    - optimization_old.py (old version, no longer necessary)
    - optimization.py
    - preprocess.py
    - process_test.py
- Several Python files that contains parameters for the inversion:
    - inversion_parameters.py
    - user_parameters.py
- run.py: Python file that you need to lauch to start the inversion analysis
- submit.slurm: File to submit job on Tigress

It contains the following directories:
- input_files: Input files for SPECFEM2D
- WT_basis: Functions for Daubechies wavelet at scales 1 to 12
