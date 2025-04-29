This repo contains  scripts for creating a basic coordinate-file with lineages for mykrobes lineage calling.  
Mykrobe requires the output  from make_lineage_reference_file.py to make its probes.fa and lineage.json files via the `mykrobe variants make-probes` command.  
The outputs from this are then used in lineage calling with the `mykrobe predict` command.  
This script requires a vcf and the *.pinecone.bootstrap.table.csv from rPinecone which has clusters and lineags assignments to samples.  


# create_matrix_from_vcf.py:
## Function:
This script creates a 'snp matrix' from a vcf file where genomic positions are the columns while the index column are samples.
the value will contain either the ref or alt alelle dependent on if a 0 or 1 is in the first position in the vcf

this file is used in the 'extract_leage_defining_snps.py' script 

### Argument Example 
--vcf path/2025-01-31_masked_snps.vcf (Required)

### Output
snp_matrix.csv

# extract_lineage_defining_snps.py:
## Function
This script takes a vcf and the "snp matrix" from create_matrix_from_vcf.py and uses it to deterime which snps in which genomic positions define the lineages defined by rPinecone.

### Argument Example 
--snp_csv path/snp_matrix.csv (Required)
--cluster_file path/PineCone2-2.pinecone.bootstrap.table.csv (Required)
--output . (Requried)
--pinecone_threshold 95 (Optional, default is 50 can enter values 95, 80, 50, 20, or 5)

### Output
lineage_defining_snps.csv

# reference_coordinate_file.py:
## Function:
This script take a vcf a produces a reference coordinates file as detailed in:
https://github.com/Mykrobe-tools/mykrobe/wiki/Custom-Panels

### Argument Example 
--vcf path/2025-01-31_masked_snps.vcf (Required)

### Output
reference_coordinates.txt

Output file structure:
```
ref	1000	A	T	DNA	
ref	2000	C	A	DNA
ref	3000	G	C	DNA	
ref	4000	T	A	DNA	
```
# make_lineage_reference_file.py:
## Function: 
This takes the reference coordinates file from reference_coordinate_file.py and adds lineage data taken from a rPinecone bootstrap.table.csv output:
further details can be found here:
https://github.com/Mykrobe-tools/mykrobe/wiki/Custom-Lineage-Calling

### Argument Example 
--reference_coordinate path/reference_coordinates.txt (Required)
--lineage_defining_snps path/lineage_defining_snps.csv(Required)
--output . (Required)

### Output
lineage_coordonate_output.txt

```
ref	1000	A	T	DNA	lineage1
ref	2000	C	A	DNA	lineage1.1
ref	3000	G	C	DNA	lineage1.2
ref	4000	T	A	DNA	lineage2
```