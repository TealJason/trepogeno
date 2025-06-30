import json
import argparse
from pathlib import Path
import pandas as pd

def get_all_lineage_calls_for_one_sample(json_dict,full_dictionary,check_all):
    keys = list(json_dict)
    sample_id = keys[0]
    check_all = True
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
                    elif genotype == [1, 1] or genotype == [0, 1]:
                        possible_calls += 1
                        calls_made += 1
        else:
            calls = json_dict[sample_id]["lineage_calls"].get(lineage, {})

            for probe_id, probe_data in calls.items():
                genotype = probe_data.get("genotype")
                if genotype == [0, 0]:
                    possible_calls += 1
                elif genotype == [1, 1] or genotype == [0, 1]:
                    possible_calls += 1
                    calls_made += 1

        single_sample_dictionary_full[sample_id][lineage] = {
            "calls_made": calls_made,
            "possible_calls": possible_calls,
             "total_support": round((calls_made / possible_calls * 100), 2)
        }

    full_dictionary.update(single_sample_dictionary_full)
    return full_dictionary

def get_json_file_paths(json_directory_path):

    json_list = []
    for file in json_directory_path.glob("*.json"):
        json_list.append(file)
    return json_list

def filter_to_single_rows(call_summary_table):
    # Filter to supported lineages only
    call_summary_table_supported = call_summary_table[call_summary_table["Calls Made"] > 0].copy()

    # Calculate lineage depth by counting '.' in lineage name
    call_summary_table_supported["lineage_depth"] = call_summary_table_supported["Lineage"].str.count("\.")

    # Sort by Sample ID, then descending lineage depth, then descending Total support
    call_summary_table_supported_sorted = call_summary_table_supported.sort_values(
        by=["Sample ID", "lineage_depth", "Total support"], 
        ascending=[True, False, False]
    )

    # Take the top lineage per Sample ID
    call_summary_supported_best = call_summary_table_supported_sorted.groupby("Sample ID").head(1)

    # Save or display
    call_summary_supported_best.to_csv("best_lineages_from_all.csv", index=False)
    print(call_summary_supported_best)

def create_and_write_table(full_dictionary,all_checked):
    data = []
    for sample_id, lineages in full_dictionary.items():
        for lineage, stats in lineages.items():
            data.append({
                "Sample ID": sample_id,
                "Lineage": lineage,
                "Calls Made": stats.get("calls_made", 0),
                "Possible Calls": stats.get("possible_calls", 0),
                "Total support": stats.get("total_support",0)
            })

    call_summary_table = pd.DataFrame(data)
    if all_checked == True:
        call_summary_table.to_csv("./snps_called_all.csv",index=False)
        filter_to_single_rows(call_summary_table)
    else:
        call_summary_table.to_csv("./snps_called.csv",index= False)
    print(call_summary_table)

def run_tabulate_json(json_directory, check_all):
    json_list = get_json_file_paths(json_directory)

    full_dictionary = {}

    for path in json_list:
        with open(path) as json_path:
            json_dict = json.load(json_path)
            full_dictionary = get_all_lineage_calls_for_one_sample(json_dict,full_dictionary,check_all)

    create_and_write_table(full_dictionary,check_all)

