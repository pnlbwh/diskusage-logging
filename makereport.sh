#!/usr/bin/env bash
set -eu
SCRIPT=$(readlink -m $(type -p $0))
SCRIPTDIR=$(dirname $SCRIPT)
indir=$SCRIPTDIR/report-lib/
outdir=$SCRIPTDIR/_data/
Rscript -e "library(knitr); knit2html('$indir/report.Rmd', output=\"$outdir/report.html\"); warnings()"

#rm report.md
#rm -r figure
