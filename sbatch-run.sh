#!/bin/bash

#SBATCH --job-name=wrf-baq-1km
#SBATCH --nodes=1
#SBATCH --ntasks=72
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --account=syseng
#SBATCH --partition=syseng
#SBATCH -o slurm.out.log
#SBATCH -e slurm.err.log
#SBATCH --priority=TOP

module load autotools prun/1.3 gnu8/8.3.0 openmpi3/3.1.4 ohpc miniconda wrf/4.3

python3 $BIN_DIR/run_wrf.py "$START_DATE" "$END_DATE" -i 3 -n 8 --srun --only-real
python3 $BIN_DIR/run_wrf.py "$START_DATE" "$END_DATE" -i 3 -n 64 --srun --only-wrf --output $WRF_OUTPUT
