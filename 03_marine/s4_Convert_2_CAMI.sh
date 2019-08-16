#!/bin/bash
#PBS -P MYCOB
#PBS -l select=1:ncpus=1:mem=100GB
#PBS -l walltime=10:00:00


cd $PBS_O_WORKDIR

module load python/3.6.5
PATH=$PATH:/home/vros8020/scratches/11_CAMI2/marine/convertion_scrips

input_dir=03_CCMetagen
output_dir=04_Results2Submit

mkdir $output_dir


## Remove taxa filtered out in CCMetagen_merge (Mammalia,Insecta,Oomycetes), keeping a backup file with original contents (.bak)
## Original files also saved in dropbox
#for r12 in $input_dir/*.csv; do
#	sed -i.bak '/Mammalia,/d' $r12
#	sed -i '/Oomycetes,/d' $r12
#	sed -i '/Insecta,/d' $r12
#done


## Now convert to CAMI2 format:
for r12 in $input_dir/*.csv; do
	o_part1=$output_dir/${r12/$input_dir\//''}
	o=${o_part1/.csv/.profile}
	sample_name=${r12/$input_dir\//''}
	echo "$o"
	ccm2cami.py -i $r12 -n $sample_name -o $o
done

