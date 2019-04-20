# diskusage-logging

Whom can we blame for using all our disk space?  Find out here.

Table of Contents
=================

   * [diskusage-logging](#diskusage-logging)
   * [Installation](#installation)
      * [Install <em>R</em> in Linux](#install-r-in-linux)
      * [Check installation (/usr/bin/R)](#check-installation-usrbinr)
      * [Version](#version)
      * [Prerequisite libraries](#prerequisite-libraries)
   * [Configuration](#configuration)
   * [Running](#running)
   * [Output](#output)
   * [Report](#report)
      * [Make report](#make-report)
      * [Mail report](#mail-report)
   * [cron job scheduling](#cron-job-scheduling)
   * [Issues](#issues)

Table of Contents Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Installation

## Install *R* in Linux

    sudo yum install R
    
## Check installation (`/usr/bin/R`)

    which R
    R --help
    R # should initiate R console

## Version

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

    
## Prerequisite libraries
The libraries are installed in `/usr/lib64/R/library/`


    knitr      = 1.22
    ggplot2    = 3.1.1
    xtable     = 1.8.3
    magrittr   = 1.5
    knitr      = 1.22
    bit64      = 0.9.7
    lubridate  = 1.6.0
    data.table = 1.11.5
    

* NOTE: the current version of `lubridate` and `data.table` in CRAN, requires 
a newer compiler than is available on CentOS 6. So, install an older version for 
them directly from source:

```
wget https://github.com/tidyverse/lubridate/archive/v1.6.0.tar.gz
sudo R CMD INSTALL v1.6.0.tar.gz  
  
wget https://github.com/Rdatatable/data.table/archive/1.11.4.tar.gz
sudo R CMD INSTALL 1.11.4.tar.gz
```

Another solution could be to install and activate devtoolset-3-toolchain before installing the above two.

However, rest of the prerequisites should be directly installated in R:

  > install.packages('knitr', 'ggplot2', 'xtable', 'magrittr', 'lubridate', 'bit64')


# Configuration

Put each file system's target directory (the one you're interested in) in a
text file `_config/dirs.txt`, one per line. E.g.

    /rfanfs/pnl-zorro/
    user@erisone.partners.org:/data/pnl

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

## Make report

In `report-lib/` there's an R markdown document that generates a disk usage graph and a summary
of last week's disk space changes.  Generate it by running

    makereport.sh

which saves the report as `_data/report.html`. 

## Mail report

`mailreport.sh <partners_username1> <partners_username2> ...` emails a copy of the report to a
list of PNL users.

# cron job scheduling

In order to monitor diskusage every week, the above procedure is run automatically 
every week through `cron` job scheduling. Schedule the following in `root`'s `cron`:

    $ sudo crontab -e
    00 00 * * 6 /rfanfs/pnl-zorro/software/cron/weekly.sh
    01 03 * * * /rfanfs/pnl-zorro/software/cron/daily.sh
    

# Issues

One issue that sometimes arises is when one of the directories is inaccessible via the
network (for PNL, this happens when the cluster is unavailable). This can add some
nonsensical data to the csvs, particularly `logdf`'s output.  If it looks like the
report is missing data or incorrect in some way, check the latest csvs and make sure
they are in proper format.
