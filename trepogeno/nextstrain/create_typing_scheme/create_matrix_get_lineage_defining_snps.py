from Bio import SeqIO
import pandas as pd
import numpy as np
import argparse
from pathlib import Path
import logging
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Build file of lineage defining snps")
    parser.add_argument("--cluster_file",type=Path)
    parser.add_argument("--output",type=Path, default="./lineage_defining_snps.csv")
    parser.add_argument("--pinecone_threshold",type=int,default=50,help="Pinecone threshold can be 95, 80, 50, 20, or 5. Default is 50")
    parser.add_argument("--vcf", type=Path, required=True)

    args = parser.parse_args()
   
    return args

def load_vcf_into_df(vcf):
    try:
        vcf_df = pd.read_csv(vcf, skiprows=46, sep="\t")
        print("VCF DataFrame:")
        print(vcf_df.head(n=2))
        return vcf_df

    except Exception as e:
        logging.error(f"Encountered error while try to read vcf file into a dataframe {e}")
        sys.exit(1)

def initialise_snp_df(vcf_df):
    samples_df = vcf_df.iloc[:, 9:]
    pos_list = vcf_df['POS'].tolist()
    samples_df_T = samples_df.T
    samples_df_T.columns = pos_list
    return samples_df_T

def create_matrix(vcf_df,output):
    snp_matrix_df = initialise_snp_df(vcf_df)
    print("Initial Matrix infered from vcf:")
    print(snp_matrix_df.head(n=2))

    #create dict for pos to ref and pos to alt
    pos_to_ref = vcf_df.set_index('POS')['REF'].to_dict()
    pos_to_alt = vcf_df.set_index('POS')['ALT'].to_dict()

    def replace_allele(value, pos):
        if pd.isna(value):  # skip if NaN
            return value
        allele_call = value.split(':')[0]
        if allele_call == '0':
            return pos_to_ref.get(pos, '_')  # if position not found
        elif allele_call == '1':
            return pos_to_alt.get(pos, '_')
        else:
            return '_'  # Unexpected value, treat as missing

    # apply replacement
    for pos in snp_matrix_df.columns:
        pos_int = int(pos)
        snp_matrix_df[pos] = snp_matrix_df[pos].apply(lambda x: replace_allele(x, pos_int))

    print("Final snp matrix:")
    print(snp_matrix_df.head(n=2))
    snp_matrix_df.to_csv(output)
    return snp_matrix_df,pos_to_alt,pos_to_ref

def get_defining_snps(cluster_id, cluster_col, snp_matrix, clusters_df,pos_to_ref,pos_to_alt):

    in_cluster_raw = clusters_df[clusters_df[cluster_col] == cluster_id]["Taxa"].str.split("__").str[0]
    out_cluster_raw = clusters_df[clusters_df[cluster_col] != cluster_id]["Taxa"].str.split("__").str[0]
    
    # Keep only samples actually present in snp_matrix (pinecone files could be made with different samples to the vcf)
    in_cluster = [s for s in in_cluster_raw if s in snp_matrix.index]
    out_cluster = [s for s in out_cluster_raw if s in snp_matrix.index]
    
    missing_samples = set(in_cluster_raw).union(set(out_cluster_raw)) - set(snp_matrix.index)

    # Warn for samples missing from snp matrix
    for missing_sample in missing_samples:
        print(f"Warning: sample '{missing_sample}' not found in SNP matrix. Skipping.")
        
    if len(in_cluster) == 0 or len(out_cluster) == 0:
        print(f"Warning: no samples left in or out of cluster {cluster_id}. Skipping cluster.") #It shouldn't happen that pinecone creates a cluster with all or none of the samples 
        return pd.DataFrame()                                                                   # but if something goes wrong this helps spot that

    in_matrix = snp_matrix.loc[in_cluster]
    out_matrix = snp_matrix.loc[out_cluster]
    
    defining_positions = []
    defining_alleles = []

    for col in snp_matrix.columns:
    alleles_in = in_matrix[col].dropna().unique()
    alleles_out = out_matrix[col].dropna().unique()

    if len(alleles_in) == 1:
        allele_in = alleles_in[0]
        if allele_in not in alleles_out:
            defining_positions.append(col)
            defining_alleles.append(allele_in)
        else:
            # Check if all in-cluster samples have REF and all out-cluster have ALT
            ref = pos_to_ref.get(int(col), "_")
            alt = pos_to_alt.get(int(col), "_")

            if (
                all(in_matrix[col] == ref) and
                all(out_matrix[col] == alt)
            ):
                defining_positions.append(col)
                defining_alleles.append(ref)

    return pd.DataFrame({
    "Cluster": cluster_id,
    "SNP_Position": [int(pos) for pos in defining_positions],
    "Allele": defining_alleles
    })

def cluster(clusters_df,snp_matrix,pinecone_threshold,output_file,pos_to_alt,pos_to_ref):

    cluster_col = f"pinecone_{pinecone_threshold}"
    all_clusters = clusters_df[cluster_col].unique()
    for cl in all_clusters:
        results_df = pd.concat([get_defining_snps(cl,cluster_col,snp_matrix,clusters_df,pos_to_ref,pos_to_alt)], ignore_index=True)

    print(f"Writing output to {output_file}")
    results_df.to_csv(output_file, index=False)

def main():
    args = parse_args()

    vcf_df = load_vcf_into_df(args.vcf)
    snp_matrix,pos_to_alt,pos_to_ref = create_matrix(vcf_df, args.output)

    print("Loading .pinecone.bootstrap.table.csv...")
    clusters_df = pd.read_csv(args.cluster_file)

    print("Extracting lineage defining SNPs...")
    cluster(clusters_df,snp_matrix,args.pinecone_threshold,args.output)

if __name__ == "__main__":
    main()
