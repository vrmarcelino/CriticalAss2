#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add taxids to nt collection and remove sequences without a valid taxid

@ V.R.Marcelino
Created on 19 June 2019
"""

import re


# input files:
acc2taxid_map="accession2taxid_clean.map"
nt_in="nt_sequential.fa"


# function to  get taxids from accession numbers
def get_tax_id_dic (accession, accession_dic):
    taxid = accession_dic.get(accession)
    if taxid == None:
        taxid = "unk_taxid"
    return taxid


# read acc2taxid.map as dictionary
with open(acc2taxid_map) as a:
    acc2tax_dic = dict(x.rstrip().split(None, 1) for x in a)
    

# read fasta file and output new file on the fly
# although it says 'open', it reads line by line and won't store the whole file in memory.
    
new_nt = open('nt_w_taxid.fas', 'w')

with open(nt_in) as nt:
    for line in nt:
        if line.startswith(">"):
            splited_rec = re.split (r'(>| )', line)
            accession = splited_rec[2]
            taxid = get_tax_id_dic(accession,acc2tax_dic)
            
            if taxid == "unk_taxid":
                pass
            
            else:
                line = ">" + taxid + "|" + "".join(splited_rec[2:])
                new_nt.write(line)
                new_nt.write(next(nt))

new_nt.close()


print ("Done!")


