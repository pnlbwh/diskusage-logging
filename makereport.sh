#!/usr/bin/env bash
set -eu
SCRIPT=$(readlink -m $(type -p $0))
SCRIPTDIR=$(dirname $SCRIPT)
indir=$SCRIPTDIR/report-lib/
outdir=$SCRIPTDIR/_data/htmlreport
datestamp=$(date +"%Y%m%d")

# change working directory to avoid permission denied errors
cd $SCRIPTDIR
Rscript -e "library(knitr); knit2html('$indir/report.Rmd', output=\"$outdir/report-${datestamp}.html\"); warnings()"


