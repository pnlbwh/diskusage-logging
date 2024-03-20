#!/bin/bash

_finger()
{
    IFS=: read -ra parts <<< "`grep $1 /etc/group`"
    IFS=,
    for u in ${parts[3]}
    do
        grep $u: /etc/passwd >> people.txt
    done
}

rm people.txt

_finger pnl:x:10012:
_finger BWH-PNL-G:x:141743:
_finger BWH-PREDICT-G:x:155016:

