#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert CCMetagen results to CAMI format

@ V.R.Marcelino
Created on Fri Aug  9 09:19:47 2019

"""
import pandas as pd
from argparse import ArgumentParser
from ete3 import NCBITaxa
import cTaxInfo_cami
import fNCBItax_cami
ncbi = NCBITaxa()

parser = ArgumentParser()
parser.add_argument('-i', '--input_fp', help="Path to the input CCM file (.csv)", required=True)
parser.add_argument('-n', '--sample_name', help="sample_name", required=True)
parser.add_argument('-o', '--output_fp', default = 'ccm4cami.profile', 
                    help='Path to the output file. Default = ccm4cami.profile', required=False)

args = parser.parse_args()
in_fp  = args.input_fp
out_fp = args.output_fp
sample_name = args.sample_name


#in_fp = "patmg_CAMI2.csv"
#out_fp = "Sample_x_tax_prof.tsv"

df = pd.read_csv(in_fp, sep=',', index_col=0)


### Takes a taxid (LCA), and return a list of objects with taxids and depth for all macthes and tax ranks:
lineage_list = []

for index, row in df.iterrows():
    match_info = cTaxInfo_cami.TaxInfo()
    match_info.TaxId = int(row['LCA_TaxId'])
    match_info.Depth = float(row['Depth'])
    match_info = fNCBItax_cami.lineage_extractor(match_info.TaxId, match_info)
    lineage_list.append(match_info)



### convert the list to a dataframe, with one line per row:
all_data = []
info = ['Depth',"superkingdom_taxid","phylum_taxid","class_taxid", \
                     "order_taxid","family_taxid","genus_taxid","species_taxid", \
                     "superkingdom","phylum","class","order","family","genus","species"]
all_data.append(info)
    
for match_info in lineage_list:
    all_data.append([match_info.Depth,match_info.Superkingdom_TaxId,match_info.Phylum_TaxId, \
                  match_info.Class_TaxId,match_info.Order_TaxId,match_info.Family_TaxId, \
                  match_info.Genus_TaxId, match_info.Species_TaxId, \
                  match_info.Superkingdom, match_info.Phylum, match_info.Class, \
                  match_info.Order, match_info.Family,match_info.Genus,match_info.Species])

    
# convert to pandas dataframe
all_data_df = pd.DataFrame(all_data)
all_data_df.columns = all_data_df.iloc[0] #name columns
all_data_df = all_data_df.drop(0) #remove col names
all_data_df = all_data_df.fillna("NA") # this is needed because groupby excludes rows with NAs 


### Output to table in a organised way:

# general info:
total_depth = sum(all_data_df['Depth'])

organised = []
organised.append(["@@TAXID","RANK","TAXPATH","TAXPATHSN","PERCENTAGE"])

f4agg = {}
f4agg['Depth']= 'sum'


# Superkingdom #
f4agg['superkingdom_taxid'] = 'first'
f4agg['superkingdom'] = 'first'

depth_by_tax = all_data_df.groupby(by=("superkingdom_taxid","superkingdom")).agg(f4agg)

for index, row in depth_by_tax.iterrows():
    taxpath = str(row['superkingdom_taxid']) 
    taxpathsn = row['superkingdom']
    perc = row['Depth'] * 100 / total_depth
    perc = round(perc, 6)
    new_line = [row['superkingdom_taxid'],'superkingdom',taxpath,taxpathsn,perc] 
    organised.append(new_line)


# Phylum #
f4agg['phylum_taxid'] = 'first'
f4agg['phylum'] = 'first'

depth_by_tax = all_data_df.groupby(by=("superkingdom_taxid","phylum_taxid","superkingdom","phylum")).agg(f4agg)

for index, row in depth_by_tax.iterrows():
    if 'unk_' in row['phylum']:
        print ("skipping %s in %s" %(row['phylum'],row['superkingdom']))
    else:
        taxpath = str(row['superkingdom_taxid']) + "|" + str(row['phylum_taxid'])
        taxpathsn = row['superkingdom'] + "|" + row['phylum']
        perc = row['Depth'] * 100 / total_depth
        perc = round(perc, 6)
        new_line = [row['phylum_taxid'],'phylum',taxpath,taxpathsn,perc] 
        organised.append(new_line)


# Class #
f4agg['class_taxid'] = 'first'
f4agg['class'] = 'first'

taxa = list(f4agg.keys())
taxa.pop(0)

depth_by_tax = all_data_df.groupby(by=taxa).agg(f4agg)

for index, row in depth_by_tax.iterrows():
    if 'unk_' in row['class']:
        print ("skipping %s in %s" %(row['class'],row['phylum']))
    else:
        taxpath = str(row['superkingdom_taxid']) + "|" + str(row['phylum_taxid']) + \
        "|" + str(row['class_taxid'])
        taxpathsn = row['superkingdom'] + "|" + row['phylum']+  "|" + str(row['class'])
        perc = row['Depth'] * 100 / total_depth
        perc = round(perc, 6)
        new_line = [row['class_taxid'],'class',taxpath,taxpathsn,perc] 
        organised.append(new_line)

# Order #
f4agg['order_taxid'] = 'first'
f4agg['order'] = 'first'

taxa = list(f4agg.keys())
taxa.pop(0)

depth_by_tax = all_data_df.groupby(by=taxa).agg(f4agg)

for index, row in depth_by_tax.iterrows():
    if 'unk_' in row['order']:
        print ("skipping %s in %s" %(row['order'],row['class']))
    else:
        taxpath = str(row['superkingdom_taxid']) + "|" + str(row['phylum_taxid']) + \
        "|" + str(row['class_taxid']) + "|" + str(row['order_taxid'])
        taxpathsn = row['superkingdom'] + "|" + row['phylum']+  "|" + str(row['class']) + \
        "|" + str(row['order'])
        perc = row['Depth'] * 100 / total_depth
        perc = round(perc, 6)
        new_line = [row['order_taxid'],'order',taxpath,taxpathsn,perc] 
        organised.append(new_line)


# Family #
f4agg['family_taxid'] = 'first'
f4agg['family'] = 'first'

taxa = list(f4agg.keys())
taxa.pop(0)

depth_by_tax = all_data_df.groupby(by=taxa).agg(f4agg)

for index, row in depth_by_tax.iterrows():
    if 'unk_' in row['family']:
        print ("skipping %s in %s" %(row['family'],row['order']))
    else:
        taxpath = str(row['superkingdom_taxid']) + "|" + str(row['phylum_taxid']) + \
        "|" + str(row['class_taxid']) + "|" + str(row['order_taxid'])+  "|" +  \
        str(row['family_taxid'])
        taxpathsn = row['superkingdom'] + "|" + row['phylum']+  "|" + str(row['class']) + \
        "|" + str(row['order']) + "|" + str(row['family'])
        perc = row['Depth'] * 100 / total_depth
        perc = round(perc, 6)
        new_line = [row['family_taxid'],'family',taxpath,taxpathsn,perc] 
        organised.append(new_line)


# Genus #
f4agg['genus_taxid'] = 'first'
f4agg['genus'] = 'first'

taxa = list(f4agg.keys())
taxa.pop(0)

depth_by_tax = all_data_df.groupby(by=taxa).agg(f4agg)

for index, row in depth_by_tax.iterrows():
    if 'unk_' in row['genus']:
        print ("skipping %s in %s" %(row['genus'],row['family']))
    else:
        taxpath = str(row['superkingdom_taxid']) + "|" + str(row['phylum_taxid']) + \
        "|" + str(row['class_taxid']) + "|" + str(row['order_taxid'])+  "|" +  \
        str(row['family_taxid']) + "|" + str(row['genus_taxid'])
        taxpathsn = row['superkingdom'] + "|" + row['phylum']+  "|" + str(row['class']) + \
        "|" + str(row['order']) + "|" + str(row['family']) + "|" + str(row['genus'])
        perc = row['Depth'] * 100 / total_depth
        perc = round(perc, 6)
        new_line = [row['genus_taxid'],'genus',taxpath,taxpathsn,perc] 
        organised.append(new_line)

# Species #
f4agg['species_taxid'] = 'first'
f4agg['species'] = 'first'

taxa = list(f4agg.keys())
taxa.pop(0)

depth_by_tax = all_data_df.groupby(by=taxa).agg(f4agg)

for index, row in depth_by_tax.iterrows():
    if 'unk_' in row['species']:
        print ("skipping %s in %s" %(row['species'],row['genus']))
    else:
        taxpath = str(row['superkingdom_taxid']) + "|" + str(row['phylum_taxid']) + \
        "|" + str(row['class_taxid']) + "|" + str(row['order_taxid'])+  "|" +  \
        str(row['family_taxid']) + "|" + str(row['genus_taxid']) + "|" + str(row['species_taxid'])
        taxpathsn = row['superkingdom'] + "|" + row['phylum']+  "|" + str(row['class']) + \
        "|" + str(row['order']) + "|" + str(row['family']) + "|" + str(row['genus']) + "|" + str(row['species'])
        perc = row['Depth'] * 100 / total_depth
        perc = round(perc, 6)
        new_line = [row['species_taxid'],'species',taxpath,taxpathsn,perc] 
        organised.append(new_line)



#### convert to dataframe and save
organised_df = pd.DataFrame(organised)

#### Remove all unk_x and None (taxid) from the table:
organised_df = organised_df.replace('NA','', regex= True)
organised_df = organised_df.replace('(unk_.+?)\|','|', regex= True)


#### File header
header = []
header.append("# Taxonomic Profiling Output")
sample_ID_line = "@SampleID:" + sample_name
header.append(sample_ID_line)
header.append("@Version:1.1.3")
header.append("@Ranks:superkingdom|phylum|class|order|family|genus|species")
header.append("@TaxonomyID:ncbi-taxonomy_2019_01_08")


#### Merge and save:
complete_table = pd.concat([pd.DataFrame(header), organised_df], ignore_index=True)
complete_table.to_csv(out_fp, sep = "\t", header=False, index=False)

print ("Dooone!")

