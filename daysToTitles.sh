#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --partition=shas
#SBATCH --output=log-%j.out 

date


# First argument is the year you want to scrape for
y=$1
# second argument takes path to directory one level up from where source code is stored(e.g. /home/kevin/projects where code is in /home/kevin/projects/code)
PROJECT_DIR=$2

if [ $# != 2 ]
then
	echo 'Usage: daysToTitles.sh <year> <path to source code directory (one level up)>'
	exit
fi


module purge
module load python/3.6.5
rm -f $PROJECT_DIR/output.txt

export PYTHONPATH=$PROJECT_DIR/src:$PYTHONPATH

python3 $PROJECT_DIR/code/getTitles.py $y >> $PROJECT_DIR/company_names_$y.txt

date
