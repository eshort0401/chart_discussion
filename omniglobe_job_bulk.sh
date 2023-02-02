#!/bin/bash
qsub -v MIN=1,MAX=24 omniglobe_job.sh
qsub -v MIN=1,MAX=24 omniglobe_wind_job.sh
for i in {24..216..24}
do
    qsub -v MIN=${i},MAX=$((i+24)) ~/chart_discussion/omniglobe_job.sh
    qsub -v MIN=${i},MAX=$((i+24)) ~/chart_discussion/omniglobe_wind_job.sh
done
