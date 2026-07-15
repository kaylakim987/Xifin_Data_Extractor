#!/bin/bash

#SBATCH --job-name=convert_to_md
#SBATCH --partition=gtc2-slurm
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --array=0-49
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# COMMAND TO RUN: sbatch convert.sh

# Move to directory containing script
cd /mnt/testenv/requisitions/Xifin_Data_Extractor/src

# Directory containing input
BASE_DIR="/mnt/testenv/requisitions/Xifin_Data_Extractor/pdf"

# List of all PDF paths to process
pdfs=()

while read -r pdf; do
  pdfs+=("$pdf")
done < <(find "$BASE_DIR" -type f -name "*.pdf" | sort)

# Assign files to each task
assigned_files=()

for ((i=$SLURM_ARRAY_TASK_ID; i<${#pdfs[@]}; i+=$SLURM_ARRAY_TASK_COUNT)); do
  assigned_files+=("${pdfs[$i]}")
done

# Run python code for each task
python3 convert_to_md.py \
  -f "${assigned_files[@]}" \
  -np $((SLURM_CPUS_PER_TASK / 4)) \
  --input_root BASE_DIR \
  --output_root /mnt/testenv/requisitions/Xifin_Data_Extractor/md
