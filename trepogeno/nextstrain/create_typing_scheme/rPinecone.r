# Usage : Rscript rPinecone_on_bootstraps.R <original_pyjar_tree> <seq_alignement.fa> <bootstrap_trees_file> <SNP.threshold> <relateability.threshold> <output.prefix>
# (should be 6 positional argument inputs)

# Run rPinecone on a pyjar tree, then compare with a series of bootstrap trees to estimate confidence clusters

# Must load a conda environment containing below dependencies (e.g. `conda activate R-latest`)
# Must provide bootstraps by rerunning IQtree : `iqtree -redo -b100 -s myfasta.fa`
# Taxa IDs must all be labelled the same, e.g.:
# `while read seq seqdh ; do perl -i -pe "s/$seqdh/seq/g" mytree.rehash.bootrees ; done < seqname.rehashing.tsv`
# `while read sample seq seqds ; do perl -i -pe "s/$seqds/$sample/g" mytree.rename.bootrees ; seqname.meta.tsv`

library('rPinecone')
library('phytools')
library('reshape2')
library('adegenet')
library('parallel')


boot_pinecone <- function(tree_list, thresh, rthreshold, quiet=TRUE){

  # Some checks
  if(!class(tree_list) %in% c("list", "multiPhylo")) stop("tree_list must be a list or 'multiPhylo' of phylo objects!")
  if(!all(unlist(lapply(tree_list, function(tree) class(tree)=="phylo")))) stop("tree_list must be a list or 'multiPhylo' of phylo objects!")
  tip.lables <- tree_list[[1]]$tip.label
  if(!all(unlist(lapply(tree_list, function(tree) {
    return(all(tree$tip.label %in% tip.lables) && (length(tree$tip.label)==length(tip.lables)))}
  )))) stop("all trees must contain the same taxa!")
  if(!(is.numeric(thresh) && thresh>0)) stop("thresh must be a positive integer!")
  if(!(is.numeric(rthreshold) && rthreshold>0)) stop("rthreshold must be a positive integer!")
  
  # Detect number of cores and use parallel processing
  num_cores <- 20
  
  pine_results <- mclapply(tree_list, function(tree) {
    return(pinecone(tree, thresh, rthreshold, quiet)$table)
  }, mc.cores = num_cores)

  # Summarise into matrix
  occ_matrix <- matrix(0, ncol=length(tip.lables), nrow=length(tip.lables),
                       dimnames = list(tip.lables, tip.lables))
  
  for (clusters in pine_results){
    for(clust in unique(clusters[,2])){
      if (sum(clusters[,2]==clust) > 1){
        pw <- t(combn(clusters[clusters[,2]==clust,1], 2))
        occ_matrix[pw] <- occ_matrix[pw] + 1
        occ_matrix[pw[,c(2,1),drop=FALSE]] <- occ_matrix[pw[,c(2,1),drop=FALSE]] + 1
      }
    }
  }
  
  diag(occ_matrix) <- length(tree_list)
  return(occ_matrix)
}

args <- commandArgs(trailingOnly = TRUE) # capture command line arguments
# Put command line arguments into variables
pyjar.file <- args[1]
myfasta.file <- args[2]
bootstraps.file <- args[3]
SNP.threshold <- as.integer(args[4])
relate.threshold <- as.integer(args[5])
outprefix <- args[6]

# First run rPinecone on pyjar tree
print("Run rPinecone on pyjar tree")
pyjar.tree <- phytools::midpoint.root(read.tree(pyjar.file))
pyjar.tree.phylo <- as.phylo(pyjar.tree)

pinecone.output <- rPinecone::pinecone(pyjar.tree.phylo,SNP.threshold,relate.threshold) # standard approach used for TPA
plot.df <- as.data.frame(pinecone.output$table)

# save object to file (can be imported to R using `readRDS(external.pinecone.file)`)
saveRDS(pinecone.output, paste0(outprefix,".pinecone.rds"))


#######

# set up bootstrap analysis
bs.trees <- read.tree(bootstraps.file)
treecount <- length(bs.trees)

dna.data.file <- myfasta.file
dna.data <- adegenet::fasta2DNAbin(dna.data.file, quiet=T, chunkSize=10, snpOnly=T)


# Rescale trees to SNP distance using the builtin ACE method
print("Now working on bootstrapped trees")
print("Now rescaling all trees")
scaled.trees <- lapply(bs.trees, rPinecone::ace_scale_phylo, dna.data)
# Run rPinecone on all trees (takes a long time)
print("Running rPinecone on all bootstrap trees")
print(paste("Bootstrapping rPinecone with", treecount, "trees"))
co.occ.matrix <- boot_pinecone(scaled.trees, thresh = SNP.threshold, rthreshold = relate.threshold) 
# melt coocurrence matrix to a dataframe
print("rPinecone complete. Now running cooccurrence analysis and preparing outputs")
co.occ.df <- reshape2::melt(co.occ.matrix)

# output matrix to file (can be imported to R using `readRDS(external.pinecone.file)`)
saveRDS(co.occ.matrix, paste0(outprefix,".pinecone.bs.matrix.rds"))

# Cluster matrix
h <- hclust(as.dist(max(co.occ.matrix) - co.occ.matrix), method = "complete")
saveRDS(h, paste0(outprefix,".pinecone.bs.hclust.rds"))

# work out some thresholds based on number of bootstrap trees available (rounds up to nearest whole number)
thresh.95 <- ceiling((treecount/100)*5)
thresh.80 <- ceiling((treecount/100)*20)
thresh.50 <- ceiling((treecount/100)*50)
thresh.20 <- ceiling((treecount/100)*80)
thresh.5 <- ceiling((treecount/100)*95)

# Calculate clusters at different threshold
temp_clust <- cutree(h, h = thresh.95)
plot.df$pinecone_95 <- temp_clust[match(plot.df$Taxa, names(temp_clust))]
temp_clust <- cutree(h, h = thresh.80)
plot.df$pinecone_80 <- temp_clust[match(plot.df$Taxa, names(temp_clust))]
temp_clust <- cutree(h, h = thresh.50)
plot.df$pinecone_50 <- temp_clust[match(plot.df$Taxa, names(temp_clust))]
temp_clust <- cutree(h, h = thresh.20)
plot.df$pinecone_20 <- temp_clust[match(plot.df$Taxa, names(temp_clust))]
temp_clust <- cutree(h, h = thresh.5)
plot.df$pinecone_5 <- temp_clust[match(plot.df$Taxa, names(temp_clust))]



# output clusters to csv file
write.csv(plot.df, file=paste0(outprefix,".pinecone.bootstrap.table",".csv"), row.names=F)

#Written by Dr Matthew Beale