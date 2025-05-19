#!/bin/bash

SCRIPT=$(readlink -m $(type -p $0))
SCRIPTDIR=$(dirname $SCRIPT)
logdir=$SCRIPTDIR/_data/logdirsizes

IFS=/ read -ra _rootdir <<< "$SCRIPTDIR"
rootdir=${_rootdir[1]}

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
    
    # logfile with current datestamp might not exist
    # local logfile=${prefix}-dirsizes-${depth}-${datestamp}.csv
    
    # so list the logfiles and use the latest one
    ls $logdir/${prefix}-dirsizes-${depth}*csv | tail -n 1
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

for path in $(cat $SCRIPTDIR/_config/dirs.txt)
do     
    
    IFS=":" read server directory <<< $path

    if [ -z $directory ]
    then
        directory=$server
        remote=false
    else
        remote=true
    fi

    # remove trailing slash from directory name
    directory=${directory%/}

    logfile=$(logfilename $directory $depth)
    echo Using logfile $logfile

    if [ $directory == /data/pnl ] || [ $directory == /data/pnlx ] || [ $directory == /rfanfs/pnl-zorro ]
    then
        _dirs="$directory $directory/home $directory/Collaborators $directory/projects"
    elif [ $directory == /data/predict1 ]
    then
        _dirs="$directory $directory/data_from_nda $directory/data_from_nda_dev $directory/home"
    fi

    for subdir in $_dirs
    do  
        prefix=$(findprefix $subdir)
        
        if [ "$remote" = true ]
        then
            # remote directories
            export REMOTE=1
            $SCRIPTDIR/size_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ssh $server "ls -d $subdir/*/"`

        else
            # local directories
            $SCRIPTDIR/size_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ls -d $subdir/*/`

        fi
        
        
    done             
    
    
done



# zip the summary folder
# copy the summary to a temp directory to avoid permission denied errors
tmpdir=$(mktemp -d)
dir_bak=`pwd`
cd $tmpdir

cp -a $summarydir .
summaryzip=${rootdir}_${datestamp}.zip
zip -r $summaryzip $datestamp/


# email the summary
domain=@mgb.org
from=tbillah$domain
for user in $@
do
    echo "" | mailx -r $from -s "/$rootdir/ disk usage spreadsheets $datestamp" \
        -a $summaryzip\
        -- $user$domain

done

cd $dir_bak
rm -r $tmpdir


