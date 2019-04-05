library(tidyverse)
library(ALDEx2)


args <- commandArgs(TRUE)
inp.abundances.path <- args[[1]]
inp.metadata.path <- args[[2]]
condition <- args[[3]]
mc.samples <- args[[4]]
test <- args[[5]]
denom <- args[[6]]
output <- args[[7]]


# load data ---------------------------------------------------------------

map <- read.delim(inp.metadata.path, row.names=1)
otu <- read.delim(inp.abundances.path, row.names=1)


# helper functions --------------------------------------------------------
run_aldex2 <- function(dat){
  countdata <- t(dat[,-1,drop=F])
  colnames(countdata) <- paste0("n", 1:ncol(countdata))
  aldex.fit <- aldex(countdata, as.character(dat$Condition),
  denom=denom, test=test, mc.samples=mc.samples)
  return(aldex.fit)
}

#' Summarise DE from Aldex2 models
#' @param fit output of run_aldex2
#' @param prob adjusted pvalue threshold
#' @return data.frame with columns DE, low, and high
summary_aldex2 <- function(fit){
  fit %>%
    as.data.frame() %>%
    rownames_to_column("category") %>%
    select(category, effect, wi.eBH) %>%
    mutate(padj=wi.eBH) %>%
    mutate(mean=effect) %>%
    mutate(low=NA, high=NA)
}


# analysis ----------------------------------------------------------------
d <- data.frame(Condition = map$`condition`, otu)

fit <- run_aldex2(d)
sfit <- summary_aldex2(fit)

sfit %>% write.table(file=output)
