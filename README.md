This repo contains two scripts one for creating a basic coordinate-file from a vcf and one for adding lineages to this file based on rPinceone outputs.
Mykrobe requires the output file from make_lineage_reference_file.py for making a probes.fa and lineage.json with the `mykrobe variants make-probes` command.
The outputs from this are then used in lineage calling with the `mykrobe predict` command:

# reference_coordinate_file.py:
## Function:
This script take a vcf a produces a reference coordinates file as detailed in:
https://github.com/Mykrobe-tools/mykrobe/wiki/Custom-Panels

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

Output file structure:
```
ref	1000	A	T	DNA	lineage1
ref	2000	C	A	DNA	lineage1.1
ref	3000	G	C	DNA	lineage1.2
ref	4000	T	A	DNA	lineage2
```