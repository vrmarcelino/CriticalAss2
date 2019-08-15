#!/bin/bash
#PBS -P MYCOB
#PBS -l select=1:ncpus=2:mem=1000GB
#PBS -l walltime=120:00:00
#PBS -M vanessa.marcelino@sydney.edu.au
#PBS -m ae

cd $PBS_O_WORKDIR

PATH=$PATH:/home/vros8020/FGEN_project/programs/kma_v1.2.10

# latest kma (KMA-1.2.10a)

# Whole ncbi nt (clean)
time kma index -i nt_w_taxid.fas -o ncbi_nt_cami -NI -Sparse TG

