#!/bin/bash
qsub -v MIN=1,MAX=24 omniglobe_job.sh
for i in {24..216..24}
do
    qsub -v MIN=${i},MAX=$((i+24)) omniglobe_job.sh
done
