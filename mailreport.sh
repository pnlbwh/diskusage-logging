#!/bin/bash
SCRIPTDIR=$( cd $(dirname $0) ; pwd -P )

# copy the report to a temp directory to avoid permission denied errors
tmpdir=$(mktemp -d)
cp $SCRIPTDIR/_data/report.html $tmpdir/report.html

# E.g.
#  mailreport.sh reckbo sylvain

DATE=$(date +"%Y%m%d")

from=tbillah@bwh.harvard.edu
for user in $@; do
    echo "" | mailx -r $from -s "PNL disk usage report: $DATE  " \
        -a $tmpdir/report.html \
        -- $user@bwh.harvard.edu
done

rm $tmpdir/report.html
rmdir $tmpdir
