#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=1:mem=100GB
#PBS -l walltime=48:00:00
#PBS -M vanessa.marcelino@sydney.edu.au
#PBS -m ae

cd $PBS_O_WORKDIR

gunzip nt.gz

awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);} END {printf("\n");}' < nt > nt_sequential.fa
