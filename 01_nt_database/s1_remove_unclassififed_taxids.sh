#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=1:mem=60GB
#PBS -l walltime=48:00:00
#PBS -M vanessa.marcelino@sydney.edu.au
#PBS -m ae

cd $PBS_O_WORKDIR

module load python/3.6.5

python remove_unclassififed_from_acc2taxidmap.py

