Who can we blame for using all our disk space?  Find out here.

# Config

Put each file system's target directory (the one you're interested in) in a
text file `_config/dirs.txt`, one per line. E.g.

    /rfanfs/pnl-zorro/
    erisone.partners.org:/data/pnl

# Run

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

In `report-lib/` there's an R markdown document that generates a disk usage graph and a summary
of last week's disk space changes.  Generate it by running

    makereport.sh

which saves the report as `_data/report.html`. `mailreport.sh
<partners_username1> <partners_username2> ...` emails a copy of the report to a
list of PNL users.

# Common Issues

One issue that sometimes arises is when one of the directories is inaccessible via the
network (for PNL, this happens when the cluster is unavailable). This can add some
nonsensical data to the csvs, particularly `logdf`'s output.  If it looks like the
report is missing data or incorrect in some way, check the latest csvs and make sure
they are in proper format.
