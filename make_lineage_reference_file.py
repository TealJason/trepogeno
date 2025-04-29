import argparse
from collections import defaultdict
from pathlib import Path
import pandas as pd
from typing import Dict, List

def parse_args():
    parser = argparse.ArgumentParser(description="Build Mykrobe panel from VCF and rPinecone clusters")
    parser.add_argument("--reference_coordinate", type=Path, required=True, help="Path to basic reference coordinate file")
    parser.add_argument("--lineage_defining_snps", type=Path, required=True, help="Path to lineage defining snps file")
    parser.add_argument("--cluster_file", type=Path, required=True, help="Path to full rPinecone table (with Sub-lineage info)")
    parser.add_argument("--pinecone_threshold", type=int, default=50, help="Pinecone threshold (default=50)")
    parser.add_argument("--output", type=Path, default="lineage_coordinate_output.txt", help="Output path for Mykrobe panel")
    return parser.parse_args()

def build_lineage_dict(lineage_df: pd.DataFrame, pinecone_df: pd.DataFrame, pinecone_number: int) -> Dict[str, List[int]]:
    pinecone_col = f"pinecone_{pinecone_number}"
    cluster_to_lineage = {}

    #Create a dictionary of lineages to clusters 
    for _, row in pinecone_df.iterrows():
        cluster = row[pinecone_col]
        sub_lineage = row["Sub-lineage"]
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

def add_lineages(coordinate_df: pd.DataFrame, lineage_snp_map: Dict[str, List[int]], output_path: Path) -> None:
    
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
        else:
            output_lines.append(f"{chrom}\t{pos}\t{ref}\t{alt}\t{dna_type}")

    with open(output_path, "w") as f:
        for line in output_lines:
            f.write(line + "\n")

def main():
    args = parse_args()

    lineage_df = pd.read_csv(args.lineage_defining_snps)
    coordinate_df = pd.read_csv(args.reference_coordinate, sep='\t', header=None)
    pinecone_df = pd.read_csv(args.cluster_file)

    print("Creating lineage to snp posistion map...")
    lineage_snp_map = build_lineage_dict(lineage_df, pinecone_df, args.pinecone_threshold)

    print("Annotating reference coordinates...")
    add_lineages(coordinate_df, lineage_snp_map, args.output)
    print(f"Done. Output written to: {args.output}")

if __name__ == "__main__":
    main()
