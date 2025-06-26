from types import SimpleNamespace as Namespace  
import os
from contextlib import redirect_stdout

from  mykrobe.cmds.amr import run as run_lineage_call

def check_lineage_file(probe_directory,):
    print(f"check_lineage_file at {probe_directory}/lineage.json")

def run_mykrobe_lineage_call(probe_directory, !sequence_path, ):
    check_lineage_file(probe_directory)

    args = Namespace(
        species="custom",
        report_all_calls=True,
        tmp=None,
        ont=False,
        sqe=sequence_path,
        kmer=21,
        force=False,
        threads=2,
        skeleton_dir= ,
        memory= ,
        sample= ,
        expected_error_rate= ,
        filters= ,
        min_variant_conf= , 
        min_gene_conf= ,
        model= , 
        min_proportion_expected_depth= ,
        ploidy= ,
        conf_percent_cutoff= , 
        min_depth= ,
        ignore_minor_calls= ,
        keep_tmp= ,
        ncbi_names= ,
    )


    run_lineage_call(None,args)
