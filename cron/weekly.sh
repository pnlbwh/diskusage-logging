#!/bin/bash

# log data
/rfanfs/pnl-zorro/software/diskusage-logging/logdirsizesall && \

# make report
/rfanfs/pnl-zorro/software/diskusage-logging/makereport.sh

recipients="yrathi tbillah ahaidar"

# mail report
/rfanfs/pnl-zorro/software/diskusage-logging/mailreport.sh $recipients

# generate and mail categorized report
export PATH=/rfanfs/pnl-zorro/software/pnlpipe3/miniconda3/envs/pnlpipe3/bin/:$PATH
/rfanfs/pnl-zorro/software/diskusage-logging/generatesummary.sh $recipients

