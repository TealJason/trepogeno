import argparse
from pathlib import Path
import pandas as pd
from typing import Dict, List
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description="create a refeerce coordinate file and build Mykrobe panel from VCF and rPinecone clusters")
    parser.add_argument("--vcf",type=Path, required=True, help="Path to VCF file")
    parser.add_argument("--lineage_defining_snps", type=Path, required=True, help="Path to lineage defining snps file")
    parser.add_argument("--cluster_file", type=Path, required=True, help="Path to full rPinecone table (with Sub-lineage info)")
    parser.add_argument("--pinecone_threshold", type=int, default=50, help="Pinecone threshold (default=50) ")
    parser.add_argument("--output", type=Path, default="lineage_coordinate_output.tsv", help="Output path for Mykrobe panel")
    args = parser.parse_args()
    return args

def extract_columns(vcf_path, output_path='./reference_coordinates.txt'):
    data = []

    with open(vcf_path, "r") as vcf_file:
        for line in vcf_file:
            if line.startswith("#"):
                continue  # Skip header lines
            columns = line.strip().split("\t")
            chrom = "ref"
            pos = columns[1]
            ref = columns[3]
            alt = columns[4]
            data.append([chrom, pos, ref, alt, "DNA"])

    # Create DataFrame
    lineage_file_df = pd.DataFrame(data, columns=["CHROM", "POS", "REF", "ALT", "TYPE"])
    
    # Save to file
    lineage_file_df.to_csv(output_path, sep="\t", index=False)

    return lineage_file_df

def build_lineage_dict(lineage_df, pinecone_df, pinecone_number):
    pinecone_col = f"pinecone_{pinecone_number}"
    cluster_to_lineage = {}

    #Create a dictionary of lineages to clusters 
    for _, row in pinecone_df.iterrows():
        cluster = row[pinecone_col]
        sub_lineage = row["Sub-lineage"]
        if sub_lineage.startswith("singleton_"):
            sub_lineage = sub_lineage.split("_")[1]
        major_lineage = row["Major.Sub-lineage"]
        lineage = f"lineage{major_lineage}.{sub_lineage}"
        cluster_to_lineage[cluster] = lineage

    #Create a dictionary of lineages to snp positions
    lineage_snp_map = defaultdict(list)
    for _, row in lineage_df.iterrows():
        cluster = row["Cluster"]
        position = int(row["SNP_Position"])
        lineage = cluster_to_lineage.get(cluster)
        if lineage:
            lineage_snp_map[lineage].append(position)

    return lineage_snp_map

def add_lineages(coordinate_df, lineage_snp_map, output_path):
    
    #Using the dictionary of lineages to snp positions annoate the reference file
    output_lines = []
    for _, row in coordinate_df.iterrows():
        chrom = row[0]
        pos = int(row[1])
        ref = row[2]
        alt = row[3]
        dna_type = row[4]

        matched_lineages = [lineage for lineage, positions in lineage_snp_map.items() if pos in positions]

        if matched_lineages:
            lineage_str = ",".join(matched_lineages)
            output_lines.append(f"{chrom}\t{pos}\t{ref}\t{alt}\t{dna_type}\t{lineage_str}")

    with open(output_path, "w") as f:
        for line in output_lines:
            f.write(line + "\n")

def main():
    args = parse_args()
    reference_coordinate_df = extract_columns(args.vcf)

    lineage_df = pd.read_csv(args.lineage_defining_snps)

    pinecone_df = pd.read_csv(args.cluster_file)

    print("Creating lineage to snp posistion map...")
    lineage_snp_map = build_lineage_dict(lineage_df, pinecone_df, args.pinecone_threshold)

    print("Annotating reference coordinates...")
    add_lineages(reference_coordinate_df, lineage_snp_map, args.output)

    print(f"Done. Output written to: {args.output}")

if __name__ == "__main__":
    main()