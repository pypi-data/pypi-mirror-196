#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle
from subprocess import Popen, getstatusoutput
from operator import itemgetter
import gc
gc.enable()


## check for numpy dependency
try:
    import numpy as np
except:
    print('\n\nnumpy is a dependency for this script\nit can be installed from:\nWindows:\nhttp://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy\nMac:\nhttp://sourceforge.net/projects/numpy/files/NumPy/\nLinux:\nhttps://launchpad.net/~scipy/+archive/ppa\n\n\n')
    
import numpy as np
from scipy.stats import mannwhitneyu as mw
    

## check for matplotlib
if '-no_graphs' in sys.argv:
    no_matplot_lib=True
    pass
else:
    print('\n\nmatplotlib is a dependency for graphs produced by this script\nit can be installed from:\nhttp://matplotlib.org/downloads.html\n\n\n')
    from matplotlib import use
    use('Agg')
    no_matplot_lib=False
    import matplotlib.pyplot as plt




###############
## basic function library
def read_file(tempFile,linesOraw):
    print('reading',tempFile)
    f=open(tempFile,'r')
    if linesOraw=='lines':
        lines=f.readlines()
        for i in range(0,len(lines)):
            lines[i]=lines[i].strip('\n')
    elif linesOraw=='raw':
        lines=f.read()
    f.close()
    return(lines)

def make_file(contents,path):
    f=open(path,'w')
    if isinstance(contents,list):
	    f.writelines(contents)
    elif isinstance(contents,str):
	    f.write(contents)
    f.close()

    
def flatten_2D_table(table,delim):
    #print(type(table))
    if str(type(table))=="<class 'numpy.ndarray'>":
        out=[]
        for i in range(0,len(table)):
            out.append([])
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    out[i].append(str(table[i][j]))
            out[i]=delim.join(out[i])+'\n'
        return(out)
    else:
        for i in range(0,len(table)):
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    table[i][j]=str(table[i][j])
            table[i]=delim.join(table[i])+'\n'
    #print(table[0])
        return(table)

def make_table(lines,delim):
    for i in range(0,len(lines)):
        lines[i]=lines[i].strip()
        lines[i]=lines[i].split(delim)
        for j in range(0,len(lines[i])):
            try:
                float(lines[i][j])
            except:
                lines[i][j]=lines[i][j].replace('"','')
            else:
                lines[i][j]=float(lines[i][j])
    return(lines)

def import_dict(f):
    f=open(f,'rb')
    d=pickle.load(f)
    f.close()
    return(d)

def save_dict(d,path):
    f=open(path,'wb')
    pickle.dump(d,f)
    f.close()

def cmd(in_message):
    Popen(in_message,shell=True).communicate()

###############




## options#############################

