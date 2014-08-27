#!/projects/schiz/software/local/bin/Rscript

library(ggplot2)

logdir <-  'logfs.dir'

# Get the input csv's
files <- list.files(logdir, full.names=T)

# read the files into a list of data.frames
data.list <- lapply(files, read.csv,colClasses=c(Datetime="Date"))

# concatenate into one big data.frame
d <- do.call(rbind, data.list)

g <- ggplot(s, aes(Datetime, Usage)) + geom_line(aes(color=Filesystem))
ggsave(filename=paste(args[1], "png", sep="."), width=7, height=7, plot=g, dpi=150)
