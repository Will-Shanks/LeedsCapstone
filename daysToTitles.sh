#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --partition=shas
#SBATCH --output=log-%j.out 


#daysToTitles.sh Usage: ./daysToTitles.sh <year> [<project dir>]
#  where year is the year of the manual you wish to get the titles from
#  project dir is the root of this code repo, and is optional if this script is called from said dir
date

# check if project dir was supplied
if [ $# -eq 2 ]
then
	PROJECT_DIR=$2
elif [ $# -eq 1 ]
# if it wasn't then check if it is current dir
then
	# if can find getTitles.py then we're good to go with $PWD
	if [ -f "$PWD/src/getTitles.py" ]
	then
		PROJECT_DIR=$PWD
	else
		echo "Error couldn't find $PWD/src/getTitles.py, must supply project dir"
		exit 1
	fi
else
# if no args given then wrongs, print usage
	echo "Usage: ./daysToTitles.sh <year> [<project dir>]"
	exit 1
fi

YEAR=$1

module purge
module load python/3.6.5

#probably not neccesary but leave just in case
export PYTHONPATH=$PROJECT_DIR/src:$PYTHONPATH

python3 $PROJECT_DIR/src/getTitles.py $YEAR > $PROJECT_DIR/company_names_$YEAR.txt

date