if '-h' in sys.argv or '--help' in sys.argv:
    print(
        """PyMINEr can be used in one of three ways

-------------------------------------------------
Method1:
    PyMINEr will run the MINE analysis and feed the output directly in
    for network analysis
    
or

Method2:
    PyMINEr can be used with pre-generated MINE outputs
    * this assumes MINE outputs have already been filtered *
    * to an appropriate MIC cutoff                         *

or

Method3:
    do not perform network analysis, only return the mine analysis
    for a one group input.
-------------------------------------------------
Usage for Method1:

python3 PyMINEr_[version].py -infile <raw_data_file.txt>
                             -dividing_col <int>
                             -MineDir <path> [options]
Options:
    -infile <data file>         This file contains all raw data formatted in the format below:
                                IDs     Group1_rep1     Group1_rep2 ... Group2_rep1     Group2_rep2 ...
                                Var1    12.3            13.2        ... 7.8             5.9         ...
                                Var2    6.8             7.1         ... 5.3             6.7         ...
                                ...
    -t < int >=2 >              Number of the number of available threads to be used for MINE analysis
                                *default is 2*
    -mem <int>                  Available memory in gigs per thread being used *default is 24*
    -MineDir <path>             Path to MINE.jar
    -MIC_cutoff <decimal float> All relationships below this cutoff will be thrown out
                                and cannot be recovered
                                *note "-MIC_cutoff1" and "-MIC_cutoff2" can also be
                                used instead to specify different
                                *cutoffs for the two groups
                                *this will be especially needed when the two groups have
                                different n, and different False Postive Rate (FPR)
    -microarray                 This option will make PyMINEr treat the input as
                                post-normalization microarray data, and will search
                                for "!series_matrix_table_begin" for the beginning of
                                the table
    -disease <str>              This variable specifies what the name of the disease
                                or treatment is for the second group
                                (past the -dividing_col) *default is "disease"*
    -control <str>              An alternative name for the control *default is "control"*
    -MINE_only                  This will prevent performing the network comparisions
                                and only return final variable-variable interaction MINE
                                output for each group
    -clean                      Cleans up temporary files created by running mine
                                (there are quite a few, but good to have when troubleshooting)
                                *off by default*
    -log_fold                   This changes the values for the fold changes to the
                                natural log of the ratio between group1 controls and
                                group2 diseased/treated: Ln(mean(diseased)/mean(treated))
                                *only applicable if graphs are being made*
    -no_graphs                  This option specifies that no graphs should be created,
                                only summary files
    -out_relationship_mat_only  Only returns a 2D matrix of interactions for both
                                control and diseased/treated
    -rainbow                    This option specifies that for graphs creaed including
                                expression as a variable the points should be rainbow
                                color-coded with blue as decreased expression, and
                                red as increased expression in the second group relative
                                to the first
                                *on by default*
    -no_rainbow                 Instead of the rainbow option, all points will be a
                                semi-transparent black
    -dpi                        Dpi for figures.  Default is 360
    -log_expression             Changes axis title of figures to include Log2;
                                this should be used if input data is log2 transformed
    -mannwhit                   Will additionally perform mann whitney comparisions
                                for all variables between groups and return
                                the uncorrected p-value as an additional column in the
                                expression summary file
    -express_only               Performs only the expression analysis
    -no_express                 Minimizes the amount of expression analysis performed

    ### cluster computing options ###
    # Clusters which support load balancing thread passing (such as openSSI)
    # should not need these options.
    # Cluster computing requiring submission to queue via "qsub" are currenly
    # the only supported cluster computing format.
    #
    # Note that these options will create a new master_cluster_sub.sh file
    # which will need to be run by command line with "sh master_cluster_sub.sh"
    # This is required because many clusters do not allow additional submission
    # spawning from compute nodes
    
    -cluster                    This option tells PyMINEr that the MINE relationship
                                detection will be done using cluster computing
    -sub_prefix                 This is a path to a file that may contain the header
                                for qsub submissions.  This file may contain email options,
                                memory options, parallele environment options,
                                package imports, etc..
    -tpsub                      This abbreviation stands for "threads per submission"
                                which will indicate how many threads should be given to each
                                *This in conjunction will the -t option will let PyMINEr
                                *know how many submissions to make via qsub

-------------------------------------------------
Usage for Method2:

python3 PyMINEr_[version].py -infile <raw_data_file.txt>
                             -dividing_col <int>
                             -in_mine1 <mine_output_control>
                             -in_mine2 <mine_output_diseased-treated>
                             [options]

Options:
    -infile <data file>         This file contains all raw data formatted in the format below:
                                IDs     Group1_rep1     Group1_rep2 ... Group2_rep1     Group2_rep2 ...
                                Var1    12.3            13.2        ... 7.8             5.9         ...
                                Var2    6.8             7.1         ... 5.3             6.7         ...
                                ...
                                *Note that formatting may be different for microarray option*
    -dividing_col <int>         Column which separates control and treated data
                                (index starts at 0)
                                (Thus number should also == the number of replicates in group1)
    -in_mine1 <path>            Mine output file for control.csv
    -in_mine2 <path>            Mine output file for diseased or treated.csv
    -microarray                 this option will make PyMINEr treat the input as
                                post-normalization microarray data, and will search for
                                "!series_matrix_table_begin" for the beginning of
                                the table
    -disease <str>              This variable specifies what the name of the disease
                                or treatment is for the second group
                                (past the -dividing_col) *default is "disease"*
    -control <str>              An alternative name for the control *default is "control"*
    -log_fold                   This changes the values for the fold changes to the
                                natural log of the ratio between group1 controls and
                                group2 diseased/treated: Ln(mean(diseased)/mean(treated))
                                *only applicable if graphs are being made*
    -no_graphs                  This option specifies that no graphs should be created,
                                only summary files
    -out_relationship_mat_only  Only returns a 2D matrix of interactions for both
                                control and diseased/treated
    -rainbow                    This option specifies that for graphs creaed including
                                expression as a variable the points should be rainbow
                                color-coded with blue as decreased expression, and red
                                as increased expression in the second group relative
                                to the first group
                                *on by default*
    -no_rainbow                 Instead of the rainbow option, all points will be a
                                semi-transparent black
    -dpi                        Dpi for figures.  Default is 360
    -log_expression             Changes axis title of figures to include Log2 - should
                                be used if input data is log2 transformed
    -mannwhit                   Will additionally perform mann whitney comparisions
                                for all variables between groups and return the
                                uncorrected p-value as an additional column in the
                                expression summary file
    -express_only               Performs only the expression analysis
    -no_express                 Minimizes the amount of expression analysis performed

-------------------------------------------------
*note - if mine1 and mine2 files are provided, PyMINEr will not run a new MINE
analysis on the input data*
-------------------------------------------------

Usage for Method3:

python3 PyMINEr_[version].py -infile <raw_data_file.txt>
                             -MineDir <path>
                             -single_network
                             [options]

    -t < int >=2 >              Number of the number of available threads to be used
                                for MINE analysis
    -mem <int>                  Available memory in gigs per thread being used
                                *default is 24*
    -MineDir <path>             Path to MINE.jar (will try ~/MINE.jar by default)
    -MIC_cutoff <decimal float> All relationships below this cutoff will be thrown
                                out and cannot be recovered
    -microarray                 This option will make PyMINEr treat the input as
                                post-normalization microarray data, and will search
                                for "!series_matrix_table_begin" for the beginning of
                                the table
    -no_express                 Minimizes the amount of expression analysis performed
    -single_network             The -single_network option indicates that there is
                                only one group and the network comparision should not
                                be done, but the MINE analysis to discover relationships
                                should still be performed

    ### cluster computing options ###
    # Clusters which support load balancing thread passing (such as openSSI)
    # should not need these options.
    # Cluster computing requiring submission to queue via "qsub" are currenly
    # the only supported cluster computing format.
    #
    # Note that these options will create a new master_cluster_sub.sh file
    # which will need to be run by command line with "sh master_cluster_sub.sh"
    # This is required because many clusters do not allow additional submission
    # spawning from compute nodes
    
    -cluster                    This option tells PyMINEr that the MINE relationship
                                detection will be done using cluster computing
    -sub_prefix                 This is a path to a file that may contain the header
                                for qsub submissions.  This file may contain email options,
                                memory options, parallele environment options,
                                package imports, etc..
    -tpsub                      This abbreviation stands for "threads per submission"
                                which will indicate how many threads should be given to each
                                *This in conjunction will the -t option will let PyMINEr
                                *know how many submissions to make via qsub

-------------------------------------------------

major dependencies are:
MINE.jar    downloadable at exploredata.net
python3     downloadable at python.org
numpy       downloadable at scipy.org/scipylib/download.html
matplotlib  required only for graphing
            downloadable at matplotlib.org/downloads.html

*note - these must all be installed in the python3 library directory,*
*not another version of python's library directory*

""")






