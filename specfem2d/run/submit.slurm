#!/bin/bash
#SBATCH --ntasks 2     #256 mpi tasks
#SBATCH -t 00:01:00      #Time in HH:MM:SS

# Load modules
module load openmpi

#Launch job
python run.py

