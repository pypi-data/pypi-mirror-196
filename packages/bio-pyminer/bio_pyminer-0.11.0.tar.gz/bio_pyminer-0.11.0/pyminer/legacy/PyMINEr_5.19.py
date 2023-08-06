#!/usr/bin/env python3
############################################################################
version = '5.19'

print('\nPyMINEr.py version',version,'\n')

credits = """
PyMINEr is freely available for academic purposes, under the AGPLv3 license.

If PyMINEr is used for publication purposes, please cite the following paper:

"""

print(credits)



## notes

"""
Changed in 5.14 from 5.13:
- fix error from title variable when using -no_sample_cluster option
- add option for degree and non-zero median expression

Changed in 5.14 to 5.15:
-fixed an error in -very_big_file

Changed in 5.15 to 5.16:
-fix an error in -very_big_file

Changed in 5.17 and 5.18:
-cleaned up the help section

Changed in 5.18 to 5.19:
-add -big_file_no_z
"""









############################################################################

##import dependency libraries
import sys,time,glob,os,pickle
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
gc.enable()


## check for numpy dependency
try:
    import numpy as np
except:
    print('\n\nnumpy is a dependency for this script\nit can be installed from:\nWindows:\nhttp://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy\nMac:\nhttp://sourceforge.net/projects/numpy/files/NumPy/\nLinux:\nhttps://launchpad.net/~scipy/+archive/ppa\n\n\n')
import scipy
import numpy as np
from scipy.stats import mannwhitneyu as mw
from scipy.linalg import eigh
    
from numpy import linalg
import random
from random import sample

random.seed(12345)
np.random.seed(12345)

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



######################################################################################
###############
## basic function library
def read_file(tempFile,linesOraw,quiet=False):
    if not quiet:
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

def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))

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


def read_table(file, sep='\t'):
    return(make_table(read_file(file,'lines'),sep))
    
def write_table(table, out_file, sep = '\t'):
    make_file(flatten_2D_table(table,sep), out_file)
    

def import_dict(f):
    f=open(f,'rb')
    d=pickle.load(f)
    f.close()
    return(d)

def save_dict(d,path):
    f=open(path,'wb')
    pickle.dump(d,f)
    f.close()

def cmd(in_message, com=True):
    print(in_message)
    time.sleep(.25)
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)

###############
def get_z_from_line(in_line):
    temp_line = strip_split(in_line)
    var=temp_line[0]
    try:
        num_vector = np.array(temp_line[1:],dtype='float32')
    except:
        print("couldn't turn this into a numeric vector:")
        sys.exit(temp_line[1:])
    mean = np.mean(num_vector)
    sd = np.std(num_vector)
    delta = num_vector - mean
    individual_z_scores = delta/sd
    return([var]+list(individual_z_scores))

def get_group_z_from_line(in_line):
    global sample_k_lists
    temp_line = strip_split(in_line)
    var=temp_line[0]
    num_vector = np.array(temp_line[1:],dtype='float32')
    mean = np.mean(num_vector)
    sd = np.std(num_vector)
    z_vector = []
    for i in range(0,len(sample_k_lists)):
        #print(len(sample_k_lists[i]))
        temp_mean = np.mean(num_vector[sample_k_lists[i]])
        delta = temp_mean - mean
        z_vector.append(delta*np.sqrt(len(sample_k_lists[i]))/sd)
    
    individual_z_scores = delta/sd
    return([var]+z_vector)




def find_table_start(table):# returns title line, variable lists, and table matrices
    global dividing_col,microarray, single_network
    if microarray:
        print('reading in microarray data')
        for i in range(0,len(table)):
            if "!series_matrix_table_begin" in table[i]:
                print('table starts on line',i+1)
                title_line=np.array(table[i+1], dtype='U32')
                print('title line')
                print(title_line)
                ID_list=[]
                #print((len(table[i+1:-1]),len(table[i+1][1:])))
                outmat=np.zeros((len(table[i+2:-1]),len(table[i+1][1:])),dtype='f8')
                outmat_index=0
                for j in range(i+2,len(table)):
                    if str(table[j][0])[0]=='!':
                        outmat=outmat[:outmat_index]
                        #print(np.shape(outmat))
                        break
                    ##print(outmat_index)
                    
                    ID_list.append(table[j][0])

                    ##print(np.array(table[j][1:]))
                    ##print(outmat[outmat_index])
                    ##print(ID_list[outmat_index])
                    ##print(table[j][0])
                    ##print(np.array(table[j][1:]))
                    
                    outmat[outmat_index]+=np.array(table[j][1:], dtype='f8')

                    
                    ##except:
                    ##    print(outmat[outmat_index])
                    ##    print(np.array(table[j][1:]))
                    ##    sys.exit()
                    outmat_index+=1
                num_vars = len(ID_list)
                print('outmat_shape:',np.shape(outmat))
                print(len(ID_list),'variables detected')
                print(ID_list[:5])
                
                #print(outmat[:,0])
                group1=np.column_stack((ID_list,outmat[:,:dividing_col].astype('U32')))
                print('group1 data shape is',np.shape(group1)[0],'rows &',np.shape(group1)[1]-1,'cols')## minus 1 because of title line
                print('first line:\n',group1[0])
                print('last line:\n',group1[-1])

                group2=np.column_stack((ID_list,outmat[:,dividing_col:].astype('U32')))
                
                print('group2 data shape is',np.shape(group2)[0],'rows &',np.shape(group2)[1]-1,'cols')## minus 1 because of title line
                print('first line:\n',group2[0])
                print('last line:\n',group2[-1])
                return(title_line,ID_list,outmat[:,:dividing_col],outmat[:,dividing_col:],group1,group2)## +2 because of title row
    else:
        title_line=np.array(table[0])
        ID_list=[]
        outmat=np.zeros((len(table)-1,len(table[0][1:])), dtype='f8')
        outmat_index=0
#        print(table[1])
        for j in range(1,len(table)):
            ID_list.append(table[j][0])
            ##print(np.array(table[j][1:]))
            ##print(outmat[outmat_index])
            outmat[outmat_index]+=np.array(table[j][1:], dtype='f8')
            outmat_index+=1
#        print(outmat[1])
        
        ##outmat=np.array(table[1:])
        ##title_line=np.array(table[0])
        ##ID_list=outmat[:,0]

        #print(list(outmat[0]))
        
        print(len(ID_list),'variables detected')
        ##print('group1:',len(outmat[:,1:dividing_col+1]))
        group1=np.column_stack((ID_list,outmat[:,:dividing_col].astype('U32')))
        print('group1 data shape is',np.shape(group1)[0],'rows &',np.shape(group1)[1],'cols')
        print(group1[0])
        group2=np.column_stack((ID_list,outmat[:,dividing_col:].astype('U32')))
        print('group2 data shape is',len(outmat[:,dividing_col:]),'rows &',len(outmat[0,dividing_col:]),'cols')
        print(group2[0])
        return(title_line,ID_list,outmat[:,1:dividing_col+1],outmat[:,dividing_col+1],group1,group2)## +2 because of title row


## input is for each subpopulation
def slice_table_col_into_2D(table, col, triangle = False):
    ## returns the lower triangle of a matrix var x var
    ## example:
    ## 
    ## for subject A if triangle:
    ##      gene1   gene2   gene3
    ##gene1 [11,11]    0       0
    ##gene2 [11,13] [13,13]
    ##gene3 [11,7]  [13,7]  [7,7]
    ##
    ## else:
    ##      gene1   gene2   gene3
    ##gene1 [11,11] [13,11] [7,11]
    ##gene2 [11,13] [13,13] [7,13]
    ##gene3 [11,7]  [13,7]  [7,7]

    #slice out column
    S=table[:,col]
    
    #multiply by length
    SL=[]
    for i in range(0,len(S)):
        SL.append(S)
    S=np.concatenate(SL)
    del SL
    S=np.reshape(S,(len(L)),len(S))

    if triangle:
        return(np.tril(np.dstack((S.transpose(),S))))
    else:
        return(np.dstack((S.transpose(),S)))


def get_MIC_matrix(out_matrix,interaction_file,column,binaryVcontinuous):## column index begins at 0
    global IDhash
    first_line=True ## begin at 1 because of title line in output MINE file
    for line in fileinput.input(interaction_file):
        if first_line:
            pass
        else:
            
            line = line.split('\t')
            row=IDhash[line[0]]
            col=IDhash[line[1]]
            if binaryVcontinuous=='continuous':
                out_matrix[row][col]=line[column]
                out_matrix[col][row]=line[column]#
            elif binaryVcontinuous=='binary':
                out_matrix[row][col]=1
                out_matrix[col][row]=1#
            else:
                sys.exit('binaryVcontinuous variable must either be "binary" or "continuous", not '+str(binaryVcontinuous))
        first_line = False
    fileinput.close()
    return(out_matrix)


###############
## write program files for running MINE analysis
def write_MINE_scripts(start_row,end_row,mem,MineDir,in_file,index,MIC_cutoff,script_path,status_path):
    print(script_path)
    print(status_path)
    python_commands=str("""
from subprocess import Popen
from time import sleep

##############

def read_file(tempFile,linesOraw):
    print('reading',tempFile)
    f=open(tempFile,'r')
    if linesOraw=='lines':
        lines=f.readlines()
        for i in range(0,len(lines)):
            lines[i]=lines[i].strip('\\n')
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
    print(type(table))
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
            out[i]=delim.join(out[i])+'\\n'
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
            table[i]=delim.join(table[i])+'\\n'
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

def cmd(in_message):
    Popen(in_message,shell=True).communicate()

##############

## run MINE analysis

infile='"""+in_file+"""'
index="""+str(index)+"""

temp_dir=str(infile).split('/')
temp_dir=('/').join(temp_dir[:-1])
transfer=temp_dir+'/transfer'+str(index)+'.txt'
summary=temp_dir+'/summary_'+str(index)+'.txt'
temp_aggregate=temp_dir+'/temp_aggregate_'+str(index)+'.txt'
aggregate_after=100
log_file='"""+script_path+""".log'
make_file("",log_file)
start_row="""+str(start_row)+"""
end_row="""+str(end_row)+"""
count=0

for i in range(start_row,end_row):
    count+=1

    ## concatenate temporary aggregate file with summary file
    if count%aggregate_after==0:
        cmd('cp '+summary+' '+summary+'_temp.txt')## these pass off the files circularly to add the new results to the summary file
        cmd('rm '+summary)
        cmd('cat '+summary+'_temp.txt '+temp_aggregate+'>'+summary)
        cmd('rm '+summary+'_temp.txt')

        ## refresh and regenerate clean temp_aggregate file
        cmd('rm '+temp_aggregate)
        cmd('cat "" > '+temp_aggregate)
    

    ## write status to temp log for this processes
    make_file("working on row "+str(i),log_file)
    
    run_MINE_string=str('java -Xmx'+str("""+str(mem)+""")+'g -jar '+'"""+MineDir+"""'+' """+in_file+"""'+' '+str(i)+' gc=10000 jobID=temp"""+str(index)+""" notify=10000')
    cmd(run_MINE_string)## this line passes run_MINE_string to bash
    
    lines=make_table(read_file('"""+in_file+""",mv='+str(i)+',cv=0.0,B=n^0.6,Results.csv','lines'),',')## this line reads the output
    if len(lines)>1:
        for line in range(1,len(lines)):## this finds where the line in the MINE output where cutoff has been reached
            if lines[line][2]<"""+str(MIC_cutoff)+""":
                break
        make_file(flatten_2D_table(lines[1:line],'\t'),transfer)## makes a temporary transfer file containing the results of the last run that met the cutoff
        cmd('cp '+temp_aggregate+' '+temp_aggregate+'_temp.txt')## these pass off the files circularly to add the new results to the summary file
        cmd('rm '+temp_aggregate)
        cmd('cat '+temp_aggregate+'_temp.txt '+transfer+'>'+temp_aggregate)
        cmd('rm '+temp_aggregate+'_temp.txt')
    cmd('rm '+'"""+in_file+"""'+',mv='+str(i)+',cv=0.0,B=n^0.6,Status.txt')
    cmd('rm '+'"""+in_file+"""'+',mv='+str(i)+',cv=0.0,B=n^0.6,Results.csv')




## append final
cmd('cp '+summary+' '+summary+'_temp.txt')## these pass off the files circularly to add the new results to the summary file
cmd('rm '+summary)
cmd('cat '+summary+'_temp.txt '+temp_aggregate+'>'+summary)
cmd('rm '+summary+'_temp.txt')
cmd('rm '+temp_aggregate)



## write the the 'done' status in the status folder for the original script to read
cmd("echo '"""+script_path+""" finished' >> '"""+status_path+"""'")

make_file("finished rows:\\n"+str(start_row)+" to "+str(end_row),log_file)

""")
    #print(python_commands)
    make_file(python_commands,script_path)

def make_intermediate_script(node_script_list,out_file):
    ## for making the intermediate python scripts which can be called in indivudal
    ## cluster submissions
    temp_script="from subprocess import Popen\nfrom time import sleep\n"
    temp_script+="""
def read_file(tempFile,linesOraw):
    print('reading',tempFile)
    f=open(tempFile,'r')
    if linesOraw=='lines':
        lines=f.readlines()
        for i in range(0,len(lines)):
            lines[i]=lines[i].strip('\\n')
    elif linesOraw=='raw':
        lines=f.read()
    f.close()
    return(lines)
"""
    for s in node_script_list:
        temp_script+='script_list='+str(node_script_list)+'\nPopen("python3 '+s+'",shell=True)\n'
    temp_script+="""\n
still_running=True
while still_running:
    sleep(60)
    still_running=False
    for s in script_list:
        temp_log=read_file(s+'.log','lines')
        if len(temp_log)==1:## The log file will have two lines if it is finished, but only 1 if it is still running
            still_running=True
print('finished with this node')
"""
    make_file(temp_script,out_file)

def linear_normalize(in_list,min_range=0,max_range=1):
    print(in_list)
    in_list=np.array(in_list,dtype='float64')
    print(in_list)
    in_list=in_list-np.amin(in_list)
    print(in_list)
    in_list=in_list+min_range
    print(in_list)
    in_list=in_list/np.amax(in_list)
    print(in_list)
    in_list=in_list*max_range
    print(in_list)
    return(in_list)

def lin_norm_rows(in_mat,min_range=0,max_range=1):
    in_mat = np.transpose(np.array(in_mat))
    in_mat = in_mat - np.min(in_mat, axis = 0)
    in_mat = in_mat / np.max(in_mat, axis = 0)
    return(np.transpose(in_mat))

######################################################################################


######################################################################################

## options#############################

