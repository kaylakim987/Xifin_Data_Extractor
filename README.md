# Xifin Data Extractor

Extract data from Xifin PDFs

## Description

The following code converts Xifin PDFs to Markdown format. 
Code for data extraction will be added eventually.

* This project was built to operate in a SLURM environment but if desired
the Python code can be run as a standalone file.

## Getting Started

### Dependencies

Install the required packages:
```bash
pip install docling
```

OR 

```bash
pip install -r requirements.txt
```

### Python Version
This project requires Python 3.12 or higher. 

### Installing 
Clone the repository:

```bash
git clone https://github.com/kaylakim987/Xifin_Data_Extractor.git

# Navigate to the source code
cd Xifin_Data_Extractor 
cd src
```

Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Executing the Program

When executing the program in a SLURM environment 
run the following Bash script.

```bash
sbatch convert.sh
```

Notable variables in convert.sh include: 

| Variable       | Meaning |
|----------------|---------|
| `cpus-per-task` | The number of CPUs must be a multiple of 4 to account for Docling's default usage of 4 CPUs to process each PDF file. |
| `array` | The number of tasks to divide the workload amongst. Example: `array=0-3` will divide the files among 4 different tasks. |

Adjust these variables according to user needs. 

* EX. When working with a larger number of PDF files it may be beneficial
to increase the length of the array. Each task will be assigned a more
reasonable number of PDFs to process.
