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

#Custom functions
from nextstrain.lineage_calling.tabulate_json import get_all_lineage_calls_for_one_sample, get_json_file_paths, create_and_write_table
from nextstrain.create_probes.create_probes import create_probes
from nextstrain.lineage_calling.run_mykrobe_lineage_calling import check_lineage_file, run_mykrobe_lineage_call

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="script to summarise lineage calls across output json's from mykrobe"
    )
    parser.add_argument(
        "--json_directory",
        help="Path to the directory con
        taining the .json files",
        type=Path
    )

    parser.add_argument(
        "--check_all",
        help="If provided, the script will check how much support was found for all lineages. Omit to check only called lineages.",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--lineage_file",
        help="If provided will create a new set of probes before running the lineage calling",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--reference_coordinate",
        help="The reference coordinate file mapping snps and lineages to genomic positions",
    )    

    args = parser.parse_args()
    if args.json_directory is None or args.reference_coordinate is None:
        parser.error("The json_directory was not found or provided correctly.")
        exit(1)
    return args

def create_probes_from_type_scheme(lineage_file):
    create_probes_from_type_scheme()


def run_mykrobe():
    check_lineage_file()
    run_mykrobe()

def concatonate_and_read_json():
    json_list = get_json_file_paths(args.json_directory)

    full_dictionary = {}
    for path in json_list:
        with open(path) as json_path:
            json_dict = json.load(json_path)
            full_dictionary = get_all_lineage_calls_for_one_sample(json_dict,full_dictionary,args.check_all)

    create_and_write_table(full_dictionary,args.check_all)

def main():
    args = parse_arguments()

    if lineage_file create_probes_from_type_scheme(args.lineage_file)

    run_mykrobe(probe_directory)

    concatonate_and_read_json(args)

if __name__ == "__main__":
    main()