if '-h' in sys.argv or '--help' in sys.argv:
    print(
        """For Spearman correlations:
PyMINEr.py -infile ~/Downloads/PyMINEr_package/examples/wine.txt -spearman -FPR 1e-6 [Options]

For MINE relationships:
pyminer_pipeline.py -infile ~/Downloads/PyMINEr_package/examples/wine.txt -FPR 1e-3 [Options]

For clustering only:
PyMINEr.py -infile ~/Downloads/PyMINEr_package/examples/wine.txt -sample_cluster_only

Options:

-infile </path/to/data/matrix.txt>
    This is a required argument which has the 

-verbose
    Boolean variable, whose use causes extra output to be 
    printed to screen. This is largely for debugging purposes.

-dividing_col <int>
    This variable is used only when the input file contains 
    two separate networks (made from the same variables), 
    whose networks will be compared to each other. The 
    integer following ‘-dividing_col’ will be the column 
    number corresponding to the last sample of the first group
    (indexed starting at 0); this will also be the number of 
    samples in the first group.

-in_mine1 </path/to/mine/or/spearman/file/made/by/a/previous/PyMINEr/run>
    If PyMINEr network analysis is to be done on an adjacency 
    list, this can be fed into this argument. Notably, this 
    should be the non-deduplicated file.

-in_mine2 </path/to/mine/or/spearman/file/made/by/a/previous/PyMINEr/run>
    For a network comparison analysis, a second network file 
    can be fed into this argument. This must be a non-deduplicated
    adjacency list, containing each relationship bi-directionally.

-mem <int/float>
    This option is only for use with MINE.jar nonparametric 
    relationship detection. It is passed

-MineDir <'~/MINE.jar'>
    The file path which contains the MINE.jar file. This option 
    is only pertinent when using the fully non-parametric MINE 
    relationship detection. If installation is performed with 
    all default settings, the MINE.jar file is moved to ~/MINE.jar,
    so the default should run without needing to manually input 
    this option.

-MIC_cutoff <float>
    This is the lower limit cutoff to use for the MIC value, 
    when testing for significance. In general this should be a 
    value that has been determined by bootstrap shuffling. If the 
    MINE method of relationship is detected, we highly recommend 
    using the PyMINEr_pipeline.py script, as this will 
    automatically shuffle the dataset, and determine the 
    appropriate MIC_cutoff for the given False Positive Rate (FPR).

-MIC_cutoff1 <float>
    The same as -MIC_cutoff, however this is for using the 2 network 
    analysis, which is determined by using the -div_col argument, 
    and providing the dividing column separating the two networks to 
    be analyzed. This particular argument indicates the MIC cutoff 
    corresponding to the first network (as these cutoffs will be 
    often be different).

-MIC_cutoff2 <float>
    The same as -MIC_cutoff1, however this is the cutoff for 
    the second network.

-microarray
    A binary argument which tells PyMINEr this is a 
    !series_matrix_file in the format typically obtained from GEO.

-disease
    The name given to the second network, when the dual network 
    analysis is invoked.

-control
    The name given to the first network, when the dual network 
    analysis is invoked.

-log_fold
    This is a boolean argument which changes the display for some 
    graphs to have the log(ratio) of group1 to group2 means.

-log_expression
    Changes the display of some expression analysis to show the 
    log2 transformed input values.

-no_graphs
    This option prevents any of the graphs from being created.

-no_rainbow
    This option forces all graphs which typically use color coded 
    values for display to be converted to black, instead of the 
    default rainbow coloration.

-t <int>
    How many processes will be initialized for relationship 
    detection. This is only used for either MINE relationship detection,
    or with the -very_big_file option, which utilizes spearman 
    correlations instead of MIC.  If a smaller input file is used, 
    and spearman correlations are the method of relationship detection, 
    it is often quicker just to use one thread. Otherwise, the file 
    must be read iteratively, which is a slow process on its own.

-MINE_only
    This is a boolean option which allows the user to end the 
    PyMINEr analysis early, and only returns the variable-variable 
    relationship files (ie: the adjacency list).

-dpi
    Dots per inch for the output figure(s), if any.

-mannwhit
    A boolean option for use when the -div_col argument is used, but
    network analysis is not desired. In this case, a Mann-Whitney 
    comparison can optionally be done comparing the variable quantities 
    between the two groups.

-express_only
    A boolean option for use if the difference between the two groups 
    is the only thing of interest, no other network analyses will be done.

-no_express
    Do not do any expression analyses. This option is only applicable
    when using -div_col, and two networks are being used.

-cluster
    A boolean option to use a computing cluster. This is only utilized
    when performing a MINE analysis for relationship detection.

-sub_prefix </path/to/file/containing/header/for/submitting/jobs/to/a/cluster>
    When submitting a job to a cluster, it may be necessary to have
    a header to import libraries which are not globally accessible. For 
    example, it may be necessary to load numpy or another dependency. This
    is a file which contains the text to be used for a header for each 
    job submission. By default we simply use “#!/bin/bash” as the header.

-tpsub <int>
    How many threads should be used for each cluster submission.  This 
    should equate to how many CPU threads are available on a given node.
    Each node gets its own submission to the cluster.

-no_page_ranks
    If PageRank calculations are not desired, we don’t need to 
    calculate them.

-pr_iters
    How many iterations should be used for calculating the page ranks.
    The default is set to 50, iterations.

-pr_alpha
    The PageRank algorithm takes a static variable, alpha. The 
    default alpha is set to 0.85, as was originally described by Larry Page.

-no_weighted_analysis
    When comparing two networks, a the weight of rewiring is calculated 
    for each variable in the networks.

-no_sample_cluster
    A boolean option, which indicates to PyMINEr that you’re not 
    interested in doing any clustering on the samples.

-sample_cluster_only
    If you only want to use the automatic clustering function, this 
    can be done with this boolean option.

-sample_k_clusters_known <int>
    If the number of desired clusters is known, PyMINEr will skip 
    the automatic k determination 
    (ie: the number of groups contained in the samples).

-sample_cluster_iter
    The number of times the k determination algorithm, and clustering 
    algorithms will be iterated. The default is set to 10 iterations; 
    however, the greater this number is, the more stable and 
    reproducible the clustering results will be.

-cluster_prob
    A boolean option, whether centroids are selected based on maximizing 
    the distance function, or probabilistically weighted based on the 
    distance function. We do not advise using this option, as in beta 
    testing, it resulted in worse clustering using the maximized 
    distance centroids.

-var_norm_for_clust
    A boolean option for performing a linear normalization on all 
    variables between 0 and 1, giving even weight to each variable 
    for clustering the samples.

-first_non_deterministic
    A boolean variable to make the first iteration of clustering 
    should be performed in a deterministic fashion selecting the 
    point maximizing the standard deviation of variables. This 
    option often has only mild to negligible effects, unless the 
    selected first sample results in a local minimum of information,
    or maximum of entropy. 

-manual_sample_groups </path/to/file/with/sample/group/identities>
    Path to a file containing the tab delimited annotations for 
    each sample. Indexing of groups should start at 0.

-spearman
    This option indicates that Spearman correlations should be used
    instead of MINE, using MIC. This option will run far more quickly
    than MINE, because of the lack of bootstrap shuffling for
    relationship detection.

-spearman_only
    This option will cause PyMINEr analysis to end after Spearman 
    relationship detection.

-FPR <float>
    The false positive rate to be used for either MINE or Spearman 
    correlation.

-rand_seed <int>
    Default is 12345. This sets the global random number generator 
    seed sequence, for reproducible results.

-anova_FDR_cutoff < 0 < float < 1 >
    This is the false discovery rate for significance during 
    1-way ANOVA comparisons between groups. FDR q values are calculated
    by the Benjamini-Hochberg correction. The default FDR cutoff for 
    significance is set to 0.05

-zscore_cutoff <float>
    This cutoff is used for the lower limit for inclusion in 
    significantly enriched datasets. The default cutoff is a 
    Z-score of 2.0.

-many_variables
    A boolean variable which indicates there are many variables, 
    and a memory issue may occur. This will still enable calculating 
    ANOVAs, Z-scores, and significant enrichment; however, this option 
    does not use multiple threads for relationship identification.

-very_big_file
    Boolean variable which tells PyMINEr to use a low memory version,
    which does not read the whole input file. This option does not 
    currently support sample clustering, 1-way ANOVAs, or calculating 
    Z-scores. The relationships detected, and their associated PageRanks
    will be the only thing returned when using this option.

-no_co_regulatory_network
    This indicates that a separate network analysis on only positive
    correlations will not be performed.

-out_relationship_mat_only
    This will return the adjacency matrix (as zeros and ones), 
    written to file, and will not continue on to calculate PageRanks.

-big_file_no_z
    This option is for extra big files that cannot hold the 
    Z-score calculations in memory

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


## continue option is not yet supported
if '-continue_MINE' in sys.argv:
    continue_mine=True
else:
    continue_mine=False

verbose=False
if '-verbose' in sys.argv:
    verbose=True
else:
    verbose=False
###




if '-in_mine1' in sys.argv:
    in_mine1=sys.argv[sys.argv.index('-in_mine1')+1]
if '-in_mine2' in sys.argv:
    in_mine2=sys.argv[sys.argv.index('-in_mine2')+1]


if '-dividing_col' in sys.argv:
    dividing_col=int(sys.argv[sys.argv.index('-dividing_col')+1])
    single_network=False
else:
    dividing_col=False
    single_network=True



if '-infile' in sys.argv:
    infile=sys.argv[sys.argv.index('-infile')+1]
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
else:
    microarray=False

if '-disease' in sys.argv:
    disease=sys.argv[sys.argv.index('-disease')+1]
else:
    disease='disease'

if '-control' in sys.argv:
    control_name=sys.argv[sys.argv.index('-control')+1]
else:
    control_name='control'

if '-log_fold' in sys.argv:
    log_fold=True
else:
    log_fold=False
if '-log_expression' in sys.argv:
    log_expression=True
else:
    log_expression=False

if '-no_graphs' in sys.argv:
    no_graphs=True
else:
    no_graphs=False
    if no_matplot_lib:
        sys.exit("""
either the -no_graphs option should be selected or you must install
matplotlib from http://matplotlib.org/downloads.html
* note - the installation must be in the python3 library, not python2 *""")
if '-no_rainbow' in sys.argv:
    rainbow=False
else:
    rainbow=True
if '-t' in sys.argv:
    t=int(sys.argv[sys.argv.index('-t')+1])
else:
    t=2

if '-MINE_only' in sys.argv:
    mineOnly=True
else:
    mineOnly=False
if '-dpi' in sys.argv:
    dpi_in=int(sys.argv[sys.argv.index('-dpi')+1])
else:
    dpi_in=360

if '-clean' in sys.argv:
    clean=True
else:
    clean=False

if '-mannwhit' in sys.argv:
    mannwhit=True
else:
    mannwhit=False

if '-express_only' in sys.argv:
    express_only=True
else:
    express_only=False

if '-no_express' in sys.argv:
    no_express=True
else:
    no_express=False


if '-cluster' in sys.argv:
    cluster=True
else:
    cluster=False

if '-sub_prefix' in sys.argv:
    sub_prefix_text=read_file(sys.argv[sys.argv.index('-sub_prefix')+1],'raw')
else:
    sub_prefix_text='#!/bin/bash'
sub_prefix_text+='\n'

if '-tpsub' in sys.argv:
    tpsub=int(sys.argv[sys.argv.index('-tpsub')+1])
else:
    tpsub=t

if not '-no_page_ranks' in sys.argv:
    page_ranks=True
    if '-pr_iters' in sys.argv:
        pr_iters=int(sys.argv[sys.argv.index('-pr_iters')+1])
    else:
        pr_iters=50 ## this is a totally arbitrary default
    if '-pr_alpha' in sys.argv:
        pr_alpha=float(sys.argv[sys.argv.index('-pr_alpha')+1])
    else:
        pr_alpha=0.85
else:
    page_ranks=False

if '-no_weighted_analysis' in sys.argv:
    weighted_analysis=False
else:
    weighted_analysis=True

if '-no_sample_cluster' in sys.argv:
    do_sample_clustering = False
    ## I might need to add the sample names as a column to the right of the below vector
    ## it's relatively untested, so at this point I'm not sure if leaving it as is 
    ## will cause any problems
    first = True
    for temp_line in fileinput.input(infile):
        if first:
            title = np.array((temp_line.strip('\n')).split('\t'), dtype='U32')
            first = False
            break
    fileinput.close()
    sample_k_table = [0]*(len(title)-1)
else:
    do_sample_clustering = True


if '-sample_cluster_only' in sys.argv:
    sample_cluster_only=True
else:
    sample_cluster_only=False


if '-sample_k_clusters_known' in sys.argv:
    sample_k_known=True
    pre_determined_sample_k=int(sys.argv[sys.argv.index('-sample_k_clusters_known')+1])
    print('pre_determined_sample_k =', pre_determined_sample_k)
else:
    sample_k_known=False

if '-sample_cluster_iter' in sys.argv:
    sample_cluster_iter = int(sys.argv[sys.argv.index('-sample_cluster_iter')+1])
else:
    sample_cluster_iter = 10

if '-cluster_prob' in sys.argv:
    cluster_prob=True
else:
    cluster_prob=False

if '-var_norm_for_clust' in sys.argv:
    var_norm_for_clust = True
else:
    var_norm_for_clust = False

if '-first_non_deterministic' in sys.argv:
    first_prob = False
else:
    first_prob = True

if '-manual_sample_groups' in sys.argv:
    manual_sample_groups_file = sys.argv[sys.argv.index('-manual_sample_groups')+1]
#    manual_sample_groups = read_table(manual_sample_groups_file)
    sample_k_table = read_table(manual_sample_groups_file)
    manual_sample_groups = True
    sample_cluster_ids = []
    for i in range(0,len(sample_k_table)):
        
        ## THIS IS IMPORTANT
        ## here we assume that the samples are all listed in the same order as in '-infile'
        ## we also assume that the group indexing starts at 0
        sample_cluster_ids.append(sample_k_table[i][1])
    sample_cluster_ids = list(map(int,sample_cluster_ids))
    sample_k_lists = []
    for i in range(0,max(sample_cluster_ids)+1):
        sample_k_lists.append([])
    #print(len(sample_k_lists))
    ## now populate the list of lists
    for i in range(0,len(sample_cluster_ids)):
        ## this appends the sample index to 
        print(sample_cluster_ids[i])
        sample_k_lists[sample_cluster_ids[i]].append(i)
    
    
else:
    manual_sample_groups = False


if '-spearman' in sys.argv:
    do_spearman = True
else:
    do_spearman = False

if '-spearman_only' in sys.argv:
    spearman_only = True
else:
    spearman_only = False
    

if '-FPR' in sys.argv:
    FPR = float(eval(sys.argv[sys.argv.index('-FPR')+1]))
else:
    FPR = 0.001

if '-rand_seed' in sys.argv:
    new_seed = int(eval(sys.argv[sys.argv.index('-rand_seed')+1]))
    random.seed(new_seed)
    np.random.seed(new_seed)
    
if '-anova_FDR_cutoff' in sys.argv:
    FDR_cutoff = float(eval(sys.argv[sys.argv.index('-anova_FDR_cutoff')+1]))
else:
    FDR_cutoff = 0.05
    
if '-zscore_cutoff' in sys.argv:
    zscore_cutoff = float(eval(sys.argv[sys.argv.index('-zscore_cutoff')+1]))
else:
    zscore_cutoff = 2

if '-many_variables' in sys.argv:
    many_variables = True
else:
    many_variables = False

if '-very_big_file' in sys.argv:
    very_big_file = True
    single_network = True
else:
    very_big_file = False


if '-no_co_regulatory_network' in sys.argv:
    co_regulatory_network=False
else:
    co_regulatory_network=True

if '-big_file_do_z' in sys.argv:
    big_file_do_z=True
else:
    big_file_do_z=False
    
#######################################


temp=str(infile).split('/')
temp=('/').join(temp[:-1])


log_out=list(time.localtime())
log_out=str(log_out[1])+'/'+str(log_out[2])+'/'+str(log_out[0])+'\t'+str(log_out[3])+':'+str(log_out[4])+':'+str(log_out[5])+'\n'+' '.join(sys.argv)
make_file(log_out,temp+'/PyMINEr.log')

perform_mine_analysis=True
if ('in_mine' in vars()) or ('in_mine1' in vars()) or ('in_mine2' in vars()):
    perform_mine_analysis=False
    if 'in_mine' in vars() and single_network:
        summary1=in_mine1
    if 'in_mine1' in vars() and single_network:
        summary1=in_mine1
    elif ('in_mine1' in vars()) and ('in_mine2' in vars()):
        summary1=in_mine1
        summary2=in_mine2
    else:
        sys.exit('only -in_mine1 or -in_mine2 given as an option.  Must be both or neither')

if express_only:
    perform_mine_analysis=False

if (perform_mine_analysis and not do_spearman) and not MineDir:
    sys.exit('-MineDir is a required argument for Method 1')
if perform_mine_analysis and not dividing_col and not single_network:
    sys.exit('-dividing_col is a required argument for Method 1')


##########################################################################################
########## here we either read in the file for small files & get ready for analysis
########## or we just use file input to start generating the relationship file
##########################################################################################


if not very_big_file:
    ## reads input raw data
    table = read_file(infile,'lines')
    table = make_table(table,'\t')

    ## separates input datafile into title lines, a list of variable IDs, a 2D numpy matrices for the raw values
    ## in each group, one with and one without the identifying variable in the zeroth col of the matrix
    title,IDlist,table1,table2,group1,group2=find_table_start(table)

    ## in case we don't want to do sample clustering
    if not do_sample_clustering:
        manual_sample_groups = True
        title_vertical = np.transpose(np.array([title[1:]]))
        #print(title_vertical)
        group_ids_vertical = np.transpose(np.array([[0]*(len(title)-1)]))
        #print(group_ids_vertical)
        sample_k_table = np.hstack((title_vertical,group_ids_vertical))
        #print(sample_k_table)
        #sys.exit()


    if single_network:
        ## this was a hacky workaround instaed of fixing the code above 
        group1=group2[:]
        del group2
        table1=table2[:]
        del table2



table_offset = 1 ## title line
if very_big_file:
    print('\ncollecting all of the sample & variable names\n')
    IDlist = []
    ## find the beginning line of the table (basically only necessary for microarray data)
    if microarray:
        start_line = None
        temp_line_count = 0
        table_started = False ## this is for keeping track of whether we need to log the IDs
        ## read through the file, looking for the first line (which will start with some non "!" character)
        
        for line in fileinput.input(infile):
            if table_started:
                temp_split_line = strip_split(line)
                if "!series_matrix_table_end" not in temp_split_line[0]:
                    IDlist.append(temp_split_line[0])
                
                
            if temp_line_count == start_line:
                temp_line = line.replace('"','')
                title = np.array((temp_line.strip('\n')).split('\t'), dtype='U32')
                table_started = True
            

            if "!series_matrix_table_begin" in line: ## looking for the beginning of the table
                start_line = temp_line_count+1
                ## update the table_offset variable if we have a very_big_file microarray
                table_offset = start_line+1
                
            
            temp_line_count+=1
            
    else:
        start_line=0
        temp_line_count = 0
        table_started = False ## this is for keeping track of whether we need to log the IDs
        ## read through the file, looking for the first line (which will start with some non "!" character)
        for line in fileinput.input(infile):
            if table_started:
                temp_split_line = strip_split(line)
                IDlist.append(temp_split_line[0])

            if temp_line_count == start_line:
                temp_line = line.replace('"','')
                title = np.array((temp_line.strip('\n')).split('\t'), dtype='U32')
                table_started = True
            
            
            temp_line_count+=1


    fileinput.close()


    


print(len(title),'samples detected')
print(title[:3],'...',title[-3:])
print(len(IDlist),'variables detected')
print(IDlist[:3],'...',IDlist[-3:])

gc.collect()


##########
## make dict with index of IDs
IDhash={}
for i in range(0,len(IDlist)):
    if IDlist[i] in IDhash:
        print('duplicate variable names detected')
        print('first encountered:',IDlist[i])
        sys.exit('please remove all duplicate variable IDs')
    IDhash[IDlist[i]]=i
##########







########################################################################################################
########################################################################################################
##############                         absolute expression analysis                       ##############
########################################################################################################
########################################################################################################

#######################################
## calculate fold changes

if not single_network and not very_big_file:
    fold_changes=[]
    mean_control=[]
    mean_disease=[]
    mann_whit_list=[]
    express_out=IDlist[:]
    if log_fold:
        express_title=['\t'.join(['ID','mean '+control_name,'mean '+disease,control_name+' SD',disease+' SD','ln('+disease+'/'+control_name+')'])]
    else:
        express_title=['\t'.join(['ID','mean '+control_name,'mean '+disease,control_name+' SD',disease+' SD',disease+'/'+control_name])]

    if mannwhit:
        express_title[0]+='\tUncorrected MW p-val\n'
    else:
        express_title[0]+='\n'
    #print(express_title)
    for i in range(0,len(group1)):
        if verbose:
            print(group1[i][1:])
        temp_g1=group1[i][1:].astype(float)
        temp_g2=group2[i][1:].astype(float)
        temp_g1_mean=temp_g1.mean()
        temp_g2_mean=temp_g2.mean()
        if not no_express:
            temp_g1_sd=np.std(temp_g1)
            temp_g2_sd=np.std(temp_g2)
        
        mean_control.append(temp_g1_mean)
        mean_disease.append(temp_g2_mean)
        if log_fold:
            temp_fold=np.log(temp_g2_mean/temp_g1_mean)
        else:
            temp_fold=temp_g2_mean/temp_g1_mean

        fold_changes.append(temp_fold)

        if not no_express:
            if mannwhit:
                try:
                    mw(temp_g1,temp_g2)
                except:
                    mann_val=-1
                else:
                    mann_val=mw(temp_g1,temp_g2)[1]
                mann_whit_list.append(mann_val)
                #print(mann_val)
                express_out[i]='\t'.join([str(express_out[i]),str(temp_g1_mean),str(temp_g2_mean),str(temp_g1_sd),str(temp_g2_sd),str(temp_fold),str(mann_val)])+'\n'
            else:
                express_out[i]='\t'.join([str(express_out[i]),str(temp_g1_mean),str(temp_g2_mean),str(temp_g1_sd),str(temp_g2_sd),str(temp_fold)])+'\n'

    if not no_express:
        express_out=express_title+express_out
        output=temp+'/expression_summary.txt'
        make_file(express_out,output)

    #print(len(fold_changes))

    if not no_graphs:
        
        #print(len(mean_control),len(mean_disease))
        print('making expression scatter plot with fold change colors')
        output=temp+'/expression_scatter_colors.png'
        plt.cla()
        if rainbow:
            heat_colors = plt.cm.jet((fold_changes-min(fold_changes))/max(fold_changes-min(fold_changes)))## linear normalization (ie: 0-1 squished distribution)
            plt.scatter(mean_control,mean_disease,marker='o',s=1,color=heat_colors)#,alpha=.5)#,edgecolors='k')
        else:
            plt.scatter(mean_control,mean_disease,marker='.',s=1,color='k')#,edgecolors='k')
        plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
        ##plt.xlabel('Log2 Control expression')
        ##plt.ylabel('Log2 CF expression')
        if not log_expression:
            plt.xlabel(control_name+' expression')
            plt.ylabel(disease+' expression')
        else:
            plt.xlabel('Log2 '+control_name+' expression')
            plt.ylabel('Log2 '+disease+' expression')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

        if mannwhit:
            #####################################################
            #### make another scatter plot with mann_whitney ####
            second_mann_whit_list=np.array(mann_whit_list,dtype='float64')
            #print(mann_whit_list)
            if rainbow:
                print('making expression scatter plot with p-value colors')
                modified_mann_whit_list=np.log10(second_mann_whit_list)*-1## log transform mann whit p_vals
                modified_mann_whit_list=linear_normalize(modified_mann_whit_list[:])## this makes the most negative p values higher in color
                #print(modified_mann_whit_list)
                modified_mann_whit_list=modified_mann_whit_list.tolist()
                #print(modified_mann_whit_list[0:20])
                mw_heat_colors = plt.cm.jet(modified_mann_whit_list)
            
            

                output=temp+'/expression_scatter_mw_colors.png'
                plt.cla()
        
            
                plt.scatter(mean_control,mean_disease,marker='o',s=1,color=mw_heat_colors)#,alpha=.5)#,edgecolors='k')

                plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
        
                if not log_expression:
                    plt.xlabel(control_name+' expression')
                    plt.ylabel(disease+' expression')
                else:
                    plt.xlabel('Log2 '+control_name+' expression')
                    plt.ylabel('Log2 '+disease+' expression')
                plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
                plt.clf()

    if express_only:
        sys.exit('finished expression analysis')
################
#######################################





##############################################################################
####################### find k means for all samples #########################

##############################################################################
#########      functions for performing k-means clustering    ################

def linear_normalization(in_matrix,axis=1):
    in_matrix = in_matrix - np.transpose( np.array( [np.min(in_matrix, axis=axis)] ) )
    in_matrix = in_matrix / np.transpose( np.array( [np.max(in_matrix, axis=axis)] ) )
    print(np.min(in_matrix, axis=axis))
    print(np.max(in_matrix, axis=axis))
    return(in_matrix)

##################
def convert_to_prob(vect):
    ## calculate probabilities based on standard deviation 
    probabilities = vect - min(vect)
    probabilities = probabilities / max(probabilities)
    probabilities = probabilities / sum(probabilities)
    return(probabilities)



########################
start_length=35
stopping_length=5
def unknown_k_means_sample(sample_names, expression_matrix, prob = False):
    global sample_k_known,temp, first_prob
    ## expressoin matrix format:
    ##        sample1, sample2, sample3 ...
    ## var1[[  1.0   ,   1.5  ,   2.0  ],
    ## var2 [  0.2   ,   1.5  ,   2.0  ],
    ## var3 [  1.0   ,   1.5  ,   2.0  ]]

    ## because the kmeans2 function from scipy clusters based on rows, 
    ## the expression matrix will be transposed

    ## samples are now in rows, and expression values are now in columns

    #### constant ####
    # go_past_for_local_min is the variable which is used for seeing how far in 
    # k selection we should go past a local minimum

    expression_matrix = np.transpose(expression_matrix)

    expression_matrix = expression_matrix.astype('float32')
    
    ## this variable is for testing passed a local minimum of the f(k) function
    stopping_length = 10
    
    if expression_matrix.shape[0] <= stopping_length:
        print('expression_matrix is too small to subdivide')
        
        output_cluster_annotations = list(zip(sample_names, [0]*len(sample_names)))
        return(output_cluster_annotations)
    
    
    ## find the variable with the greatest number of interactions (or total expression)
    row_std = np.std(expression_matrix, axis = 1)
    print(row_std)
    max_row_std = np.max(row_std)
    if prob or first_prob:
        probabilities = convert_to_prob(row_std)
        centroid_initialization_index = np.random.choice ( list( range(0,len(sample_names)) ) , size = 1, replace = False, p = probabilities ) 
    else:
        centroid_initialization_index = sample(list(np.where(row_std == max_row_std)[0]), 1)
    print('first centroid index:',centroid_initialization_index)
    centroid_indices = list(centroid_initialization_index[:])
    
    temp_centroids, variable_labels = kmeans2(expression_matrix, expression_matrix[centroid_indices,:], minit='matrix', iter=10)
    
    print('\ncentroid_indices for k =',len(centroid_indices))
    print(centroid_indices)
    print('\n\n')
    
    ## initialize with k = 1
    Sk = None
    Ak = None
    temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, [list(variable_labels)], expression_matrix)
    f_list = [temp_f]
    centroid_distances_matrix = np.array(get_all_distances_from_a_centroid(expression_matrix[centroid_indices[-1]], expression_matrix))
    
    print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)


    
    while k_stopping_function(f_list, num_vars = len(sample_names)):
        ## len(f_list) must be at least the length of the stopping_length +1 for k=1
        ## then the first time that min(f(k)) is not within the stopping length, 
        ## then stop and return the optimal k

        ## first thing to do is find out all the current distances from all centroids
        if len(centroid_indices)>1:
            centroid_distances_matrix = np.hstack((centroid_distances_matrix, np.array(get_all_distances_from_a_centroid(expression_matrix[centroid_indices[-1]], expression_matrix))))
        
        ## find the index of the next centroid based on the current distance matrix
        if prob:
            next_centroid = get_next_centroid_index(centroid_distances_matrix, existing_centroids = centroid_indices, prob = True)
        else:
            next_centroid = get_next_centroid_index(centroid_distances_matrix, existing_centroids = centroid_indices)
        if next_centroid in centroid_indices:
            ## this means that the newly of the remaining points, there are now ties
            ## with already existing centroids for farthest away from other centroids
            print('already established centroid was picked again')
            break
        print(centroid_indices)
        centroid_indices.append(next_centroid)
        print('\ncentroid_indices for k =',len(centroid_indices))
        print(centroid_indices)
        print('\n\n')
        
        temp_centroids, variable_labels = kmeans2(expression_matrix, expression_matrix[centroid_indices,:], minit='matrix', iter=10)
        
        ## this function will take variable labels of format [0,1,1,0,0,2]
        ## and change it to: 
        ## [[0,3,4], ## centroid 0
        ##    [1,2],   ## centroid 1
        ##     [5]]     ## centroid 2
        variable_labels = rearrange_variable_labels(variable_labels)
       # print('variable_labels\n',variable_labels)
        if len(variable_labels) < len(centroid_indices):
            ## this means that two centroids have converged during the k-means clustering, indicating
            ## that the number of centroids is already oversaturated
            print("centroids converged, stopping due to overfit")
            break
        
        
        temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, variable_labels, expression_matrix)
        f_list.append(temp_f)
        print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)
        
    print(k_stopping_function(f_list, num_vars = len(sample_names)))
    if not k_stopping_function(f_list, num_vars = len(sample_names)):
        
        print(f_list)
    if not sample_k_known:
        optimal_k_index = get_estimated_k_from_f_list(f_list)
        print('optimal k =',optimal_k_index+1)
    elif sample_k_known:
        print('sample k known')
        optimal_k_index = int(pre_determined_sample_k-1)
    print('optimal k index:',optimal_k_index)
#    if not no_graphs:
#        plt.clf()
#        plt.plot(np.arrange(1,len(flist)),f_list,'o-')
#        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    optimal_centroid_indices = centroid_indices[:optimal_k_index+1]
    #print(optimal_centroid_indices)
    
    final_centroids, final_variable_labels = kmeans2(expression_matrix, expression_matrix[optimal_centroid_indices,:], minit='matrix', iter=10)
    
    ## convert the final variable labels into a list of lists containing the variable names
    rearranged_var_labels = rearrange_variable_labels(final_variable_labels)
    out_var_group_list_of_lists = []
    for r in rearranged_var_labels:
        out_var_group_list_of_lists.append(list(sample_names[var] for var in r))
    
    
        
    output_cluster_annotations = list(map(list,zip(sample_names, final_variable_labels)))
    
    
    if sample_k_known:
        copy_centroids=optimal_centroid_indices[:]
        print(list(map(str,copy_centroids)))
        #cmd('mkdir '+temp+'/sample_clustering_and_summary/')
        #make_file('\n'.join(list(map(str,copy_centroids))),temp+'/sample_clustering_and_summary/centroid_indices.txt')
    
    return(output_cluster_annotations, out_var_group_list_of_lists, f_list, optimal_centroid_indices)

########################################################################

def find_k_clusters(PC_scores, group = 'group1'):
    global page_ranks, temp
    if not page_ranks:
        return(None, None)
    global IDlist
    if group == 'group1':
        global c_PR_list, control_name
        name = control_name
        temp_PR_list = c_PR_list
    elif group == 'group2':
        global d_PR_list, disease
        name = disease
        temp_PR_list = d_PR_list
    ## first this function finds the variable with the greatest cumulative variance along the 
    ## given principal components
    ## following this step, 
    ## initialize the 

    

    ## not sure if I'll actually use the max_centroids as a part of the algorithm
    max_centroids = int(.5 * PC_scores.shape[1])
    print('max_centroids =',max_centroids)
    
    ## sum all of the |rows| (ie: PC scores along the row axis)
    ## then find the row with the maximum sum PC score
    ## * note * sample function is used just in case there are any ties
    print(PC_scores.shape)
    sum_PC_scores = np.array(np.sum(np.absolute(PC_scores), axis = 1))
    print(sum_PC_scores)
    centroid_indices = [sample(list(np.where(sum_PC_scores == np.max(sum_PC_scores))[0]), 1)[0]]
    
    ## intitialize matrix of centroids
    centroids = PC_scores[centroid_indices[0]]
    
    ## initialize and build centroid distance matrix
    #centroid_distances_matrix = np.transpose(np.array([get_all_distances_from_a_centroid(PC_scores[centroid_indices[-1]], PC_scores)]))
    #centroid_distances_matrix = np.transpose(np.array(get_all_distances_from_a_centroid(PC_scores[centroid_indices[-1]], PC_scores)))
    centroid_distances_matrix = np.array(get_all_distances_from_a_centroid(PC_scores[centroid_indices[-1]], PC_scores))
    
    
    print('centroid #',len(centroid_indices),centroid_indices[0], IDlist[centroid_indices[0]], 'PR:', temp_PR_list[centroid_indices[0]])
    print(centroid_distances_matrix.shape)
    print(centroid_distances_matrix)
    while len(centroid_indices) < max_centroids:#stop_function():
    
        ##
        #centroid_indices[-1]
    
        ## find the index of the next centroid based on the current distance matrix
        next_centroid = get_next_centroid_index(centroid_distances_matrix)
        centroid_indices.append(next_centroid)
        centroids = np.vstack((centroids,PC_scores[next_centroid]))
        print('centroid #',len(centroid_indices), next_centroid, IDlist[next_centroid], 'PR:', temp_PR_list[next_centroid])
        next_distances = get_all_distances_from_a_centroid (PC_scores[next_centroid], PC_scores)
        centroid_distances_matrix = np.hstack((centroid_distances_matrix, next_distances))
        
        print('centroid_distances_matrix\n',centroid_distances_matrix.shape)
        print(centroid_distances_matrix)
    
    
    ########################################################################
    ## do K means clustering initialized at the above obtained centroids    ################################################# needs to be finished
    ######################################################################
    
    
    ## prepare these matricies to be written to a file
    print('centroids')
    print(centroids)
    print('centroids shape')
    print(centroids.shape)
    output_file_centroids = flatten_2D_table(centroids, '\t')
    output_file_centroid_distances_matrix = flatten_2D_table(centroid_distances_matrix[:], '\t')
    output_file_centroid_distances_matrix_title_line = ['variables']
    for i in range(0,len(centroid_indices)):
        output_file_centroids[i] = str(IDlist[centroid_indices[i]])+'\t'+output_file_centroids[i]
        output_file_centroid_distances_matrix_title_line[0] = output_file_centroid_distances_matrix_title_line[0] + '\t'+ str(IDlist[centroid_indices[i]])
    output_file_centroid_distances_matrix_title_line[0]+='\n'
    output_file_centroid_distances_matrix = output_file_centroid_distances_matrix_title_line + output_file_centroid_distances_matrix
    
    for i in range(1,len(output_file_centroid_distances_matrix)):
        output_file_centroid_distances_matrix[i]=IDlist[i-1]+'\t'+output_file_centroid_distances_matrix[i]
    
    make_file(output_file_centroids, temp+'/'+name+'_centroids.txt')
    #print(output_file_centroid_distances_matrix)
    make_file(output_file_centroid_distances_matrix, temp+'/'+name+'_centroid_distances.txt')
    
    
    
    #do_k_means(centroids, PC_scores, name)
    
    
    
    return(centroid_indices, centroids, centroid_distances_matrix)

#####################

def get_all_distances_from_a_centroid(centroid, in_mat):
    euclidean_distances = []
    for i in range(0, in_mat.shape[0]):
        ## get the euclidean distance of each variable from given centroid
        temp_dist=linalg.norm(in_mat[i] - centroid)
        euclidean_distances.append(temp_dist**2)
#        euclidean_distances.append(temp_dist)
    return(np.transpose(np.array([np.array(euclidean_distances)])))

######################

multiply_by_min = True
def get_next_centroid_index(distance_list, existing_centroids = [], prob = False):
    ## this function calculates the sum of the squares of the euclidean distances from
    ## the all of the current centroids for all variables, then returns the index of the
    ## variable with the maximum sum of the square euclidean distances from all centroids
    global multiply_by_min
    
    #print('distance_list')
    #print(distance_list)
    
    temp_dist_mat=np.array(distance_list)
    #row_sum=np.sum(temp_dist_mat * temp_dist_mat, axis=1)
    row_sum=np.sum(temp_dist_mat, axis=1)
    #print(temp_dist_mat)
    if multiply_by_min:
        row_max=np.amax(temp_dist_mat,axis=1)
        row_min=np.amin(temp_dist_mat,axis=1)
        #print(row_min)
        row_range_plus1=(row_max-row_min)+1
        #print(row_range_plus1)
    
        
        all_distances=row_sum*row_min
    else:
        all_distances=row_sum

    
    #print(all_distances)
    #sys.exit()

    ## add all subsequent squared distances

    if prob:
        ## calculate probabilities based on standard deviation 
        probabilities = convert_to_prob(all_distances)
        max_indices = np.random.choice ( list( range(0, np.shape(distance_list)[0] ) ) , size = 1, replace = False, p = probabilities ) 
        
        num_max_indices = 1
    else:
        max_indices = np.where(all_distances == np.max(all_distances))[0]
        num_max_indices = np.shape(max_indices)[0]
        print('\n\tnumber equal to max',num_max_indices)
    
    
    final_candidate_next_centroids = []
    if num_max_indices > 1:
        max_indices = list(max_indices)
        final_candidate_next_centroids = []
        for i in range(0,num_max_indices):
            if max_indices[i] not in existing_centroids:
                final_candidate_next_centroids.append(max_indices[i])
        if final_candidate_next_centroids == []:
            return(sample(max_indices,1)[0])
        else:
            return(sample(final_candidate_next_centroids,1)[0])
        
    else:
        return(sample(list(max_indices),1)[0])


##################

from scipy.cluster.vq import kmeans2
def do_k_means(centroids, in_matrix, name, temp_IDs, iters = 10):
    global temp, IDlist
    
    final_centroids, variable_labels = kmeans2(in_matrix, centroids, minit='matrix', iter=iters)
    
    print(final_centroids)
    print(variable_labels)
    make_file(flatten_2D_table([['variable','group']]+list(map(list,list(zip(temp_IDs, variable_labels)))), '\t'), temp+'/'+name+'_k_groups.txt')
    #sys.exit()
    
    return

#################

def euclidean_distance(row1,row2):
    global linalg
    temp_eucl_dist = linalg.norm(row1-row2)
    return(temp_eucl_dist)


#################

def get_distance_matrix(PC_array):
    ## this function returns the symetric matrix of euclidean distance between
    ## all genes based on the principal components that are passed into this 
    ## function

    ## initialize the distance matrix with zeros
    distance_matrix = np.zeros((PC_array.shape[0],PC_array.shape[0]))
    
    for i in range(0,PC_array.shape[0]):
        for j in range(i,PC_array.shape[0]):
            temp_dist = euclidean_distance(PC_array[i], PC_array[j])
            distance_matrix[i][j] = temp_dist

    
    
    return(distance_matrix)


#######################

def global_impact_of_k_clusters(centroids, members, interaction_matrix):
    ## centroids is a list of the centroids
    ## members is a list of the indices of each member belonging to the ith centroid
    ## the interaction matrix is given for subsetting the members out
    #print('centroids')
    #print(type(centroids))
    
    if len(members) != centroids.shape[0]:
        print('incorrect dimentions\tmembers:',len(members), '\tcentroids:', centroids.shape[0])
        sys.exit('incorrect dimentions')
    Sk=0
    Sk_vector=[]
    for i in range(0,len(members)):
        ## dummy is set because this function returns the erroneous IDs for the subset matrix
        ## this function does this because it thinks it's getting the full interaction matrix,
        ## even though in reality it is getting a subsetted matrix
        #dummy, member_subset = subset_interaction_matrix(members[i], interaction_matrix)
        member_subset = interaction_matrix[members[i],:]
        
        ## trim the centroid to only include the indices of the subset matrix
        
        #temp_centroid = centroids[i,members[i]]
        temp_centroid = centroids[i,]
        
        #print(members[i])
        distance_vector = get_all_distances_from_a_centroid(temp_centroid, member_subset)
        temp_sk = np.sum(distance_vector)
        
        Sk_vector.append(temp_sk)
        Sk += temp_sk

    return(Sk)

####################

def f_of_k(prior_Sk, prior_Ak, centroids, members, interaction_matrix):
    ## * note that if k == 1, or k == 2, the 'prior_Ak' argument is not actually used
    ## so any dumby value can be fed into the function without ill effect
    print('prior_Sk',prior_Sk)
    print('prior_Ak',prior_Ak)
    #print('centroids')
    #print(centroids)
    #print('members')
    #print(members)
    #print('interaction_matrix')
    #print(interaction_matrix)
    k = len(members)
    Nd = interaction_matrix.shape[0]
    if k == 1:
        cur_Ak = None


    ## this function should only be run on 'clusters' with at least two possible members
    if Nd == 1:
        return (None, None, None)

    ## calculate Sk 
    else:
        cur_Sk = global_impact_of_k_clusters(centroids, members, interaction_matrix)
    
    ## calculate the current Ak
    if k == 2 and Nd > 1:
        cur_Ak = 1 - ( 3 / ( 4 * Nd ) )
    elif k > 2 and Nd > 1:
        cur_Ak = prior_Ak + ( (1 - prior_Ak) / 6 )

    
    ## calculate the k evaluation function
    if k == 1 or (prior_Sk == 0 and k > 1):
        f = 1
    else:
#        print('original f(k)',cur_Sk / (cur_Ak * prior_Sk))
        f = cur_Sk / (cur_Ak * prior_Sk)

#        print('new f(k)',f)

    return(f, cur_Sk, cur_Ak)

###################

def k_stopping_function(f_list, num_vars = None, starting_length=None, stopping_length=5, delta_cutoff=10):
    ## returning True allows the k search to continue, while returning False makes it stop
    if starting_length==None:
        starting_length = int(np.sqrt(num_vars)+1) ## this is a guess for the max number of groups to test at the beginning, barring any run-offs of local minimas
    global sample_k_known, pre_determined_sample_k
    if sample_k_known:
        if len(f_list) < pre_determined_sample_k:
            return(True)
        if len(f_list) == pre_determined_sample_k:
            return(False)
    else:
        if len(f_list)==1:
            return(True)
        if (f_list[-1] - f_list[-2]>10):
            return(False)
        if (len(f_list) < starting_length+1):
            return(True)
        if (min(f_list) in f_list[-stopping_length:]):
            return(True)

def get_estimated_k_from_f_list(f_list):
    global sample_k_known, pre_determined_sample_k
    if sample_k_known:
        return(pre_determined_sample_k-1)
    else:
        f_deltas=[]
        f_delta_delta=[]
        for f in range(1,len(f_list)):
            f_deltas.append(f_list[f]-f_list[f-1])
            f_delta_delta.append(f_list[f]-f_deltas[-1])
        
        #optimal_k=f_delta_delta.index(min(f_delta_delta))
#        print('f_delta_delta')
#        print(f_delta_delta)
        min_f=min(f_list)
        optimal_k_index=f_list.index(min_f)
        #next_best=min(f_list[optimal_k_index+1:])
        #if next_best < min_f*1:
        #    optimal_k_index=f_list.index(next_best)
        return(optimal_k_index)


##################

def rearrange_variable_labels(variable_labels):
    ## this function will take variable labels of format [0,1,1,0,0,2]
    ## and change it to: 
    ## [[0,3,4], ## centroid 0
    ##    [1,2],   ## centroid 1
    ##     [5]]     ## centroid 2
    max_label = max(variable_labels)
    variable_labels = np.array(variable_labels)
    new_var_labels=[]
    for i in range(0,max_label+1):## plus1 because the range function is exclusive in python, not inclusive
        new_var_labels.append(list(np.where(variable_labels == i)[0]))
    return(new_var_labels)

##############################################################################
###########     perform k-means clustering on the samples      ###############

if not very_big_file:
    if not single_network:
        print(group1)
        print(group2)
        #full_expression = np.transpose(np.hstack((group1[:,1:],group2[:,1:])))
        full_expression = np.hstack((group1[:,1:],group2[:,1:])).astype('float32')
    else:
        #full_expression = np.transpose(table1[:,1:])
        full_expression = group1[:,1:].astype('float32')
    print(title[1:])
    print(full_expression.shape)
    print(full_expression)




#########################################################
upper_nine_k = True
def do_unknown_k_means_clustering_iter(title, full_expression, cluster_iter = 10, performed_on_samples = False):
    global sample_k_known, pre_determined_sample_k, cluster_prob, upper_nine_k
    sample_k_table_list_list=[]
    sample_k_lists_list=[]
    f_list_list=[]
    optimal_centroid_indices_list=[]
    min_f=[]
    k_estimate_list = []

    for i in range(0,cluster_iter):
        if i == 0:
            print(title)
            print(full_expression)
            a = unknown_k_means_sample(title, full_expression, prob=False)
            print(len(a))
            for i in a:
                print(i)
            temp_sample_k_table, temp_sample_k_lists, temp_f_list, temp_optimal_centroid_indices = unknown_k_means_sample(title, full_expression, prob=False)
        else:
            temp_sample_k_table, temp_sample_k_lists, temp_f_list, temp_optimal_centroid_indices = unknown_k_means_sample(title, full_expression, prob=cluster_prob)
        
        sample_k_table_list_list.append(temp_sample_k_table)
        sample_k_lists_list.append(temp_sample_k_lists)
        f_list_list.append(temp_f_list)
        if sample_k_known:
            min_f.append(temp_f_list[pre_determined_sample_k-1])
        else:
            min_f.append(min(temp_f_list))
        k_estimate_list.append(temp_f_list.index(min_f[-1])+1)
        
        optimal_centroid_indices_list.append(temp_optimal_centroid_indices)

    cmd('mkdir "'+temp+'/sample_clustering_and_summary/"')
    if performed_on_samples:
        if sample_k_known:
            write_table(f_list_list,temp+'/sample_clustering_and_summary/f_lists_k_known.txt')
        else:
            write_table(f_list_list,temp+'/sample_clustering_and_summary/f_lists_k_not_known.txt')

    if upper_nine_k and not sample_k_known:
        sample_k_known = True
        
        temp_k_list = k_estimate_list[:]
        temp_k_list = sorted(temp_k_list)
        pre_determined_sample_k = temp_k_list[ int(round(cluster_iter*.9, 0)) - 1 ]
        
        return( do_unknown_k_means_clustering_iter(title, full_expression, cluster_iter = cluster_iter, performed_on_samples = performed_on_samples) )
        
    ############
    print('k estimate list',k_estimate_list)
    for f in range(0,len(f_list_list)):
        print('iter',f,'k estimate',k_estimate_list[f],'f',min_f[f],f_list_list[f])

        
    
    ############
    if True:#sample_k_known:
        global_min_f = min(min_f)
        print('global_min_f',global_min_f)
        global_min_f_indices = min_f.index(global_min_f)
        print('global_min_f_indices',global_min_f_indices)
        if type(global_min_f_indices) == int:
            optimal_k_iter=global_min_f_indices
        else:
            optimal_k_iter = sample(list(global_min_f_indices),1)[0]
        f_list = f_list_list[optimal_k_iter]
        optimal_centroid_indices=optimal_centroid_indices_list[optimal_k_iter]
    
        print(optimal_centroid_indices)
        
        sample_k_table_list = sample_k_table_list_list[optimal_k_iter]
        sample_k_lists = sample_k_lists_list[optimal_k_iter]
    ############
    
    #print(full_expression[:,optimal_centroid_indices])
    

    return(sample_k_table_list, sample_k_lists, f_list, optimal_centroid_indices)
        
#########################################################

gc.collect()

if not very_big_file:
    if not manual_sample_groups and do_sample_clustering:
        start_time = time.time()
        if cluster_prob or first_prob:
            if var_norm_for_clust:
                sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = do_unknown_k_means_clustering_iter(title[1:], lin_norm_rows(full_expression), cluster_iter = sample_cluster_iter, performed_on_samples = True)
            else:
                sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = do_unknown_k_means_clustering_iter(title[1:], full_expression, cluster_iter = sample_cluster_iter, performed_on_samples = True)
        else:
            if var_norm_for_clust:
                sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = unknown_k_means_sample(title[1:], lin_norm_rows(full_expression), cluster_iter = sample_cluster_iter, performed_on_samples = True)
            else:
                sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = unknown_k_means_sample(title[1:], full_expression, cluster_iter = sample_cluster_iter, performed_on_samples = True)
        elapsed_seconds = time.time()-start_time
    else:
        ## here we create the vector of sample ids
        sample_ids = title[1:]
        if len(sample_ids)!=len(sample_k_table):
            sys.exit('number of input known sample groups does not equal the number of samples in the input file')
        sample_cluster_ids = np.zeros(len(sample_ids),dtype = int)-1 ## first start out with -1 as default groups
        ## then we go through the sample_k_table finding the index of that sample
        ## then plug in the sample cluster id in the right spot
        for i in range(0,len(sample_ids)):
            #temp_index = sample_ids.where(sample_k_table[i][0])
            temp_index = np.where(sample_ids == sample_k_table[i][0])
            sample_cluster_ids[temp_index]=sample_k_table[i][1]
        
        #print(sample_cluster_ids)
        ## now we need to reorder the list into a list of lists for each cluster
        
        sample_k_lists = []
        for i in range(0,max(sample_cluster_ids)+1):
            sample_k_lists.append([])
        #print(len(sample_k_lists))
        ## now populate the list of lists
        for i in range(0,len(sample_cluster_ids)):
            ## this appends the sample index to 
            #print(sample_cluster_ids[i])
            sample_k_lists[sample_cluster_ids[i]].append(sample_ids[i])


## write the results of the cell clustering 
sample_dir = temp+'/sample_clustering_and_summary/'
cmd('mkdir "'+sample_dir+'"')

if not very_big_file or manual_sample_groups:
    write_table(sample_k_table,sample_dir+'sample_k_means_groups.txt')

    if not manual_sample_groups:
        print('optimal k =',len(optimal_centroid_indices))
        copy_centroids=optimal_centroid_indices[:]
        print(list(map(str,copy_centroids)))
        make_file('\n'.join(list(map(str,copy_centroids))),temp+'/sample_clustering_and_summary/centroid_indices.txt')
        print(f_list)








####################################################################
#######   calculate the enrichment for individual samples  #########
####################################################################

gc.collect()
if very_big_file and big_file_do_z:
    sample_var_enrichment_numeric=[]
    line_counter = 0
    for line in fileinput.input(infile):
        if line_counter >= table_offset:
            if (microarray and line[0]!='!') or not microarray:
                sample_var_enrichment_numeric.append(get_z_from_line(line))
        line_counter+=1
    fileinput.close()    
    
    write_table([title]+sample_var_enrichment_numeric, sample_dir+'sample_var_enrichment_Zscores.txt')

    ######################
    if manual_sample_groups:
        sample_k_group_enrichment_numeric = []

        line_counter = 0
        for line in fileinput.input(infile):
            if line_counter >= table_offset and line[0] != '!':
                sample_k_group_enrichment_numeric.append(get_group_z_from_line(line))
                
            line_counter+=1
        fileinput.close()    
    
    group_names = [['var_names']]
    for k in range(0,len(sample_k_group_enrichment_numeric[0])-1):
        group_names[0].append('sample_group_'+str(k))
    write_table(group_names + sample_k_group_enrichment_numeric, sample_dir+'k_group_enrichment.txt')



if not very_big_file:
    
    ## first normalize the expression matrix linearly between 1 and 2
    #sample_var_enrichment = lin_norm_rows(full_expression) + 1
    sample_var_enrichment = full_expression

    ## then calculate the mean for each variable
    norm_row_means = np.transpose(np.array([np.mean(sample_var_enrichment, axis = 1)]))
    print(norm_row_means)
    ## then calculate the sd for each variable
    norm_row_sd = np.transpose(np.array([np.std(sample_var_enrichment, axis = 1)]))
    print(norm_row_sd)
    ## then calculate the delta for each variable
    norm_row_delta = sample_var_enrichment - norm_row_means

    ## calculate the z-score (ie: how many standard deviations away from the mean is each sample)
    sample_var_enrichment_numeric = norm_row_delta/norm_row_sd
    print(sample_var_enrichment_numeric)
    #sys.exit()

    

    ## add the titles
    sample_var_enrichment = np.vstack((title[1:],sample_var_enrichment_numeric))

    row_titles = np.transpose(np.array([['variables']+IDlist]))

    sample_var_enrichment = np.hstack((row_titles,sample_var_enrichment))
    
    write_table(sample_var_enrichment, sample_dir+'sample_var_enrichment_Zscores.txt')




    if sample_cluster_only:
        optimal_k = len(sample_k_lists)
        make_file(str(optimal_k)+'\n'+str(elapsed_seconds),sample_dir+'k_means_k_and_time.txt')
        sys.exit('finished sample clustering')



########################################################################################################
########################################################################################################
##############                         perform mine analysis                              ##############
########################################################################################################
########################################################################################################

if perform_mine_analysis and not do_spearman and not very_big_file:
    starting_mine_time=time.clock()
    ##############################################################
    ##For Methods 1 & 3, create new files and run MINE analysis ##
    ##    *Note - this will likely take quite a while*          ##
    ##############################################################

    ## Segregate the file into Group1 (Usually Control) and Group2 (Usually Diseased or Treated)

    if not continue_mine:
        if not single_network:
            disease_dir=temp+'/'+disease
            if os.path.exists(disease_dir):
                cmd('rm -r '+disease_dir+'/*')
            #cmd('mkdir '+disease_dir)
            Popen('mkdir "'+disease_dir+'"',shell=True).communicate()

        control_dir=temp+'/'+control_name
        if os.path.exists(control_dir):
            cmd('rm -r '+control_dir+'/*')
        cmd('mkdir "'+control_dir+'"')
        if os.path.exists(control_dir):
            cmd('rm -r '+temp+'/scripts/*')
        cmd('mkdir "'+temp+'/scripts"')
        make_file('',temp+'/status.txt')

    else:
        ############# in case the original mine analysis was interrupted
        ############# we should be able to pickup the analysis where the
        ############# previous one left off to avoid redundancy
        
        #################################################
        ## needs to be finished                        ###########################################
        #################################################
        pass


    ## this chunk will find out the most efficient allocation of
    ## threads to each group
    if not single_network:
        ####################################
        ## if there are two networks that must be built, figure out how many threads to give each netowrk

        ## begin with equal allocation of one thread per network
        c_threads=1
        d_threads=1

        c_reps=dividing_col
        d_reps=len(title)-1-dividing_col

        if t>2:
            ## if there are more than two threads allocated, then figure out which network should get how many 
            temp_t=t-2
            if c_reps == d_reps:
                ## split them evenly, if the n is equal between groups
                c_threads+=int(temp_t/2)
                d_threads+=int(temp_t/2)

            elif t==3:
                ## if there is only one extra thread, we will give it to the one with more replicates
                if c_reps > d_reps:
                    c_reps+=1
                else:
                    d_reps+=1
            else:
                #####################################################################################################################################
                ##sys.exit('made it to speed test')
                ## emperically determine the speed at which the two groups will go
                ## so as to allocate threads to end at roughly the same time.
                ## this was done because the MINE algorithm does not scale linearly, so 
                ## it will be more realistic to simply emperically get their speed ratios

                ## make a temp directory for the MINE files, which will then be deleted
                speed_temp_dir = temp+'/scripts/speed_temp'
                cmd('mkdir "'+speed_temp_dir+'"')
                ## number of MINE comparisons to perform for temporary test
                num_test_rows = min(len(IDlist),100)## 100 was an arbitrary choice, but it produced roughly equivalent results to 1000

                ## copy the data over to a temporary directory to emperically determine how fast each will take
                c_file=speed_temp_dir+'/'+control_name+'_raw_data_speed_test.tsv'
                d_file=speed_temp_dir+'/'+disease+'_raw_data_speed_test.tsv'
                make_file(flatten_2D_table(group1,'\t'),c_file)
                make_file(flatten_2D_table(group2,'\t'),d_file)

                ##### run simulation study to determine best allocation of threads
                start=time.time()
                for i in range(1,num_test_rows):
                    cmd("java -jar "+MineDir+" '"+c_file+"' 0 "+str(i)+" cv=0.1 exp=0.6 c=10")
                end=time.time()
                hang_time1=end-start
                

                start=time.time()
                for i in range(1,num_test_rows):
                    cmd("java -jar "+MineDir+" '"+d_file+"' 0 "+str(i)+" cv=0.1 exp=0.6 c=10")
                end=time.time()
                hang_time2=end-start
                

                adding_c_threads = int(temp_t*(hang_time1/(hang_time1+hang_time2)))
                adding_d_threads = int(temp_t*(hang_time2/(hang_time1+hang_time2)))


                c_threads+=adding_c_threads
                d_threads+=adding_d_threads
                c_time_estimate = len(IDlist)*hang_time1/c_threads
                d_time_estimate = len(IDlist)*hang_time2/d_threads
                total_estimated_time = max([c_time_estimate,d_time_estimate])
                
                
            if c_threads+d_threads < t:
                ## if an even number of threads was supplied by the user,
                ## PyMINEr will allocate the remaining thread to the control group
                c_threads+=1
            elif c_threads+d_threads > t:
                ## just in case there was some rounding error
                c_threads-=1

            if 'speed_temp_dir' in vars():
                #c_time_estimate = len(IDlist)*hang_time1/c_threads
                #d_time_estimate = len(IDlist)*hang_time2/d_threads
                #total_estimated_time = max([c_time_estimate,d_time_estimate])

                cmd('rm -r '+speed_temp_dir)
            
            
    else:
        ### if this is a single network analysis, give the only group all of the allocated threads
        c_threads=t

    if 'hang_time1' in vars():
        print(control_name+" took ",hang_time1/(num_test_rows-1)," seconds per comparision")
        print('group one gets',c_threads,'threads')
        print('group one is estimated to take',c_time_estimate,'for MINE analysis')
    else:
        pass
        #print('estimated to take',c_time_estimate,'for MINE analysis')
    
    if 'hang_time2' in vars():
        print(disease+" took ",hang_time2/(num_test_rows-1)," seconds per comparision")
        print('group two gets',d_threads,'threads')
        print('group two is estimated to take',d_time_estimate,'for MINE analysis')

        print('total estimated time is:',total_estimated_time/60,"minutes")


    ##################################################################
    
    c_previous_index=0## keeps track of where previous thread left off
    script_list=[]
    for i in range(1,c_threads+1):
        c_file=control_dir+'/'+control_name+'_raw_data'+str(i)+'.tsv'
        c_py=temp+'/scripts/'+control_name+'_raw_data'+str(i)+'.py'

        if i==1:
            make_file(flatten_2D_table(group1,'\t'),c_file)## make copies of the split raw data files to prevent any accidental cross talk between threads
        else:
            ## the cp function is faster than the python write function
            cmd('cp '+control_dir+'/'+control_name+'_raw_data1.tsv '+c_file)## make copies of the split raw data files to prevent any accidental cross talk between threads
        
        ##############################################################################################
        ## write secondary scripts for running in parallel                                          ##
        ## write_MINE_scripts(start_row,end_row,mem,MineDir,in_file,index,MIC_cutoff,script_path)   ##
        ##############################################################################################
        
        if i<c_threads:
            write_MINE_scripts(c_previous_index,(i*len(IDlist))//c_threads,AvailableMemInGig,MineDir,c_file,i,MIC_cutoff1,c_py,temp+'/status.txt')
            script_list.append(c_py)
            c_previous_index=(i*len(IDlist))//c_threads
        elif i==c_threads:
            write_MINE_scripts(c_previous_index,len(IDlist),AvailableMemInGig,MineDir,c_file,i,MIC_cutoff1,c_py,temp+'/status.txt')
            script_list.append(c_py)

    if not single_network:
        d_previous_index=0## keeps track of where previous thread left off
        for i in range(1,d_threads+1):
            d_file=disease_dir+'/'+disease+'_raw_data'+str(i)+'.tsv'
            d_py=temp+'/scripts/'+disease+'_raw_data'+str(i)+'.py'

            ## make copies of the split raw data files to prevent 
            ## any accidental cross talk between threads
            make_file(flatten_2D_table(group2,'\t'),d_file)

            #################################################################
            ## write secondary scripts for running in parallel             ##
            ## write_MINE_scripts(start_row,end_row,mem,MineDir,in_file,index,MIC_cutoff,script_path)   ##
            #########################################################################################
            
            if i<d_threads:
                write_MINE_scripts(d_previous_index,(i*len(IDlist))//d_threads,AvailableMemInGig,MineDir,d_file,i,MIC_cutoff2,d_py,temp+'/status.txt')
                script_list.append(d_py)
                d_previous_index=(i*len(IDlist))//d_threads
            elif i==d_threads:
                write_MINE_scripts(d_previous_index,len(IDlist),AvailableMemInGig,MineDir,d_file,i,MIC_cutoff2,d_py,temp+'/status.txt')
                script_list.append(d_py)

    ## initialize the MINE scripts
    print('initializing scripts for running MINE')

    if cluster:
        #####################################################################################################
        ## for working with computing clusters, this section will lead to 'qsub' calls for parallelization ##
        #####################################################################################################

        ## figure out how many qsub submissions are needed using the threads per submission & total threads arguments
        total_subs=t//tpsub
        if t%tpsub!=0:
            total_subs+=1
        
        cmd('mkdir "'+temp+'/scripts/cluster_scripts"')
        cluster_sub_script_list=[]
        for s in range(0,total_subs):
            ## cycle through every tpsub script set assigning it to an intermediate (s) python script
            ## to be called by sub_file_s.sh
            temp_sub_scirpt=sub_prefix_text+'\n'
            temp_py_script_path=temp+'/scripts/cluster_scripts/intermediate_'+str(s)+'.py'
            
            ## for each script chunk to be submitted by qsub, create the python file to initalize those scripts
            ## to later be called by the qsub bash script
            if s!=total_subs-1:
                make_intermediate_script(script_list[s*tpsub:(s+1)*tpsub],temp_py_script_path)
            else:
                make_intermediate_script(script_list[s*tpsub:],temp_py_script_path)

            ## add the python script call to the end the bash script for queue submission
            temp_sub_scirpt+='python3 '+temp_py_script_path+'\n'
            temp_sub_scirpt_file=temp+'/scripts/cluster_scripts/sub_file_'+str(s)+'.sh'

            ## this file is submitted by qsub
            make_file(temp_sub_scirpt,temp_sub_scirpt_file)
            
            cluster_sub_script_list.append('qsub '+temp_sub_scirpt_file)

        ## create the master qsub submission script
        master_cluster_sub_bash='#!/bin/bash\n'
        master_cluster_sub_bash+='\n'.join(cluster_sub_script_list)
        make_file(master_cluster_sub_bash,temp+'/master_cluster_sub.sh')
        cmd('chmod a+x '+temp+'/master_cluster_sub.sh')
        print(temp+'/master_cluster_sub.sh is ready to be run')

        ############################################################################################
    else:
        ## for basic 
        for s in range(0,len(script_list)):
            print(script_list[s])
            #cmd('python3 '+script_list[s])#,shell=True)
            Popen('python3 '+script_list[s],shell=True)

    ## periodically loop through checking on the status
    gc.collect()
    loop = True
    while loop:
        threads_done=read_file(temp+'/status.txt','lines')
        if len(threads_done)==t:
            
            os.chdir(temp)
            ## combine all threads for both groups
            TOc=temp+'/_TOc.tsv'
            c_final_summary_file=temp+'/'+control_name+'_final_relationship_summary.tsv'
            in_mine1=c_final_summary_file[:]
            make_file("""X var\tY var\tMIC (strength)\tMIC-p^2 (nonlinearity)\tMAS (non-monotonicity)\tMEV (functionality)\tMCN (complexity)\tLinear regression (p)\n""",TOc)

            if not single_network:
                TOd=temp+'/_TOd.tsv'
                d_final_summary_file=temp+'/'+disease+'_final_relationship_summary.tsv'
                in_mine2=d_final_summary_file[:]
                make_file("""X var\tY var\tMIC (strength)\tMIC-p^2 (nonlinearity)\tMAS (non-monotonicity)\tMEV (functionality)\tMCN (complexity)\tLinear regression (p)\n""",TOd)


            os.chdir(temp)
            cmd('cat '+TOc+' '+control_dir+'/summary* > '+c_final_summary_file)
            cmd('rm '+TOc)
            if not single_network:
                cmd('cat '+TOd+' '+disease_dir+'/summary* > '+d_final_summary_file)
                cmd('rm '+TOd)
            time.sleep(10)
            loop=False

            ## removes title line files
            
##            rm_command='rm '+TOc
##            print(rm_command)
##            cmd(rm_command).communicate()
##            if not single_network:
##                rm_command='rm '+TOd
##                print(rm_command)
##                cmd(rm_command).communicate()
                

        else:
            time.sleep(60)

    end_mine_time=time.clock()
    total_mine_time=end_mine_time-starting_mine_time
    print('\ntotal time for MINE analysis:',total_mine_time,'\n')

    if clean:
        #############################################################################
        ## clean up all of the temporary files created by running MINE in parallel ##
        #############################################################################
        os.chdir(control_dir)
        cmd('rm *')
        if not single_network:
            os.chdir(disease_dir)
            cmd('rm *')
        os.chdir(temp+'/scripts/')
        cmd('rm *')
    os.chdir(temp)
    
    #sys.exit()



    #######################################











######################################################################################
#####      this module will find the spearman correlations instead of using    #######
#####          the non-parametric, non-monotonic MINE algorithm                #######
######################################################################################


def index_pairs_output_lines(index_pairs, p_val_mat, rho_mat, name):
    global IDhash, IDlist
    output_lines = [["X_var","Y_var","empty1","empty2","empty3","empty4","Spearman_p_val","Spearman_rho"]]
    for i in range(0,np.shape(index_pairs)[0]):
        x_index = index_pairs[i,0]
        x_var = IDlist[x_index]
        y_index = index_pairs[i,1]
        y_var = IDlist[y_index]
        temp_p = p_val_mat[x_index, y_index]
        temp_rho = rho_mat[x_index, y_index]
        temp_line = [x_var, y_var, 'NA', 'NA', 'NA', 'NA', temp_p, temp_rho]
        
        output_lines.append(temp_line)
        
    write_table(output_lines, temp+'/'+name+'_final_relationship_summary.tsv')
    
    

def do_spearman_on_mat(in_mat, name):
    global temp, FPR, many_variables
    print('finding the spearman correlations for',name)
    print('this may take a while if your dataset has lots of variables...')
    num_vars = np.shape(in_mat)[0]
    if not many_variables:
        rho, p_val = scipy.stats.spearmanr(in_mat, axis=1)
        ## set the diagonal p values to 1, we aren't interested in self-correlations...
        np.fill_diagonal(p_val, 1.0)
    else:
        rho = np.zeros((num_vars,num_vars))
        p_val = np.ones((num_vars,num_vars))
        for var1 in range(0,num_vars):
            if var1 % 10 == 0:
                print('working on variable #',var1,'out of',num_vars)
                print("~", (1-((num_vars-var1)**2/num_vars**2) )*100,"%")
            #r,p=scipy.stats.spearmanr(np.array([in_mat[var1,:]]), in_mat[range(var1,)], axis=1)
            #rho[var1,:]=r
            #p_val[var1,:]=p
            for var2 in range(var1+1,np.shape(in_mat)[0]):
                r,p=scipy.stats.spearmanr(in_mat[[var1,var2],:], axis=1)
                rho[var1,var2]=r
                p_val[var1,var2]=p
                rho[var2,var1]=r
                p_val[var2,var1]=p
            
            #print(rho)
    


    
    

    
    
    ## figure out which areas of the interaction matrix are less than the specified false positive rate
    masked_p_val_mat = np.ma.getmaskarray(np.ma.masked_less_equal(p_val, FPR))
    
    ## get the index pairs of all the 
    significant_indices = np.transpose(np.nonzero(masked_p_val_mat))
    
    ## the total number of relationships found:
    print('number of relationships detected =',np.sum(masked_p_val_mat)/2)
    
    print('\ncreating the relationship file')
    
    index_pairs_output_lines(significant_indices, p_val, rho, name)
    
    return()
    
    
    
if perform_mine_analysis:
    c_final_summary_file = temp+ '/' + control_name + '_final_relationship_summary.tsv'
    in_mine1=c_final_summary_file[:]
    if not single_network:
        d_final_summary_file=temp+'/'+disease+'_final_relationship_summary.tsv'
        in_mine2=d_final_summary_file[:]
    

if not very_big_file:
    ## when the input matrix is small, it's quicker to do the relationship detection
    ## on the full matrix, as this is done by C code from scipy, & will run much more quickly
    if perform_mine_analysis and do_spearman:
        do_spearman_on_mat( group1[:,1:].astype('float32') , control_name)
#        c_final_summary_file = temp+ '/' + control_name + '_final_relationship_summary.tsv'
#        in_mine1=c_final_summary_file[:]
        if not single_network:
            do_spearman_on_mat(group2[:,1:].astype('float32'), disease)
            d_final_summary_file=temp+'/'+disease+'_final_relationship_summary.tsv'
            in_mine2=d_final_summary_file[:]



###########################################################################

def get_spearman_big_file(file_name, var_index, offset = 1):

    ## the offset is for a ! denoted header
    ## in general, this should be 1 because of the title line
    global temp, FPR, many_variables, IDlist, verbose, num_vars
    
    output_lines = []

    #rho = np.zeros((num_vars,num_vars), dtype = 'Float16')
    #p_val = np.ones((num_vars,num_vars), dtype = 'Float16')
    
    line_count = 0
    
    start_collecting_correlations = False
    for line in fileinput.input(file_name):
    
        if start_collecting_correlations:
            if line_count - offset == num_vars:
                print(line)
            if line_count - offset < num_vars:
                r,p=scipy.stats.spearmanr(current_compare_var, strip_split(line)[1:])
                
                if p <= FPR:
                    #print('found a relationship',r,p)
                    output_lines.append([IDlist[var_index], IDlist[line_count - offset], 'NA', 'NA', 'NA', 'NA', p, r])
                    output_lines.append([IDlist[line_count - offset], IDlist[var_index], 'NA', 'NA', 'NA', 'NA', p, r])

        if line_count == var_index+offset:
            current_compare_var = strip_split(line)[1:] ## the 1: clips the variable name
            start_collecting_correlations = True
        
        
        
        
        
        line_count+=1
        if verbose:
            if line_count % 10000 ==0:
                print(line_count)


    fileinput.close()
    
    if output_lines != []:
        return(output_lines)
    else:
        return(None)


#########

num_vars = len(IDlist)

def get_comparison_area(start_index):
    global num_vars
    return((start_index**2/2)-(num_vars*start_index))

def area_comparisons_to_perform(start_index, end_index):
    return(get_comparison_area(start_index) - get_comparison_area(end_index))

def get_start_end_indices_for_each_thread(num_comparisons_per_thread):
    global num_vars, t
    remaining_t = t-1 ## we subtract 1 so that we can keep the main thread running
    start_indices = [0]
    end_indices = []
    line_count = 0
    while line_count < num_vars:
        if area_comparisons_to_perform(start_indices[-1],line_count) >= num_comparisons_per_thread:
            start_indices.append(line_count)
            end_indices.append(line_count)
        
    
        line_count+=1

        
    ## set the start and end for the final thread
#    start_indices.append(end_indices[-1])
    end_indices.append(num_vars+1)
    
    return(start_indices, end_indices)
        
#########################################################################################
def write_big_file_parallel_spearman(start_row,end_row,offset,num_vars,in_file,index,FPR,script_path,status_path):
    print(script_path)
    print(status_path)
    python_commands=str("""
from subprocess import Popen
from time import sleep
from scipy.stats import spearmanr
import fileinput
##############

def read_file(tempFile,linesOraw):
    print('reading',tempFile)
    f=open(tempFile,'r')
    if linesOraw=='lines':
        lines=f.readlines()
        for i in range(0,len(lines)):
            lines[i]=lines[i].strip('\\n')
    elif linesOraw=='raw':
        lines=f.read()
    f.close()
    return(lines)

def strip_split(line, delim = '\\t'):
    return(line.strip('\\n').split(delim))

    
def write_table(table, out_file, sep = '\t'):
    make_file(flatten_2D_table(table,sep), out_file)

def make_file(contents,path):
    f=open(path,'w')
    if isinstance(contents,list):
        f.writelines(contents)
    elif isinstance(contents,str):
        f.write(contents)
    f.close()

def flatten_2D_table(table,delim):
    print(type(table))
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
            out[i]=delim.join(out[i])+'\\n'
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
            table[i]=delim.join(table[i])+'\\n'
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

def cmd(in_message):
    Popen(in_message,shell=True).communicate()


##################################################################################


def get_spearman_big_file(file_name, var_index, offset = 1):

    ## the offset is for a ! denoted header
    ## in general, this should be 1 because of the title line
    global temp, FPR, many_variables, IDlist, verbose, num_vars
    
    output_lines = []


    line_count = 0
    
    start_collecting_correlations = False
    for line in fileinput.input(file_name):
    
        if start_collecting_correlations:
            if line_count - offset == num_vars:
                print(line)
            if line_count - offset < num_vars:
                temp_line = strip_split(line)
                cur_var_name2 = temp_line[0]
                if cur_var_name1 != cur_var_name2:
                    r,p=spearmanr(current_compare_var, temp_line[1:])
                
                    if p <= FPR:
                        #print('found a relationship',r,p)
                        output_lines.append([cur_var_name1, cur_var_name2, 'NA', 'NA', 'NA', 'NA', p, r])
                        output_lines.append([cur_var_name2, cur_var_name1, 'NA', 'NA', 'NA', 'NA', p, r])

        if line_count == var_index+offset:
            temp_line = strip_split(line)
            current_compare_var = temp_line[1:] ## the 1: clips the variable name
            cur_var_name1 = temp_line[0]
            start_collecting_correlations = True
        
        
        

        
        
        
        line_count+=1
        ## write status to temp log for this processes
        make_file("working on row "+str(i),log_file)


    fileinput.close()
    
    if output_lines != []:
        return(output_lines)
    else:
        return(None)





##################################################################################


##############

## run spearman analysis

infile='"""+in_file+"""'
index="""+str(index)+"""

temp_dir=str(infile).split('/')
temp_dir=('/').join(temp_dir[:-1])
transfer=temp_dir+'/transfer'+str(index)+'.txt'
summary=temp_dir+'/summary_'+str(index)+'.txt'
temp_aggregate=temp_dir+'/temp_aggregate_'+str(index)+'.txt'
aggregate_after=100
log_file='"""+script_path+""".log'
make_file("",log_file)
start_row="""+str(start_row)+"""
end_row="""+str(end_row)+"""
offset = """+str(offset)+"""
num_vars = """+str(num_vars)+"""
FPR = """+str(FPR)+"""

count=0


print('finding the spearman correlations for very big file')
print('this may take a while if your dataset has lots of variables...')


#output_lines = [["X_var","Y_var","empty1","empty2","empty3","empty4","Spearman_p_val","Spearman_rho"]]
output_lines = []


for i in range(start_row,end_row):
    count+=1



    new_lines = get_spearman_big_file(infile, i, offset = offset)
    if new_lines != None:## this means that there were at least some detected correlations
        output_lines = output_lines + new_lines
        
        print("currently we've found",(len(output_lines))/2,"unique relationships")


    
write_table(output_lines, summary)




### append final
#cmd('cp '+summary+' '+summary+'_temp.txt')## these pass off the files circularly to add the new #results to the summary file
#cmd('rm '+summary)
#cmd('cat '+summary+'_temp.txt '+temp_aggregate+'>'+summary)
#cmd('rm '+summary+'_temp.txt')
#cmd('rm '+temp_aggregate)



## write the the 'done' status in the status folder for the original script to read
cmd("echo '"""+script_path+""" finished' >> '"""+status_path+"""'")

make_file("finished rows:\\n"+str(start_row)+" to "+str(end_row),log_file)

""")
    #print(python_commands)
    make_file(python_commands,script_path)

#########################################################################################

if very_big_file and perform_mine_analysis:
    ## for a very big file, we need to run through the file loading in lines one at a time
    ## this takes a really long time, but there's no real way around it for files
    ## that won't fit in memory
    
    
    ## first thing we want to do is figure out which variable indicies will be done by which threads
    total_number_of_comparisons = num_vars**2 / 2
    num_comparisons_per_thread = total_number_of_comparisons / (t)
    
    start_indices, end_indices = get_start_end_indices_for_each_thread(num_comparisons_per_thread)
    

    print('finding the spearman correlations for very big file')
    print('this may take a while if your dataset has lots of variables...')

    control_dir=temp+'/'+control_name
    if os.path.exists(control_dir):
        cmd('rm -r '+control_dir+'/*')
    cmd('mkdir "'+control_dir+'"')
    ## make dir for all of the scripts
    if os.path.exists(control_dir):
       cmd('rm -r '+temp+'/scripts/*')
    cmd('mkdir "'+temp+'/scripts"')
    make_file('',temp+'/status.txt')

        
    script_list=[]
    for program in range(0,t):
        c_file=control_dir+'/'+control_name+'_raw_data'+str(program)+'.tsv'
        c_py=temp+'/scripts/'+control_name+'_raw_data'+str(program)+'.py'

        print('infile:',infile)
        cmd('cp "'+infile+'" "'+c_file+'"')
        
        script_list.append(c_py)

        
        ##############################################################################################
        ## write secondary scripts for running in parallel                                          ##
        ## write_MINE_scripts(start_row,end_row,mem,MineDir,in_file,index,MIC_cutoff,script_path)   ##
        ##############################################################################################
        
        write_big_file_parallel_spearman(start_indices[program],end_indices[program],start_line+1,num_vars,c_file,program,FPR,c_py,temp+'/status.txt')


    
        ## make copies of the in_file
        
        ## figure out the path for each program
        
        ## make the directory which will have the copies of the input file
        
        

    
#    for var1 in range(0,num_vars):
#        number_not_done = (num_vars-var1)**2
#        print((1-(number_not_done/total_number_of_comparisons) ) * 100,'%')
#        new_lines = get_spearman_big_file(infile, var1, offset = start_line+1)
#        if new_lines != None:## this means that there were at least some detected correlations
#            output_lines = output_lines + new_lines
#        
#        print("currently we've found",(len(output_lines)-1)/2,"unique relationships")
#
#
#    
#    write_table(output_lines, c_final_summary_file)


    for script in script_list:
        cmd('python3 '+script,com=False)
    
    loop=True
    while loop:
        threads_done=read_file(temp+'/status.txt','lines',quiet=True)
        if len(threads_done)==t:
            os.chdir(temp)
            TOc=temp+'/_TOc.tsv'
            c_final_summary_file=temp+'/'+control_name+'_final_relationship_summary.tsv'
            in_mine1=c_final_summary_file[:]
            
            make_file("""X_var\tY_var\tempty1\tempty2\tempty3\tempty4\tSpearman_p_val\tSpearman_rho\n""",TOc)


            os.chdir(temp)
            cmd('cat '+TOc+' '+control_dir+'/summary* > '+c_final_summary_file)
            cmd('rm '+TOc)

            time.sleep(10)
            loop=False





######################################################################################

if mineOnly:
    sys.exit('finished finding relationships')

if single_network and not page_ranks:
    sys.exit('finished finding relationships')


if very_big_file:
    print('done with relationship detection for very big file')
    cmd('remove_dups.py -infile "'+in_mine1+'"')
    #sys.exit('done with relationship detection for very big file')


##############################################################################
####                                                                      ####
#### script could be split here differentiating Method1 and Method2       ####
####                                                                      ####
##############################################################################




######################################
## import all relationships
if not perform_mine_analysis:
    ## if the interaction file is fed in at command line
    control_file=summary1
    if not single_network:
        diseased_file=summary2
else:
    ## if the mine files were created in this same call
    control_file=c_final_summary_file
    if not single_network:
        diseased_file=d_final_summary_file




######################################

##########
## go through each gene-gene pair for both control and diseased
## and compare whether or not there exists a relationship between them
##########

control_binary_interactions=np.zeros((len(IDlist),len(IDlist)),dtype='bool')
if not single_network:
    diseased_binary_interactions=np.zeros((len(IDlist),len(IDlist)),dtype='bool')


print('creating binary interaction matrices')
control_binary_interactions=get_MIC_matrix(control_binary_interactions,control_file,2,'binary')##################
if not single_network:
    diseased_binary_interactions=get_MIC_matrix(diseased_binary_interactions,diseased_file,2,'binary')###############


make_file('\n'.join(IDlist),temp+'/ID_list.txt')
if '-out_relationship_mat_only' in sys.argv:
    if verbose:
        print(control_binary_interactions[0])
        print(control_binary_interactions[1])
    make_file(flatten_2D_table(control_binary_interactions,'\t'),temp+'/control_binary_interaction_matrix.txt')

    if not single_network:
        make_file(flatten_2D_table(diseased_binary_interactions,'\t'),temp+'/diseased_binary_interaction_matrix.txt')
    


gc.collect()


#########################################################################################################
#########################################################################################################
##################                                                                     ##################
##################                     Page Rank Calculations                          ##################
##################                                                                     ##################
#########################################################################################################
#########################################################################################################


##########################################################
########## functions for calculating page ranks ##########
##########################################################

def get_variable_relationship_list(input_interactor_index_vector):
    global IDlist
    input_interactor_index_vector=list(input_interactor_index_vector[0])
    if verbose:
        print(input_interactor_index_vector)
    interactor_name_list=[]
    for i in input_interactor_index_vector:
        interactor_name_list.append(IDlist[i])
    return(interactor_name_list)
        

def get_total_relationships():
    ## this creats a dictionary with each variable as a key,
    ## the value is the number of relationships that variable has
    ## this is the 
    
    global single_network, IDhash, IDlist
    
    ## make copies of variable dictionaries, to be
    ## later re-populated with number of relationships
    ## each variable has in each dataset
    global control_binary_interactions
    control_num_relationship_dict={}
    control_relationship_dict={}
    
    if not single_network:
        global diseased_binary_interactions
        diseased_num_relationship_dict={}
        diseased_relationship_dict={}

    for g in IDlist:
        ## goes through for each variable looking at the interaction matrix and summing the number of relationships
        temp_index=IDhash[g]
        if verbose:
            print('control',g)
            print(control_binary_interactions[temp_index])
        interactions=np.ma.getmaskarray(np.ma.masked_inside(control_binary_interactions[temp_index],.5,1.5))

        if verbose:
            for i in range(0,len(interactions)):
                print(interactions[i],'\t',control_binary_interactions[temp_index][i],'\t',IDlist[i])

        control_num_relationship_dict[g]=np.sum(interactions)

        control_relationship_dict[g]=get_variable_relationship_list(np.where(interactions))
        
        if verbose:
            print(control_num_relationship_dict[g],'\n',control_relationship_dict[g],'\n\n')

    if not single_network:
        for g in IDlist:
            ## goes through for each variable looking at the interaction matrix and summing the number of relationships
            temp_index=IDhash[g]
            if verbose:
                print('diseased',g)
                print(diseased_binary_interactions[temp_index])
            interactions=np.ma.getmaskarray(np.ma.masked_inside(diseased_binary_interactions[temp_index],.5,1.5))

            if verbose:
                for i in range(0,len(interactions)):
                    print(interactions[i],'\t',diseased_binary_interactions[temp_index][i],'\t',IDlist[i],i)
        
            diseased_num_relationship_dict[g]=np.sum(interactions)

            diseased_relationship_dict[g]=get_variable_relationship_list(np.where(interactions))

            if verbose:
                print(diseased_num_relationship_dict[g],'\n',diseased_relationship_dict[g],'\n\n')

    if single_network:
        return(control_num_relationship_dict, control_relationship_dict)
    else:
        return(control_num_relationship_dict, control_relationship_dict, diseased_num_relationship_dict, diseased_relationship_dict)



def calculate_page_rank(variable, temp_pr_dict, dataset='control'):
    global IDlist ## this is a dictionary for all variables with indexes for where they are in a matrix
    if dataset=='control':
        global control_num_relationship_dict, control_relationship_dict
    else:
        global diseased_num_relationship_dict, diseased_relationship_dict
    

    ## initialize the sum of interacting pageranks at zero
    running_undampened_pr=0

    if dataset=='control':
        
        for interacting_var in control_relationship_dict[variable]:
            ## run through each of the interacting variables
            ## and add the temporary page rank of the 
            ## interacting variable over the total number of links
            ## 
            ## sum(PRi/Li)
            ## 
#            running_undampened_pr += (temp_pr_dict[interacting_var] / control_num_relationship_dict[interacting_var])

            ## this if statement was created to gaurd against errors caused by using empty martices
            if control_num_relationship_dict[interacting_var] != 0:

                running_undampened_pr += (temp_pr_dict[interacting_var] / control_num_relationship_dict[interacting_var])
            else:
                print(variable, interacting_var)
                print(control_relationship_dict[variable])
                print(control_num_relationship_dict[variable])
                print(control_relationship_dict[interacting_var])
                print(control_num_relationship_dict[interacting_var])
                sys.exit('\n\n\n'+variable+' '+interacting_var)

        
        new_pr=(1-pr_alpha)+(pr_alpha*running_undampened_pr)
        return(new_pr)


    else:
        ## using diseased dataset
        for interacting_var in diseased_relationship_dict[variable]:
            ## run through each of the interacting variables
            ## and add the temporary page rank of the 
            ## interacting variable over the total number of links
            ## 
            ## sum(PRi/Li)
            ## 

            if diseased_num_relationship_dict[interacting_var] != 0:

                running_undampened_pr += (temp_pr_dict[interacting_var] / diseased_num_relationship_dict[interacting_var])

            else:
                print(variable, interacting_var)
                print(diseased_relationship_dict[variable])
                print(diseased_num_relationship_dict[variable])
                print(diseased_relationship_dict[interacting_var])
                print(diseased_num_relationship_dict[interacting_var])
                sys.exit('\n\n\n'+variable+' '+interacting_var)

            

        
        new_pr=(1-pr_alpha)+(pr_alpha*running_undampened_pr)
        return(new_pr)
        
    
    

def initialize_page_ranks(initialization=1):
    ## because of the general size of datasets expected, for decreased floating point calculation errors
    ## the default is set to 1 instead of 1/n variables
    global IDhash
    tempPR=IDhash.copy() ## make a copy
    for i in IDlist:
        tempPR[i]=initialization
    return(tempPR)

def update_page_ranks(pr_dict, dataset='control'):
    new_pr_dict=pr_dict.copy()

    for k in list(new_pr_dict.keys()):
        new_pr_dict[k]=calculate_page_rank(k, pr_dict, dataset)

    return(new_pr_dict)


#########################################
####### calculate page ranks ############
#########################################

if single_network:
    control_num_relationship_dict, control_relationship_dict = get_total_relationships()
else:
    control_num_relationship_dict, control_relationship_dict, diseased_num_relationship_dict, diseased_relationship_dict = get_total_relationships()


if single_network and page_ranks:
    c_PR_list=[]

    #control_num_relationship_dict, control_relationship_dict = get_total_relationships()
    
    c_PR=initialize_page_ranks()
    for i in range(0,pr_iters):
        print('page rank iteration#',i)
        c_PR=update_page_ranks(c_PR)

    ## write out page ranks
    pr_output=[['variable','group1_page_ranks']]
    for var in IDlist:
        pr_output.append([var,c_PR[var]])
        c_PR_list.append(c_PR[var])
    make_file(flatten_2D_table(pr_output,'\t'),temp+'/page_ranks.txt')

    if not no_graphs:
        print('creating histogram')
        plt.clf()
        output=temp+'/'+control_name+'_histogram_of_page_ranks.png'
        hist, bins = np.histogram(c_PR_list)#,bins = 100)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width)
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

    

if not single_network and page_ranks:
    c_PR_list=[]
    d_PR_list=[]
    delta_PR_list=[]
    abs_delta_PR_list=[]

    #control_num_relationship_dict, control_relationship_dict, diseased_num_relationship_dict, diseased_relationship_dict = get_total_relationships()
    
    c_PR=initialize_page_ranks()
    for i in range(0,pr_iters):
        print('group1 page rank iteration#',i)
        c_PR=update_page_ranks(c_PR)
    
    d_PR=initialize_page_ranks()
    for i in range(0,pr_iters):
        print('group2 page rank iteration#',i)
        d_PR=update_page_ranks(d_PR, dataset='diseased')

    ## write out page ranks
    pr_output=[['variable','group1_page_ranks','group2_page_ranks','delta_page_rank','abs(delta_page_rank)']]
    for var in IDlist:
        pr_output.append([var, c_PR[var], d_PR[var], d_PR[var]-c_PR[var],abs(d_PR[var]-c_PR[var])])
        c_PR_list.append(c_PR[var])
        d_PR_list.append(d_PR[var])
        delta_PR_list.append(d_PR[var]-c_PR[var])
        abs_delta_PR_list.append(abs(d_PR[var]-c_PR[var]))
        

    make_file(flatten_2D_table(pr_output,'\t'),temp+'/page_ranks.txt')

    if not no_graphs:
        print('creating histogram')
        plt.clf()
        output=temp+'/'+control_name+'_histogram_of_page_ranks.png'
        hist, bins = np.histogram(c_PR_list)#,bins = 100)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width)
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

        print('creating histogram')
        plt.clf()
        output=temp+'/'+disease+'_histogram_of_page_ranks.png'
        hist, bins = np.histogram(d_PR_list)#,bins = 100)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width)
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

        print('creating histogram')
        plt.clf()
        output=temp+'/histogram_of_delta_page_ranks.png'
        hist, bins = np.histogram(delta_PR_list)#,bins = 100)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width)
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

        print('creating histogram')
        plt.clf()
        output=temp+'/histogram_of_abs_delta_page_ranks.png'
        hist, bins = np.histogram(abs_delta_PR_list)#,bins = 100)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width)
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)



