#!/usr/bin/env bash

Rscript -e "pkgs <-c('ggplot2', 'data.table', 'xtable', 'magrittr', 'lubridate', 'bit64', 'knitr');for(p in pkgs) install.packages(p); warnings()"
