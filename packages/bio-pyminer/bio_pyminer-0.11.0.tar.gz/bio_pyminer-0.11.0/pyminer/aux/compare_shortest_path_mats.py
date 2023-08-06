#!/usr/bin/env python3
##import dependency libraries
import sys,time,glob,os,pickle
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
gc.enable()

import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['agg.path.chunksize'] = 10000


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


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return(in_path+'/')



def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))

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

############################################################################################

## read in the necessary arguments
##############################################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-short_path_mat1", "-sp1",
    help="the first of two shortest path matrices")
parser.add_argument("-short_path_mat2", "-sp2",
    help="the first of two shortest path matrices")
parser.add_argument("-adj1", "-adj_list1",
    help="the adjacency list for the first dataset")
parser.add_argument("-adj2", "-adj_list2",
    help="the adjacency list for the second dataset")
parser.add_argument("-ID_list", "-id_list","-ids","-IDs",
    help="the list of all IDs that made the networks")
parser.add_argument("-out_dir", 
    help="the directory to place the output file(s)")

args = parser.parse_args()
##############################################################

if args.out_dir != None:
    out_dir = args.out_dir
else:
    out_dir = args.short_path_mat1.split('/')
    out_dir = '/'.join(out_dir[:-1])+'//'


if args.ID_list!=None:
    ID_list = read_file(args.ID_list, "lines")
    ID_hash = {}
    for i in range(0,len(ID_list)):
        ID_hash[ID_list[i]] = i
# else:
#     sys.exit('-ID_list </path/to/file> is a required argument')
###############################################################

if args.adj1 != None and args.adj2 != None:
    ## set up the sp1_relationships and sp2_relationships matrices
    
    sp1_relationships = np.zeros((len(ID_list),len(ID_list)),dtype='i4')
    sp2_relationships = np.zeros((len(ID_list),len(ID_list)),dtype='i4')

    print('populating the first adjacency matrix')
    first = True
    for line in fileinput.input(args.adj1):
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            index1 = ID_hash[temp_line[0]]
            index2 = ID_hash[temp_line[1]]
            sp1_relationships[index1,index2] = 1
            sp1_relationships[index2,index1] = 1
    fileinput.close()

    print('populating the second adjacency matrix')
    first = True
    for line in fileinput.input(args.adj2):
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            index1 = ID_hash[temp_line[0]]
            index2 = ID_hash[temp_line[1]]
            sp2_relationships[index1,index2] = 1
            sp2_relationships[index2,index1] = 1
    fileinput.close()

    print("getting shortest path 1")
    sp1 = scipy.sparse.csgraph.shortest_path(sp1_relationships)
    print("getting shortest path 2")
    sp2 = scipy.sparse.csgraph.shortest_path(sp2_relationships)



if args.short_path_mat1 != None and  args.short_path_mat2 != None:
    sp1 = np.array(read_table(args.short_path_mat1),dtype = 'f4')

    sp2 = np.array(read_table(args.short_path_mat2),dtype = 'f4')

