#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --partition=shas
#SBATCH --output=log-%j.out 

DAY_DIR='/scratch/summit/diga9728/Moodys/Industrials/OCRrun1930/' #050/OCRoutputIndustrial19300007-005670.day'

# update this var to where you cloned the repo to
PROJECT_DIR='/home/'$USER'/projects/LeedsCapstone'

module purge
module load python/3.6.5
rm -f $PROJECT_DIR/output.txt

echo date

for i in $(grep ,1 $DAY_DIR/mastercolumns1930.csv | cut -d',' -f1 | cut -c -23); do
  file=$(find $DAY_DIR -name "OCRoutput"$i"70.day" -type f)
  echo $file":" >> $PROJECT_DIR/output.txt
  python3 $PROJECT_DIR/src/getTitles.py $file >> $PROJECT_DIR/output.txt

  echo "" >> /home/wish9643/projects/output.txt
done

echo date
