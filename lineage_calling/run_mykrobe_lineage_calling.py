from types import SimpleNamespace as Namespace  
from  nextstrain.mykrobe.src.mykrobe.cmds.amr import run as run_lineage_call

def check_lineage_file(probe_directory,):
    print(f"check_lineage_file at {probe_directory}/lineage.json")

def get_sequence(line):
    ID, sequence1, sequence2 = line.strip().split(",")
    return ID, sequence1, sequence2

def run_mykrobe_lineage_call(probe_json_directory, sequence_manifest,json_directory):
    check_lineage_file(probe_json_directory)

    with open(sequence_manifest, "r") as manifest:
        next(manifest)  # Skip header line
        for line in manifest:
            if not line.strip():
                continue  # Skip empty lines
            if line.startswith("#"): # skip comments
                  continue

            ID, sequence1, sequence2 = get_sequence(line)
            sequences = [sequence1]
            if sequence2:
                sequences.append(sequence2)

            args = Namespace(
                custom_probe_set_path=f"{probe_json_directory}/probes.fa",
                custom_lineage_json=f"{probe_json_directory}/lineage.json",
                species="custom",
                report_all_calls=True,
                sample=ID,
                output_format="json",
                output=f"{json_directory}/{ID}.json",
                seq=sequences,

                tmp=None, #this tmp variable and below are mocked to defaults, above are set based on input arguments
                ont=False,
                kmer=21,
                force=False,
                threads=2,
                skeleton_dir="mykrobe/data/skeletons/",
                memory="1GB",
                filters=['MISSING_WT', 'LOW_PERCENT_COVERAGE', 'LOW_GT_CONF', 'LOW_TOTAL_DEPTH'],
                min_variant_conf=150,
                min_gene_conf=1,
                model="kmer_count",
                min_proportion_expected_depth=0.3,
                ploidy="diploid",
                conf_percent_cutoff=100,
                min_depth=1,
                ignore_minor_calls=False,
                keep_tmp=False,
                ncbi_names=None,
                custom_variant_to_resistance_json=None,
                expected_error_rate=0.05,
                guess_sequence_method=False,
                ctx=None,
                ignore_filtered=False,
                dump_species_covgs=None,
                min_gene_percent_covg_threshold=100
            )

            run_lineage_call(None, args)