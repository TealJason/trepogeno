from types import SimpleNamespace as Namespace  

from  mykrobe.cmds.amr import run as run_lineage_call

def check_lineage_file(probe_directory,):
    print(f"check_lineage_file at {probe_directory}/lineage.json")

def get_sequence(line):
    ID, sequence1, sequence2 = line.strip().split(",")
    return ID, sequence1, sequence2

def run_mykrobe_lineage_call(probe_directory, sequence_manifest,json_directory):
    check_lineage_file(probe_directory)

    with open(sequence_manifest, "r") as manifest:
        next(manifest)  # Skip header line
        for line in manifest:
            if not line.strip():
                continue  # Skip empty lines
            
            ID, sequence1, sequence2 = get_sequence(line)

            sequences = [sequence1]
            if sequence2:
                sequences.append(sequence2)

            args = Namespace(
                custom_probe_set_path=f"{probe_directory}/probes.fa",
                species="custom",
                report_all_calls=True,
                tmp=None,
                ont=False,
                seq=sequences,
                kmer=21,
                force=False,
                threads=2,
                skeleton_dir="data/skeletons/",
                memory="1GB",
                sample=ID,
                filters=["MISSING_WT", "LOW_PERCENT_COVERAGE", "LOW_GT_CONF", "LOW_TOTAL_DEPTH"],
                min_variant_conf=150,
                min_gene_conf=1,
                model="median_depth",
                min_proportion_expected_depth=0.3,
                ploidy="diploid",
                conf_percent_cutoff=100,
                min_depth=100,
                ignore_minor_calls=False,
                keep_tmp=False,
                ncbi_names=None,
                custom_variant_to_resistance_json=None,
                custom_lineage_json=None,
                expected_error_rate=0.05,
                guess_sequence_method=False,
                output_format="json",
                output=f"{json_directory}/{ID}.json"
            )

            run_lineage_call(None, args)