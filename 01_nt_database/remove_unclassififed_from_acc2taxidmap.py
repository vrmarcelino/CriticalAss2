#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove taxids from unclassiffied organisms from accession2taxid.map
@ V.R.Marcelino
Created on Wed Jun 19 09:35:25 2019 (NCBItaxonomy updated)
"""

from ete3 import NCBITaxa
ncbi = NCBITaxa()

input_acc2taxid = "accession_taxid_nucl.map"



## taxids_two_exclude:

descendants_artificial = ncbi.get_descendant_taxa(28384) # 14882 taxids

descendants_env_euks = ncbi.get_descendant_taxa(61964) # 295 taxids

descendants_env_proks = ncbi.get_descendant_taxa(48479) # 26083

descendants_unclassified_seq = ncbi.get_descendant_taxa(12908) # 942


# join all ists
all_unclassified = descendants_artificial + descendants_env_euks + descendants_env_proks + descendants_unclassified_seq



# write line sthat are not in the list to a new file:
new_acc2taxid = open('accession2taxid_clean.map', 'w')
with open(input_acc2taxid) as ass:
    next(ass) #skip first line
    for line in ass:
        if int(line.split('\t')[1]) in all_unclassified:
            pass
        else:
            new_acc2taxid.write(line)
        
new_acc2taxid.close()


print ('Done!')

