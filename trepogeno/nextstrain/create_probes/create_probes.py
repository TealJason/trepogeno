# This script is called from the main script of genotreponema
from types import SimpleNamespace as Namespace  
import os
from contextlib import redirect_stdout

#mykrobe functions
from nextstrain.mykrobe.src.mykrobe.cmds.makeprobes import run as run_make_variant_probes

def create_probes(reference_coordinate_filepath, reference_filepath,probe_and_lineage_dir,probe_lineage_name):
    default_lineage_path = os.path.join(probe_and_lineage_dir,"/lineage.json") #The probe_and_lineage_dir argument is used for both the lineage and probes file
    default_probe_path = os.path.join(probe_and_lineage_dir, "probe.fa") # we use them to set deault paths to the files  

    if probe_lineage_name:
        lineage_path = f"{probe_and_lineage_dir}/{probe_lineage_name}.json"
    else:
        lineage_path = default_lineage_path

    args = Namespace(
        no_backgrounds=True,
        database=False,
        vcf=None,
        genbank=None,
        text_file=reference_coordinate_filepath,
        kmer=21,
        lineage=lineage_path, # Mykrobe requries a path to store the lineage json 
        reference_filepath=reference_filepath
    )

    # Mykrobe doesn't take the probe path as an argumen instead relying on users redirecting standard out with >
    # As such we need to redirect standard out when using the function to the probe path
    os.makedirs(probe_and_lineage_dir, exist_ok=True)
    if probe_lineage_name:
        probes_path = os.path.join(probe_and_lineage_dir, f"{probe_lineage_name}.fa")
    else:
        probes_path = default_probe_path

    with open(probes_path, "w") as f:
        with redirect_stdout(f):  # Redirects all sys.stdout writes
            run_make_variant_probes(None, args)

