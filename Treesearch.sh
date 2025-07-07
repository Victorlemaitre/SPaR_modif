#!/bin/bash
#SBATCH --job-name=TravailGPU # name of job
#SBATCH --output=TravailGPU%j.out # output file (%j = job ID)
#SBATCH --error=TravailGPU%j.err # error file (%j = job ID)
#SBATCH --constraint=a100 # reserve 80 GB A100 GPUs
#SBATCH --nodes=1 # reserve 2 nodes
#SBATCH --ntasks=16 # reserve 16 tasks (or processes)
#SBATCH --gres=gpu:1 # reserve 8 GPUs per node
#SBATCH --cpus-per-task=8 # reserve 8 CPUs per task (and associated memory)
#SBATCH --time=00:05:00 # maximum allocation time "(HH:MM:SS)"
#SBATCH --hint=nomultithread # deactivate hyperthreading
#SBATCH --account=xyz@a100 # A100 accounting


module purge # purge modules inherited by default
conda deactivate # deactivate environments inherited by default

module load arch/a100 # select modules compiled for A100
module load pytorch-gpu/py3/2.3.0 # load modules
module load vllm/0.5.4

set -x # activate echo of


sleep(30)
echo "test"

