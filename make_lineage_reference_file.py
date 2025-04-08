import argparse
from collections import defaultdict
from pathlib import Path
import pandas as pd
from typing import Dict, List, Set

def parse_args():
    parser = argparse.ArgumentParser(description="Build Mykrobe panel from VCF and rPinecone clusters")
    parser.add_argument("--reference_coordinate",type=Path, required=True, help="Path to basic reference coordinate file")
    parser.add_argument("--pinecone_csv",type=Path, required=True, help="Path to rPinecone clusters")
    parser.add_argument("--output",type=Path, default="lineage_coordinate_output.txt", help="Output path for Mykrobe panel")
    parser.add_argument("--pinecone_threshold",type=int,default=50,help="Pinecone threshold can be 95, 80, 50, 20, or 5. Default is 50")

    args = parser.parse_args()
    if args.pinecone_threshold not in [5, 20, 50, 80, 95]:
        raise ValueError("Pinecone threshold must be one of [5, 20, 50, 80, 95]")
        exit()
    if args.reference_coordinate is None or args.pinecone_csv is None:
        raise ValueError("Both reference_coordinate and pinecone_csv must be provided")
        exit()
    return args

def build_pinecone_dict(pinecone_df: pd.DataFrame, pinecone_number: int) -> Dict[str, List[str]]:
    pinecone_threshold = f"pinecone_{pinecone_number}"
    print(pinecone_threshold)
    sublineage_dict = defaultdict(list)

    for index, row in pinecone_df.iterrows():
        sub_lineage = row['Sub-lineage']
        position = row[pinecone_threshold]
        sublineage_dict[sub_lineage].append(position)
    return sublineage_dict

def add_lineages(coordinate_df: pd.DataFrame, pinecone_dict: Dict[str,list[int]], output_path: Path,)-> None:
    with open(output_path, "w") as out_file:
        for index, row in coordinate_df.iterrows():
            chrom = row[0]
            pos = row[1]
            ref = row[2]
            alt = row[3]
            dna_type = row[4]
            lineages = []
            for sublineage, positions in pinecone_dict.items():
                if pos in positions:
                    lineages.append(sublineage)
            if lineages:
                out_file.write(f"{chrom}\t{pos}\t{ref}\t{alt}\t{dna_type}\t{','.join(lineages)}\n")
            else:
                out_file.write(f"{chrom}\t{pos}\t{ref}\t{alt}\t{dna_type}\n")

def main():
    args = parse_args()
    pinecone_df = pd.read_csv(args.pinecone_csv)
    coordinate_df = pd.read_csv(args.reference_coordinate,sep='\t',header=None)
    print(pinecone_df.head(3))
    print(coordinate_df.head(3))
    pinecone_dict = build_pinecone_dict(pinecone_df, args.pinecone_threshold)
    add_lineages(coordinate_df,pinecone_dict,args.output)

if __name__ == "__main__":
    main()
