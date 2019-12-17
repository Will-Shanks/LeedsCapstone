#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --partition=shas
#BATCH --output=log-%j.out 

DIR='/scratch/summit/diga9728/Moodys/Industrials/OCRrun1930/' #050/OCRoutputIndustrial19300007-005670.day'

module purge
module load python/3.6.5
rm -f /home/wish9643/projects/output.txt

echo date

for i in $(grep ,1 $DIR/mastercolumns1930.csv | cut -d',' -f1 | cut -c -23); do
  file=$(find $DIR -name "OCRoutput"$i"70.day" -type f)
  echo $file":" >> /home/wish9643/projects/output.txt
  python3 /home/wish9643/projects/LeedsCapstone/tasks/task1/makeText.py $file > /scratch/summit/wish9643/tmp.txt
  python3 /home/wish9643/projects/LeedsCapstone/tasks/task1/getTitles.py /scratch/summit/wish9643/tmp.txt >> /home/wish9643/projects/output.txt

  echo "" >> /home/wish9643/projects/output.txt
done

echo date


