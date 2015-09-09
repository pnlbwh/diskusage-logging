#!/bin/bash

# E.g.
#  mailreport.sh reckbo sylvain

dir=/projects/schiz/log/report
from=reckbo@bwh.harvard.edu
for user in $@; do
    echo "" | mailx -r $from -s "disk usage report" \
        -a $dir/report.html \
        -- $user@bwh.harvard.edu
done
