Who can we blame for using all our disk space?  Find out here
(its probably ryan)

# Config

Put each file system's target directory (the one you're interested in) in a
text file `config/dirs.txt`, one per line.

# Run

    logbigfiles <dir> # finds files > 300M in `<dir>`, writes csv output to `_data/logbigfiles/`
    logdirsizes <dir> # writes directory sizes in `<dir>` (default depth 3) to `_data/logdirsizes/`
    logdirsizesall # calls `logdirsizes` for each directory in config file `config/dirs.txt`
    mydf # prints file system usage for each directory in config file `config/dirs.txt`
    logdf # writes `mydf` output to `_data/logdf/`

# Output

Each script generates a csv file when you run it, and saves it to its log directory.
`logdirsizesall` and `logdf` should be run regularly to get a revealing profile of
disk usage changes.

# Report

In `report/` there's an R markdown document that generates a disk usage graph and a summary
of last week's disk space changes.  Generate it by running

    makereport.sh

which saves the report as `_data/report.html`.
