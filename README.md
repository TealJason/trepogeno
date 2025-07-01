This repo contains scripts that intend to wrap around mykrobe for eventual lineage calling of treponema strains

To set up functionality you must: 
1. cd ..
2. git clone mykrobe/
3. cd mykrobe
4. pip3 install . && mykrobe panels update_metadata && mykrobe panels update_species all
5. cd. ../nextstrain

If having problems with cannot find "mccortex31" expected to find it at "path/mccortex31" try the below

1. cd mykrobe
2. git clone --recursive -b geno_kmer_count https://github.com/Mykrobe-tools/mccortex mccortex
3. cd mccortex
4. make
5. cp bin/mccortex31 /path/mykrobe/expected/

## Genotreponema
This is the main script, call it with python -m nextstrain.genotreponema and provide the relevent arguments

## create_typing_scheme
This subdirectory contains scripts that with a vcf and reference could be used to semi-automate the process of screating a 
typing scheme for later probe creation and lineage file creation for lineage calling.

## example command to create probes and lineage files

python -m nextstrain.genotreponema --json_directory files/json_outputs --reference_coordinate files/Tpallidum_Mykrobe_input.SNP.table_all_hierarchies_2025-05-14.tsv --genomic_reference files/reference/nc_021508.fasta.gz --probe_and_lineage_dir files/probes --make_probes

## example command to call a lineage

python -m nextstrain.genotreponema --json_directory files/json_outputs --genomic_reference files/reference/nc_021508.fasta --probe_and_lineage_dir files/probes --lineage_call --seq_manifest /data/pam/team230/jb71/scratch/nexstrain/manifest.csv

## example command to call process and summarise the mykrobe json outputs
python -m nextstrain.genotreponema --json_directory files/json_outputs --tabulate_jsons 