#################################################################################################
## this section calculates the degree and non-zero median expression values to examine their relationship

if not no_graphs:
    from scipy.stats import gaussian_kde

def smooth_hist(data, name):
    ## this makes a smooth density kernel plot and saves it to name.png in the local directory
    ## adpoted from: Justin Peel https://stackoverflow.com/questions/4150171/how-to-create-a-density-plot-in-matplotlib
    global temp, dpi_in, gaussian_kde
    plt.clf()
    output=temp+'/'+str(name)+'.png'
    density = gaussian_kde(data)
    xs = np.linspace(min(data),max(data),200)
    density.covariance_factor = lambda : .25
    density._compute_covariance()
    plt.plot(xs,density(xs))
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

def line_non_zero_med(line):
    line = line[np.nonzero(line)]
    count = np.shape(line)[0]
    return(count, np.median(line))

def get_non_zero_median_expression(dataset_to_use = 'group1'):
    ## to reduce the memory footprint, we just have the function point to the already existing
    ## data matrix for the expression of either group1 or group 2
    global num_vars
    out_vect = []
    if dataset_to_use == 'group1':
        global group1
        for i in range(0,num_vars):
            out_vect.append(line_non_zero_med(group1[i,1:].astype('float32') ))
        
    else:
        global group2
        for i in range(0,num_vars):
            out_vect.append(line_non_zero_med(group2[i,1:].astype('float32') ))



