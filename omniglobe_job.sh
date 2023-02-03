#!/bin/bash
#PBS -q normal
#PBS -P w40
#PBS -l ncpus=4
#PBS -l mem=16GB
#PBS -l jobfs=64GB
#PBS -l walltime=04:00:00
#PBS -l wd
#PBS -l storage=gdata/w40+gdata/wr45+gdata/rt52+gdata/hh5+gdata/hj10+gdata/rq0

rm -rf ~/chart_discussion/omniglobe_job.sh.{e,o}*
python3 ~/chart_discussion/gen_omniglobe_fig_script.py -m $MIN -M $MAX
for ((j=$MIN; j<$MAX; j++))
do
        j_STR=$(printf "%04d" $j)
        FILE=/g/data/w40/esh563/chart_discussion_figs/ACCESS_G/mslp_${j_STR}.png
	SAVEFILE=/g/data/w40/esh563/chart_discussion_figs/mslp_${j_STR}.png
        convert $FILE -resize 4000x2000\! $SAVEFILE
	mv $SAVEFILE $FILE
done
