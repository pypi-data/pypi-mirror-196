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
parser.add_argument("-out","-o",
    help="directory for output")
parser.add_argument("-stats_call","-stats","-s",
    help="a file containing the get_stats.py invocation call")
parser.add_argument("-negative_control","-neg_ctrl","-neg","-n",
    help="the name of the treatment that is the negative control. This changes the stats from a test of independence to a goodness of fit relative to the negative control.")

args = parser.parse_args()
########################################################
if args.out[-1] != '/':
    args.out+='/'
if not os.path.isdir(args.out):
    cmd("mkdir "+args.out)
########################################################
script_dir = os.path.dirname(os.path.abspath(__file__))+"/"
cont_table_script = script_dir+"pyminer_make_cont_table.py"
chi_res_script = script_dir+"pyminer_chi_res.py"
within_group_dif_script=script_dir+"pyminer_within_group_differences.py"

## first we need to make the contingency table
cont_table_call = "python3 "+cont_table_script+" -classes "+args.classes
cont_table_call += " -sg "+args.sample_groups
cont_table_call += " -out "+args.out
cmd(cont_table_call)

cont_table_file=args.out+"group_class_contingency_table.txt"

## then we'll run the chi square analysis
chi_call="python3 "+chi_res_script
chi_call+=" -i "+cont_table_file
chi_call+=" -out "+args.out
if args.negative_control!= None:
    chi_call+=" -neg_ctrl "+args.negative_control
cmd(chi_call)

## then we'll look for differences within cell types across classes
within_class_dir = args.out#+"class_differences_within_cell_type/"
cmd("mkdir "+within_class_dir)
within_grp_dif_call="python3 "+within_group_dif_script
within_grp_dif_call+=" -classes "+args.classes
within_grp_dif_call+=" -sg "+args.sample_groups
within_grp_dif_call+=" -cont_table "+cont_table_file
within_grp_dif_call+=" -out "+within_class_dir
within_grp_dif_call+=" -stats "+args.stats_call
cmd(within_grp_dif_call)


