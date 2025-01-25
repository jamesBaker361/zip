#!/bin/bash

#SBATCH --partition=main       # Partition (job queue)

#SBATCH --requeue                 # Return job to the queue if preempted

#SBATCH --nodes=1                 # Number of nodes you require

#SBATCH --ntasks=1               # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1         # Cores per task (>1 if multithread tasks)

#SBATCH --mem=64000                # Real memory (RAM) required (MB)

#SBATCH --time=3-00:00:00           # Total run time limit (D-HH:MM:SS)

#SBATCH --output=slurm/generic/%j.out  # STDOUT output file

#SBATCH --error=slurm/generic/%j.err   # STDERR output file (optional)

day=$(date +'%m/%d/%Y %R')
echo "main" ${day} $SLURM_JOBID "node_list" $SLURM_NODELIST $@  "\n" >> jobs.txt
module purge
eval "$(conda shell.bash hook)"
conda activate zip
export TRANSFORMERS_CACHE="/scratch/jlb638/trans_cache"
export HF_HOME="/scratch/jlb638/trans_cache"
export HF_HUB_CACHE="/scratch/jlb638/trans_cache"
export TORCH_CACHE="/scratch/jlb638/torch_hub_cache"
export WANDB_DIR="/scratch/jlb638/wandb"
export WANDB_CACHE_DIR="/scratch/jlb638/wandb_cache"
export HPS_ROOT="/scratch/jlb638/hps-cache"
export IMAGE_REWARD_PATH="/scratch/jlb638/reward-blob"
export IMAGE_REWARD_CONFIG="/scratch/jlb638/ImageReward/med_config.json"
srun python3 $@
conda deactivate