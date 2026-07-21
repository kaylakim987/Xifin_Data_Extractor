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

mkdir -p logs

# Directory containing input
BASE_DIR="/mnt/testenv/requisitions/Xifin_Data_Extractor/pdf"
OUTPUT="/mnt/testenv/requisitions/Xifin_Data_Extractor/md"

# List of all PDF paths to process
pdfs=()

while read -r pdf; do
  # Path to md
  relative_path="${pdf#$BASE_DIR/}"
  md_file="$OUTPUT/${relative_path%.pdf}.md"

  if [[ ! -f "$md_file" ]]; then
    pdfs+=("$pdf")
  fi
done < <(find "$BASE_DIR" -type f -name "*.pdf" | sort)

# Check if no PDFs need to be processed
if [ ${#pdfs[@]} -eq 0 ]; then
    echo "No PDFs need processing"
    exit 0
fi

# Assign files to each task
assigned_files=()

for ((i=$SLURM_ARRAY_TASK_ID; i<${#pdfs[@]}; i+=$SLURM_ARRAY_TASK_COUNT)); do
  assigned_files+=("${pdfs[$i]}")
done

# Debug information
echo "========================================"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "Array Task ID: $SLURM_ARRAY_TASK_ID"
echo "Total PDFs needing processing: ${#pdfs[@]}"
echo "PDFs assigned to this task: ${#assigned_files[@]}"
echo "========================================"

for ((j=0; j<${#assigned_files[@]}; j++)); do
    echo "Processing $((j+1))/${#assigned_files[@]}:"
    echo "  ${assigned_files[$j]}"
done

echo "========================================"

# Run python code for each task
python3 convert_to_md.py \
  -f "${assigned_files[@]}" \
  -np $((SLURM_CPUS_PER_TASK / 4)) \
  --input_root $BASE_DIR \
  --output_root /mnt/testenv/requisitions/Xifin_Data_Extractor/md
