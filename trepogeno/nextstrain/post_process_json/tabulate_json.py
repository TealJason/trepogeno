import json
import pandas as pd

#This function is imported for injecting java script into the html
from nextstrain.post_process_json.style import style_html

def get_all_lineage_calls_for_one_sample(json_dict,full_dictionary):
    #This function creates a dictionary which records the number of calls made vs the number of possible calls in a dictionary
    #We do this for one sample at a time so its not memory intensive even with many probes
    keys = list(json_dict)
    sample_id = keys[0]
    lineage_list = list(json_dict[sample_id]["lineage_calls"]) #Access the "lineage calls" key and put it in a list
        

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
    filter_to_single_rows(call_summary_table)

    style_html(html_path)

##This function has been written by the brilliant people over at genotyphi
def get_mykrobe_best_call(genotype,base_id):

    full_lineage_data = genotype[base_id]["phylogenetics"]

    genotype_details = full_lineage_data['lineage']['calls_summary']
    genotype_list = list(genotype_details.keys())
    # intialise empty values for best score and corresponding genotype
    best_score = 0
    best_genotype = None
    # node support is the number of 'good nodes' called by mykrobe
    # needs to be X/Y, where Y is the total number of levels at that genotype

# loop through each genotype
    for genotype in genotype_list:
        # the maximum score we can get is the total depth of the heirarchy
        max_score = genotype_details[genotype]['tree_depth']
        # the actual score is a sum of the values within each levels call
        actual_score = sum(list(genotype_details[genotype]['genotypes'].values()))
        # if actual score is equal to the max score, then this is the best genotype
        if actual_score == max_score:
            best_score = actual_score
            best_genotype = genotype

        # if actual score is < max score, but is greater than the current best score,
        # then this is our best genotype for the moment
        elif actual_score < max_score and actual_score > best_score:
            best_score = actual_score
            best_genotype = genotype
            #node_support = genotype_details[best_genotype]['good_nodes']

    print(f"best genotype for {base_id} is {best_genotype}")
    
#This is function contols the flow of this script
def run_tabulate_json(json_directory):
    #First we get the paths to the json file and collect them in a list
    json_list = get_json_file_paths(json_directory)

    full_dictionary = {}
    #For each json path
    for path in json_list:
        
        with open(path) as json_path:
            genotype = json.load(json_path) #Load the json into a dictionary 

            base_id = path.stem #collect the Sample ID, this should also match the top level key of the nested dictionary we just initilised 

            full_dictionary = get_all_lineage_calls_for_one_sample(genotype,full_dictionary) #We create a dictionary for each lineage per sample and the number of calls possible vs made for each lineage 
            get_mykrobe_best_call(genotype,base_id) #This just parses the 'full' dictionary to get which lineage had a highest flat perportion of calls made
            
    create_and_write_table(full_dictionary) #write out the 'best' calls (which lineage for each sample had the highest proportion of calls made)
