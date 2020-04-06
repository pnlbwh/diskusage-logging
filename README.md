# diskusage-logging

Whom can we blame for using all our disk space?  Find out here.

Developed by Ryan Eckbo, Tashrif Billah, and Isaiah Norton

Table of Contents
=================

   * [diskusage-logging](#diskusage-logging)
   * [Installation](#installation)
      * [1. Install <em>R</em> in Linux](#1-install-r-in-linux)
      * [2. Check installation (/usr/bin/R)](#2-check-installation-usrbinr)
      * [3. Version](#3-version)
      * [4. Prerequisite libraries](#4-prerequisite-libraries)
   * [Configuration](#configuration)
   * [Running](#running)
   * [Output](#output)
   * [Report](#report)
      * [1. Make report](#1-make-report)
      * [2. Mail report](#2-mail-report)
      * [3. Categorized spreadsheet](#3-categorized-spreadsheet)   
   * [cron job scheduling](#cron-job-scheduling)
      * [1. <em>cron.d</em> directory](#1-crond-directory)
      * [2. User crontab](#2-user-crontab)
   * [Issues](#issues)


Table of Contents Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Installation

## 1. Install *R* in Linux

    sudo yum install R
    
## 2. Check installation (`/usr/bin/R`)

    which R
    R --help
    R # should initiate R console

## 3. Version

Current *diskusage-logging* is on the following version of R:
    
    > version
    
    platform       x86_64-redhat-linux-gnu
    arch           x86_64
    os             linux-gnu
    system         x86_64, linux-gnu
    status
    major          3
    minor          5.2
    year           2018
    month          12
    day            20
    svn rev        75870
    language       R
    version.string R version 3.5.2 (2018-12-20)
    nickname       Eggshell Igloo

    > sessionInfo()
    
    sessionInfo()
    R version 3.5.2 (2018-12-20)
    Platform: x86_64-redhat-linux-gnu (64-bit)
    Running under: CentOS release 6.8 (Final)

    Matrix products: default
    BLAS: /usr/lib64/R/lib/libRblas.so
    LAPACK: /usr/lib64/R/lib/libRlapack.so
    ...
    ...

    
## 4. Prerequisite libraries
The following libraries are installed in `/usr/lib64/R/library/` (you can check version info
with `packageVersion("knitr")`:


    knitr      = 1.22
    ggplot2    = 3.1.1
    xtable     = 1.8.3
    magrittr   = 1.5
    knitr      = 1.22
    bit64      = 0.9.7
    lubridate  = 1.6.0
    data.table = 1.11.5
    

* NOTE: the current version of `lubridate` and `data.table` in CRAN, requires 
a newer compiler than is available on CentOS 6. If required, you can install an older version of 
them directly from source:

```
wget https://github.com/tidyverse/lubridate/archive/v1.6.0.tar.gz
sudo R CMD INSTALL v1.6.0.tar.gz  
  
wget https://github.com/Rdatatable/data.table/archive/1.11.4.tar.gz
sudo R CMD INSTALL 1.11.4.tar.gz
```

Another solution could be to install and activate devtoolset-3-toolchain before installing the above two.

However, rest of the prerequisites should be directly installated in R:

  > install.packages('knitr', 'ggplot2', 'xtable', 'magrittr', 'bit64')


# Configuration

Put each file system's target directory (the one you're interested in) in a
text file `_config/dirs.txt`, one per line. E.g.

    /rfanfs/pnl-zorro/
    user@eris1n2.partners.org:/data/pnl

* NOTE: replace user with whomever has sudo access.
    
# Running

    logbigfiles <dir> # finds files > 300M in <dir>, writes csv output to _data/logbigfiles/
    logdirsizes <dir> # writes directory sizes in `<dir>` (default depth 3) to `_data/logdirsizes/`
    logdirsizesall # calls `logdirsizes` for each directory in _config file `_config/dirs.txt`
    mydf # prints file system usage for each directory in _config file `_config/dirs.txt`
    logdf # writes `mydf` output to `_data/logdf/`

# Output

Each script generates a csv file when you run it, and saves it to its log directory.
`logdirsizesall` and `logdf` should be run regularly to get a revealing profile of
disk usage changes.

# Report

## 1. Make report

In `report-lib/` there's an R markdown document that generates a disk usage graph and a summary
of last week's disk space changes. Generate it by running:

    makereport.sh

which saves the report as `_data/htmlreport/report-*.html`. 

## 2. Mail report

Email a copy of the report to a list of PNL users:

    mailreport.sh <partners_username1> <partners_username2> ...

## 3. Categorized spreadsheet

Apart from generating html summary, you can also generate a spreadsheet of size-sorted entitities. 
Generate and email it by running:

    generatesummary.sh <partners_username1> <partners_username2> ...

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
