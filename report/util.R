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

changes <- function(df) {
    df %>%
        filter(!grepl("Trash", Directory)) %>%
        group_by(Directory) %>%
        mutate(Datetime=as.character(Datetime)) %>%
        mutate(change=(Size - lag(Size))/1024/1024/1024,
                Datetime.before=lag(Datetime)) %>%
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

worst <- function(tbl) {
    d <- tbl %>%
        arrange(desc(change)) %>%
        filter(change > 0.1)
        head(d, 10)
}

best <- function(tbl) {
    d <- tbl %>%
        arrange(change) %>%
        filter(change < -0.1)
        head(d, 10)
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
    prefix <- substring(prefix, 2) # remove first '_'
    paste0('../logdirsizes.dir/', prefix, "*.csv")
}

print_week_changes <- function(dir) {
    d <- df_from_files(dir2glob(dir))
    d.changes <- changes(d)
    printtable(worst(d.changes))
    printtable(best(d.changes))
}
