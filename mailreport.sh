#!/bin/bash
SCRIPTDIR=$( cd $(dirname $0) ; pwd -P )

# copy the report to a temp directory to avoid permission denied errors
tmpdir=$(mktemp -d)

# E.g.
# mailreport.sh reckbo sylvain

# obtain prefix
for s in $(cat $SCRIPTDIR/_config/dirs.txt)
do
    IFS='/' read -ra parts <<< "$s"
    prefix=${parts[1]}
    break
done

datestamp=$(date +"%Y%m%d")
cp $SCRIPTDIR/_data/htmlreport/report-${prefix}-${datestamp}.html $tmpdir/

domain=@mgb.org
from=tbillah$domain
for user in $@
do
    echo "" | mailx -r $from -s "/${prefix}/ disk usage report: $datestamp  " \
        -a $tmpdir/*.html \
        -- $user$domain
done

rm -r $tmpdir


