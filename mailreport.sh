#!/bin/bash
SCRIPTDIR=$( cd $(dirname $0) ; pwd -P )

# E.g.
#  mailreport.sh reckbo sylvain

from=reckbo@bwh.harvard.edu
for user in $@; do
    echo "" | mailx -r $from -s "disk usage report" \
        -a $SCRIPTDIR/_data/report.html \
        -- $user@bwh.harvard.edu
done
