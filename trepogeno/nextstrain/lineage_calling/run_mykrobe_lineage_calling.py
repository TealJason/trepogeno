from types import SimpleNamespace as Namespace  
from  nextstrain.mykrobe.src.mykrobe.cmds.amr import run as run_lineage_call
import os 

def check_lineage_file(json_directory,):
    os.makedirs(json_directory, exist_ok=True)



def run_mykrobe_lineage_call(probe_json_directory, sequence_manifest,json_directory,probe_lineage_name):
    check_lineage_file(json_directory)

    with open(sequence_manifest, "r") as manifest: #This is loop is for parsing a manifest with the structure ID,Read1,Read2
        next(manifest)  # Skip header line
        for line in manifest: # For each new unique sample
            if not line.strip(): 
                continue  # Skip empty lines
            if line.startswith("#"): # Skip comments
                  continue

            ID, sequence1, sequence2 = line.strip().split(",") #Get each part 
            sequences = [sequence1]
            if sequence2: #The fastq does not have to be paired if it in't we can continute with the first fastq (validation of the file suffix should be added)
                sequences.append(sequence2)

            if probe_lineage_name: #If we are using probe and lineage files with custom name
                probe_name = f"{probe_lineage_name}.fa"
                lineage_name = f"{probe_lineage_name}.json"
            else: #If we are using the deafult names
                probe_name = "probe.fa"
                lineage_name = "lineage.json"

            #Mykrobe has many different arguments captured from the user, we mockup this namespace below so we can use it in our function call
            args = Namespace(
                custom_probe_set_path=f"{probe_json_directory}/{probe_name}",
                custom_lineage_json=f"{probe_json_directory}/{lineage_name}",
                species="custom",
                report_all_calls=True,
                sample=ID,
                output_format="json",
                output=f"{json_directory}/{ID}.json",
                seq=sequences,

                tmp=None, #This tmp variable and below are set at the defaults when running lineage calling although most are never used, above are set dynamically
                ont=False,
                kmer=21, # Must add argument to override 
                force=False, # Must add argument to override
                threads=2, # Must add argument to override
                skeleton_dir="mykrobe/data/skeletons/",
                memory="2GB", # Must add argument to override
                filters=['MISSING_WT', 'LOW_PERCENT_COVERAGE', 'LOW_GT_CONF', 'LOW_TOTAL_DEPTH'],
                min_variant_conf=150,
                min_gene_conf=1,
                model="kmer_count",
                min_proportion_expected_depth=0.3,
                ploidy=None, # This is only in use if using args.ONT is set (would otherwise be set to diploid by defualt)
                conf_percent_cutoff=100,
                min_depth=1,
                ignore_minor_calls=False,
                keep_tmp=False,# Must add argument to override
                ncbi_names=None,
                custom_variant_to_resistance_json=None,
                expected_error_rate=0.05,
                guess_sequence_method=False,
                ctx=None,
                ignore_filtered=False,
                dump_species_covgs=None,
                min_gene_percent_covg_threshold=100
            )

            run_lineage_call(None, args) #Runs the function imported from mykrobe, the first variable is unused in the function the second contains our mocked arguments