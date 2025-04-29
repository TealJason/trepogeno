import pandas as pd 
import numpy as np
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Script to create SNP matrix from VCF")
    parser.add_argument("--vcf", type=Path, required=True)
    args = parser.parse_args()
    return args

def load_vcf_into_df(vcf):
    vcf_df = pd.read_csv(vcf, skiprows=46, sep="\t")
    return vcf_df

def initialise_snp_df(vcf_df):
    samples_df = vcf_df.iloc[:, 9:]
    pos_list = vcf_df['POS'].tolist()
    samples_df_T = samples_df.T
    samples_df_T.columns = pos_list
    return samples_df_T

def create_matrix(vcf_df):
    snp_matrix_df = initialise_snp_df(vcf_df)
    print("Initial SNP Matrix:")
    print(snp_matrix_df.head(n=2))

    print("VCF DataFrame:")
    print(vcf_df.head(n=2))

    #create dict for pos to ref and pos to alt
    pos_to_ref = vcf_df.set_index('POS')['REF'].to_dict()
    pos_to_alt = vcf_df.set_index('POS')['ALT'].to_dict()

    def replace_allele(value, pos):
        if pd.isna(value):  # skip if NaN
            return value
        allele_call = value.split(':')[0]
        if allele_call == '0':
            return pos_to_ref.get(pos, '_')  # 'N' if position not found
        elif allele_call == '1':
            return pos_to_alt.get(pos, '_')
        else:
            return '_'  # Unexpected value, treat as missing

    # apply replacement
    for pos in snp_matrix_df.columns:
        pos_int = int(pos)
        snp_matrix_df[pos] = snp_matrix_df[pos].apply(lambda x: replace_allele(x, pos_int))

    print("\nFinal SNP Matrix:")
    print(snp_matrix_df.head())
    snp_matrix_df.to_csv("/data/pam/team230/jb71/scratch/NextStrain/new_snp_matrix.csv")

def main():
    args = parse_args()
    vcf_df = load_vcf_into_df(args.vcf)
    create_matrix(vcf_df)

if __name__ == "__main__":
    main()
