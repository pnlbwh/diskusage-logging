#!/projects/schiz/software/local/bin/Rscript

library(ggplot2)

logdir <-  'logdirsizes.dir'
pattern <- 'projects_schiz-dirsizes-1-.*.csv'

files <- list.files(logdir, pattern=pattern, full.names=T)
data.list <- lapply(files, read.csv, colClasses=c(Datetime="Date"))
d <- do.call(rbind, data.list)

last_date_d <- subset(d, Datetime==max(d$Datetime))
top_5 <- head(last_date_d[with(last_date_d, order(-Size)), ], 5)
top_5_d <- subset(d, Directory %in% top_5$Directory)

g <- ggplot(top_5_d, aes(Datetime, Size)) + 
    geom_line(aes(color=Directory)) +
    scale_y_continuous(labels=function(x){sprintf("%.fG",x/1024/1024/1024)}) + 
    xlab("") +
    ylab("") +
    ggtitle("/projects/schiz") 

ggsave(filename='plots/schiz.png', width=7, height=7, plot=g, dpi=150)