if True:
    #sp_dif_mat = np.abs(sp2 - sp1)
    print('getting lower triangles')
    sp1_lower = np.tril(sp1)
    sp2_lower = np.tril(sp2)

    print('converting them to linear vectors')
    sp1_lower = sp1_lower.reshape((len(ID_list)**2,))
    sp2_lower = sp2_lower.reshape((len(ID_list)**2,))

    print('removing the zeros')
    sp1_zero_mask = sp1_lower == 0
    sp2_zero_mask = sp2_lower == 0
    zero_mask = sp1_zero_mask+sp2_zero_mask
    #print(zero_mask)
    print(np.sum(zero_mask))
    non_zero_mask = zero_mask * -1
    non_zero_mask += 1
    non_zero_mask = np.array(non_zero_mask, dtype = bool)
    print(non_zero_mask)
    print(np.sum(non_zero_mask))


    sp1_non_zero = sp1_lower[non_zero_mask]
    sp2_non_zero = sp2_lower[non_zero_mask]


    print('removing the inifinities')


    sp1_inf_mask = np.isinf(sp1_non_zero)
    sp2_inf_mask = np.isinf(sp2_non_zero)

    inf_mask = sp1_inf_mask + sp2_inf_mask

    non_inf_mask = inf_mask * -1
    non_inf_mask += 1
    non_inf_mask = np.array(non_inf_mask, dtype = bool)

    ##
    sp1_non_zero_non_inf = sp1_non_zero[non_inf_mask]
    sp2_non_zero_non_inf = sp2_non_zero[non_inf_mask]



    print(sp1_non_zero_non_inf)
    print(sp2_non_zero_non_inf)

    print('calculating stats\n\n')

    print('spearman:')
    print(scipy.stats.spearmanr(sp1_non_zero_non_inf,sp2_non_zero_non_inf))
    print('\npearson:')
    print(scipy.stats.pearsonr(sp1_non_zero_non_inf,sp2_non_zero_non_inf))




    print('\nmaking plot #1')
    ax = sns.regplot(x=sp1_non_zero_non_inf,
     y=sp2_non_zero_non_inf, color="g",
     ci=95,
     x_jitter=.2,
     y_jitter=.2,
     scatter_kws={'alpha':0.01})



    ax.set(xlabel='Shortest path network-1', ylabel='Shortest path network-2')

    plt.savefig(out_dir+'/short_path_correlation.png',dpi=360)

    plt.clf()

    print('making plot #2')
    m, b = np.polyfit(sp1_non_zero_non_inf, sp2_non_zero_non_inf, 1)

    ax = plt.hexbin(sp1_non_zero_non_inf, sp2_non_zero_non_inf, cmap=plt.cm.afmhot_r,
        gridsize = int(max(sp1_non_zero_non_inf)/2))

    plt.plot(sp1_non_zero_non_inf, m*sp1_non_zero_non_inf + b, '-',color='b',lw=2)

    #ax.set_xlabel('Shortest path network-1')
    #ax.set_ylabel('Shortest path network-2')

    plt.savefig(out_dir+'/short_path_correlation_2.png',dpi=360)

    ax = plt.hexbin(sp1_non_zero_non_inf, sp2_non_zero_non_inf, cmap=plt.cm.afmhot_r,bins='log',
        gridsize = int(max(sp1_non_zero_non_inf)/2))


    plt.plot(sp1_non_zero_non_inf, m*sp1_non_zero_non_inf + b, '-',color='b',lw=2)

    #ax.set_xlabel('Shortest path network-1')
    #ax.set_ylabel('Shortest path network-2')
    #ax.set(xlab='Shortest path Network1', ylab='Shortest path Network2')

    plt.savefig(out_dir+'/short_path_correlation_2_log.png',dpi=360)

    ## make_contingency_table
    print('\nchi-squared')
    sp1_relationships = np.array(sp1_non_zero == 1,dtype = int)
    sp2_relationships = np.array(sp2_non_zero == 1,dtype = int)

    
if args.adj1 == None and args.short_path_mat1 == None:
    sys.exit('you must either specify an adj-list set, or a shortest path matrix set')

print('calculating the contingency table and chi-square')
#print(sp2_relationships)
dif_vect = sp1_relationships-sp2_relationships
in_sp1_only = np.sum(dif_vect == 1)
in_sp2_only = np.sum(dif_vect == -1)
equal_in_both = np.array(sp1_relationships == sp2_relationships,dtype=bool)
## where it's equal in both, it will be 1, and multiplying by sp1_relationships will
## convert it to equal in both and equal to 1
#in_both = np.sum(np.array(equal_in_both * sp1_relationships, dtype = bool))
in_both = np.sum((sp1_relationships + sp2_relationships) == 2)
in_neither = np.sum(equal_in_both != sp1_relationships)

contingency_table = np.zeros((2,2))
contingency_table[0,0]=in_both
contingency_table[0,1]=in_sp1_only
contingency_table[1,0]=in_sp2_only
contingency_table[1,1]=in_neither

print("""\n% of graph1 also in graph2:""",in_both/(in_both+in_sp1_only) * 100)
print("""\n% of graph2 also in graph1:""",in_both/(in_both+in_sp2_only) * 100,'\n')


print("\ncontingency table")
print(contingency_table)
chi_sqr_result = scipy.stats.chi2_contingency(contingency_table)
print('\nchi:',chi_sqr_result[0])
print('p:',chi_sqr_result[1])
print('df:',chi_sqr_result[2])
print('expected:\n',chi_sqr_result[3],'\n')

print('\nfisher exact test:')
oddsratio, pval = scipy.stats.fisher_exact(contingency_table)
print('odds ratio:',oddsratio)
print('p value:',pval,'\n')

print('fold change:\n',contingency_table/chi_sqr_result[3])
print('log2 fold change:\n',np.log2(contingency_table/chi_sqr_result[3]))

actually_in_both = contingency_table[0,0]
expected_in_both = chi_sqr_result[3][0,0]



