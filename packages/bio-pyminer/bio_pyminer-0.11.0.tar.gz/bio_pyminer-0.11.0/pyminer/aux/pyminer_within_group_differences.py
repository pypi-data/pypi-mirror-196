#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
import pandas as pd
from scipy.stats.contingency import margins
from scipy.stats import chi2,chi2_contingency
import seaborn as sns
from matplotlib import pyplot as plt

##############################################################
## basic function library
def read_file(tempFile,linesOraw='lines',quiet=False):
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


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return(in_path+'/')


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



##############################################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-classes", "-sample_classes","-sample_class","-class",
    help="the file containing the sample classes (for example WT and mutant). This is a text file that has sample names in the first column and the second column has the classes.")
parser.add_argument("-sample_groups","-sg","-unsupervised_clustering",
    help="this file has the results of the pyminer unsupervised clustering")
parser.add_argument("-cont_table",
    help="this file is the contingency table made from pyminer_make_cont_table.py")
parser.add_argument("-out",
    help="directory for output")
parser.add_argument("-stats_call","-stats","-s",
    help="a file containing the get_stats.py invocation call")
    
args = parser.parse_args()
########################################################
if args.out[-1] != '/':
    args.out+='/'
########################################################

class_table=np.array(read_table(args.classes))
groups_table=np.array(read_table(args.sample_groups))
cont_table = np.array(read_table(args.cont_table))
cont_array = np.array(cont_table[1:,1:],dtype=float)
stats_call_base = read_file(args.stats_call)[0]
print(stats_call_base)

top_dir = args.out+"within_group_differences/"
cmd("mkdir "+top_dir)

## figure out which groups have enough cells to be worth comparing
## we'll use a cufoff of having at least 5 cells in each group
ge5_array = np.array(cont_array>=5,dtype=int)
num_ge5 = np.sum(ge5_array,axis=1)
groups_with_enough_cells = num_ge5>=2
print(np.sum(np.array(groups_with_enough_cells,dtype=int)),"groups will be compared for within group differences by class")
groups_with_enough_cells = groups_with_enough_cells.tolist()

## go through each of the groups and run the stats
for i in range(0,len(groups_with_enough_cells)):
    if groups_with_enough_cells[i]:
        temp_dir = top_dir+"class_differences_in_sample_group"+str(i)
        cmd("mkdir "+temp_dir)
        stats_call = stats_call_base + " -within_group "+str(i)
        stats_call += " -classes "+args.classes
        stats_call += " -out_dir "+temp_dir
        cmd(stats_call)

