import json
import argparse
from pathlib import Path

def get_all_lineage_calls_for_one_sample(json_dict,full_dictionary,check_all):
    keys = list(json_dict)
    sample_id = keys[0]
    if check_all == False:
        lineage_list = json_dict[sample_id]["phylogenetics"]["lineage"]["lineage"]
    else:
        lineage_list = list(json_dict[sample_id]["lineage_calls"])

    single_sample_dictionary_full = {
        sample_id: {}
    }

    for lineage in lineage_list:
        possible_calls = 0
        calls_made = 0

        if check_all == False:
            calls = json_dict[sample_id]["phylogenetics"]["lineage"]["calls"].get(lineage, {})
            for sublineage, probes in calls.items():
                for probe_id, probe_data in probes.items():
                    genotype = probe_data.get("genotype")
                    if genotype == [0, 0]:
                        possible_calls += 1
                    elif genotype == [1, 1]:
                        possible_calls += 1
                        calls_made += 1
        else:
            calls = json_dict[sample_id]["lineage_calls"].get(lineage, {})
            for probe_id, probe_data in calls.items():
                genotype = probe_data.get("genotype")
                if genotype == [0, 0]:
                    possible_calls += 1
                elif genotype == [1, 1]:
                    possible_calls += 1
                    calls_made += 1

        single_sample_dictionary_full[sample_id][lineage] = {
            "calls_made": calls_made,
            "possible_calls": possible_calls
        }

        full_dictionary.update(single_sample_dictionary_full)
    return full_dictionary

def get_json_file_paths(json_directory_path):

    json_list = []
    for file in json_directory_path.glob("*.json"):
        json_list.append(file)
    return json_list

def create_and_write_table(full_dictionary):
    for sample_id, lineages in full_dictionary.items():
        for lineage, stats in lineages.items():
            print(f"Sample {sample_id} found {stats['calls_made']} SNP's to support lineage {lineage}, out of a total possible of {stats['possible_calls']}")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="script to summarise lineage calls across output json's from mykrobe"
    )
    parser.add_argument(
        "--json_directory",
        help="Path to the directory containing the .json files",
        type=Path
    )

    parser.add_argument(
        "--check_all",
        help="If provided, the script will check how much support was found for all lineages. Omit to check only called lineages.",
        action="store_true",
        default=False
    )

    args = parser.parse_args()
    if args.json_directory is None:
        parser.error("The json_directory was not found or provided correctly.")
        exit(1)
    return args

def main():
    args = parse_arguments()

    json_list = get_json_file_paths(args.json_directory)

    full_dictionary = {}
    for path in json_list:
        with open(path) as json_path:
            json_dict = json.load(json_path)
            full_dictionary = get_all_lineage_calls_for_one_sample(json_dict,full_dictionary,args.check_all)

    create_and_write_table(full_dictionary)

if __name__ == "__main__":
    main()


""" 
   single_sample_dictionary_full = {
        sample_id{
            TPE.1.1"{
                calls_made:0,possible_calls:0
            }
            TPE.1.3{
                calls_made:0,possible_calls:0
            }
        }
    }
"""

'''
Simple table:

Sample_id   |Lineage |Calls made |Possible calls|              |
----------- |--------|-----------|--------------|--------------|
SRR14277265 |TPE     |  33       |      42      |              |
----------- |--------|-----------|--------------|--------------|
ERR9768236  |TPE.3.1 |  30       |      38      |              |

'''