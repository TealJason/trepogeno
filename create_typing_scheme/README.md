# THESE SCRIPTS ARE STANDALONE FROM THE MAIN WORK FLOW
# The following scripts are _one_ way you can make a lineage_coordinate/typing-scheme file required by mykrobe
# There is a premade tpying scheme in the main repo you can use  
# This describes one method in which to produce similar scheme should you have a vcf you wish to use

This repo contains  scripts for creating a basic coordinate-file with lineages for mykrobes lineage calling.  
Mykrobe requires the output from create_full_reference_coordinate_file to make its probes.fa and lineage.json files via the `mykrobe variants make-probes` command.  
The outputs from the make-probes command are used for lineage calling with `mykrobe predict`.  
These scripts require a vcf and the .pinecone.bootstrap.table.csv from rPinecone which has clusters and lineage cluster assignments against samples.  
Whith these the scripts can work out which snps define a lineage my checking which snps are present in all members of a lineage cluster while being absent from all other samples.

# create_probes.sh
## Function:
This is a bash script that will execute the below two scripts in order and will then run mykrobe make-probes automatically, this is offered as a streamlined way to process the files and create mykrobe probes and lineage file for calling.
The script require a path to the vcf, path to the pinecone clusters file, pinecone threshold number, and a path to the reference fasta of the same sample used in the vcf. 

### Argument Example
./create_probes.sh  
-v /data/pam/team230/jb71/scratch/NextStrain/files/2025-01-31_masked_snps.vcf  
-c /data/pam/team230/jb71/scratch/NextStrain/rPinecone/Results/rPineCone20-5.pinecone.bootstrap.table.csv  
-p 95  
-r /data/pam/team230/jb71/scratch/NextStrain/files/reference/NC/nc_021508.fasta  

### Output
lineage_defining_snps.csv (see below).  
lineage_coordinate_output.txt (see below).  
test_probes.fa (mykrobe probes file used for lineage calling).  
lineage95.json (mykrobe lineage fine used for lineage calling).  


# create_matrix_get_lineage_defining_snps.py.py:
## Function:
This script creates a 'snp matrix' from a vcf file where genomic positions are the columns while the index column are samples.
the value will contain either the ref or alt alelle dependent on if a 0 or 1 is in the first position in the vcf
It will then takes the vcf and the "snp matrix" from and use them to deterime which snps in which genomic positions define the lineage cluters calculated by rPinecone.

### Argument Example 
--vcf path/2025-01-31_masked_snps.vcf (Required)  
--cluster_file path/PineCone2-2.pinecone.bootstrap.table.csv (Required)  
--output . (Requried)  
--pinecone_threshold 95 (Optional, default is 50 will only work with values 95, 80, 50, 20, or 5)  

### Output
lineage_defining_snps.csv

```
Cluster, SNP_Position, Allele
    671,       651723, A
    671,       657912, T
    671,       994070, C
    723,        24485, A
    723,       290357, T
    723,       699367, A
    723,       785674, A
```

# create_full_reference_coordinate_file.py:
## Function:
This script takes a vcf, path to the previously created lineage defining snp file, pinecone lineage clusters csv, as well as optionally a pinecone threshold and output path/name. It produces a reference coordinate file as detailed in with lineages annotating the fine dependent on which snp define them.
further details can be found here:
https://github.com/Mykrobe-tools/mykrobe/wiki/Custom-Panels
https://github.com/Mykrobe-tools/mykrobe/wiki/Custom-Lineage-Calling

### Argument Example 
--vcf path/2025-01-31_masked_snps.vcf (Required)  
--lineage_defining_snps path/lineage_defining_snps.csv(Required)  
--cluster_file path/PineCone2-2.pinecone.bootstrap.table.csv (Required)  
--pinecone_threshold 95 (Optional, default is 50 only works with values 95, 80, 50, 20, or 5)  
--output lineage_coordinate_output.txt (Optional, default is './lineage_coordinate_output.txt')  

### Output
lineage_coordinate_output.txt

```
ref	1000	A	T	DNA	lineage1
ref	2000	C	A	DNA	lineage1.1
ref	3000	G	C	DNA	lineage1.2
ref	4000	T	A	DNA	lineage2
```

#### Improvements
This script as of yet is not considering a situation where all samples carry the alternative allele against reference used in the vcf which may be lineage defining. 