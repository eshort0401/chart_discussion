#!/bin/bash
export PATH=$PATH:/usr/bin
export SSH_AUTH_SOCK=/run/user/1512441557/keyring/ssh
export SSH_PRIVATE_KEY=/home/student.unimelb.edu.au/shorte1/.ssh/laptop_key
export HOME=/home/student.unimelb.edu.au/shorte1
echo "Launching GADI omniglobe jobs at $(date)"
/usr/bin/ssh esh563@gadi.nci.org.au -t "cd chart_discussion; rm ./omniglobe*job.sh.{e,o}*; sh ./omniglobe_job_bulk.sh"
#/usr/bin/ssh esh563@gadi.nci.org.au -t "/bin/echo 'test' > /home/563/esh563/text.txt"