## calculate the degree of all variables

if single_network:
    output_degree_nonzero_med_express = [['variable',control_name+'_degree',control_name+'_med_no_zero_vals',control_name+'_countNonZero']]

    ## make a plot of the degree
    if not no_graphs:
        smooth_hist(np.log2(np.array(list(control_num_relationship_dict.values()))+1),control_name+'_log2_degree')
        
    ## go through the ID_list and get the degree    
    

if not single_network:
    output_degree_nonzero_med_express = [['variable',control_name+'_degree',control_name+'_med_no_zero_vals',control_name+'_countNonZero', disease+'_degree',disease+'_med_no_zero_vals',disease+'_countNonZero']]
    if not no_graphs:
        smooth_hist(np.log2(np.array(list(control_num_relationship_dict.values()))+1),control_name+'_log2_degree')
        smooth_hist(np.log2(np.array(list(diseased_num_relationship_dict.values()))+1),disease+'_log2_degree')
        #smooth_hist(control_num_relationship_dict.values(),control_name+'_degree')
        #smooth_hist(diseased_num_relationship_dict.values(),disease+'_degree')

if not very_big_file:
    ## go through each 
    group1_degree=[]
    group1_med_non_zero_expression = []
    if not single_network:
        group2_degree=[]
        group2_med_non_zero_expression = []
    for i in range(0,num_vars):
    
        temp_var_id = IDlist[i]
        temp_new_line = [temp_var_id]
        temp_new_line.append(control_num_relationship_dict[temp_var_id])
        temp_count, temp_non_zero_med = line_non_zero_med(group1[i,1:].astype('float32') )
        temp_new_line.append(temp_non_zero_med)
        temp_new_line.append(temp_count)
        group1_degree.append(temp_new_line[1])
        group1_med_non_zero_expression.append(temp_new_line[2])
        
        if not single_network:
    
            temp_new_line.append(diseased_num_relationship_dict[temp_var_id])
    
    
            temp_count, temp_non_zero_med = line_non_zero_med(group2[i,1:].astype('float32') )
            temp_new_line.append(temp_non_zero_med )
            temp_new_line.append(temp_count)
            
            group2_degree.append(temp_new_line[4])
            group2_med_non_zero_expression.append(temp_new_line[5])
    
        
        output_degree_nonzero_med_express.append(temp_new_line)
    
    ## write this data table to file
    write_table(output_degree_nonzero_med_express, temp+'/degree_nonzero_med_express.txt')
    
