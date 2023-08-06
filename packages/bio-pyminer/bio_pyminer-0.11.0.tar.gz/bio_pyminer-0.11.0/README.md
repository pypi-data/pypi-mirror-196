# README #

### Tutorials ###

I've made some videos that walk you through the outputs as well as how to install and use PyMINEr here:
www.ScienceScott.com/pyminer

### What is this repository for? ###

* cell type identification using novel clustering algorithms that outperform some competitors when applied to both real-world and synthetic datasets
* basic statistics & enrichment analyses
* pathway analyses
* Spearman correlation-based expression graphs that enable analyses by graph theory 
* creation of in silico predicted autocrine/paracrine signaling networks within and across cell types
* creation of publication-ready visuals based on these analyses
* generation of a web page explaining the results of the run

* Future releases will contain updated clustering methods that work for reconstructing single cell lineages, among other cool functions 

### How do I get set up? ###

PyMINEr is now pip installable:
`python3 -m pip install bio-pyminer`
Note that there was another package called pyminer for mining bit-coin - this is definitely not that, so be sure to install bio-pyminer instead!

You can also install using the setup.py script in the distribution like so:
`python3 setup.py install`


### How do I run PyMINEr? ###
#### Video Tutorials ####
There are some video tutorials over [here](https://www.sciencescott.com/pyminer)! But if you just want the cliff-est of cliff-notes, there's a brief description below, for using an AnnData object, like you would with Scanpy. Or using tab delimited files, or hdf5 files as input in the section below that.

#### Using Scanpy or AnnData as an interface? ####
After you've filtered out low quality cells, normalized, and log transformed your data, it's ready to be run with PyMINEr!
```
from pyminer.pyminer import pyminer_analysis
pm_analysis = pyminer_analysis(adata=adata,
				               analysis_dir = "pyminer_analysis/",
				               louvain_clust = True,
				               sc_clust=True)

```
This yields you a pyminer results object that should be very easy to navigate and explore because the help and descriptions are built into the print function!
```
>>> print(pm_analysis)
PyMINEr object:

Each of the elements contained within the PyMINEr object is it's own class
		You can print each of these objects to get the help section on it.
	<object>.gene_anno: an object that contains tables annotating the input genes
	<object>.clust: This object has lots of info on the clusters, differential 
		expression, pathway analysis, etc. just do print(<object>.clust) to get the details!
	<object>.goi: If you used genes of interest, the direcotry of the output 
		plots and the shortest-paths of all other genes to them are located here.
	<object>.network: The co-expression network and details on gene-module 
		usage, module pathway analysis, etc
	<object>.ap: Details of the autocrine/paracrine signaling between clusters 
		and pathway analysis of those signaling networks.

There is also the PyMINEr website file that provides a walk-through of the results:
/home/scott/Downloads/temp/pyminer_analysis/PyMINEr_summary.html
```
However, as noted in the last line above, we also have an easy to navigate web-browser that lets you explore the analysis, just look for the "PyMINEr_summary.html" file in the analysis_dir!


#### With a tab-delimited text file as input ####
PyMINEr takes as input a cleaned and normalized (typically log transformed) tab delimited 2D matrix text file.
For example:

    genes	cell_1	cell_2	...
    ACTB   5.3012	 6.3102	...
    ...	...	...	...

You can feed this text file into PyMINEr in the command line:

`pyminer.py -i expression.txt`

If you have a really big file, you can convert it to hdf5 so that you can run the pipeline outside of memory:

`tab_to_h5.py expression.txt`

This will generate 3 files:
* *expression.hdf5* 
* *ID_list.txt* the list of genes (no header line)
* *column_IDs.txt* the sample names for the columns.

That's about it. There are some other interesting things you can do though, like if you are working with something that isn't human, you should be able to pass in the argument -species, 
followed by a species code that is taken by gProfiler. This will automate tons of pathway analyses, so long as the variables you're working with can be mapped over to Ensembl gene IDs by gProfiler.
The default is homo sapiens (hsapiens).

A list of the gProfiler accepted species codes is listed here: https://biit.cs.ut.ee/gprofiler/page/organism-list

### License ###
For non-commercial use, PyMINEr is available via the AGPLv3 license. Commercial entities should inquire with scottyler89@gmail.com

### Who do I talk to? ###

* Repo owner/admin: scottyler89+bitbucket@gmail.com