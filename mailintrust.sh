#!/bin/bash

for user in $@; do
    echo "" | mailx -s 'Intrust Site Counts' -a /projects/schiz/log/intrust_site_counts_`date +"%Y%m%d"`.pdf $user@bwh.harvard.edu;
done
