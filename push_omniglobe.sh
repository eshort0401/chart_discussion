#!/bin/bash
export PATH=$PATH:/usr/bin
export SSH_AUTH_SOCK=/run/user/1512441557/keyring/ssh
export SSH_PRIVATE_KEY=/home/student.unimelb.edu.au/shorte1/.ssh/laptop_key
export HOME=/home/student.unimelb.edu.au/shorte1
BASE_DIR=/home/student.unimelb.edu.au/shorte1/Documents/chart_discussion
GADI_DIR=/g/data/w40/esh563/chart_discussion_figs
echo "Pushing data to omniglobe at $(date)" >> ${BASE_DIR}/push_log.txt
/usr/bin/rsync -vr esh563@gadi.nci.org.au:${GADI_DIR}/ACCESS_G ${BASE_DIR}/  >> ${BASE_DIR}/push_log.txt
/usr/bin/rsync -vr esh563@gadi.nci.org.au:${GADI_DIR}/ACCESS_G_wind /${BASE_DIR}/  >> ${BASE_DIR}/push_log.txt
/usr/bin/sshpass -f ${BASE_DIR}/omniglobe_pass.txt /usr/bin/scp ${BASE_DIR}/ACCESS_G/mslp_*.png omniglobe:C:/OmniGlobe/Content/ACCESS_G_mslp/  >> ${BASE_DIR}/push_log.txt
/usr/bin/sshpass -f ${BASE_DIR}/omniglobe_pass.txt /usr/bin/scp ${BASE_DIR}/ACCESS_G_wind/wind_*.png omniglobe:C:/OmniGlobe/Content/ACCESS_G_wind/  >> ${BASE_DIR}/push_log.txt
