#!/bin/bash
#PBS -P MYCOB
#PBS -l select=1:ncpus=2:mem=2000GB
#PBS -l walltime=120:00:00
#PBS -M vanessa.marcelino@sydney.edu.au
#PBS -m ae

cd $PBS_O_WORKDIR

# kma version 1.1.7 (the one we used in the benchmarking)
PATH=$PATH:/home/vros8020/FGEN_project/programs/kma/

# Whole ncbi nt (clean)
kma_index -i nt_w_taxid.fas -o ncbi_nt_cami -NI -Sparse TG