## plot the relationship between degree and med non-zero epxression
def degree_non_zero_plot(non_zero_med, degree, name):
    global temp, dpi_in, gaussian_kde
    plt.clf()
    output=temp+'/'+str(name)+'_MedNonZero_Degree.png'
    
    degree = np.log2(np.array(degree)+1)
    
    # Calculate the point density
    xy = np.vstack([non_zero_med, degree])
    z = gaussian_kde(xy)(xy)
    
    fig, ax = plt.subplots()
    ax.scatter(non_zero_med, degree, c=z, s=5, edgecolor='')
    ax.set_xlabel('Median Non-Zero Expression')
    ax.set_ylabel('log2(degree+1)')
    
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

do_non_zero_degree = False
if do_non_zero_degree and not no_graphs and not very_big_file:
    degree_non_zero_plot(group1_med_non_zero_expression,group1_degree, control_name)
    if not single_network:
        degree_non_zero_plot(group2_med_non_zero_expression,group2_degree, disease)





#################################################################################################


#################################################################################################
#################################################################################################
################     dimention reduction on the interaction matrices      #######################
################          then find and initialize k-clusters             #######################
#################################################################################################
#################################################################################################



def do_k_means_unknown_k(large_cluster_name, variable_names, interaction_matrix, expression_matrix = False):
    interaction_matrix = interaction_matrix.astype('float32')
    if not expression_matrix:
        np.fill_diagonal(interaction_matrix, 1.0)
    
    ## this variable is for testing passed a local minimum of the f(k) function
    stopping_length = 10
    
    if interaction_matrix.shape[0] <= stopping_length:
        print('interaction_matrix is too small to subdivide')
        large_cluster_list = [large_cluster_name]*len(variable_names)
        output_cluster_annotations = list(zip(variable_names, large_cluster_list, [0]*len(variable_names)))
        return(output_cluster_annotations)
    
    
    ## find the variable with the greatest variance
    row_std = np.std(interaction_matrix, axis = 0)
    max_row_std = np.max(row_std)
    centroid_initialization_index = sample(list(np.where(row_std == max_row_std)[0]), 1)
    
    centroid_indices = centroid_initialization_index[:]
    
    temp_centroids, variable_labels = kmeans2(interaction_matrix, interaction_matrix[centroid_indices,:], minit='matrix', iter=10)
    
    print('\ncentroid_indices for k =',len(centroid_indices))
    print(centroid_indices)
    print('\n\n')
    
    ## initialize with k = 1
    Sk = None
    Ak = None
    temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, [list(variable_labels)], interaction_matrix)
    f_list = [temp_f]
    centroid_distances_matrix = np.array(get_all_distances_from_a_centroid(interaction_matrix[centroid_indices[-1]], interaction_matrix))
    
    print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)
    
    while k_stopping_function(f_list, num_vars = len(variable_names)):
        ## first thing to do is find out all the current distances from all centroids
        if len(centroid_indices)>1:
            centroid_distances_matrix = np.hstack((centroid_distances_matrix, np.array(get_all_distances_from_a_centroid(interaction_matrix[centroid_indices[-1]], interaction_matrix))))
        
        ## find the index of the next centroid based on the current distance matrix
        next_centroid = get_next_centroid_index(centroid_distances_matrix, existing_centroids = centroid_indices)
        if next_centroid in centroid_indices:
            ## this means that the newly of the remaining points, there are now ties
            ## with already existing centroids for farthest away from other centroids
            print('already established centroid was picked again')
            break
        centroid_indices.append(next_centroid)
        print('\ncentroid_indices for k =',len(centroid_indices))
        print(centroid_indices)
        print('\n\n')
        
        temp_centroids, variable_labels = kmeans2(interaction_matrix, interaction_matrix[centroid_indices,:], minit='matrix', iter=10)
        
        ## this function will take variable labels of format [0,1,1,0,0,2]
        ## and change it to: 
        ## [[0,3,4], ## centroid 0
        ##    [1,2],   ## centroid 1
        ##     [5]]     ## centroid 2
        variable_labels = rearrange_variable_labels(variable_labels)
       # print('variable_labels\n',variable_labels)
        if len(variable_labels) < len(centroid_indices):
            ## this means that two centroids have converged during the k-means clustering, indicating
            ## that the number of centroids is already oversaturated
            print("centroids converged, stopping due to overfit")
            break
        
        
        temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, variable_labels, interaction_matrix)
        f_list.append(temp_f)
        print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)
        
    print(k_stopping_function(f_list, num_vars = len(variable_names)))
    if not k_stopping_function(f_list, num_vars = len(variable_names)):
        
        print(f_list)