##########################################
## parse input arguments

## check if programs are in in the $PATH variable
status, result = getstatusoutput('PyMINEr.py')
print(status)
if status==1:## called without arguments PyMINEr.py will result in a 1 exit status
    add_python3=False
else:## if PyMINEr.py is called, but is not in the path it will exit with a different (non-zero) status number
    add_python3=True
print('add_python3',add_python3)

    



if '-pyminer' in sys.argv:
    pyminer_location=str(sys.argv[sys.argv.index('-pyminer')+1]+' ')
else:
    pyminer_location='PyMINEr.py '
    
if add_python3:
    PyMINEr_message_to_pass='python3 '
else:
    PyMINEr_message_to_pass=''


PyMINEr_message_to_pass+=pyminer_location


## continue option is not yet supported
if '-continue_MINE' in sys.argv:
    continue_mine=True
else:
    continue_mine=False
###



if '-in_mine1' in sys.argv:
    sys.exit('this pipeline is required only for determining the appropriate\nMIC cutoffs prior to creating the mine files')
if '-in_mine2' in sys.argv:
    sys.exit('this pipeline is required only for determining the appropriate\nMIC cutoffs prior to creating the mine files')
if '-dividing_col' in sys.argv:
    dividing_col=int(sys.argv[sys.argv.index('-dividing_col')+1])
    if '-single_network' in sys.argv:
        sys.exit('-dividing_col cannot be used with -single_network')
else:
    dividing_col=False# index starting at 0 ## temporary - will throw error
    if '-single_network' not in sys.argv:
        sys.exit('the user must specify if the input is a single network or two')
