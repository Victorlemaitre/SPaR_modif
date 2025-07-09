#!/bin/bash
#SBATCH --job-name=TravailGPU # name of job
#SBATCH --output=TravailGPU%j.out # output file (%j = job ID)
#SBATCH --error=TravailGPU%j.err # error file (%j = job ID)
#SBATCH --constraint=a100 # reserve 80 GB A100 GPUs
#SBATCH --nodes=1 # reserve 2 nodes
#SBATCH --ntasks=1 # reserve 16 tasks (or processes)
#SBATCH --gres=gpu:1 # reserve 8 GPUs per node
#SBATCH --cpus-per-task=8 # reserve 8 CPUs per task (and associated memory)
#SBATCH --time=01:00:00 # maximum allocation time "(HH:MM:SS)"
#SBATCH --hint=nomultithread # deactivate hyperthreading
#SBATCH --account=mpz@a100 # A100 accounting


module purge # purge modules inherited by default
conda deactivate # deactivate environments inherited by default

module load arch/a100 # select modules compiled for A100
module load cuda/12.1.0
module load nccl/2.19.3-1-cuda
module load cudnn/9.2.0.82-cuda
module load openmpi/4.1.5-cuda
module load magma/2.7.1-cuda
module load vllm/0.5.4

set -x # activate echo of

cd src

n_gpu=1
n_input=100
n_input_judge=500
: <<'COMMENT'
bash infer.sh $n_gpu $n_input

python process_data.py "infer" $n_gpu

bash judge.sh $n_gpu $n_input_judge

python process_data.py "judge" $n_gpu

COMMENT


MODEL_PATH="/lustre/fswork/projects/rech/mpz/uip95qy/Qwen2.5-0.5B"
VLLM_PORT=8000                       # default port used by vllm
LOGFILE="vllm_server.log"
SERVER_URL="http://localhost:$VLLM_PORT/health"

echo "[INFO] Starting vLLM server..."
vllm serve "$MODEL_PATH" &

# Save the server PID to kill it later if needed
VLLM_PID=$!

# === WAIT FOR SERVER TO BE READY ===
echo "[INFO] Waiting for vLLM server to become available..."
until curl --silent --fail "$SERVER_URL" > /dev/null; do
    sleep 2
done
echo "[INFO] vLLM server is up."

# START

python tree_search.py

python process_data.py "tree" $n_gpu


# === OPTIONAL: KILL vLLM SERVER ===
echo "[INFO] Shutting down vLLM server..."
kill $VLLM_PID

echo "[INFO] All tasks completed."

