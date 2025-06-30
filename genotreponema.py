import json
import argparse
from pathlib import Path
import pandas as pd
from typing import Dict, List
from collections import defaultdict
from Bio import SeqIO
import numpy as np
import logging
import sys

#custom functions
from post_process_json.tabulate_json import get_all_lineage_calls_for_one_sample, get_json_file_paths, create_and_write_table
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
        "--check_all",
        help="If provided, the script will check how much support was found for all lineages. Omit to check only the support for lineages called by mykrobe.",
        action="store_true",
        default=False
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
        "--reference_coordinate",
        help="The reference coordinate file mapping snps and lineages to genomic positions",
    )

    parser.add_argument(
        "--genomic_reference",
        help="The path to the genomic reference fasta",
    )

    parser.add_argument(
        "--seq_manifest",
        help="If you want to call preform back to back lineage calls you can provide a manifest of reads for which lineage calls will be preformed",
        type=Path,
    )

    parser.add_argument(
        "--probe_and_lineage_dir",
        help="The directory in which to save the probe and lineage files if being regenerated and or the location in which the probe and lineage file can be found for lineage calling",
        default="./",
    )

    args = parser.parse_args()
    if args.json_directory is None:
        parser.error("The json_directory was not found or provided correctly.")
        exit(1)
    return args

def create_probes_from_type_scheme(lineage_file,reference_coordinate,genomic_reference,probe_and_lineage_dir):
    create_probes(lineage_file,reference_coordinate,genomic_reference,probe_and_lineage_dir)

def run_lineage_call(probe_directory,sequence_manifest):
    run_mykrobe_lineage_call(probe_directory,sequence_manifest)

def concatenate_and_read_json(json_directory,check_all):
    json_list = get_json_file_paths(json_directory)

    full_dictionary = {}
    for path in json_list:
        with open(path) as json_path:
            json_dict = json.load(json_path)
            full_dictionary = get_all_lineage_calls_for_one_sample(json_dict,full_dictionary,check_all)

    create_and_write_table(full_dictionary,check_all)

def main():
    args = parse_arguments()

    if args.make_probes: 
        lineage_directory = args.probe_and_lineage_dir + "/lineage.json"
        create_probes_from_type_scheme(lineage_directory, args.reference_coordinate, args.genomic_reference, args.probe_and_lineage_dir)

    if args.lineage_call:
        run_lineage_call(args.probe_and_lineage_dir,args.seq_manifest)

    if args.tabulate_jsons:
        concatenate_and_read_json(args.json_directory,args.check_all)

if __name__ == "__main__":
    main()
