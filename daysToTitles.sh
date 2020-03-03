#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --partition=shas
#SBATCH --output=log-%j.out 

date

# update this var to where you cloned the repo to
PROJECT_DIR='/home/'$USER'/projects/LeedsCapstone'

module purge
module load python/3.6.5
rm -f $PROJECT_DIR/output.txt

export PYTHONPATH=$PROJECT_DIR/src:$PYTHONPATH

python3 $PROJECT_DIR/src/getTitles.py 1930 # >> $PROJECT_DIR/output.txt

date
