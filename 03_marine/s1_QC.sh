#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=10:mem=90GB
#PBS -l walltime=24:00:00

cd $PBS_O_WORKDIR

module load trimmomatic

# parameters:
th=10 # threads
input_dir=reads
output_dir=01_QualityControl
mkdir $output_dir

# first deinterleave files:
for r12 in $input_dir/marmgCAMI2_short_read*; do
	o=${r12/.fq/}
	bash z_deinterleave_fastq.sh < $r12 $o.R1.fq $o.R2.fq
done

# then run trimmomatic for QC:
for r1 in $input_dir/*reads.R1.fq; do
	r2=${r1/reads.R1.fq/reads.R2.fq}
	o_part1=$output_dir/${r1/$input_dir\//''}
	o=${o_part1/_reads.R1.fq/}
	echo "$o"
	trimmomatic PE -threads $th -phred33 $r1 $r2 $o.R1_good $o.R1_unpaired $o.R2_good $o.R2_unpaired SLIDINGWINDOW:4:20 MINLEN:70
done

