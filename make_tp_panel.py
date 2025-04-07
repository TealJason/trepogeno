import argparse
import csv
import json
import vcf  # pyvcf
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description="Build Mykrobe panel from VCF and rPinecone clusters")
    parser.add_argument("--vcf", required=True, help="Path to multi-sample SNP VCF file")
    parser.add_argument("--csv", required=True, help="Path to rPinecone bootstrap table CSV")
    parser.add_argument("--bootstrap", default="pinecone_50", help="Column in CSV to define clusters")
    parser.add_argument("--output", default="treponema_panel.json", help="Output path for Mykrobe panel")
    return parser.parse_args()

def load_clusters(csv_path, pinecone_level):
    sample_to_cluster = {}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample = row["Taxa"].split("__")[0]
            cluster = row[pinecone_level]
            sample_to_cluster[sample] = f"cluster_{cluster}"
    return sample_to_cluster

def parse_vcf(vcf_path, clusters):
    reader = vcf.Reader(open(vcf_path, 'r'))
    cluster_samples = defaultdict(set)
    
    # Group samples by their cluster
    for sample, cluster in clusters.items():
        cluster_samples[cluster].add(sample)

    snv_presence = defaultdict(lambda: defaultdict(set))  # pos -> allele -> samples

    for record in reader:
        if not record.is_snp:
            continue  # skip indels and MNPs
        chrom = record.CHROM
        pos = record.POS
        ref = record.REF
        
        # Iterate over the alternative alleles (ALT)
        for alt_index, alt in enumerate(record.ALT):
            if alt is None:
                continue
            variant_key = f"{chrom}:{pos}:{ref}>{alt}"
            
            # Now, let's check each sample's genotype
            for sample in record.samples:
                # Check if the sample is part of the clusters
                if sample.sample not in clusters:
                    continue
                
                # Extract the sample's data (GT:AD:AF:DP:GQ:PL)
                sample_data = sample.data
                sample_fields = str(sample_data).split(":")  # Split the colon-separated fields

                # The first field is the genotype (GT), which is what we're interested in
                gt = sample_fields[0]  # This should be 0 (reference) or 1 (alternate)

                # Ensure the genotype is not missing (i.e., not equal to '.')
                if gt == ".":
                    continue
                
                # Check if the sample carries the alternate allele (genotype = 1)
                if gt == "1":  # If the genotype is 1, the sample carries the alternate allele
                    snv_presence[variant_key][clusters[sample.sample]].add(sample.sample)

    return snv_presence, cluster_samples

def find_unique_snvs(snv_presence, cluster_samples):
    snvs_by_cluster = defaultdict(dict)
    for snv, present_by_cluster in snv_presence.items():
        for cluster, cluster_samples_present in present_by_cluster.items():
            if cluster_samples_present == cluster_samples[cluster]:
                # ensure it's not present in any other cluster
                other_clusters = set(cluster_samples.keys()) - {cluster}
                present_elsewhere = any(
                    present_by_cluster.get(other_cluster)
                    for other_cluster in other_clusters
                )
                if not present_elsewhere:
                    snvs_by_cluster[cluster][snv] = {}
    return snvs_by_cluster

def write_mykrobe_panel(snvs_by_cluster, output_path):
    panel = {
        "species": "treponema",
        "schema_version": 2,
        "genotyping": {}
    }
    for cluster, snvs in snvs_by_cluster.items():
        if snvs:
            panel["genotyping"][cluster] = {"variants": snvs}
    with open(output_path, "w") as out:
        json.dump(panel, out, indent=2)

def main():
    args = parse_args()
    clusters = load_clusters(args.csv, args.bootstrap)
    snv_presence, cluster_samples = parse_vcf(args.vcf, clusters)
    snvs_by_cluster = find_unique_snvs(snv_presence, cluster_samples)
    write_mykrobe_panel(snvs_by_cluster, args.output)
    print(f"Mykrobe panel written to: {args.output}")

if __name__ == "__main__":
    main()
