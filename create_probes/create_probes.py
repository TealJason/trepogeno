import json
import argparse import Namespace
from pathlib import Path
import pandas as pd
from typing import Dict, List
from collections import defaultdict
from Bio import SeqIO
import numpy as np
import logging
import sys

from mykrobe.cmds.makeprobes import run as run_make_variant_probes

#called from main script of genotreponmea
def create_probes_from_type_scheme(reference_coordinate_filepath,lineage,reference_filepath):
    args = Namespace(
    'no-backgrounds'=True,
    'database'=False,
    'vcf''=None,
    'genbank'=None,
    'text_file'=reference_coordinate_filepath
    'kmer'=21,
    'lineage'=lineage,
    'reference_filepath'=reference_filepath
)

    run_make_variant_probes(None,args)


