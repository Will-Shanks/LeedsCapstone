#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --partition=shas
#SBATCH --output=sample-%j.out

script1=/projects/$USER/LeedsCapstone/tasks/task1/Task1b_Zijun_Liu.py
script2=/projects/$USER/LeedsCapstone/tasks/task1/task1b.py
dayDIR=/scratch/summit/diga9728/Moodys/Industrials/OCRrun1930/
outFile=/projects/$USER/output.txt

rm -f $outFile

Y=1930
b=70

#NOTE: need to install numpy and pandas
#ex: pip3 install numpy --user

module purge
module load python/3.6.5

#YYYY0mmm-iiiiibb.day
#images 0001-0010 in m=000

echo "== This is the scripting step! ==" >> $outFile
for dir in {000..010}; do
  for f in $(ls $dayDIR/$dir/*$b.day); do
    echo $f >> $outFile
    python3 $script1 $f >> $outFile
    echo""
    python3 $script2 $f >> $outFile
  done
done
echo "== End of Job ==" >> $outFile
