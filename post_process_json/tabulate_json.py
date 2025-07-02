import json
import argparse
from pathlib import Path
import pandas as pd

from nextstrain.post_process_json.style import style_html

def get_all_lineage_calls_for_one_sample(json_dict,full_dictionary):
    keys = list(json_dict)
    sample_id = keys[0]
    lineage_list = list(json_dict[sample_id]["lineage_calls"])
        

    single_sample_dictionary_full = {
        sample_id: {}
    }

    for lineage in lineage_list:
        possible_calls = 0
        calls_made = 0

        
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

def create_and_write_table(full_dictionary):
    data = []
    for sample_id, lineages in full_dictionary.items():
        for lineage, stats in lineages.items():
            data.append({
                "Sample ID": sample_id,
                "Lineage": lineage,
                "Calls Made": stats.get("calls_made", 0),
                "Possible Calls": stats.get("possible_calls", 0),
                "Total support": stats.get("total_support", 0)
            })

    call_summary_table = pd.DataFrame(data)


    csv_path = "./snps_called.csv"
    html_path = "./snps_called.html"
    call_summary_table.to_csv(csv_path, index=False)
    call_summary_table.to_html(html_path, index=False)

    style_html(html_path)

def run_tabulate_json(json_directory):
    json_list = get_json_file_paths(json_directory)

    full_dictionary = {}

    for path in json_list:
        with open(path) as json_path:
            json_dict = json.load(json_path)
            full_dictionary = get_all_lineage_calls_for_one_sample(json_dict,full_dictionary)

    create_and_write_table(full_dictionary)

