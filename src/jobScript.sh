#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --partition=shas
#SBATCH --output=sample-%j.out

#python scrypt to run in home directory on summit
script=/home/$USER/superday/draw5.py 

#location of the ocr output files
dayDIR=/scratch/summit/diga9728/Moodys/Industrials/OCRrun1930 


#NOTE: need to install numpy and pandas
#ex: pip3 install numpy --user
module purge
module load python/3.6.5

for i in {00..99}; do
	for j in {01..99}; do 
		python3 draw5.py $dayDIR/*/OCRoutputIndustrial193000$i-00$j*.day
	done
done


