# CriticalAss2
Description of the steps used to analyse CAMI II datasets with KMA and CCMetagen.


## Software and dependencies

#### Dependencies:

  * [Python 3.6](https://www.python.org/downloads/)
CCMetagen requires Python modules [pandas (>0.23)](https://pandas.pydata.org/) and [ETE3](http://etetoolkit.org/). The easiest way to install these modules is via conda or pip:

`conda install pandas`

  * You need a C-compiler and zlib development files to install KMA:

`sudo apt-get install libz-dev`


  * [Krona](https://github.com/marbl/Krona) is required for graphs in CCMetagen. They are not used in these datasets, but it will return an error if not installed. If you don;t want to install krona, you can run CCMetagen with the flag -m text,w hich will not affect the results.

```
wget https://github.com/marbl/Krona/releases/download/v2.7/KronaTools-2.7.tar
tar xvf KronaTools-2.7.tar 
cd  KronaTools-2.7
./install.pl --prefix . 
```

#### Read mapping and taxonomic assignment:

 * Read mapper: [KMA](https://bitbucket.org/genomicepidemiology/kma) version 1.1.7.

 * Taxonomic organizaion: [CCMetagen](https://github.com/vrmarcelino/CCMetagen) version 1.1.3.
These versions can also be found in the folder [00_software](https://github.com/vrmarcelino/CriticalAss2/tree/master/00_software), and kma needs to be installed with `make`.


#### Quality control:

For the pathogen challenge, I used [KneadData](http://huttenhower.sph.harvard.edu/kneaddata) v0.6.1 to filter out human and low quality sequences.
kneaddata used Bowtie2 v.2.2.5 and Trimmomatic v.0.38.

I used the human transcriptome (hg38) reference database to filter out human reads, which can be downloaded as: `kneaddata_database --download human_transcriptome bowtie2 $DIR`. 

For the marine challenge, I used Trimmomatic v.0.38.



## Database construction

After downloading the NCBI nt database as of 2019/01/08 and the NCBI accession to taxid mapping as of 2019/01/08 from the CAMI website, these steps were followed:

All PBS scripts and custom python scripts can be found in the [01_nt_database folder](https://github.com/vrmarcelino/CriticalAss2/tree/master/01_nt_database).

1: Remove entries from nt without a taxid from the accession2taxonomy NCBI file using a custom python script (remove_unclassififed_from_acc2taxidmap.py).
2: Convert the interleaved fasta to sequential fasta.
3: Add a taxid to the nt sequence headers, excluding sequences that do not have a taxid with rename_clean_nt.py
4: Built a KMA index

Again - commands for each of these steps are given [here](https://github.com/vrmarcelino/CriticalAss2/tree/master/01_nt_database).



## Pathogen challenge

Step 1: Run kneaddata:






