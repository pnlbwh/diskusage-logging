library(plyr,warn.conflicts = FALSE, quietly=TRUE)
library(dplyr,warn.conflicts = FALSE, quietly=TRUE)
library(xtable)

df_from_files <- function(globpattern) {
    files <- Filter(function(x) file.info(x)$size > 0, Sys.glob(globpattern))
    data.list <- lapply(files, read.csv, colClasses=c(Datetime="Date"))
    #data.list <- lapply(files, read.csv, colClasses=c(Datetime="character"))
    d <- do.call(rbind.fill, data.list) %>%
    arrange(Datetime)
}

changes <- function(df, k=1) {
    df %>%
        filter(!grepl("Trash", Directory)) %>%
        group_by(Directory) %>%
        mutate(Datetime=as.character(Datetime)) %>%
        mutate(change=(as.numeric(Size) - lag(as.numeric(Size), k))/1024/1024/1024,
                Datetime.before=lag(Datetime, k)) %>%
        ungroup() %>%
        filter(Datetime==max(df$Datetime)) %>%
        arrange(desc(change))
}

selectpretty <- function(tbl) {
    select(tbl, "Week Starting"=Datetime.before,
            "Week Ending"=Datetime,
            Directory,
            "change (G)"=change)
}

worst <- function(tbl, num=10) {
    d <- tbl %>%
        arrange(desc(change)) %>%
        filter(change > 0.1)
        head(d, num)
}

best <- function(tbl, num=10) {
    d <- tbl %>%
        arrange(change) %>%
        filter(change < -0.1)
        head(d, num)
}

printtable <- function(tbl) {
    x <- xtable(tbl %>% selectpretty())
    if(nrow(x) > 1) {
        print(x, type="html", include.rownames=FALSE)
    }
}

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

dir2glob <- function(dir) {
    if (grepl(':', dir)) {
        dir <- unlist(strsplit(dir, ':'))[2]
    }
    prefix <- gsub('/', '_', trim(dir))
    prefix <- gsub('_$', '', prefix)
    prefix <- substring(prefix, 2) # remove first '_'
    paste0('../_data/logdirsizes/', prefix, "*.csv")
}

print_period_changes <- function(dir, numentries=10, numdates=1) {
    d <- df_from_files(dir2glob(dir))
    d.changes <- changes(d,numdates)
    printtable(worst(d.changes, numentries))
    printtable(best(d.changes, numentries))
}

print_largest <-  function(dir) {
    d <- df_from_files(dir2glob(dir))
    d2 <- d %>% mutate(Datetime=as.character(Datetime)) %>%
          group_by(Datetime) %>%
          top_n(n=6,wt=Size) %>%
      filter(Datetime==max(d$Datetime)) %>%
      select(Datetime, Directory, Last.Modified, SizeG) %>%
      arrange(desc(SizeG))
    x <- xtable(d2)
    if(nrow(x) > 1) {
        print(x, type="html", include.rownames=FALSE)
    }
 }
