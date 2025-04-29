from Bio import SeqIO
import pandas as pd
import numpy as np
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Build file of lineage defining snps")
    parser.add_argument("--cluster_file",type=Path,default="/data/pam/team230/jb71/scratch/NextStrain/rPinecone/Results/rPineCone2-1.pinecone.bootstrap.table.csv")
    parser.add_argument("--snp_csv",type=Path,default="/data/pam/team230/jb71/scratch/NextStrain/new_snp_matrix.csv")
    parser.add_argument("--output",type=Path, default="/data/pam/team230/jb71/scratch/NextStrain/lineage_defining_snps.csv")
    parser.add_argument("--pinecone_threshold",type=int,default="50",help="Pinecone threshold can be 95, 80, 50, 20, or 5. Default is 50")

    args = parser.parse_args()
   
    return args

def get_defining_snps(cluster_id, cluster_col, snp_matrix, clusters_df):
    in_cluster_raw = clusters_df[clusters_df[cluster_col] == cluster_id]["Taxa"].str.split("__").str[0]
    out_cluster_raw = clusters_df[clusters_df[cluster_col] != cluster_id]["Taxa"].str.split("__").str[0]
    
    # Keep only samples actually present in snp_matrix
    in_cluster = [s for s in in_cluster_raw if s in snp_matrix.index]
    out_cluster = [s for s in out_cluster_raw if s in snp_matrix.index]
    
    missing_samples = set(in_cluster_raw).union(set(out_cluster_raw)) - set(snp_matrix.index)

    # Warn for samples missing from snp matrix
    for missing_sample in missing_samples:
        print(f"Warning: sample '{missing_sample}' not found in SNP matrix. Skipping.")
        
    if len(in_cluster) == 0 or len(out_cluster) == 0:
        print(f"Warning: no samples left in or out of cluster {cluster_id}. Skipping cluster.")
        return pd.DataFrame()

    in_matrix = snp_matrix.loc[in_cluster]
    out_matrix = snp_matrix.loc[out_cluster]
    
    defining_positions = []
    defining_alleles = []

    for col in snp_matrix.columns:
        alleles_in = in_matrix[col].unique()
        alleles_out = out_matrix[col].unique()
        
        if len(alleles_in) == 1 and alleles_in[0] not in alleles_out:
            defining_positions.append(col)
            defining_alleles.append(alleles_in[0])
            
    
    return pd.DataFrame({
        "Cluster": cluster_id,
        "SNP_Position": defining_positions,
        "Allele": defining_alleles
    })

def cluster(clusters_df,snp_matrix,pinecone_threshold,output_file):

    cluster_col = f"pinecone_{pinecone_threshold}"
    all_clusters = clusters_df[cluster_col].unique()
    results_df = pd.concat([get_defining_snps(cl,cluster_col,snp_matrix,clusters_df) for cl in all_clusters], ignore_index=True)

    print(f"Writing output to {output_file}")
    results_df.to_csv(output_file, index=False)

def main():
    print
    args = parse_args()

    print("Loading .pinecone.bootstrap.table.csv...")
    clusters_df = pd.read_csv(args.cluster_file)

    print("Loading SNPS matrix")
    # Filter matrix to match cluster samples
    snp_matrix = pd.read_csv(args.snp_csv, index_col = 0)
    print(snp_matrix.head(n=3))

    print("Extracting defining SNPs...")
    cluster(clusters_df,snp_matrix,args.pinecone_threshold,args.output)

if __name__ == "__main__":
 main()
