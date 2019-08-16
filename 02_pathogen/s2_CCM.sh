#!/bin/bash
#PBS -P MYCOB
#PBS -l select=1:ncpus=4:mem=500GB
#PBS -l walltime=1:00:00

# using new 'clean' database and newest version of CCMetagen (v.1.1.3)
# also using old kma (KMA-1.1.7)

cd $PBS_O_WORKDIR

PATH=$PATH:/home/vros8020/FGEN_project/programs/kma/
PATH=$PATH:/home/vros8020/FGEN_project/programs/CCMetagen_v1.1.3
PATH=$PATH:/home/vros8020/FGEN_project/programs/KronaTools-2.7/bin
module load python/3.6.5

th=4

nt_db=../CAMI_nt/nt_kma_1.1.7/ncbi_nt_cami


r1=01_QualityControl/patmg_CAMI2_QCd_R1.fq
r2=01_QualityControl/patmg_CAMI2_QCd_R2.fq

mkdir 02_KMA_v1.1.7

kma -ipe $r1 $r2 -o 02_KMA_v1.1.7/patmg_CAMI2 -t_db $nt_db -t $th -1t1 -mem_mode -and -apm f

mkdir -p 03_CCMetagen

CCMetagen.py -i 02_KMA_v1.1.7/patmg_CAMI2.res -o 03_CCMetagen/patmg_CAMI2
CCMetagen_merge.py -i 03_CCMetagen # just to check, not used
CCMetagen_merge.py -i 03_CCMetagen -kr r -tlist Eukaryota -l Superkingdom -o microbial_taxa # final taxa





