#Create reference coordinate file
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="create a refeerce coordinate file")
    parser.add_argument("--vcf",type=Path, required=True, help="Path to VCF file")
    args = parser.parse_args()
    return args

def extract_columns(vcf_path, output_path='./reference_coordinates.txt'):
    with open(vcf_path, "r") as vcf_file, open(output_path, "w") as out_file:
        for line in vcf_file:
            if line.startswith("#"):
                continue  # Skip header lines
            columns = line.strip().split("\t")
            chrom = columns[0]
            pos = columns[1]
            ref = columns[3]
            alt = columns[4]
            out_file.write(f"{chrom}\t{pos}\t{ref}\t{alt}\tDNA\n")
def main():
    args = parse_args()
    extract_columns(args.vcf)


if __name__ == "__main__":
    main()
