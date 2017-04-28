pkgs <-c('ggplot2', 'data.table', 'xtable', 'magrittr', 'lubridate')
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
