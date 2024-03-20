#!/bin/bash

ssh -o StrictHostKeyChecking=no eristwo.partners.org "/data/predict1/diskusage-logging/manual_finger.sh"

cd /data/predict1/diskusage-logging/

/data/predict1/miniconda3/bin/python manual_finger.py

rsync -a user_name.csv pnl-x80-1.partners.org:/rfanfs/pnl-zorro/software/diskusage-logging/

