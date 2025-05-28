## Tabulate 
## Function:
This script is made for the purpose of collecting the json files produced by mykrobe collating important information and outputting it in a more human readable readible and condensed form.

### Argument Example

python3 tabulate_json.py --json_directory /path/to/json/files/directory/ --check_all

#### Internal
This nested dictionary structure is created internally during procesing. 
Each json file is a top level key with each containing sets of dictionaries for each lineage that had support
If the flag --check_all is set the script creates a dictionary and checks how many snps were called for every lineage not just the lineages  with support
```
   single_sample_dictionary_full = { 
        ERR9768236{ 
            TPE"{ 
                calls_made:668,possible_calls:700 
            }, 
            TPE.1.3{ 
                calls_made:0,possible_calls:90 
            } 
            ... 
        }, 
        SRR14277265{ 
            TPE"{ 
                calls_made:1,possible_calls:700 
            }, 
            TPE.1.3{ 
                calls_made:0,possible_calls:0 
            } 
            ... 
        } 
    } 
```
### Output

Simple table:

Sample_id   |Lineage |Calls made |Possible calls| 
----------- |--------|-----------|--------------|
SRR14277265 |TPE     |  33       |      42      |     
----------- |--------|-----------|--------------|
ERR9768236  |TPE.3.1 |  30       |      38      |