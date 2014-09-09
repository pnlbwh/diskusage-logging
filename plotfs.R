#!/projects/schiz/software/local/bin/Rscript

library(ggplot2)

logdir <-  'logfs.dir'

files <- list.files(logdir, full.names=T)
data.list <- lapply(files, read.csv, colClasses=c(Datetime="Date"))
d <- do.call(rbind, data.list)

last_date_d <- subset(d, Datetime==max(unique(d$Datetime)))
min_date_d <- subset(d, Datetime==min(unique(d$Datetime)))

g <- ggplot(d, aes(Datetime, Usage)) + 
    geom_line(aes(color=Filesystem)) +
    scale_y_continuous(breaks=seq(0,100,by=5), labels=function(x){sprintf("%s%%",x)}) + 
    xlab("") +
    ylab("") +
    ggtitle("Filesystem Usage") +
    geom_text(data=last_date_d, aes(label=Usage, color=Filesystem),  hjust = 0.9, vjust = -0.3) +
    geom_text(data=min_date_d, aes(label=Filesystem, color=Filesystem),  hjust = 0.0, vjust = -0.3) +
    theme(legend.position="none")

ggsave(filename='plots/fs.png', width=7, height=7, plot=g, dpi=150)
