## suppressWarnings(library(data.table, quietly=TRUE))
## suppressWarnings(library(ggplot2, quietly=TRUE))
## suppressWarnings(library(magrittr, quietly=TRUE))
## suppressWarnings(library(lubridate, quietly=TRUE))
## suppressWarnings(library(xtable, quietly=TRUE))

pkgs <-c('ggplot2', 'data.table', 'xtable', 'magrittr', 'lubridate', 'xtable')

for(p in pkgs) suppressPackageStartupMessages( stopifnot(
                                               library(p, quietly=TRUE,
                                                        logical.return=TRUE,
                                                        character.only=TRUE)))

printTable <- function(d) {
  tbl <- xtable(d)
  if (nrow(tbl) > 1) {
    print(tbl, type="html", include.rownames=FALSE)
  }
}


stripHost <- function(hostpath) {
  if (grepl(':', hostpath)) {
      unlist(strsplit(rootDir, ':'))[2]
  } else {
    hostpath
  }
}

changes <- function(dt, k) {

  }

##   %>%
##         filter(!grepl("Trash", Directory)) %>%
##         group_by(Directory) %>%
##         mutate(Datetime=as.character(Datetime)) %>%
##         mutate(change=(as.numeric(Size) - lag(as.numeric(Size), k))/1024/1024/1024,
##                 Datetime.before=lag(Datetime, k)) %>%
##         ungroup() %>%
##         filter(Datetime==max(df$Datetime)) %>%
##         arrange(desc(change))
