#!/bin/bash
#PBS -P MYCOB
#PBS -l select=1:ncpus=1:mem=250GB
#PBS -l walltime=2:00:00
#PBS -M vanessa.marcelino@sydney.edu.au
#PBS -m ae

cd $PBS_O_WORKDIR

module load python/3.6.5

python rename_clean_nt.py

# input files (coded in python script)
# acc2taxid_map="accession2taxid_clean.map"
# nt_in="nt_sequential.fa"