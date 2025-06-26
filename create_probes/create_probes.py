import json
import argparse
from types import SimpleNamespace as Namespace  # Correct way to mock argparse.Namespace
from pathlib import Path
import pandas as pd
from typing import Dict, List
from collections import defaultdict
from Bio import SeqIO
import numpy as np
import logging
import sys

#mykrobe functions
from mykrobe.cmds.makeprobes import run as run_make_variant_probes

# Called from main script of genotreponema
def create_probes(lineage,reference_coordinate_filepath, reference_filepath):
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

    run_make_variant_probes(None, args)
