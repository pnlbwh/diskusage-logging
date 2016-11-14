#!/usr/bin/env bash
set -eu
# script=$(readlink -f $(type -p "$0"))
#dir=$(dirname $script)
indir=report/
outdir=_data/
Rscript -e "library(knitr); knit2html('$indir/report.Rmd', output=\"$outdir/report.html\")"

rm report.md
rm -r figure
