This repo contains scripts that intend to wrap around mykrobe for eventual lineage calling of treponema strains

To set up functionality you must: 
1. git clone --recusrive https://gitlab.internal.sanger.ac.uk/sanger-pathogens/nextstrain.git
2. cd nextstrain/trepogeno/
3. pip3 install -e . 

If you experience problems with 'cannot find mccortex31 expected to find it at path/expected/mccortex31' try the below

1. cd mykrobe
2. git clone --recursive -b geno_kmer_count https://github.com/Mykrobe-tools/mccortex mccortex
3. cd mccortex
4. make
5. cp bin/mccortex31 /path/mykrobe/expected/

## Genotreponema
This is the main script, call it with python -m nextstrain.genotreponema and provide the relevent arguments

## create_typing_scheme
This subdirectory contains scripts that with a vcf and reference could be used to streamline the process of creating a 
typing scheme for later probe creation and lineage calling.

## example command to create probes and lineage files

trepogeno \
--json_directory files/json_outputs \
--type_scheme files/Tpallidum.SNP.table_hierarchies_2025-05-14.tsv \
--genomic_reference files/reference/nc_021508.fasta \
--probe_and_lineage_dir files/probes \
--make_probes

## example command to call a lineage

trepogeno \
--json_directory files/json_outputs \
--genomic_reference files/reference/nc_021508.fasta \
--probe_and_lineage_dir files/probes \
--seq_manifest /data/pam/team230/jb71/scratch/nexstrain/manifest.csv \
--lineage_call

## example command to call process and summarise the mykrobe json outputs
trepogeno \
--json_directory files/json_outputs \
--tabulate_jsons

## All paramaters 
``` 

Make Probes
-----------
--make_probes
    Used to indicate you wish to generate a new set of probes during the work flow

--type_scheme
    Path to the file that maps snps to specific genomic coordiantes to lineages, to learn more review mykrobe custom lineage calling documentation.

--genomic_reference
    A fasta file that acts as the genomic reference, must match the reference in the type scheme

--probe_and_lineage_dir
    This is the directory in which to save the probe and lineage file during probe creation

--probe_lineage_name
    what to call the probe.fa file and lineage.json when writing an output

Lineage Calling
-----------
--lineage_call
    Used to indicate you wish to call lineages

--json_directory
    A path to the directory for mykrobe to save json files after calling a lineage

--seq_manifest
    A manifest of Sample ID sequences as a CSV, the heading should be ID,Read1,Read2. If you are not using paired end fastqs and only have one Read leave a trailing , e.g. 'ReadID,/fastq/ReadID1.fastq,'

--genomic_reference
    A fasta file that acts as the genomic reference, must match the reference in the type scheme

--probe_and_lineage_dir
    This is the directory in which to save the probe and lineage file during probe creation

--probe_lineage_name
    The name of the probe.fa and lineage.json files


Json Processing
-----------
--tabulate_jsons
    Used to indicate you wish to proccess and tabulate the jsons output by mykrobe

--json_directory
    A path to the directory mykrobe saved its json's for processing

```

