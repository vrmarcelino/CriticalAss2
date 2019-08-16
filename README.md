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

 * The aligner [KMA](https://bitbucket.org/genomicepidemiology/kma) version 1.1.7

 * [CCMetagen](https://github.com/vrmarcelino/CCMetagen) version 1.1.3
These versions can also be found in the folder [00_software](https://github.com/vrmarcelino/CriticalAss2/tree/master/00_software), and kma needs to be installed with `make`.


#### Quality control:

For the pathogen challenge, I used [KneadData](http://huttenhower.sph.harvard.edu/kneaddata) v0.6.1 to filter out human and low quality sequences.
kneaddata used Bowtie2 v.2.2.5 and Trimmomatic v.0.38.

I used the human transcriptome (hg38) reference database to filter out human reads, which can be downloaded as: `kneaddata_database --download human_transcriptome bowtie2 $DIR`. 

For the marine challenge, I used Trimmomatic v.0.38.



## Database



