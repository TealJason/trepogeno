from types import SimpleNamespace as Namespace  
import os
from contextlib import redirect_stdout

from  mykrobe.cmds.amr import run as run_lineage_call

def check_lineage_file(probe_directory,):
    print(f"check_lineage_file at {probe_directory}/lineage.json")

def get_sequence(line):
    ID,seqeunce1, sequence2 = line.splt(",")
    return ID,seqeunce1, sequence2 

def run_mykrobe_lineage_call(probe_directory, sequence_manifest):
    check_lineage_file(probe_directory)

    with open (sequence_manifest,"r") as manifest:
        for line in manifest:
            ID,seqeunce1, sequence2  = get_sequence(line)
            
            args = Namespace(
                species="custom",
                report_all_calls=True,
                tmp=None,
                ont=False,
                seq=[seqeunce1, sequence2], 
                kmer=21,
                force=False,
                threads=2,
                skeleton_dir="data/skeletons/",
                memory="1GB" ,
                sample=ID,
                filters=["MISSING_WT", "LOW_PERCENT_COVERAGE", "LOW_GT_CONF", "LOW_TOTAL_DEPTH"],
                min_variant_conf=150 , 
                min_gene_conf=1 ,
                model="median_depth" , 
                min_proportion_expected_depth=0.3 ,
                ploidy="diploid",
                conf_percent_cutoff=100 , 
                min_depth=100 ,
                ignore_minor_calls=False ,
                keep_tmp=False ,
                ncbi_names= None,
            )


            run_lineage_call(None,args)
