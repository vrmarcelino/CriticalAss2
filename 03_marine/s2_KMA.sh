#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=4:mem=600GB
#PBS -l walltime=120:00:00

# using new 'clean' database and newest version of CCMetagen (v.1.2.3)
# also using old kma (KMA-1.1.7)

cd $PBS_O_WORKDIR

PATH=$PATH:/home/vros8020/FGEN_project/programs/kma/

th=4

nt_db=../CAMI_nt/nt_kma_1.1.7/ncbi_nt_cami

input_dir=01_QualityControl
output_dir=02_KMA

mkdir $output_dir

for r1 in $input_dir/*.R1_good; do
	r2=${r1/.R1_good/.R2_good}
	o_part1=$output_dir/${r1/$input_dir\//''}
	o=${o_part1/.R1_good/}
	echo "$o"
	kma -ipe $r1 $r2 -o $o -t_db $nt_db -t $th -1t1 -mem_mode -and -apm f
done

