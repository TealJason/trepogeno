This repo contains scripts that intend to wrap around mykrobe for eventual lineage calling of treponema strains

To set up functionality you must: 
1. cd ..
2. git clone mykrobe/
3.cd mykrobe
4. pip3 install . && mykrobe panels update_metadata && mykrobe panels update_species all
5. cd. ../nextstrain


## genotreponeme
this is the main script, call it with genotreponema.py and provide the relevent arguments

## create_probes
The scripts to impoar and make the correct calls to create mykrobe to create the k-mer probes

## lineage_calling
The scripts to import and make the correct calls to mykrobe for lineage_calling

## mykrobe_pre-processing_scripts
This subdirectory contains scripts that will take a vcf and a lineage cluster csv from pinecone to produce a file suitable for creating a probes and lineage.json with mykrobe.

## mykrobe_post_processing_scripts
This subdirectory contains scripts and information for tabulating and concatenating important information from the the output json files created by mykrobe 

## example command to create probes and lineage files

python -m nextstrain.genotreponema --json_directory files/json_outputs --reference_coordinate files/Tpallidum_Mykrobe_input.SNP.table_all_hierarchies_2025-05-14.tsv --genomic_reference files/reference/nc_021508.fasta.gz --probe_and_lineage_dir files/probes --make_probes

## example command to call a lineage

python -m nextstrain.genotreponema --json_directory files/json_outputs --genomic_reference files/reference/nc_021508.fasta --probe_and_lineage_dir files/probes --lineage_call --seq_manifest /data/pam/team230/jb71/scratch/nexstrain/manifest.csv

## example command to call process and summarise the mykrobe json outputs
python -m nextstrain.genotreponema --json_directory files/json_outputs --tabulate_jsons 