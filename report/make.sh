#!/usr/bin/env bash
set -eu
script=$(readlink -f $(type -p "$0"))
dir=$(dirname $script)
Rscript -e "library(knitr); knit2html('$dir/report.Rmd', output=\"$dir/report.html\")"
