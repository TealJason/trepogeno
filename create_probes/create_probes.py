# This script is called from the main script of genotreponema
from types import SimpleNamespace as Namespace  
import os
from contextlib import redirect_stdout

#mykrobe functions
from mykrobe.cmds.makeprobes import run as run_make_variant_probes
def create_probes(lineage,reference_coordinate_filepath, reference_filepath,probe_and_lineage_dir):
    args = Namespace(
        no_backgrounds=True,
        database=False,
        vcf=None,
        genbank=None,
        text_file=reference_coordinate_filepath,
        kmer=21,
        lineage=lineage,
        reference_filepath=reference_filepath
    )
    os.makedirs(probe_and_lineage_dir, exist_ok=True)
    probes_path = os.path.join(probe_and_lineage_dir, "probes.fa")

    with open(probes_path, "w") as f:
        with redirect_stdout(f):  # Redirects all sys.stdout writes
            run_make_variant_probes(None, args)