if '-infile' in sys.argv:
    infile=sys.argv[sys.argv.index('-infile')+1]
    PyMINEr_message_to_pass+=' -infile '+infile
else:
    sys.exit('-infile is a required argument\n\nUse the -h or --help option for usage instructions')
if '-mem' in sys.argv:
    AvailableMemInGig=sys.argv[sys.argv.index('-mem')+1]
else:
    AvailableMemInGig=24
if '-MineDir' in sys.argv:
    MineDir=sys.argv[sys.argv.index('-MineDir')+1]
else:
    MineDir='~/MINE.jar'
if '-MIC_cutoff' in sys.argv:
    MIC_cutoff1=sys.argv[sys.argv.index('-MIC_cutoff')+1]
    MIC_cutoff2=sys.argv[sys.argv.index('-MIC_cutoff')+1]
else:
    MIC_cutoff1=.8
    MIC_cutoff2=.8
if '-MIC_cutoff1' in sys.argv:
    MIC_cutoff1=sys.argv[sys.argv.index('-MIC_cutoff1')+1]
if '-MIC_cutoff2' in sys.argv:
    MIC_cutoff2=sys.argv[sys.argv.index('-MIC_cutoff2')+1]

if '-microarray' in sys.argv:
    microarray=True
    PyMINEr_message_to_pass+=' -microarray'
else:
    microarray=False
if '-disease' in sys.argv:
    disease=sys.argv[sys.argv.index('-disease')+1]
    PyMINEr_message_to_pass+=' -disease '+disease
else:
    disease='group2'
if '-control' in sys.argv:
    control_name=sys.argv[sys.argv.index('-control')+1]
    PyMINEr_message_to_pass+=' -control '+control_name
else:
    control_name='group1'
if '-log_fold' in sys.argv:
    log_fold=True
    PyMINEr_message_to_pass+=' -log_fold'
else:
    log_fold=False
    
if '-log_expression' in sys.argv:
    log_expression=True
    PyMINEr_message_to_pass+=' -log_expression'
if '-no_graphs' in sys.argv:
    no_graphs=True
    PyMINEr_message_to_pass+=' -no_graphs'
else:
    no_graphs=False
    if no_matplot_lib:
        sys.exit("""
either the -no_graphs option should be selected or you must install
matplotlib from http://matplotlib.org/downloads.html
* note - the installation must be in the python3 library, not python2 *""")
if '-no_rainbow' in sys.argv:
    rainbow=False
    PyMINEr_message_to_pass+=' -no_rainbow'
else:
    rainbow=True
if '-t' in sys.argv:
    t=int(sys.argv[sys.argv.index('-t')+1])
else:
    t=2
PyMINEr_message_to_pass+=' -t '+str(t)+' '
if '-MINE_only' in sys.argv:
    mineOnly=True
    PyMINEr_message_to_pass+=' -MINE_only '
else:
    mineOnly=False
if '-dpi' in sys.argv:
    dpi_in=int(sys.argv[sys.argv.index('-dpi')+1])
    PyMINEr_message_to_pass+=' -dpi '+str(dpi_in)
else:
    dpi_in=360
if '-clean' in sys.argv:
    clean=True
    PyMINEr_message_to_pass+=' -clean'
else:
    clean=False
if '-mannwhit' in sys.argv:
    mannwhit=True
    PyMINEr_message_to_pass+=' -mannwhit '
else:
    mannwhit=False
if '-express_only' in sys.argv:
    express_only=True
    PyMINEr_message_to_pass+=' -express_only'
else:
    express_only=False
if '-no_express' in sys.argv:
    no_express=True
    PyMINEr_message_to_pass+=' -no_express'
else:
    no_express=False
if '-single_network' in sys.argv:
    single_network=True
else:
    single_network=False
if '-cluster' in sys.argv:
    cluster=True
    PyMINEr_message_to_pass+=' -cluster '
else:
    cluster=False
if '-sub_prefix' in sys.argv:
    sub_prefix_text=read_file(sys.argv[sys.argv.index('-sub_prefix')+1],'raw')
    PyMINEr_message_to_pass+='-sub_prefix '+str(tpsub)
else:
    if cluster:
        sub_prefix_text='#!/bin/bash'

if cluster:
    sub_prefix_text+='\n'


if '-tpsub' in sys.argv:
    tpsub=int(sys.argv[sys.argv.index('-tpsub')+1])
    PyMINEr_message_to_pass+=' -tpsub '+str(tpsub)
