#!/usr/bin/env bash

SCRIPT=$(readlink -m $(type -p $0))
SCRIPTDIR=$(dirname $SCRIPT)
logdir=$SCRIPTDIR/_data/logdirsizes

datestamp=$(date +"%Y%m%d")
depth=3
summarydir=$SCRIPTDIR/_data/logdirsummary/$datestamp
mkdir -p $summarydir

findprefix() {
    echo $1 | sed 's,\/,_,g' | sed 's,_$,,' | sed 's,^_,,'
}
    


logfilename() {
    local dir=$1
    local depth=$2
    local prefix=$(findprefix $dir)
    local logfile=${prefix}-dirsizes-${depth}-${datestamp}.csv
    echo $logdir/$logfile
}

remote_server() {
    IFS=":" read server remotepath <<< "$1"
    if [ -n ${remotepath} ]
    then
        echo true
    else
        echo false 
    fi
    
}



# main function =======================

while read path
do     
    
    IFS=":" read server directory <<< $path

    if [ -z $directory ]
    then
        directory=$server
        remote=false
    else
        remote=true
    fi
    
    logfile=$(logfilename $directory $depth)


    for subdir in $directory $directory/home $directory/Collaborators $directory/projects
    do  
        prefix=$(findprefix $subdir)
        
        if [ "$remote" = true ]
        then
            # local directories
            $SCRIPTDIR/dir_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ssh $server "ls -d $subdir/*/"`
        else
            # remote directories
            $SCRIPTDIR/dir_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ls -d $subdir/*/`
        fi
        
        
    done             
    
    
done < $SCRIPTDIR/_config/dirs.txt



# zip the summary folder
# copy the summary to a temp directory to avoid permission denied errors
tmpdir=$(mktemp -d)
dir_bak=`pwd`
cd $tmpdir

cp -a $summarydir .
summaryzip=$datestamp.zip
zip -r $summaryzip $datestamp/



# mail the summary
from=tbillah@bwh.harvard.edu
for user in tbillah sylvain mglyons
do
    echo "" | mailx -r $from -s "Categorized spread sheet for disk usage: $datestamp  " \
        -a  $summaryzip\
        -- $user@bwh.harvard.edu
done

cd $dir_bak
rm -r $tmpdir


