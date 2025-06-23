#!/bin/bash

# Set variables for input files and parameters
while getopts v:c:p:r: flag
do
    case "${flag}" in
        v) VCF_FILE=${OPTARG};;
        c) CLUSTER_FILE=${OPTARG};;
        p) PINECONE_THRESHOLD=${OPTARG};;
        r) REFERENCE=${OPTARG};;
    esac
done

LINEAGE_DEFINGING_SNPS="lineage_defining_snps.csv"
LINEAGE_COORDINATE_FILE="./lineage_coordinate.txt"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Step 1: Run create_matrix_get_lineage_defining_snps.py
echo "Running create_matrix_get_lineage_defining_snps.py..."

python3 $SCRIPT_DIR/create_matrix_get_lineage_defining_snps.py \
    --vcf "$VCF_FILE" \
    --cluster_file "$CLUSTER_FILE" \
    --pinecone_threshold "$PINECONE_THRESHOLD" \

# Step 2: Run create_full_reference_coordinate_file.py
echo "Running create_full_reference_coordinate_file.py..."

python3 $SCRIPT_DIR/create_full_reference_coordinate_file.py \
    --vcf "$VCF_FILE" \
    --cluster_file "$CLUSTER_FILE" \
    --pinecone_threshold "$PINECONE_THRESHOLD" \
    --output "$LINEAGE_COORDINATE_FILE" \
    --lineage_defining_snps "$LINEAGE_DEFINGING_SNPS"

mykrobe variants make-probes -k 21 \
-t $LINEAGE_COORDINATE_FILE \
--lineage lineage$PINECONE_THRESHOLD.json  \
"$REFERENCE" > probes_test.fa

echo "Pipeline completed successfully."