#    optimal_k_index = f_list.index(min(f_list))
    optimal_k_index=get_estimated_k_from_f_list(f_list)
    print('optimal k =',optimal_k_index+1)
    
    optimal_centroid_indices = centroid_indices[:optimal_k_index+1]
    #print(optimal_centroid_indices)
    
    final_centroids, final_variable_labels = kmeans2(interaction_matrix, interaction_matrix[optimal_centroid_indices,:], minit='matrix', iter=10)
    
    ## convert the final variable labels into a list of lists containing the variable names
    rearranged_var_labels = rearrange_variable_labels(final_variable_labels)
    out_var_group_list_of_lists = []
    for r in rearranged_var_labels:
        out_var_group_list_of_lists.append(list(variable_names[var] for var in r))
    
    
    ## sipmly make a list of the original cluster name for a column in the output file
    large_cluster_list = [large_cluster_name]*len(variable_names)
    
    output_cluster_annotations = list(map(list,zip(variable_names, large_cluster_list, final_variable_labels)))
    
    return(output_cluster_annotations, out_var_group_list_of_lists)

###########################################################################################################################


def do_PCA(group = 'group1'):
    if 'plt' not in globals():
        print('matplotlib is required for PCA analysis of co-regulation matrix')
        return(None)
    global IDlist, linalg, temp, plt, eigh
    ## do the PCA using the eigenvectors and eigenvalues of the covariance matrix
    ## of the binary interaction matrix from np.linalg.eigh
    ## 
    print('creating eigenvectors and eigenvalues')

    
    ## calculate covariance matrix for calculating eigen-vectors/values
    
    if group == 'group1':
        global control_binary_interactions
        cov_mat=np.cov(control_binary_interactions.astype(np.dtype('int8')))
    elif group == 'group2':
        global diseased_binary_interactions
        cov_mat=np.cov(diseased_binary_interactions.astype(np.dtype('int8')))
    
    ######### use scipy's eigh on the covariance matrix #########
    
    print(cov_mat)

    ## get the eigen values and eigenvectors of the covariance matrix
    eig_vals, eig_vecs = eigh(cov_mat)
    
    ## sort by greatest eigenvalues
    ## this will bring show us the eivenvectors of of greatest variation
    idx = np.argsort(eig_vals)[::-1]
    eig_vals = eig_vals[idx]
    
    # sort eigenvectors according to same index
    eig_vecs = eig_vecs[:,idx]
    
    ## get the singluar values and PC_scores
    singluar_values = np.nan_to_num(np.sqrt(eig_vals))
    print('c_singluar_values\n', singluar_values)
    
    PC_scores = eig_vecs * singluar_values
    print('c_PC_scores\n',PC_scores)
    



    
    
    print('c_eig_vecs',eig_vecs.shape)
    print(eig_vecs)
    print('c_eig_vals',eig_vals.shape)
    print(eig_vals)
    
    for ev in eig_vecs:
        np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
    print('np.sum, axis = 0:',np.sum(eig_vecs, axis = 0))
    print('np.sum, axis = 1:',np.sum(eig_vecs, axis = 1))
        
    percent_var = eig_vals / np.sum(eig_vals)
    print('percent_var\n',percent_var)
    
    cumulative_var = np.cumsum(percent_var)
    print('cumulative_var\n',cumulative_var)
    
    ##########################################################################
    ## how many eigenvectors to include?
    ## the cutoff is to determine which eigenvector will be the last
    ## based on the percentage of variance accounted for
    ## as indicated by the eivenvalues
    cum_var_cutoff = 0.90
    
    

    ## find the cutoff eigenvector whose cumulative variance explained is greater than 
    ## the predetermined cutoff (ie: cum_var_cutoff)
    index_cutoff = np.amin(np.where(cumulative_var >= cum_var_cutoff))

    print(cumulative_var[0:index_cutoff+1])
    
    print('cutoff:',index_cutoff)

    output_PCs = flatten_2D_table(PC_scores, '\t')
    PC_column_titles = ['variable']
    for load in range(1,len(PC_scores[0])):
        ## PC#_(%variance explained) % variance explained is determined by eigenvalue, not singular value
        PC_column_titles[0]+='\tPC_'+str(load)+'_('+str(cumulative_var[load])+')'
    PC_column_titles+='\n'
    
    ## append variable names to each row
    for i in range(0,len(IDlist)):
        output_PCs[i] = IDlist[i] + '\t' + output_PCs[i]
    
    ## append the title columns onto the rest of the data
    output_PCs = PC_column_titles + output_PCs
    important_PC_scores = PC_scores[:,0:index_cutoff+1]
    
    ## write output of all PC PC_scores
    if group == 'group1':
        make_file(output_PCs, temp+'/'+control_name+'_PC_scores.txt')
    elif group == 'group2':
        make_file(output_PCs, temp+'/'+disease+'_PC_scores.txt')
        
    
    
    
    ## select only the top n eigenvectors
    important_eig_vec_mat = eig_vecs[:,0:index_cutoff+1]
    
    output_eigen_vectors=flatten_2D_table(important_eig_vec_mat,'\t')
    
    ## make the titles for columns
    eigen_vector_column_titles=['variable']

    for eig in range(1,index_cutoff+2):
        eigen_vector_column_titles+='\teigen_vector_'+str(eig)+'_('+str(eig_vals[eig-1])+')'
    eigen_vector_column_titles+='\n'
    
    ## append variable names to each row
    for i in range(0,len(IDlist)):
        output_eigen_vectors[i] = IDlist[i] + '\t' + output_eigen_vectors[i]
    
    ## append the title columns onto the rest of the data
    output_eigen_vectors = eigen_vector_column_titles + output_eigen_vectors
    
    
    if group == 'group1':
        make_file(output_eigen_vectors, temp+'/'+control_name+'_eigenvectors_up_to_'+str(cum_var_cutoff)+'.txt')
    if group == 'group2':
        make_file(output_eigen_vectors, temp+'/'+disease+'_eigenvectors_up_to_'+str(cum_var_cutoff)+'.txt')    
    
    
    #from scipy.spatial.distance import pdist
    
    dist_euc = get_distance_matrix(important_PC_scores)
    #dist_euc = pdist(important_PC_scores)
    #print(dist_euc)
    print(dist_euc.shape)
    
    import scipy.cluster.hierarchy as hclust
    
    Y = hclust.linkage(dist_euc, method='centroid', metric='euclidean')
    print(Y.shape)
    print(Y)
    
    
    

    
    if not no_graphs:
        
        if group == 'group1':
            output=temp+'/'+control_name+'_PCA_interactions.png'
        elif group == 'group2':
            output=temp+'/'+disease+'_PCA_interactions.png'
        plt.clf()
        ## heatmap script here
        
        fig = plt.figure(figsize=(8,8))
        ax1 = fig.add_axes([0.09, 0.1, 0.2, 0.6])
        
        Z1 = hclust.dendrogram(Y, orientation='right', color_threshold = .5*np.amax(Y[:,2]))
        
        
        print(dir(Z1))
        print(Z1)
        print(Y[:,2])
        print(.5*np.amax(Y[:,2]))
        
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Plot distance matrix.
        axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
        idx1 = Z1['leaves']
        important_PC_scores = important_PC_scores[idx1,:]

        im = axmatrix.matshow(important_PC_scores, aspect='auto', origin='lower', cmap=plt.cm.seismic)
        axmatrix.set_xticks([])
        axmatrix.set_yticks([])
        
        # Plot colorbar.
        axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
        plt.colorbar(im, cax=axcolor)
        
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

    return(important_PC_scores)




###### filter interaction matrices for only variables that have at least 1 relationship #####
## I found that with these orphan nodes included, the algorithm used for initializing 
## centroids tendend to largely assign orphan nodes their own centroid. While true that these 
## are in their own groups, it is often not useful for large scale analyses to include


## find indices that have the row sum == 0 in the interaction matrix



c_non_zero_indices = np.where(np.sum(control_binary_interactions.astype('int8'), axis = 0) != 0)
print(list(c_non_zero_indices[0]))
c_non_zero_indices=list(c_non_zero_indices[0])
c_binary_non_zero_intaractions = control_binary_interactions[c_non_zero_indices,:][:,c_non_zero_indices].astype('int8')
c_non_zero_vars = [IDlist[i] for i in c_non_zero_indices]



print(c_non_zero_vars)
print(c_binary_non_zero_intaractions)

if not single_network:
    d_non_zero_indices = np.where(np.sum(diseased_binary_interactions.astype('int8'), axis = 0) != 0)
    d_non_zero_indices=list(d_non_zero_indices[0])
    d_binary_non_zero_intaractions = diseased_binary_interactions[d_non_zero_indices,:][:,d_non_zero_indices].astype('int8')
    print(d_non_zero_indices)
    
    d_non_zero_vars = [IDlist[i] for i in d_non_zero_indices]
    
    
    print(d_non_zero_vars)
    print(d_binary_non_zero_intaractions)
    

##############################################################################
## go through each group and generate mean and sd summaries, then write to file

if not very_big_file:
    
    sample_names = list(title)[1:]
    print(sample_names)
    list_of_k_sample_indices=[]
    
    for k in sample_k_lists:
        print(k)
        temp_indices_list=[]
        for i in range(0,len(k)):
            temp_indices_list.append(sample_names.index(k[i]))
        list_of_k_sample_indices.append(temp_indices_list)


    print(list_of_k_sample_indices)
    list_of_k_sample_indices = np.array(list_of_k_sample_indices)

    ## initialize mean and sd output tables
    print(list_of_k_sample_indices[0])
    test=full_expression[:,list_of_k_sample_indices[0]]
    #print(np.mean(test.astype('float32'), axis = 1))
    #print(full_expression[:,list_of_k_sample_indices[0]].shape)




    ## calculate the means accross rows
    all_sample_mean = np.transpose(np.array([np.mean(full_expression, axis=1)]))
    all_sample_sd = np.transpose(np.array([np.std(full_expression, axis=1)]))
    k_group_means = np.transpose(np.array([np.mean(full_expression[:,list_of_k_sample_indices[0]], axis=1)]))
    k_group_sd = np.transpose(np.array([np.std(full_expression[:,list_of_k_sample_indices[0]], axis=1)]))


    for k in range(1,len(list_of_k_sample_indices)):
        ## calc row means
        new_mean_col = np.transpose(np.array([np.mean(full_expression[:,list_of_k_sample_indices[k]], axis=1)]))
        k_group_means = np.hstack((k_group_means, new_mean_col))
    
        ## calc sd
        new_sd_col = np.transpose(np.array([np.std(full_expression[:,list_of_k_sample_indices[k]], axis=1)]))
        k_group_sd = np.hstack((k_group_sd, new_sd_col))

##############################################################################
########### use the means of the k-means groups to calculate the enrichment



    ## calculate the sample group z-scores ((Xbar-Mu)/sigma) * sqrt(n), or (Xbar-Mu)/(sigma/sqrt(n))
    print("calculating the sample group vs all sample means")
    print("np.shape(k_group_means)")
    print(np.shape(k_group_means))
    print("np.shape(all_sample_mean)")
    print(np.shape(all_sample_mean))
    row_delta = np.array(k_group_means.transpose() - all_sample_mean.transpose()).transpose()
    print(np.shape(row_delta))
    for k in range(0,len(list_of_k_sample_indices)):
        print(k)
        row_delta[:,k] = np.array(row_delta[:,k].transpose() / all_sample_sd[:,0].transpose()).transpose()
        row_delta[:,k] = row_delta[:,k] * np.sqrt(len(list_of_k_sample_indices[k]))

    sample_k_group_enrichment = row_delta
    sample_k_group_enrichment_numeric = sample_k_group_enrichment




    #######################################################


    #sample_k_group_enrichment = np.log2(k_group_means_norm / mean_of_group_means)
    print(np.shape(sample_k_group_enrichment))
    print('sample_k_group_enrichment',sample_k_group_enrichment)


    sample_groups = []
    for k in range(0,len(list_of_k_sample_indices)):
        #print(k)
        sample_groups.append('sample_group_'+str(k))
        #print(sample_groups)
    sample_groups = np.array(sample_groups)
    print(np.shape(sample_groups))
    print(sample_groups)

    k_group_means = np.vstack((sample_groups,k_group_means))
    k_group_sd = np.vstack((sample_groups,k_group_sd))
    sample_k_group_enrichment = np.vstack((sample_groups, sample_k_group_enrichment))

    ##############################################################################
    ##### prepare the k-means enrichment for writing to file, then write it
    
    ## these are the names of the variables, making the row labels for the output table
    row_names = np.transpose(np.array([['var_names']+IDlist]))
    
    
    k_group_means = np.hstack((row_names, k_group_means))
    k_group_sd = np.hstack((row_names, k_group_sd))
    sample_k_group_enrichment = np.hstack((row_names, sample_k_group_enrichment))



    write_table(k_group_means,sample_dir+'k_group_means.txt')
    write_table(k_group_sd,sample_dir+'k_group_sd.txt')
    write_table(sample_k_group_enrichment, sample_dir+'k_group_enrichment.txt')
    
    
    print('sample_k_group_enrichment')
    print(sample_k_group_enrichment)
    print(sample_k_group_enrichment[1:,:][:,1:])


##################################################################################################################
##### do a one way anova between groups to test for variables that are significantly different between them ######

from scipy.stats.mstats import f_oneway as aov

def get_anova(index):
    #print('\n'*10)
    global full_expression, list_of_k_sample_indices
    list_of_group_values=[]
    for group in range(0,len(list_of_k_sample_indices)):
        #print(len(list_of_k_sample_indices[group]))
        list_of_group_values.append(full_expression[i,list_of_k_sample_indices[group]])
        #print(np.shape(list_of_group_values[-1]))
        #print(list_of_group_values[-1])
        
    return_val = list(aov(*list_of_group_values))
#    print(return_val)
    return(return_val)


