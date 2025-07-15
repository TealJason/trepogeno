import argparse
from pathlib import Path
import logging

#custom functions
from nextstrain.post_process_json.tabulate_json import run_tabulate_json
from nextstrain.create_probes.create_probes import create_probes
from nextstrain.lineage_calling.run_mykrobe_lineage_calling import run_mykrobe_lineage_call

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="script to summarise lineage calls across output json's from mykrobe"
    )
    parser.add_argument(
        "--json_directory",
        help="Path to the directory in which to save and read the mykrobe .json files",
        type=Path
    )

    parser.add_argument(
        "--make_probes",
        help="Provide this flag if you want to create a new set of probes before running the lineage calling",
        action="store_true",
    )

    parser.add_argument(
        "--tabulate_jsons",
        help="Provide this flag to if you want to tabulate the json outputs produced by mykrobe",
        action="store_true",
    )

    parser.add_argument(
        "--lineage_call",
        help="Provide this flag to preform the custom lineage calling with mykrobe",
        action="store_true",
    )

    parser.add_argument(
        "--type_scheme",
        help="The reference coordinate file mapping snps and lineages to genomic positions",
    )

    parser.add_argument(
        "--genomic_reference",
        help="The path to the genomic reference fasta",
    )

    parser.add_argument(
        "--seq_manifest",
        help="A manifest of Sample ID sequences as a CSV, the heading should be ID,Read1,Read2. ",
        type=Path,
    )

    parser.add_argument(
        "--probe_and_lineage_dir",
        help="The directory in which to save the probe and lineage files if being regenerated and or the location in which the probe and lineage file can be found for lineage calling",
        default="./",
    )

    parser.add_argument(
        "--probe_lineage_name",
        help="Provide this flag if you want you want to name the probes and lienage json when creating a new set of probes, otherwise defaults to probes.fa & lineage.json, provide this flag with lineage calling if using non default probe names",
    )

    args = parser.parse_args()

    if  args.tabulate_jsons and args.json_directory is None:
        parser.error("The json_directory was not found or provided correctly for processing!")
        exit(1)

    if args.make_probes:
        if not args.type_scheme:
            parser.error("The typeing scheme was not provided but is required for making probes")
            exit(1)
        if not args.genomic_reference:    
            parser.error("The genomic reference was not provided but is required for making probes")
            exit(1)

    if args.lineage_call:
        if not args.genomic_reference:
            parser.error("The genomic reference was not provided but is required for calling lineages")
            exit(1)
        if not args.seq_manifest:
            parser.error("A sequence manifest was not provided but is required for calling lineages")
            exit(1)
        if not args.json_directory:
            parser.error("A direcory to store jsons was not provided but is required for calling lineages")
            exit(1)
    return args

def create_probes_from_type_scheme(lineage_directory,type_scheme,genomic_reference,probe_and_lineage_dir,probe_lineage_name):
    create_probes(lineage_directory,type_scheme,genomic_reference,probe_and_lineage_dir,probe_lineage_name)

def run_lineage_call(probe_directory,sequence_manifest,json_directory,probe_lineage_name):
    run_mykrobe_lineage_call(probe_directory,sequence_manifest,json_directory,probe_lineage_name)

def concatenate_and_read_json(json_directory):
    run_tabulate_json(json_directory)

def main():
    args = parse_arguments()

    if args.make_probes: 
        lineage_directory = args.probe_and_lineage_dir + "/lineage.json"
        create_probes_from_type_scheme(lineage_directory, args.type_scheme, args.genomic_reference, args.probe_and_lineage_dir, args.probe_lineage_name)

    if args.lineage_call:
        run_lineage_call(args.probe_and_lineage_dir,args.seq_manifest,args.json_directory,args.probe_lineage_name)

    if args.tabulate_jsons:
        concatenate_and_read_json(args.json_directory)

if __name__ == "__main__":
    main()
