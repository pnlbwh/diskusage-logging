#!/bin/bash
SCRIPTDIR=$( cd $(dirname $0) ; pwd -P )

# copy the report to a temp directory to avoid permission denied errors
tmpdir=$(mktemp -d)

# E.g.
# mailreport.sh reckbo sylvain

datestamp=$(date +"%Y%m%d")
cp $SCRIPTDIR/_data/htmlreport/report-${datestamp}.html $tmpdir/

from=tbillah@bwh.harvard.edu
for user in $@
do
    echo "" | mailx -r $from -s "PNL disk usage report: $datestamp  " \
        -a $tmpdir/*.html \
        -- $user@bwh.harvard.edu
done

rm -r $tmpdir


