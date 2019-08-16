#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=6:mem=100GB
#PBS -l walltime=12:00:00
#PBS -M vanessa.marcelino@sydney.edu.au
#PBS -m ae

cd $PBS_O_WORKDIR

#load knead
PATH=$PATH:/home/vros8020/.local/bin/
module load trimmomatic
module load bowtie2

# parameters:
th=6 # threads
process=4

r1=00_reads/patmg_CAMI2_short_read_R1.fastq.gz
r2=00_reads/patmg_CAMI2_short_read_R2.fastq.gz

db=/home/vros8020/FGEN_project/databases/kneadData/knead_human/

output_dir=01_QualityControl
mkdir $output_dir

kneaddata -i $r1 -i $r2 -o $output_dir/patmg_CAMI2_QCd -db $db -t $th -p $process


mv 01_QualityControl/patmg_CAMI2_QCd/patmg_CAMI2_short_read_R1_kneaddata_paired_1.fastq 01_QualityControl/patmg_CAMI2_QCd_R1.fq
mv 01_QualityControl/patmg_CAMI2_QCd/patmg_CAMI2_short_read_R1_kneaddata_paired_2.fastq 01_QualityControl/patmg_CAMI2_QCd_R2.fq