## this function was adopted from emre's stackoverflow answer found here:
## https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python
def correct_pvalues_for_multiple_testing(pvalues, correction_type = "Benjamini-Hochberg"):                
    """                                                                                                   
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    from numpy import array, empty
    pvalues = array(pvalues)
    n = float(pvalues.shape[0])
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        for rank, vals in enumerate(values):
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue
    elif correction_type == "Benjamini-Hochberg":                                                         
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        values.reverse()
        new_values = []
        for i, vals in enumerate(values):
            rank = n - i
            pvalue, index = vals
            new_values.append((n/rank) * pvalue)
        for i in range(0, int(n)-1):
            if new_values[i] < new_values[i+1]:
                new_values[i+1] = new_values[i]
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]
    return new_pvalues


if not very_big_file:
    if len(list_of_k_sample_indices) > 1:
        enough_k_samples = True
    else:
        enough_k_samples = False
else:
    enough_k_samples = False



if not very_big_file and enough_k_samples:
    anova_output = [['Variable', 'F', 'uncorrected_p-val', 'BH_corrected_p-val','-log10(BH_cor_p-val)']]
    aov_uncorrected_p_val_list=[]

## go through each variable and get the uncorrected anova stats
    for i in range(0,len(IDlist)):
        anova_output.append([IDlist[i]]+get_anova(i))
        aov_uncorrected_p_val_list.append(anova_output[-1][-1])

    #print(aov_uncorrected_p_val_list)
    #for line in anova_output:
    #    print(line)
    ## correct the p-values with Benjamini-Hochberg 
    BH_corrected_aov = correct_pvalues_for_multiple_testing(aov_uncorrected_p_val_list)
    indices_less_than_FDR_cutoff=[]
    for i in range(0,len(IDlist)):
        anova_output[i+1]+=[BH_corrected_aov[i], -1*np.log10(BH_corrected_aov[i])]
        if BH_corrected_aov[i] <= FDR_cutoff:
            indices_less_than_FDR_cutoff.append(i)


    cmd('mkdir "'+temp+'/sample_clustering_and_summary/significance"')
    write_table(anova_output , temp+'/sample_clustering_and_summary/significance/groups_1way_anova_results.txt')

    ################################################################################################
    ############# Find the significantly different & enriched variables for each group #############
    ################################################################################################

    ## we start off with the variables that are significantly different between groups
    
    ## this is a list of lists for each 
    group_sig_enriched_bool=[]


    for i in range(0,len(IDlist)):
        ## check to see if this variable was significant in the BH corrected 1-way anova
        if i in indices_less_than_FDR_cutoff:
            var_significant = True
        else:
            var_significant = False
        
        ## if it's significant, we want to go in and check which, if any sample groups 
        ## show an elevated z-score enrichment (greater than the zscore_cutoff variable)
        if var_significant:
            temp_sig_enriched_bool_list = list(sample_k_group_enrichment_numeric[i,] >= zscore_cutoff)
        else: 
            temp_sig_enriched_bool_list = [False]*len(list_of_k_sample_indices)
        
        group_sig_enriched_bool.append(temp_sig_enriched_bool_list)
    
    bool_sample_groups = []
    for s in sample_groups:
        bool_sample_groups.append('bool_'+s)
    bool_sample_groups = np.array(bool_sample_groups)
    
    group_sig_enriched_bool = np.array(group_sig_enriched_bool)
    group_sig_enriched = np.vstack((bool_sample_groups,group_sig_enriched_bool))
    group_sig_enriched = np.hstack((row_names,group_sig_enriched))
    
    write_table(group_sig_enriched, temp+'/sample_clustering_and_summary/significance/significant_and_enriched_boolean_table.txt')
    
    ## go through each group, and make a list of the variables that are significant and enriched
    num_sig_enriched = []
    for group in range(0,len(list_of_k_sample_indices)):
        sig_and_enriched_for_this_group = []
        for var in range(0,len(IDlist)):
            if group_sig_enriched_bool[var,group]:
                sig_and_enriched_for_this_group.append(IDlist[var])
        num_sig_enriched.append(len(sig_and_enriched_for_this_group))
        make_file('\n'.join(sig_and_enriched_for_this_group), temp+'/sample_clustering_and_summary/significance/'+sample_groups[group]+'_significant_enriched.txt')
    
#    print(np.shape(sample_groups))
#    print(np.shape(np.array(num_sig_enriched)))
#    print(num_sig_enriched)
    num_sig_enriched = np.transpose(np.vstack((np.array([sample_groups]),np.array([num_sig_enriched]))))
    
    num_sig_enriched = np.vstack((np.array([['sample_group', 'number_of_significant_and_enriched_vars']]), num_sig_enriched))
    
    write_table(num_sig_enriched, temp+'/sample_clustering_and_summary/significance/number_of_variables_significant_and_enriched_for_each_group.txt')


################################################################################################
####################           find all connected components          ##########################
################################################################################################
if very_big_file:
    connected_graph=False
else:
    connected_graph=True
    

## if a connected component of the graph contains x% ("sub_connectivity_cutoff") of all nodes
## then put it through k-means clustering to find if there are any sub-sets that fall out
sub_connectivity_cutoff = 0.01

def subset_interaction_matrix(indices, interaction_matrix):
    ## this function will return a symetric subset matrix
    ## example:
    ## input matrix    ->     subset from indices [0,1,2]
    ## [[a,a,a,b,b,b],            [[a,a,a],
    ##  [a,a,a,b,b,b],             [a,a,a],
    ##  [a,a,a,b,b,b],             [a,a,a]]
    ##  [b,b,b,b,b,b],
    ##  [b,b,b,b,b,b],
    ##  [b,b,b,b,b,b]]
    global IDlist
    
    subset_matrix = interaction_matrix [indices,:][:,indices]
    subset_vars = [IDlist[i] for i in indices]
    return(subset_vars, subset_matrix)

def get_component_sizes(number_of_components, component_labels):
    ## quantifies how many members there are in each component
    ## this is then used to compare with the sub_connectivity_cutoff to
    ## see if it's big enough to do k clustering on
    global sub_connectivity_cutoff, IDlist
    print(component_labels)
    component_labels = list(component_labels)
    print(component_labels)
    num_vars = len(IDlist)
    component_qunatifications = []
    components_greater_than_cutoff = []
    for i in range(0,number_of_components):
        temp_count = component_labels.count(i)
        component_qunatifications.append([i,temp_count, temp_count/num_vars])
        if (temp_count>6) and (temp_count/num_vars > sub_connectivity_cutoff):
            ## the component must have at least 6 members in it, or be larger than the sub_connectivity_cutoff
            components_greater_than_cutoff.append(i)
    return(component_qunatifications, components_greater_than_cutoff)


def get_var_sub_component_dict(num_sub_components, list_of_sub_components):
    global IDhash
    ## list of components is organized like this:
    ## [['var1', 0],
    ##  ['var2', 0]...]
    print('get_var_sub_component_dict')
    print(list_of_sub_components)
    sub_component_members = {}
    for i in range(0,num_sub_components):
        print('component',i)
        if i not in list(sub_component_members.keys()):
            sub_component_members[i]={}
            sub_component_members[i]['IDs']=[]
            sub_component_members[i]['indices']=[]
            #print(sub_component_members[i])
        for j in range(0, len(list_of_sub_components)):
            if list_of_sub_components[j][1]==i:
                #print(sub_component_members[i])
                #print('\n',list_of_sub_components[j])
                temp_component = sub_component_members[i]
                #print(temp_component)
                temp_component['IDs'] = temp_component['IDs'][:] + [list_of_sub_components[j][0]]
                #print(temp_component)
                temp_component['indices'] = temp_component['indices'][:] + [IDhash[list_of_sub_components[j][0]]]
                
                
                sub_component_members[i] = temp_component
                #temp_component_indices = sub_component_members[i]['indices']
                #sub_component_members[i]['indices'] = temp_component_indices.append(IDhash[list_of_sub_components[j][0]])
    return(sub_component_members)


if connected_graph:
    print('getting all connected components')
    from scipy.sparse.csgraph import connected_components
    
    ###############################################################
    ###############################################################
    def do_component_k_analysis(interaction_matrix, group='group1'):
        global IDlist, IDhash
        if group == 'group1':
            global contorl_name, cluster_prob
            name = control_name
        elif group == 'group2':
            global disease, cluster_prob
            name = disease
        print(name)
        ## get all of the connected components
        number_of_components, component_labels = connected_components(interaction_matrix)
        
        ## figure out how big each component is, and whether they should be sub-clustered
        component_qunatifications, components_greater_than_cutoff = get_component_sizes(number_of_components, component_labels)
        ## if a component is smaller than 6, we'll assume there are no subcomponents

    
        ## get ready to export the connected components\t
        component_labels = list(map(list,zip(IDlist,list(component_labels))))
        
        component_membership = get_var_sub_component_dict(number_of_components, component_labels)
        print(component_membership)
        make_file(flatten_2D_table([['variable','component']]+list(map(list,list(component_labels))), '\t'), temp+'/'+name+'_components.txt')
        cmd('mkdir "'+temp+'/'+name+'_sub_components"')
        all_component_subcomponent_list = [['variable','component','sub_group']]
        
        for component in range(0,number_of_components):
            if component in components_greater_than_cutoff:
                cmd('mkdir "'+temp+'/'+name+'_sub_components/'+str(component)+'"')
                print(component_membership[component]['indices'])
                temp_subset_vars, temp_interaction_sub_matrix = subset_interaction_matrix(component_membership[component]['indices'], interaction_matrix)
                
                make_file('\n'.join(temp_subset_vars), temp+'/'+name+'_sub_components/'+str(component)+'.txt')
                ########### perform k means on expression within this component #########
                #print(component_membership[component]['indices'])
                #print(component_membership[component]['IDs'])
                #print(IDlist[component_membership[component]['indices'][0]])
                if cluster_prob or first_prob:
                    sub_component_list, sub_component_var_list, f_list, optimal_centroid_indices = do_unknown_k_means_clustering_iter(temp_subset_vars, np.transpose(linear_normalization(full_expression))[:,component_membership[component]['indices']])
                    
                else:
                    sub_component_list, sub_component_var_list, f_list, optimal_centroid_indices = unknown_k_means_sample(temp_subset_vars, np.transpose(linear_normalization(full_expression))[:,component_membership[component]['indices']])
                
                for i in range( 0, len(sub_component_list) ):
                    sub_component_list[i] = [sub_component_list[i][0],component,sub_component_list[i][1]]
                print(len(sub_component_list), len(sub_component_list[0]))
                print(sub_component_list[0])
                print(len(sub_component_var_list),len(sub_component_var_list[0]))


                print('component#',component, '\tsubcomponents')
                for c in sub_component_list:
                    print(c)
                for s in range(0,len(sub_component_var_list)):
                    print('subcomponent:',s)
                    print(sub_component_var_list[s])
                
                for s in range(0,len(sub_component_var_list)):
                    make_file('\n'.join(map(str,sub_component_var_list[s])),temp+'/'+name+'_sub_components/'+str(component)+'/'+str(s)+'.txt')
            else:
                temp_subset_vars, temp_interaction_sub_matrix = subset_interaction_matrix(component_membership[component]['indices'], interaction_matrix)
                sub_component_list = map(list,zip(temp_subset_vars, [component] * len(temp_subset_vars), [0] * len(temp_subset_vars)))
            all_component_subcomponent_list += sub_component_list
        #print('\n\n\nall_component_subcomponent_list')
        #print(all_component_subcomponent_list)
        
        all_component_subcomponent_list[0]+=['unique_group_subgroup_id']
        
        unique_component_subcomponent_dict = {}
        unique_component_subcomponent_list = []
        
        
        sub_comp_vector_correctly_ordered = np.zeros(len(IDlist),dtype=int)
        for i in range(1,len(all_component_subcomponent_list)):
            temp_id = str(all_component_subcomponent_list[i][1:])
            #print(temp_id)
            #sys.exit('temp_id')
            if temp_id not in unique_component_subcomponent_list:
                unique_component_subcomponent_list.append(temp_id)
                unique_component_subcomponent_dict[temp_id] = len(unique_component_subcomponent_list)
            all_component_subcomponent_list[i]+=[unique_component_subcomponent_dict[temp_id]]
            print(all_component_subcomponent_list[i])
            temp_var_id = all_component_subcomponent_list[i][0]
            sub_comp_vector_correctly_ordered[IDhash[temp_var_id]] = all_component_subcomponent_list[i][-1]-1## -1 because subcomponent lists start with 1 instead of zero, if this isn't corrected, it will throw an error
            print(sub_comp_vector_correctly_ordered[IDhash[temp_var_id]])
            
        
        all_component_subcomponent_list_copy = all_component_subcomponent_list[:]
        
        make_file(flatten_2D_table(all_component_subcomponent_list_copy,'\t'),temp+'/'+name+'_components_and_sub_components.txt')
        #sys.exit()
        ## make the general stats on how many members are in each sub_component
        sub_comp_list = []
        for i in range(1,len(all_component_subcomponent_list)):## starting at 1 to skip title line
            ## -1 because for some reason the subcomponents came out starting at 1 instead of zero.  Not sure where that is in the code though
            #print(all_component_subcomponent_list[i])
            sub_comp_list.append(int(all_component_subcomponent_list[i][-1])-1)
            
        
        sub_comp_list = rearrange_variable_labels(list(sub_comp_vector_correctly_ordered))
        
        sub_comp_output_stats = [['unique_subcomponet_id','number_of_members']]
        for sub in range(0,len(sub_comp_list)):
            sub_comp_output_stats.append([sub+1,len(sub_comp_list[sub])])
            print(sub_comp_output_stats[-1])
            print(sub_comp_list[sub])
        sub_comp_stats_file = temp+'/'+name+'_sub_component_stats.txt'
        make_file(flatten_2D_table(sub_comp_output_stats,'\t'),sub_comp_stats_file)
        
        return(sub_comp_list)
    
    ###############################################################
    ###############################################################
    
    g1_sub_comp_list = do_component_k_analysis(control_binary_interactions,group = 'group1')
    if not single_network:
        g2_sub_comp_list = do_component_k_analysis(diseased_binary_interactions,group = 'group2')
        

#######################################################################################
#######################################################################################
## calculate the sample enrichment for each variable component/subcomponent

def group_component_enrichment(sub_comp_list, sample_k_group_enrichment):
    sample_k_group_enrichment = sample_k_group_enrichment.astype('float32')
    ## initialize the output component group enrichment matrix
    
    print('comp0 subset')
    
    print(sub_comp_list[0])
    for s in sub_comp_list[0]:
        print(s)
        print(IDlist[s])
        print(sample_k_group_enrichment[s,:])
    print(sample_k_group_enrichment[np.array(sub_comp_list[0]),:])

    group_component_enrichment = np.array([np.median(sample_k_group_enrichment[np.array(sub_comp_list[0]),:], axis = 0)])
    print(group_component_enrichment)
    #sys.exit()

    for comp in range(1,len(sub_comp_list)):
        ## subset the current component's variable indices
        temp_comp = np.array(sub_comp_list[comp])

        ## subset these indices from the enrichment table
        #temp_comp_enrichment_median = np.mean(sample_k_group_enrichment[temp_comp,:], axis = 0)
        temp_comp_enrichment_median = np.median(sample_k_group_enrichment[temp_comp,:], axis = 0)

        #print(temp_comp_enrichment_median)
        group_component_enrichment = np.vstack((group_component_enrichment , temp_comp_enrichment_median))
    
    ## make and append the column and row names
    col_names = []
    for i in range(0,len(sample_k_group_enrichment[0])):
        col_names.append('sample_group_'+str(i))
    row_names = ['component_id']
    for i in range(0,len(sub_comp_list)):
        row_names.append('unique_group_subgroup_id_'+str(i+1))
    
    
    print(np.array(col_names))
    print(np.array(row_names))
    group_component_enrichment = np.vstack((np.array([col_names]) , group_component_enrichment))
    group_component_enrichment = np.hstack((np.transpose(np.array([row_names])) , group_component_enrichment))
    
    return(group_component_enrichment, sub_comp_list)


if not very_big_file:
    g1_comp_enrichment, g1_sub_comp_list = group_component_enrichment(g1_sub_comp_list, sample_k_group_enrichment[1:,:][:,1:])
    cmd('mkdir "'+temp+'/component_group_enrichment"')
    write_table(g1_comp_enrichment, temp+'/component_group_enrichment/'+control_name+'_group_component_enrichment.txt')
    if not single_network:
        g2_comp_enrichment, g2_sub_comp_list = group_component_enrichment(g2_sub_comp_list, sample_k_group_enrichment[1:,:][:,1:])
        write_table(g2_comp_enrichment, temp+'/component_group_enrichment/'+disease+'_group_component_enrichment.txt')


#######################################################################################
#######################################################################################



#################################################################################
#######   calculate the subcomponent enrichment for individual samples  #########
#################################################################################


## calculate the median of the gene enrichment, for each subcomponent within each sample
## For this we use the sample_var_enrichment matrix defined earlier


#print(type(g1_sub_comp_list))
#print(g1_sub_comp_list[0])

#g1_sub_comp_list = np.array(g1_sub_comp_list)


#temp_sub_comp_list = np.array(g1_sub_comp_list)

## I need to find the variable that has the subcomponent list of lists (with indices)

def get_sample_subcomp_enrichment(temp_sub_comp_list, name = 'control'):
    global sample_var_enrichment_numeric
    #print(g1_sub_comp_list)
    #temp_sub_comp_list = g1_sub_comp_list
    
    first_subset = np.array(sample_var_enrichment_numeric[temp_sub_comp_list[0],:], dtype = float)
    print(first_subset)
    sample_subcomp_enrichment = np.array([np.median(first_subset, axis = 0)])
    print(sample_subcomp_enrichment)
    print(np.shape(sample_subcomp_enrichment))
    comp_names =['unique_subcomponent_ids', 'unique_group_subgroup_id_1']
    if(np.shape(temp_sub_comp_list)[0]>1):
        for i in range(1, np.shape(temp_sub_comp_list)[0]):
            temp_comp_enrichment = np.median(sample_var_enrichment_numeric[temp_sub_comp_list[i],:], axis = 0)
            sample_subcomp_enrichment = np.vstack((sample_subcomp_enrichment, temp_comp_enrichment))
            comp_names.append('unique_group_subgroup_id_'+str(i+1))
    
    comp_names = np.transpose(np.array([comp_names]))
    print(np.shape(comp_names))
    print(comp_names)
    ## now we append the titles
    print(sample_var_enrichment[0,1:])
    sample_subcomp_enrichment = np.vstack((sample_var_enrichment[0,1:] , sample_subcomp_enrichment))
    sample_subcomp_enrichment = np.hstack((comp_names , sample_subcomp_enrichment))
    print(sample_subcomp_enrichment)
    
    
    
    write_table(sample_subcomp_enrichment, sample_dir+name+'_sample_subcomp_enrichment.txt')

if not very_big_file:
    get_sample_subcomp_enrichment(g1_sub_comp_list, name = control_name)
    if not single_network:
        get_sample_subcomp_enrichment(g2_sub_comp_list, name = disease)

################################################################################################
cmd('remove_dups.py -infile "'+in_mine1+'"')
if not single_network:
    cmd('remove_dups.py -infile "'+in_mine2+'"')
################################################################################################


do_PCA_analysis = False

## actually run all of the above code for dimention reduction and clustering
if do_PCA_analysis:
    g1_important_PC_scores = do_PCA(group = 'group1')
    #g1_centroid_indices, g1_initial_centroids, g1_intitial_distances = find_k_clusters(g1_important_PC_scores, group = 'group1')
    #g1_centroid_indices, g1_initial_centroids, g1_intitial_distances = find_k_clusters(control_binary_interactions.astype('int8'), group = 'group1')
    g1_centroid_indices, g1_initial_centroids, g1_intitial_distances = find_k_clusters(c_binary_non_zero_intaractions, group = 'group1')
    #print(control_binary_interactions[g1_centroid_indices,:])
    #print(control_binary_interactions[g1_centroid_indices,:].shape)
    print('these are the first 14 centroids\n\n\n')
    print(c_binary_non_zero_intaractions[g1_centroid_indices[:25],:].astype('int8'))
    print(c_binary_non_zero_intaractions[g1_centroid_indices[:25],:].astype('int8').shape)
    print('\n\n\n')
    do_k_means(c_binary_non_zero_intaractions[g1_centroid_indices[:25],:].astype('int8'), c_binary_non_zero_intaractions, control_name, c_non_zero_vars, iters=25)
    if not single_network:
        if do_PCA_analysis:
            g2_important_PC_scores = do_PCA(group = 'group2')
        #g2_centroid_indices, g2_initial_centroids, g2_intitial_distances = find_k_clusters(g2_important_PC_scores, group = 'group2')
        #g2_centroid_indices, g2_initial_centroids, g2_intitial_distances = find_k_clusters(diseased_binary_interactions.astype('int8'), group = 'group2')
        g2_centroid_indices, g2_initial_centroids, g2_intitial_distances = find_k_clusters(d_binary_non_zero_intaractions, group = 'group2')
        #print(diseased_binary_interactions[g2_centroid_indices,:])
        #print(diseased_binary_interactions[g2_centroid_indices,:].shape)
        print('these are the first 14 centroids\n\n\n')
        print(d_binary_non_zero_intaractions[g2_centroid_indices[:25],:].astype('int8'))
        print(d_binary_non_zero_intaractions[g2_centroid_indices[:25],:].astype('int8').shape)
        do_k_means(d_binary_non_zero_intaractions[g2_centroid_indices[:25],:].astype('int8'), d_binary_non_zero_intaractions, disease, d_non_zero_vars, iters=25)
        print('\n\n\n')
        #sys.exit()


#################################################################################################
########################        co-regulatory netowork analysis             #####################
#################################################################################################

def filter_mine_by_corr(temp_mine_file,corr_cutoff):
    print('filtering mine file for positive correlations:')
    global temp, fileinput
    temp_output=[]
    line_counter=0
    pass_counter=0
    for line in fileinput.input(temp_mine_file):
        
        if line_counter==0:
            temp_output.append(line)
        else:
            temp_line=line[:]
            temp_line=temp_line.split('\t')
            if float(temp_line[-1])>=corr_cutoff:
                temp_output.append(line)
                pass_counter+=1
        line_counter+=1
        if line_counter%100000==0:
            print(pass_counter,'passed out of ',line_counter,round(100*pass_counter/line_counter,2),'%')
    
    fileinput.close()
    outfile=temp_mine_file[:-4]+'_pos_corr.tsv'
    make_file(temp_output,outfile)
    return(outfile)

if do_spearman:
    ## this is set to 0 because, anything above zero will still be significantly postively regulated if spearman test is performed instead of the mine
    corr_coeff_cutoff=0
else:
    corr_coeff_cutoff=0.5
if co_regulatory_network:

    c_mine_cor_filter=filter_mine_by_corr(in_mine1, corr_coeff_cutoff)

    pyminer_dir=os.path.realpath(__file__)
    
    if not single_network:
        d_mine_cor_filter=filter_mine_by_corr(in_mine2, corr_coeff_cutoff)

    pyminer_co_reg_cmd='python3 '+pyminer_dir+' -in_mine1 "'+c_mine_cor_filter+'"'
    if not single_network:
        pyminer_co_reg_cmd+=' -in_mine2 "'+d_mine_cor_filter+'"'
        pyminer_co_reg_cmd+=' -dividing_col '+str(dividing_col)
    else:
        pyminer_co_reg_cmd+=' -single_network'

    cmd('mkdir "'+temp+'/pos_cor"')
    cmd('cp "'+infile+'" "'+temp+'/pos_cor"')

    file_name_only=infile.split('/')
    file_name_only=file_name_only[-1]
    pyminer_co_reg_cmd+=' -infile "'+temp+'/pos_cor/'+file_name_only+'"'

    if very_big_file:
        pyminer_co_reg_cmd+=' -very_big_file '
    if big_file_do_z:
        pyminer_co_reg_cmd+=' -big_file_do_z '

    if page_ranks:
        pyminer_co_reg_cmd+=' -page_ranks'
        pyminer_co_reg_cmd+=' -pr_iters '+str(pr_iters)
        pyminer_co_reg_cmd+=' -pr_alpha '+str(pr_alpha)

    pyminer_co_reg_cmd+=' -no_co_regulatory_network '

    if microarray:
        pyminer_co_reg_cmd+=' -microarray'

    if '-disease' in sys.argv:
        pyminer_co_reg_cmd+=' -disease '+disease
    
    if '-control' in sys.argv:
        pyminer_co_reg_cmd+=' -control '+control_name
    
    if log_fold:
        pyminer_co_reg_cmd+=' -log_fold'
    if log_expression:
        pyminer_co_reg_cmd+=' -log_expression'

    if no_graphs:
        pyminer_co_reg_cmd+=' -no_graphs'
    
    if not rainbow:
        pyminer_co_reg_cmd+=' -no_rainbow'
    pyminer_co_reg_cmd+=' -dpi '+str(dpi_in)
    
    if clean:
        pyminer_co_reg_cmd+=' -clean'

    if mannwhit:
        pyminer_co_reg_cmd+=' -mannwhit'
    
    if no_express:
        pyminer_co_reg_cmd+=' -no_express'

    if weighted_analysis:
        pyminer_co_reg_cmd+=' -weighted_analysis'
    
    if not very_big_file or manual_sample_groups:
        pyminer_co_reg_cmd+=' -manual_sample_groups "'+temp+'/sample_clustering_and_summary/sample_k_means_groups.txt"'


    print('\n\n\n',pyminer_co_reg_cmd)
    time.sleep(5)
    cmd(pyminer_co_reg_cmd)




##################################################################################################################
##################################################################################################################
##########     the remainder of the script is solely for analyzing differences between networks      #############
##################################################################################################################
##################################################################################################################


if single_network:
    sys.exit('finished finding relationships')



###################################################
##  generate detailed relationship summary file ###
###################################################



def get_unID_hash(dataset='group1'):
    ## this creates a unique identifier for each relationship pair
    ## under the form var1_var2
    ## this id is later used to cross check two datsets' relationships, and 
    ## annotate whether the relationship is found in both or just one dataset
    
    global IDlist ## this is a dictionary for all variables with indexes for where they are in a matrix
    if dataset=='group1':
        global control_relationship_dict
        vars_with_relationships_in_cur_dataset = list(control_relationship_dict.keys())
    else:
        global diseased_relationship_dict
        vars_with_relationships_in_cur_dataset = list(diseased_relationship_dict.keys())
    
    h={}
    
    for i in range(0,len(vars_with_relationships_in_cur_dataset)):
        ## go through each var, and concatenate relatinoshiops into a single
        if dataset == 'group1':
            temp_interactions = control_relationship_dict[vars_with_relationships_in_cur_dataset[i]]
        elif dataset == 'group2':
            temp_interactions = diseased_relationship_dict[vars_with_relationships_in_cur_dataset[i]]
        
        for j in temp_interactions:
            both_id_list = [vars_with_relationships_in_cur_dataset[i],j]
            h['_'.join(both_id_list)]=both_id_list
    return(h)


detailed_summary=[['X_var','Y_var','group_specificity']]

c_hash=get_unID_hash(dataset='group1')
d_hash=get_unID_hash(dataset='group2')

for k in list(c_hash.keys()):
    if k in d_hash:
        detailed_summary.append(c_hash[k][:2]+['both'])
        del d_hash[k]
    else:
        detailed_summary.append(c_hash[k][:2]+[control_name])
for k in list(d_hash.keys()):
    detailed_summary.append(d_hash[k][:2]+[disease])
    
if not weighted_analysis:
    make_file(flatten_2D_table(detailed_summary,'\t'),temp+'/detailed_relationship_summary.txt')


##########
## compare the interaction matricies
change_distrib=[]
max_deform_ID=''
max_deform_quant=0
hist_list=[]
broken_list=[]
gained_list=[]
difference_total_list=[["ID","Num_of_Gained_Relationships","Num_of_Broken_Relationships","Total_Num_Changed_Relationships"]]

print('finding gained and broken relationships')
count=5000
for i in range(0,len(control_binary_interactions)):
    
    ## counter is only for printing progress
    if i==count:
        print('on variable',count)
        count+=5000
        gc.collect()

    ## subtract

    Diff_mat=(np.ma.getmaskarray(np.ma.masked_inside(control_binary_interactions[i],.5,1.5))).astype(int)-(np.ma.getmaskarray(np.ma.masked_inside(diseased_binary_interactions[i],.5,1.5))).astype(int)
    #print(i,Diff_mat)
    temp_deform=sum(abs(Diff_mat))
    #print(temp_deform)
    #sys.exit()

    ## mask matrices of binary interactions to 
    num_gained=sum(np.ma.less(Diff_mat,-.5))  ## having the cutoff at -0.5 & +0.5 provides wiggle room
    num_broken=sum(np.ma.greater(Diff_mat,.5))## necessary because of the use of empty matricies, instead of zeros
                                              ## this was done to conserve memory

    broken_list.append(num_broken)
    gained_list.append(num_gained)
    if verbose:
        print(i,num_gained)
    difference_total_list.append([IDlist[i],num_gained,num_broken,num_broken+num_gained])

    #sys.exit()
    
    hist_list.append(temp_deform)
    change_distrib.append([IDlist[i],temp_deform])
    if abs(temp_deform) > abs(max_deform_quant):
        max_deform_quant=temp_deform
        max_deform_ID=IDlist[i]
        #print(i)

# prints the most dysregulated variable

if max_deform_ID == '':
    sys.exit("couldn't find any relationships - try lowering the MIC cutoff")
if verbose:
    print(max_deform_ID)
    print(IDhash[max_deform_ID])
    print(max_deform_quant)
    print(max_deform_ID+"["+str(IDhash[max_deform_ID])+"]:",max_deform_quant)

change_distrib=sorted(change_distrib,key=itemgetter(1))[::-1]

## prints the top most dysregulated variables
for i in range(0,10):
    print(change_distrib[i][0]+'\t'+str(change_distrib[i][1]))

#sys.exit()


####################################################################
## make graphs                                                    ##
####################################################################


########################
## plot deformation histogram
if not no_graphs:
    print('creating histogram')
    plt.clf()
    output=temp+'/histogram_of_changes.png'
    hist, bins = np.histogram(hist_list)#,bins = 100)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.bar(center, hist, align = 'center', width = width)
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

print('creating gained/broken relationship summary file\n'+temp+'/gain_loss_of_relationship_summary.txt')
##print(difference_total_list[0])
if not weighted_analysis:
    output_gain_loss_summary=flatten_2D_table(difference_total_list[:],'\t')
    make_file(output_gain_loss_summary,temp+'/gain_loss_of_relationship_summary.txt')



#### import change summary files
## only for over-riding re-calculation of difference tables

relationship_table=np.array(difference_total_list)
relationships_broken=broken_list[:]#relationship_table[1:,2].astype(float)
relationships_gained=gained_list[:]#relationship_table[1:,1].astype(float)


if not no_graphs:
    print('plotting number of gained vs broken relationships')
    output=temp+'/gained_broken_relationship_scatter.png'
    plt.clf()
    ## usually looked messier with rainbow
    #if rainbow:
    #    #heat_colors = plt.cm.Spectral_r((fold_changes-min(fold_changes))/max(fold_changes-min(fold_changes)))
    #    heat_colors = plt.cm.jet((fold_changes-min(fold_changes))/max(fold_changes-min(fold_changes)))
    #plt.scatter(relationships_broken,relationships_gained,color=heat_colors,marker='.',alpha=.3)
    #else:
    plt.scatter(relationships_broken,relationships_gained,color='k',marker='.',alpha=.3)
    plt.xlabel('Number of Broken Relationships')
    plt.ylabel('Number of Gained Relationships')
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

broken_list=np.array(broken_list)
print('broken_list_shape:',np.shape(broken_list))
gained_list=np.array(gained_list)
print('gained_list_shape:',np.shape(gained_list))
fold_changes=np.array(fold_changes)
print('fold_changes_shape:',np.shape(fold_changes))

if not no_graphs:
    print('creating miscellaneous graphs')
    output=temp+'/expression_scatter_colors_gained_size.png'
    ## calculate linear scaled # gained from range 1-750 for plotting size
    relationships_gained_size_scaled=linear_normalize(relationships_gained[:],min_range=1,max_range=750).tolist()

    plt.clf()
    if rainbow:
        
        plt.scatter(mean_control,mean_disease,marker='.',s=relationships_gained_size_scaled,facecolor=heat_colors,edgecolors='k',alpha=.5)
    else:
        plt.scatter(mean_control,mean_disease,marker='.',s=relationships_gained_size_scaled,facecolor='none',edgecolors='k',alpha=.5)
    plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
    if log_expression:
        plt.ylabel('Log2 '+control_name+' expression')
        plt.xlabel('Log2 '+disease+' expression')
    else:
        plt.ylabel(control_name+' expression')
        plt.xlabel(disease+' expression')
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    plt.clf()

    output=temp+'/expression_scatter_colors_broken_size.png'
    plt.clf()

    ## calculate linear scaled # broken from range 1-750 for plotting size
    relationships_broken_size_scaled=linear_normalize(relationships_broken[:],min_range=1,max_range=750).tolist()

    if rainbow:
        
        plt.scatter(mean_control,mean_disease,marker='.',s=relationships_broken_size_scaled,facecolor=heat_colors,edgecolors='k',alpha=.5)
    else:
        plt.scatter(mean_control,mean_disease,marker='.',s=relationships_broken_size_scaled,facecolor='none',edgecolors='k',alpha=.5)
    plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
    if log_expression:
        plt.ylabel('Log2 '+control_name+' expression')
        plt.xlabel('Log2 '+disease+' expression')
    else:
        plt.ylabel(control_name+' expression')
        plt.xlabel(disease+' expression')
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    plt.clf()


    output=temp+'/num_gain_fold.png'
    plt.clf()
    plt.cla()
    print(np.shape(fold_changes),np.shape(gained_list))
    if rainbow:
        
        plt.scatter(fold_changes,gained_list,marker='.',color='k',edgecolors=heat_colors)
    else:
        
        plt.scatter(fold_changes,gained_list,marker='.',color='k',edgecolors='k')
    
    if log_fold:
        plt.plot([0,0],[0,max(gained_list)],color='.5')
        plt.xlabel('Ln '+disease+'/'+control_name+' expression')
    else:
        plt.plot([1,1],[0,max(gained_list)],color='.5')
        plt.xlabel(disease+'/'+control_name+' expression')
    plt.ylabel('Number of Gained Relationships')
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    plt.clf()


    output=temp+'/num_broken_fold.png'
    plt.clf()
    plt.cla()
    
    if rainbow:
        plt.scatter(x=broken_list,y=fold_changes,marker='.',color='k',edgecolors=heat_colors)
    else:
        plt.scatter(broken_list,fold_changes,marker='.',color='k',edgecolors='k')
    
    if log_fold:
        plt.plot([0,max(broken_list)],[0,0],color='.5')
        plt.ylabel('Ln '+disease+'/'+control_name+' expression')
    else:
        plt.plot([0,max(broken_list)],[1,1],color='.5')
        plt.ylabel(disease+'/'+control_name+' expression')
    plt.xlabel('Number of Broken Relationships')
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    plt.clf()

################ same graphs as above, using mw colors instead of fold_change ###############
    if rainbow and mannwhit:
        output=temp+'/expression_scatter_mw_colors_gained_size.png'
        plt.clf()
        plt.scatter(mean_control,mean_disease,marker='.',s=relationships_gained_size_scaled,facecolor=mw_heat_colors,edgecolors='k',alpha=.5)
        plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
        if log_expression:
            plt.ylabel('Log2 '+control_name+' expression')
            plt.xlabel('Log2 '+disease+' expression')
        else:
            plt.ylabel(control_name+' expression')
            plt.xlabel(disease+' expression')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

        ####
        
        output=temp+'/expression_scatter_mw_colors_broken_size.png'
        plt.clf()

        plt.scatter(mean_control,mean_disease,marker='.',s=relationships_broken_size_scaled,facecolor=mw_heat_colors,edgecolors='k',alpha=.5)
        plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
        if log_expression:
            plt.ylabel('Log2 '+control_name+' expression')
            plt.xlabel('Log2 '+disease+' expression')
        else:
            plt.ylabel(control_name+' expression')
            plt.xlabel(disease+' expression')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

        ####
        
        output=temp+'/num_gain_mw_colors.png'
        plt.clf()
        plt.cla()
        plt.scatter(fold_changes,gained_list,marker='.',color='k',edgecolors=mw_heat_colors)
        if log_fold:
            plt.plot([0,0],[0,max(gained_list)],color='.5')
            plt.xlabel('Ln '+disease+'/'+control_name+' expression')
        else:
            plt.plot([1,1],[0,max(gained_list)],color='.5')
            plt.xlabel(disease+'/'+control_name+' expression')
        plt.ylabel('Number of Gained Relationships')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

        ####

        output=temp+'/num_broken_mw_colors.png'
        plt.clf()
        plt.cla()
        
        plt.scatter(x=broken_list,y=fold_changes,marker='.',color='k',edgecolors=mw_heat_colors)
        
        if log_fold:
            plt.plot([0,max(broken_list)],[0,0],color='.5')
            plt.ylabel('Ln '+disease+'/'+control_name+' expression')
        else:
            plt.plot([0,max(broken_list)],[1,1],color='.5')
            plt.ylabel(disease+'/'+control_name+' expression')
        plt.xlabel('Number of Broken Relationships')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()









####################################################################
## determining weighted dysregulation factor                      ##
####################################################################


if weighted_analysis:
    gc.collect()
    print('\n\nbeginning the weighted analysis\n\nif you have a large dataset, you may\nwant to take a coffee break now')
    ## this is by definition an O^2/2(ish) problem,
    ## so it's going to take a while for large datasets
    ## because of the potential size of this computation
    ## & likely memory shortages, the pairwise variable dysregulation similarity
    ## are stored in a sqlite3 database

    import sqlite3
    db_file=temp+'/pairwise_weights.db'

    conn=sqlite3.connect(db_file)
    c=conn.cursor()

    c.execute('DROP TABLE IF EXISTS gain_table;')
    c.execute('DROP TABLE IF EXISTS broken_table;')
    c.execute('DROP TABLE IF EXISTS conserved_table;')

    c.execute('CREATE TABLE gain_table(var1, var2, weight)')
    c.execute('CREATE TABLE broken_table(var1, var2, weight)')
    c.execute('CREATE TABLE conserved_table(var1, var2, weight)')

    def var_similarity(var1,var2,table):
        ## table should equal either 'gain_table' or 'broken_table'
        global control_binary_interactions, diseased_binary_interactions, c, conn, IDhash
        
        
        ## for memory's sake these are calculated on the fly (again)
        v1_index=IDhash[var1]
        v1_diff_mat=(np.ma.getmaskarray(np.ma.masked_inside(control_binary_interactions[v1_index],.5,1.5))-np.ma.getmaskarray(np.ma.masked_inside(diseased_binary_interactions[v1_index],.5,1.5))).astype(float)

        v2_index=IDhash[var2]
        v2_diff_mat=(np.ma.getmaskarray(np.ma.masked_inside(control_binary_interactions[v2_index],.5,1.5))-np.ma.getmaskarray(np.ma.masked_inside(diseased_binary_interactions[v2_index],.5,1.5))).astype(float)

        ########
        ## similarity is determined as follows:
        ## of all gained or broken relationships among the two variables,
        ## what proportion of them are the same gained or broken relationships.
        ## Weight is 1 - similarity, so gained or broken relationships between
        ## nodes with dissimilar dysregulation count for more than those which are
        ## a part of the same dysregulated cluster
##
##        print('v1_diff_mat')
##        print(v1_diff_mat)
##        print('v2_diff_mat')
##        print(v2_diff_mat)
##        print('v1_diff_mat-v2_diff_mat')
##        print(v1_diff_mat-v2_diff_mat)
##        print('abs(v1_diff_mat-v2_diff_mat)')
##        print(abs(v1_diff_mat-v2_diff_mat))
##        print('abs(v2_diff_mat)')
##        print(abs(v2_diff_mat))
##        print('abs(v1_diff_mat)')
##        print(abs(v1_diff_mat))
####
##        print('sum(abs(v1_diff_mat-v2_diff_mat))')
##        print(sum(abs(v1_diff_mat-v2_diff_mat)))
##
##        print('sum(abs(v2_diff_mat)+abs(v1_diff_mat))')
##        print(sum(abs(v2_diff_mat)+abs(v1_diff_mat)))
        
        weight=sum(abs(v1_diff_mat-v2_diff_mat))/sum(abs(v2_diff_mat)+abs(v1_diff_mat))
        similarity=1-weight
        

        #print('similarity',similarity)
        #print(var1,var2,'weight',weight)

        insertion=('","').join([var1,var2,str(weight)])
        
        execInsert=('INSERT INTO '+table+' values ("'+insertion+'")')
        ## print(execInsert)
        c.execute(execInsert)

        ##return(weight)
        return(weight)

    detailed_summary[0].append('relationship_weight')
    count=5000
    for i in range(1,len(detailed_summary)):
        if i==count:
            count+=5000
            print('on variable pair #',i)
            conn.commit()

        
        if detailed_summary[i][2]==control_name:## this will be a broken relationship
            weight=var_similarity(detailed_summary[i][0],detailed_summary[i][1],'broken_table')
            #print(detailed_summary[i][0],detailed_summary[i][1])
        elif detailed_summary[i][2]==disease:## this will be a gained relationship
            weight=var_similarity(detailed_summary[i][0],detailed_summary[i][1],'gain_table')
            #print(detailed_summary[i][0],detailed_summary[i][1])
        else:
            weight=0
            execInsert=('INSERT INTO conserved_table values ("'+
                ('","').join([detailed_summary[i][0],detailed_summary[i][1],'0'])+'")')
            c.execute(execInsert)
        detailed_summary[i].append(weight)
            




    make_file(flatten_2D_table(detailed_summary[:],'\t'),temp+'/detailed_relationship_summary_with_weights.txt')

    ###########
    ## need to update these file outputs to have the weights embedded

    ## go through for each variable and get the sum of the gained and broken weights to add them to the summary file
    difference_total_list[0]+=['sum_gained_weights','sum_broken_weights','sum_all_weights']


    def sum_weights(var,table):
        c.execute('select weight from '+table+' where var1="'+var+'"')
        all_relationship_weights=c.fetchall()
        all_relationship_weights=np.array(all_relationship_weights,dtype='float64')
        return(np.sum(all_relationship_weights))

    g_weight_all_list=[]
    b_weight_all_list=[]
    t_weight_all_list=[]

    for i in range(1,len(difference_total_list)):
        ## weight sums to summary output file
        var=difference_total_list[i][0]
        g_weight_sum=sum_weights(var,'gain_table')
        b_weight_sum=sum_weights(var,'broken_table')
        t_weight_sum=g_weight_sum+b_weight_sum

        difference_total_list[i]+=[g_weight_sum,b_weight_sum,t_weight_sum]

        g_weight_all_list.append(g_weight_sum)
        b_weight_all_list.append(b_weight_sum)
        t_weight_all_list.append(t_weight_sum)

    output_gain_loss_summary=flatten_2D_table(difference_total_list,'\t')
    make_file(output_gain_loss_summary,temp+'/gain_loss_of_relationship_summary.txt')


    g_weight_all_list=np.array(g_weight_all_list)
    b_weight_all_list=np.array(b_weight_all_list)
    t_weight_all_list=np.array(t_weight_all_list)



    ##################################
    ##################################
    if not no_graphs:
        ########################
        ## plot deformation histogram
        
        print('creating histogram')
        plt.clf()
        output=temp+'/histogram_of_weighted_sums.png'
        hist, bins = np.histogram(t_weight_all_list)#,bins = 100)
        width = 0.7*(bins[1]-bins[0])
        center = (bins[:-1]+bins[1:])/2
        plt.bar(center, hist, align = 'center', width = width)
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

        ####

        print('plotting number of gained vs broken relationships')
        output=temp+'/sum_gained-broken_weights_scatter.png'
        plt.clf()
        ## usually looked messier with rainbow
        #if rainbow:
        #    #heat_colors = plt.cm.Spectral_r((fold_changes-min(fold_changes))/max(fold_changes-min(fold_changes)))
        #    heat_colors = plt.cm.jet((fold_changes-min(fold_changes))/max(fold_changes-min(fold_changes)))
        #plt.scatter(relationships_broken,relationships_gained,color=heat_colors,marker='.',alpha=.3)
        #else:
        plt.scatter(b_weight_all_list,g_weight_all_list,color='k',marker='.',alpha=.3)
        plt.xlabel('Weighted Sum of Broken Relationships')
        plt.ylabel('Weighted Sum of Gained Relationships')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)

        ####

        print('creating miscellaneous weighted graphs')
        output=temp+'/expression_scatter_colors_gained_size_weights.png'
        plt.clf()

        ## linear normalize gained weights to 1-750
        scaled_g_weight_all_list=linear_normalize(g_weight_all_list[:],min_range=1,max_range=750)

        if rainbow:
            #heat_colors = plt.cm.jet((fold_changes-min(fold_changes))/max(fold_changes-min(fold_changes)))
            plt.scatter(mean_control,mean_disease,marker='.',s=scaled_g_weight_all_list,facecolor=heat_colors,edgecolors='k',alpha=.5)
        else:
            plt.scatter(mean_control,mean_disease,marker='.',s=scaled_g_weight_all_list,facecolor='none',edgecolors='k',alpha=.5)
        plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
        if log_expression:
            plt.ylabel('Log2 '+control_name+' expression')
            plt.xlabel('Log2 '+disease+' expression')
        else:
            plt.ylabel(control_name+' expression')
            plt.xlabel(disease+' expression')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

        ####

        output=temp+'/expression_scatter_colors_weighted_broken_size.png'
        plt.clf()

        ## linear scaled broken weights
        scaled_b_weight_all_list=linear_normalize(b_weight_all_list[:],min_range=1,max_range=750)

        if rainbow:
            #heat_colors = plt.cm.jet((fold_changes-min(fold_changes))/max(fold_changes-min(fold_changes)))
            plt.scatter(mean_control,mean_disease,marker='.',s=scaled_b_weight_all_list,facecolor=heat_colors,edgecolors='k',alpha=.5)
        else:
            plt.scatter(mean_control,mean_disease,marker='.',s=scaled_b_weight_all_list,facecolor='none',edgecolors='k',alpha=.5)
        plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
        if log_expression:
            plt.ylabel('Log2 '+control_name+' expression')
            plt.xlabel('Log2 '+disease+' expression')
        else:
            plt.ylabel(control_name+' expression')
            plt.xlabel(disease+' expression')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

        ####

        output=temp+'/sum_gain_weights_fold.png'
        plt.clf()
        plt.cla()
        
        if rainbow:
            plt.scatter(fold_changes,g_weight_all_list,marker='.',color='k',edgecolors=heat_colors)
        else:
            plt.scatter(fold_changes,g_weight_all_list,marker='.',color='k',edgecolors='k')
        
        if log_fold:
            plt.plot([0,0],[0,max(g_weight_all_list)],color='.5')
            plt.xlabel('Ln '+disease+'/'+control_name+' expression')
        else:
            plt.plot([1,1],[0,max(g_weight_all_list)],color='.5')
            plt.xlabel(disease+'/'+control_name+' expression')
        plt.ylabel('Sum of Gained Relationship Weights')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

        ####

        output=temp+'/sum_borken_weights_fold.png'
        plt.clf()
        plt.cla()
        
        if rainbow:
            #pass
            plt.scatter(b_weight_all_list,fold_changes,marker='.',color='k',edgecolors=heat_colors)
        else:
            plt.scatter(b_weight_all_list,fold_changes,marker='.',color='k',edgecolors='k')
        
        if log_fold:
            plt.plot([0,max(b_weight_all_list)],[0,0],color='.5')
            plt.ylabel('Ln '+disease+'/'+control_name+' expression')
        else:
            plt.plot([0,max(b_weight_all_list)],[1,1],color='.5')
            plt.ylabel(disease+'/'+control_name+' expression')
        plt.xlabel('Sum of Broken Relationship Weights')
        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
        plt.clf()

################## same graphs as above with colors changed to mw_heat_colors########
        if rainbow and mannwhit:
            output=temp+'/expression_scatter_mw_colors_gained_size_weights.png'
            plt.clf()

            plt.scatter(mean_control,mean_disease,marker='.',s=scaled_g_weight_all_list,facecolor=mw_heat_colors,edgecolors='k',alpha=.5)
            plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
            if log_expression:
                plt.ylabel('Log2 '+control_name+' expression')
                plt.xlabel('Log2 '+disease+' expression')
            else:
                plt.ylabel(control_name+' expression')
                plt.xlabel(disease+' expression')
            plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
            plt.clf()

            ####

            output=temp+'/expression_scatter_mw_colors_weighted_broken_size.png'
            plt.clf()
            plt.scatter(mean_control,mean_disease,marker='.',s=scaled_b_weight_all_list,facecolor=mw_heat_colors,edgecolors='k',alpha=.5)
            plt.plot([min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],[min([min(mean_control),min(mean_disease)]),max([max(mean_control),max(mean_disease)])],color='k',alpha=.5)
            if log_expression:
                plt.ylabel('Log2 '+control_name+' expression')
                plt.xlabel('Log2 '+disease+' expression')
            else:
                plt.ylabel(control_name+' expression')
                plt.xlabel(disease+' expression')
            plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
            plt.clf()

            ####

            output=temp+'/sum_gain_weights_fold_mw_colors.png'
            plt.clf()
            plt.cla()
            
            plt.scatter(fold_changes,g_weight_all_list,marker='.',color='k',edgecolors=mw_heat_colors)
            
            if log_fold:
                plt.plot([0,0],[0,max(g_weight_all_list)],color='.5')
                plt.xlabel('Ln '+disease+'/'+control_name+' expression')
            else:
                plt.plot([1,1],[0,max(g_weight_all_list)],color='.5')
                plt.xlabel(disease+'/'+control_name+' expression')
            plt.ylabel('Sum of Gained Relationship Weights')
            plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
            plt.clf()

            ####

            output=temp+'/sum_borken_weights_fold_mw_colors.png'
            plt.clf()
            plt.cla()
            
            plt.scatter(b_weight_all_list,fold_changes,marker='.',color='k',edgecolors=mw_heat_colors)
            
            if log_fold:
                plt.plot([0,max(b_weight_all_list)],[0,0],color='.5')
                plt.ylabel('Ln '+disease+'/'+control_name+' expression')
            else:
                plt.plot([0,max(b_weight_all_list)],[1,1],color='.5')
                plt.ylabel(disease+'/'+control_name+' expression')
            plt.xlabel('Sum of Broken Relationship Weights')
            plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
            plt.clf()





#################################################################################################

if page_ranks and weighted_analysis and not single_network:
    weighted_delta_pr_switch=[]
    weighted_delta_pr_switch_output=[['ID','weighted_delta_pr_switch']]
    for i in range(0,len(IDlist)):
        weighted_delta_pr_switch.append(1/(abs_delta_PR_list[i]+1) * t_weight_all_list[i])
        weighted_delta_pr_switch_output.append([IDlist[i],weighted_delta_pr_switch[-1]])
    
    make_file(flatten_2D_table(weighted_delta_pr_switch_output, '\t'),temp+'/weighted_delta_pr_switch.txt')


    #c_PR_list
    #d_PR_list
    #delta_PR_list
    #abs_delta_PR_list










print('\n\nFinished PyMINEr analysis! You may now frolick through the meadows of data')









