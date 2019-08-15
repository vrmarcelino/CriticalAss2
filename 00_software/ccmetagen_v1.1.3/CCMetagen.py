#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCMetagen main script


@ V.R.Marcelino
Created on Wed Jul 25 17:13:10 2018

"""

version_numb = 'v1.1.3'

# imports
import sys
import pandas as pd
from argparse import ArgumentParser
import subprocess
from ete3 import NCBITaxa

# local imports
from ccmetagen import fParseKMA
from ccmetagen import cTaxInfo # needed in fParseKMA
from ccmetagen import fNCBItax # needed in fParseKMA

# help
if len(sys.argv) == 1:
    print ("")
    print ("CCMetagen - Identify species in metagenome datasets")
    print (version_numb)
    print ("To be used with KMA")
    print ("")
    print ("Usage: CCMetagen.py <options> ")
    print ("Ex: CCMetagen.py -i KMA_out/2_mtg.res -o 2_mtg_result")
    print ("")
    print ("")
    print ("""When running CCMetagen on multiple files in a folder:
input_dir=KMA_out
output_dir=CCMetagen_results
mkdir $output_dir
for f in $input_dir/*.res; do
    out=$output_dir/${f/$input_dir\/}
    CCMetagen.py -i $f -o $out
done""")
    print ("")
    print ("For help and options, type: CCMetagen.py -h")
    print ("")
    print ("")
    sys.exit()


parser = ArgumentParser()

parser.add_argument('-m', '--mode', default = 'both',
                    help="""what do you want CCMetagen to do?
                    Valid options are 'visual', 'text' or 'both':
                        text: parses kma, filters based on quality and output a text file with taxonomic information and detailed mapping information
                        visual: parses kma, filters based on quality and output a simplified text file and a krona html file for visualization
                        both: outputs both text and visual file formats. Default = both""", required=False)

parser.add_argument('-i', '--res_fp', help='Path to the KMA result (.res file)', required=True)
parser.add_argument('-o', '--output_fp', default = 'CCMetagen_out',
                    help='Path to the output file. Default = CCMetagen_out', required=False)
parser.add_argument('-r', '--reference_database', default = 'nt',
                    help='Which reference database was used. Options: UNITE, RefSeq or nt. Default = nt', required=False)

parser.add_argument('-du', '--depth_unit', default = 'kma',
                    help="""Desired unit for Depth(abundance) measurmeents.
                    Default = kma (KMA default depth, which is the number of nucleotides overlapping each template,
                    divided by the lengh of the template).
                    Alternatively, you can simply count the number of nucleotides overlaping the template (option 'nc')
                    If you use the 'nc' option, remember to change the default --depth parameter accordingly for more accurate results.
                    Valid options are nc and kma""", required=False)
parser.add_argument('-d', '--depth', default = 0.2,
                    help="""minimum sequencing depth. Default = 0.2.
                    If you use --depth_unit nc, change this accordingly. For example, -d 200 (200 nucleotides) 
                    is similar to -d 0.2 when using the default '--depth_unit kma' option.""",type=float, required=False)

parser.add_argument('-c', '--coverage', default = 20,
                    help='Minimum coverage. Default = 20',type=float, required=False)
parser.add_argument('-q', '--query_identity', default = 50,
                    help='Minimum query identity (Phylum level). Default = 50', type=float, required=False)
parser.add_argument('-p', '--pvalue', default = 0.05,
                    help='Minimum p-value. Default = 0.05.',type=float, required=False)

# similarity thresholds:
parser.add_argument('-st', '--species_threshold', default = 98.41,
                    help='Species-level similarity threshold. Default = 98.41',type=float, required=False)
parser.add_argument('-gt', '--genus_threshold', default = 96.31,
                    help='Genus-level similarity threshold. Default = 96.31',type=float, required=False)
parser.add_argument('-ft', '--family_threshold', default = 88.51,
                    help='Family-level similarity threshold. Default = 88.51',type=float, required=False)
parser.add_argument('-ot', '--order_threshold', default = 81.21,
                    help='Order-level similarity threshold. Default = 81.21',type=float, required=False)
parser.add_argument('-ct', '--class_threshold', default = 80.91,
                    help='Class-level similarity threshold. Default = 80.91',type=float, required=False)
parser.add_argument('-pt', '--phylum_threshold', default = 0,
                    help='Phylum-level similarity threshold. Default = 0 - not applied',type=float, required=False)
parser.add_argument('-off', '--turn_off_sim_thresholds', default = 'n',
                    help='Turns simularity-based filtering off. Options = y or n. Default = n', required=False)

parser.add_argument('--version', action='version', version=version_numb)

args = parser.parse_args()


mode = args.mode
f = args.res_fp
ref_database = args.reference_database
c = args.coverage
q = args.query_identity
du = args.depth_unit
d = args.depth
p = args.pvalue

# taxononomic thresholds:
off = args.turn_off_sim_thresholds

if off == 'y':
    st = 0
    gt = 0
    ft = 0
    ot = 0
    ct = 0
    pt = 0

elif off == 'n':
    st = args.species_threshold
    gt = args.genus_threshold
    ft = args.family_threshold
    ot = args.order_threshold
    ct = args.class_threshold
    pt = args.phylum_threshold

else:
    print ("-off argument should be either y or n. ")
    sys.exit("Try again.")

# developing and debugging:
#args.output_fp = "CCMetagen_nt_results"
#f = "2_mtg_nt_test.res"
#ref_database = "nt"
#mode = 'both'
#c = 20
#q = 50
#d = 0.2
#p = 0.05
#st = 99
#gt = 98
#ft = 95
#ot = 80
#ct = 0
#pt = 0
#du = 'kma'

## Run implicitly ete3.NCBITaxa.__init__() to check for valid taxonomy database
NCBITaxa()

# Warning if RefDatabase is unknown
if ref_database not in ("UNITE", "RefSeq","nt"):
    print (""" Reference database (-r) must be either UNITE, RefSeq or nt.
           the input is case sensitive and the default is nt.""")
    sys.exit("Try again.")


### Read input files and output a pandas dataframe
print ("")
print ("Reading file %s" %(f))
print ("")

df = pd.read_csv(f, sep='\t', index_col=0, encoding='latin1')

# Rename headers:
df.index.name = "Closest_match"

# adjust depth to reflect number of bases:
if du == 'nc':
    df['Depth'] = df.Depth * df.Template_length
    print ("calculating depth as number of nucleotides, ignoring template length")
    print ("""remember to adjust minimum depth value (ex: -d 200). """)
elif du == 'kma':
    print ("")
else:
    print ("--depth_unit option must be nc or kma. Treating it as 'kma'.")
    print ("")


# first quality filter (coverage, query identity, Depth and p-value)
df = fParseKMA.res_filter(df, ref_database, c, q, d, p)

# add tax info
df = fParseKMA.populate_w_tax(df, ref_database, st, gt, ft, ot, ct, pt)


##### Output a file with tax info
if (mode == 'text') or (mode == 'both'):

    # save to file
    out = args.output_fp + ".csv"
    pd.DataFrame.to_csv(df, out)

    print ("csv file saved as %s" %(out))
    print ("")

##### Output a Krona file
if (mode == 'visual') or (mode == 'both'):
    krona_info = df[['Depth','Superkingdom','Kingdom','Phylum','Class','Order','Family','Genus','Species']]

    # remove the unk_xx for better krona representation
    krona_info = krona_info.replace('unk_.*$', value = '',regex=True)

    # save dataframe to file
    out1 = args.output_fp + ".tsv"
    pd.DataFrame.to_csv(krona_info, out1, sep='\t', index=False, header=False)

    # save krona file
    out2 = args.output_fp + ".html"

    shell_command = "ktImportText " + out1 + " -o " + out2
    subprocess.run(shell_command, shell=True)

    print ("krona file saved as %s" %(out2))
    print ("")
