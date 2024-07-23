# diskusage-logging

Whom can we blame for using all our disk space?  Find out here.

Developed by Ryan Eckbo, Tashrif Billah, and Isaiah Norton


# Install diskusage-logging and Packages
```bash
git clone https://github.com/pnlbwh/diskusage-logging.git
cd diskusage-logging
pip install -r requirements.txt
```

Current *diskusage-logging* is on the following version of Python:

    Python 3.6.10 |Anaconda, Inc.| (default, May  8 2020, 02:54:21)
    [GCC 7.3.0] on linux

Package versions:

    Jinja2==3.0.3
    matplotlib==3.3.4
    pandas==1.1.5


# Configuration

Put each file system's target directory (the one you're interested in) in a
text file `_config/dirs.txt`, one per line. E.g.

    /rfanfs/pnl-zorro/
    user@eris1n2.partners.org:/data/pnl

* NOTE: replace user with whomever has sudo access.

Modify `html-report-generator/generate_usage_report.py` to change defaults in the html report.

# Running

## Scripts
    logbigfiles <dir> # finds files > 300M in <dir>, writes csv output to _data/logbigfiles/

    logdirsizes <dir> # writes directory sizes in `<dir>` (default depth 3) to `_data/logdirsizes/`

    logdirsizesall # calls `logdirsizes` for each directory in _config file `_config/dirs.txt`

    mydf # prints file system usage for each directory in _config file `_config/dirs.txt`

    logdf # writes `mydf` output to `_data/logdf/`

## Script Output

Each script generates a csv file when you run it, and saves it to its log directory.

`logdf` should be run more frequently (~daily) to get a generalized view of total disk usage trends

`logdirsizesall` should be run less frequently (~weekly) to get a more nuanced view of disk usage of individual directories

# Report

The python file `html-report-generator/generate_usage_report.py` generates an HTML report with detailed diskusage data.

### To run this in a bash script where python/conda is not installed system-wide (i.e. when using cron):

First, allow executable:
```bash
chmod +x html-report-generator/generate_usage_report.py
```
Every time you want it to run:
```bash
export PATH=/path/to/miniconda3/envs/diskusage/bin/
html-report-generator/generate_usage_report.py
```

This saves the report as `_data/htmlreport/report-{filesystem_name}-{date}.html`.

## 2. Mail report

Email a copy of the report to a list of PNL users:

    mailreport.sh <partners_username1> <partners_username2> ...

## 3. Categorized spreadsheet

Apart from generating html summary, you can also generate a spreadsheet of size-sorted entitities.
Generate and email it by running:

    generatesummary.sh <partners_username1> <partners_username2> ...

**NOTE** To integrate recipients of [#2](#2-mail-report) and [#3](#3-categorized-spreadsheet), they can be defined via a variable:

    recipients="partners_username1 partners_username2 ..."
    mailreport.sh $recipients
    generatesummary.sh $recipients


# cron job scheduling

## 1. *cron.d* directory

In order to monitor diskusage every week, the above procedure is run automatically
every week through `cron` job scheduling. Schedule the following in `pnl_crontab` file
and place it in `/etc/cron.d/` in `root`'s `cron`:

    # minute (0-59),
    #    hour (0-23),
    #       day of the month (1-31),
    #          month of the year (1-12),
    #             day of the week (0-6, 0=Sunday),
    #               user
    MAILTO=tbillah@bwh.harvard.edu
    00 02 * * 6 tb571 /rfanfs/pnl-zorro/software/cron/weekly.sh
    01 03 * * * tb571 /rfanfs/pnl-zorro/software/cron/daily.sh

`MAILTO` sends all the output of `cron` job to the specified email address. However, `mail` should be
set up and functional.

## 2. User crontab

Also, the above job can be put under a specific user's crontab:

    crontab -e

However, both the above may experience permission issue of accessing some files
whose size we are trying to calculate. In that case, the job can be run with
administrative privilege:

    sudo crontab -e


# Issues

One issue that sometimes arises is when one of the directories is inaccessible via the
network (for PNL, this happens when the cluster is unavailable). This can add some
nonsensical data to the csvs, particularly `logdf`'s output.  If it looks like the
report is missing data or incorrect in some way, check the latest csvs and make sure
they are in proper format.
