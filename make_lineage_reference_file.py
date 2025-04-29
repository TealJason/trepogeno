import argparse
from collections import defaultdict
from pathlib import Path
import pandas as pd
from typing import Dict, List, Set

def parse_args():
    parser = argparse.ArgumentParser(description="Build Mykrobe panel from VCF and rPinecone clusters")
    parser.add_argument("--reference_coordinate",type=Path, required=True, help="Path to basic reference coordinate file")
    parser.add_argument("--lineage_defining_snps",type=Path, required=True, help="Path to lineage defining snps file")
    parser.add_argument("--output",type=Path, default="lineage_coordinate_output.txt", help="Output path for Mykrobe panel")

    args = parser.parse_args()
    if args.reference_coordinate is None or args.lineage_defining_snps is None:
        raise ValueError("Both reference_coordinate and pinecone_csv must be provided")
        exit()
    return args

def build_lineage_dict(lineage_df: pd.DataFrame, pinecone_number: int) -> Dict[str, List[str]]:
    pinecone_threshold = f"pinecone_{pinecone_number}"
    sublineage_dict = defaultdict(list)

    for index, row in pinecone_df.iterrows():
        sub_lineage = row['Sub-lineage']
        major_lineage = row['Major.Sub-lineage']
        lineage= f"lineage{major_lineage}.{sub_lineage}"
        position = row[pinecone_threshold]
        sublineage_dict[lineage].append(position)

    return sublineage_dict

def add_lineages(coordinate_df: pd.DataFrame, pinecone_dict: Dict[str,list[int]], output_path: Path,)-> None:
    with open(output_path, "w") as out_file:
        for index, row in coordinate_df.iterrows():
            chrom = row[0]
            pos = row[1]
            ref = row[2]
            alt = row[3]
            dna_type = row[4]
            lineage = None
            for lineage_key, positions in pinecone_dict.items():
                if pos in positions:
                    lineage = lineage_key
                 
            if lineage:
                out_file.write(f"{chrom}\t{pos}\t{ref}\t{alt}\t{dna_type}\t{','.join(lineage)}\n")
            else:
                out_file.write(f"{chrom}\t{pos}\t{ref}\t{alt}\t{dna_type}\n")

def main():
    args = parse_args()
    lineage_defined_df = pd.read_csv(args.lineage_defining_snps)
    coordinate_df = pd.read_csv(args.reference_coordinate,sep='\t',header=None)
    print(lineage_defined_df.head(n=3))
    print(lineage_defined_df.head(n=3))

    lineage_dict = build_lineage_dict(pinecone_df, args.pinecone_threshold)
    add_lineages(coordinate_df,pinecone_dict,args.output)

if __name__ == "__main__":
    main()