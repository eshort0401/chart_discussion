echo "Launching GADI omniglobe jobs at $(date)" >> /home/student.unimelb.edu.au/shorte1/Documents/chart_discussion/push_log.txt
ssh esh563@gadi.nci.org.au -t "cd chart_discussion; rm ./omniglobe*job.sh.{e,o}*; sh omniglobe_job_bulk.sh"
