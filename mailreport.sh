#!/bin/bash
SCRIPTDIR=$( cd $(dirname $0) ; pwd -P )

# copy the report to a temp directory to avoid permission denied errors
tmpdir=$(mktemp -d)

# E.g.
# mailreport.sh reckbo sylvain

datestamp=$(date +"%Y%m%d")
cp $SCRIPTDIR/_data/htmlreport/report-${datestamp}.html $tmpdir/

domain=@partners.org
from=tbillah$domain
for user in $@
do
    echo "" | mailx -r $from -s "PNL disk usage report: $datestamp  " \
        -a $tmpdir/*.html \
        -- $user$domain
done

rm -r $tmpdir


