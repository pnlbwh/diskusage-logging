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
    
    # logfile with current datestamp might not exist
    # local logfile=${prefix}-dirsizes-${depth}-${datestamp}.csv
    
    # so list the logfiles and use the latest one
    IFS=' ', read -ra logfiles <<< `ls $logdir/${prefix}*${depth}*csv`
    
    echo ${logfiles[-1]}
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

    # remove trailing slash from directory name
    directory=${directory%/}

    logfile=$(logfilename $directory $depth)
    echo Using logfile $logfile

    for subdir in $directory $directory/home $directory/Collaborators $directory/projects
    do  
        prefix=$(findprefix $subdir)
        
        if [ "$remote" = true ]
        then
            # remote directories
            $SCRIPTDIR/size_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ssh $server "ls -d $subdir/*/"`

            # $SCRIPTDIR/date_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ssh $server "ls -d $subdir/*/"`
        else
            # local directories
            $SCRIPTDIR/size_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ls -d $subdir/*/`

            # $SCRIPTDIR/date_sort.py $logfile $summarydir/${prefix}-${datestamp}.csv `ls -d $subdir/*/`
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



# email the summary
domain=@partners.org
from=tbillah$domain
for user in $@
do
    echo "" | mailx -r $from -s "Categorized spread sheet for disk usage: $datestamp  " \
        -a  $summaryzip\
        -- $user$domain

#    echo "" | mailx -r $from -s "Last-access-date sorted spread sheet for disk usage: $datestamp  " \
#        -a  $summaryzip\
#        -- $user$domain

done

cd $dir_bak
rm -r $tmpdir


