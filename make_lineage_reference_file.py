import argparse
from collections import defaultdict
from pathlib import Path
from tyepings import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Build Mykrobe panel from VCF and rPinecone clusters")
    parser.add_argument("--reference_coordinate",type=Path, required=True, help="Path to basic reference coordinate file")
    parser.add_argument("--output",type=Path, default="treponema_panel.json", help="Output path for Mykrobe panel")
    return parser.parse_args()

def add_lineages(reference_coordinate: Path, output_path:path)-> None:
    with open(reference_coordinate, "r") as ref_file, with open (output_path, "w") as out_file:
        for line in ref_file:
            parts = line.strip().split("\t")
            pos = parts[2]



def main():
    args = parse_args()
    add_lineages(args.reference_coordinate, args.output)

if __name__ == "__main__":
    main()
