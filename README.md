Who can we blame for using all our disk space?  Find out here!
(its probably ryan)

# Config

Put each file system's target directory (the one you're interested in) in a
text file `DIRS`, one per line.

# Run

    logbigfiles <dir> # finds files > 300M in `<dir>`, writes csv output to `logbigfiles.dir/`
    logdirsizes <dir> # writes directory sizes in `<dir>` (default depth 3) to `logdirsizes.dir/`
    logdirsizesall # calls `logdirsizes` for each directory in config file `DIRS`
    mydf # prints file system usage for each directory in config file `DIRS`
    logdf # writes `mydf` output to `logdf.dir/`

# Output

Each script generates a csv file when you run it, and saves it to its log directory.
`logdirsizesall` and `logdf` should be run regularly to get a revealing profile of 
disk usage changes.

# Report

In `report/` there's an R markdown document that generates a disk usage graph and a summary
of last week's disk space changes.  Unfortuantely it can be finnicky and needs adjustments
to keep it working.  
    As an alternative, you can import all the csv's into your favorite database and run
queries from there.
