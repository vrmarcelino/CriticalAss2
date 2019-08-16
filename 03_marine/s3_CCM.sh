#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=1:mem=100GB
#PBS -l walltime=4:00:00

# using new 'clean' database and newest version of CCMetagen (v.1.2.3)
# also using old kma (KMA-1.1.7)

cd $PBS_O_WORKDIR

PATH=$PATH:/home/vros8020/FGEN_project/programs/CCMetagen_v1.1.3
PATH=$PATH:/home/vros8020/FGEN_project/programs/KronaTools-2.7/bin
module load python/3.6.5

input_dir=02_KMA
output_dir=03_CCMetagen

mkdir $output_dir

for r12 in $input_dir/*.res; do
	o_part1=$output_dir/${r12/$input_dir\//''}
	o=${o_part1/.res/}
	echo "$o"
	CCMetagen.py -i $r12 -o $o
done


CCMetagen_merge.py -i 03_CCMetagen -o all_samples_and_taxa_marine # only used to verify results

CCMetagen_merge.py -i 03_CCMetagen -kr r -tlist Mammalia,Insecta,Oomycetes -l Class -o all_samples_marine_only # final results





