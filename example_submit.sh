#!/bin/bash -l
# Standard output and error:
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
# Initial working directory:
# Job Name:
#SBATCH -J test{jobid}
#SBATCH -D {wd} #DO NOT CHANGE THIS LINE
# Queue (Partition):
#SBATCH --partition=gpu

# Number of nodes and MPI tasks per node:
#SBATCH --nodes=1
#SBATCH --ntasks={gpus}
#SBATCH --cpus-per-task=18


# Request say 32 GB of main Memory per node in Units of MB:
#SBATCH --mem=32000

# GPU stuff
#SBATCH --constraint="gpu"
#SBATCH --gres=gpu:{gpus}

# Wall clock limit:
#SBATCH --time=00:05:00

# Run the program:
# For pinning threads correctly:
export OMP_PLACES=cores
export SLURM_HINT=multithread
export GMX_ENABLE_DIRECT_GPU_COMM=1
export GMX_GPU_PME_DECOMPOSITION=1

module load gromacs/2023.3

srun -n {gpus} gmx_mpi mdrun -noconfout -s ../start.tpr -maxh 0.083 -pin on -bonded {bonded} -nb {nb} -pme {pme} -ntomp {ntomp} -deffnm md
