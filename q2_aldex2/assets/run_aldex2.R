#!/usr/bin/env Rscript

# load arguments ---------------------------------------------------------
cat(R.version$version.string, "\n")

args <- commandArgs(TRUE)
inp.abundances.path <- args[[1]]
inp.metadata.path <- args[[2]]
condition <- args[[3]]
mc.samples <- as.integer(args[[4]])
test <- args[[5]]
denom <- args[[6]]
output <- args[[7]]

# load data ---------------------------------------------------------------
map <- read.delim(inp.metadata.path, check.names=FALSE, row.names=1)
otu <- read.delim(inp.abundances.path, check.names=FALSE, row.names=1)

# load libraries ----------------------------------------------------------
suppressWarnings(library(ALDEx2))

# analysis ----------------------------------------------------------------

fit <- aldex(t(otu), as.character(map[[condition]]),
	     denom=denom, test=test, mc.samples=mc.samples)
sfit <- as.data.frame(fit)
write.csv(sfit, file=output)