else:
    tpsub=t
if '-page_ranks' in sys.argv:
    PyMINEr_message_to_pass+=' -page_ranks'
    page_ranks=True
    if '-pr_iters' in sys.argv:
        pr_iters=int(sys.argv[sys.argv.index('-pr_iters')+1])
        PyMINEr_message_to_pass+=' -pr_iters ' + str(pr_iters)
    else:
        pr_iters=50 ## this is a totally arbitrary default
    if '-pr_alpha' in sys.argv:
        pr_alpha=float(sys.argv[sys.argv.index('-pr_alpha')+1])
        PyMINEr_message_to_pass+=' -pr_alpha ' + str(pr_alpha)
    else:
        pr_alpha=0.85
else:
    page_ranks=False

if '-weighted_analysis' in sys.argv:
    weighted_analysis=True
    PyMINEr_message_to_pass+=' -weighted_analysis '
else:
    weighted_analysis=False


#################### bootstrap variables ############################3
if add_python3:
    make_bootstrap_file_cmd='python3 '
else:
    make_bootstrap_file_cmd=''

if '-create_boot_file_script' in sys.argv:
    make_bootstrap_file_cmd+=str(sys.argv[sys.argv.index('-create_boot_file_script')+1]+' ')
else:
    make_bootstrap_file_cmd+="create_within_group_boot.py "
    #sys.exit('-create_boot_file_script is a required argument\nthis pipeline needs to know where the "create_within_group_boot_vX.XX.py" script is')

if '-single_network' in sys.argv:
    single_network=True
    dividing_col=0
    make_bootstrap_file_cmd+='-single_network '
    PyMINEr_message_to_pass+='-single_network '
else:
    single_network=False

if '-dividing_col' in sys.argv:
    dividing_col=int(sys.argv[sys.argv.index('-dividing_col')+1])
    make_bootstrap_file_cmd+='-dividing_col '+str(dividing_col)+' '
else:
    if not single_network:
        sys.exit('-diving_col is a required argument when -single_network is not in use')

if '-infile' in sys.argv:
    infile=sys.argv[sys.argv.index('-infile')+1]
    make_bootstrap_file_cmd+='-infile '+infile+' '
else:
    ##temporary
    ##infile='/media/extra_data/matrix_analysis/data/negative_control_bootstrap/within_group_bootstrap/GSE38609-GPL10558_series_matrix.txt'
    sys.exit('-infile is a required argument\n\nUse the -h or --help option for usage instructions')

if '-microarray' in sys.argv:
    microarray=True
    make_bootstrap_file_cmd+='-microarray '
    PyMINEr_message_to_pass+='-microarray '
else:
    microarray=False

if '-num' in sys.argv:
    number_of_arrays_to_return=int(sys.argv[sys.argv.index('-num')+1])
    make_bootstrap_file_cmd+='-num '+str(number_of_arrays_to_return)+' '
else:
    number_of_arrays_to_return=1
    #number_of_arrays_to_return=10

if '-seed' in sys.argv:## seed for randomizing
    change_seed=int(sys.argv[sys.argv.index('-infile')+1])
    seed(change_seed)
    make_bootstrap_file_cmd+='-seed '+str(change_seed)+' '
else:
    pass

PyMINEr_message_to_pass+=' -MineDir '+MineDir

###############################################################################################################################
##############             first step is to create the bootstrap shuffled input file                ###########################
###############################################################################################################################





##############################################################################################################################
#############                                           write call log                                  ######################
##############################################################################################################################

temp_directory=infile.split('/')
temp_directory=temp_directory[:-1]
temp_directory='/'.join(temp_directory)

make_file(' '.join(sys.argv),temp_directory+'/pyminer_pipeline_call.txt')

##############################################################################################################################
#############                       run PyMINEr on the within group bootstrap file                      ######################
##############################################################################################################################


if add_python3:
    pyminer_boot_cmd='python3 '+pyminer_location
else:
    pyminer_boot_cmd=pyminer_location



if single_network:
    pyminer_boot_cmd+=' -single_network'
else:
    pyminer_boot_cmd+=' -dividing_col '+str(dividing_col)
pyminer_boot_cmd+=' -no_express'
pyminer_boot_cmd+=' -no_graphs'
pyminer_boot_cmd+=' -no_page_ranks'
pyminer_boot_cmd+=' -t '+str(t)
pyminer_boot_cmd+=' -mem '+str(AvailableMemInGig)
pyminer_boot_cmd+=' -infile '+temp_directory+'/boot_1/within_group_boot_1.txt'
pyminer_boot_cmd+=' -control '+control_name+'_boot_1'
pyminer_boot_cmd+=' -disease '+disease+'_boot_1'
pyminer_boot_cmd+=' -MineDir '+MineDir
pyminer_boot_cmd+=' -MIC_cutoff '+str(0.05)### this should be made an option, but I haven't gotten to it yet








##############################################################################################################################
#############               find the MIC cutoff for each group that gives the desired FPR               ######################
##############################################################################################################################

if add_python3:
    FPR_script_cmd='python3 '
else:
    FPR_script_cmd=''


if '-FPR_curve_script' in sys.argv:
    FPR_script_cmd+=sys.argv[sys.argv.index('-FPR_curve_script')+1]
else:
    FPR_script_cmd+='FPR_curve_script.py'
#    sys.exit("""-FPR_curve_script is a requirement for this pipeline, 
#             if the appropriate MIC cutoffs have already been determined, for the desired
#             false positive rate, those MICs should be fed into PyMINEr directly,
#             the PyMINEr_pipeline is only for streamlining the boostrapping
#             and false positive rate MIC cutoff, then calling PyMINEr with them""")


if '-FPR' in sys.argv:
    fpr=float(eval(sys.argv[sys.argv.index('-FPR')+1]))
else:
    sys.exit("""-FPR is a requirement for this pipeline, 
             if the appropriate MIC cutoffs have already been determined, for the desired
             false positive rate, those MICs should be fed into PyMINEr directly,
             the PyMINEr_pipeline is only for streamlining the boostrapping
             and false positive rate MIC cutoff, then piping those to PyMINEr""")

FPR_script_cmd+=' -FPR_target '+str(fpr)
FPR_script_cmd+=' -infile '+temp_directory+'/boot_1/within_group_boot_1.txt'
FPR_script_cmd+=' -FPR_mine1 '+temp_directory+'/boot_1/'+control_name+'_boot_1_final_relationship_summary.tsv'
if not single_network:
    FPR_script_cmd+=' -FPR_mine2 '+temp_directory+'/boot_1/'+disease+'_boot_1_final_relationship_summary.tsv'
    FPR_script_cmd+=' -group2_name '+disease+' -dpi '+str(dpi_in)
FPR_script_cmd+=' -group1_name '+control_name






##############################################################################################################################################################
##############################################################################################################################################################
########################################                       start running the pipeline                  ###################################################
##############################################################################################################################################################
##############################################################################################################################################################



print('\n\n\n',make_bootstrap_file_cmd)
print('\n\n\n',pyminer_boot_cmd)
print('\n\n\n',FPR_script_cmd)
#sys.exit()

print('\n\n\n',make_bootstrap_file_cmd)
time.sleep(5)
cmd(make_bootstrap_file_cmd)


print('\n\n\n',pyminer_boot_cmd)
time.sleep(5)
cmd(pyminer_boot_cmd)


print('\n\n\n',FPR_script_cmd)
time.sleep(5)
cmd(FPR_script_cmd)



######## read in the MIC cutoff value(s)
FPR_to_MIC=read_file(temp_directory+'/boot_1/MIC_for_target_summary.txt','lines')
MIC1=FPR_to_MIC[1].split(' = ')
MIC1=MIC1[1]
print('\n\nMIC_cutoff1 =',MIC1)
PyMINEr_message_to_pass+=' -MIC_cutoff1 '+MIC1

if not single_network:
    MIC2=FPR_to_MIC[3].split(' = ')
    MIC2=MIC2[1]
    print('\n\nMIC_cutoff2 =',MIC2)
    PyMINEr_message_to_pass+=' -MIC_cutoff2 '+MIC2
    


PyMINEr_message_to_pass+=' -infile '+infile
if single_network:
    PyMINEr_message_to_pass+=' -single_network'
else:
    PyMINEr_message_to_pass+=' -dividing_col '+str(dividing_col)

if '-co_regulatory_network' in sys.argv:
    PyMINEr_message_to_pass+=' -co_regulatory_network '

if weighted_analysis:
    PyMINEr_message_to_pass+=' -weighted_analysis '



print('\n\n\n',PyMINEr_message_to_pass,'\n\n\n')
#sys.exit()

cmd(PyMINEr_message_to_pass)










