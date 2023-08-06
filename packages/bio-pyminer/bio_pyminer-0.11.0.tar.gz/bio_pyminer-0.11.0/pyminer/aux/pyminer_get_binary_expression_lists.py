#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput, random
import numpy as np
#import pandas as pd
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

all_calls = []
def cmd(in_message, com=True):
	global all_calls
	if type(in_message)==list:
		in_message = ' '.join(in_message)
	print(in_message)
	all_calls.append(in_message)
	time.sleep(.25)
	if com:
		Popen(in_message,shell=True).communicate()
	else:
		Popen(in_message,shell=True)

def check_infile(infile):
	if os.path.isfile(infile):
		return
	else:
		sys.exit(str('could not find '+infile))

def outfile_exists(outfile):
	if os.path.isfile(outfile):
		statinfo = os.stat(outfile)
		if statinfo.st_size!=0:
			return(True)
		else:
			return(False)
	else:
		return(False)
##############################################################
##############################################################

import argparse
parser = argparse.ArgumentParser()


parser.add_argument("-mean_expression_file","-mean" ,
    help="the summary table ",
    type = str)
parser.add_argument("-percent_expression_file","-percent" ,
    help="the summary table of the percentage of the cells of each cell type detectably expressing the gene",
    type = str)
parser.add_argument("-out", "-o",
    help="the output folder in which the final output enrichemnt files should go",
    type = str,
    default = "")
args = parser.parse_args()
#############################################################

mean_expression_table = np.array(read_table(args.mean_expression_file))
expression_numeric = np.array(mean_expression_table[1:,1:],dtype=float)

gene_vect = mean_expression_table[1:,0]
cell_types = mean_expression_table[0,1:]

out_expressed_gene_vects = []
if args.out[-1]!="/":
    args.out+='/'

expression_vect = np.sort(expression_numeric.flatten())
## non-zero values
expression_vect = expression_vect[np.where(expression_vect>0)[0]]
cutoff_idx = int(np.shape(expression_vect)[0] * 0.05)
expression_cutoff = expression_vect[cutoff_idx]
print('expression cutoff:',expression_cutoff)

for i in range(0,np.shape(expression_numeric)[1]):
    expressed_indices = np.where(expression_numeric[:,i]>0)[0]#expression_cutoff)[0]
    out_expressed_gene_vects.append(gene_vect[expressed_indices].tolist())
    make_file('\n'.join(out_expressed_gene_vects[-1][:]),args.out+cell_types[i]+'_binary_expression.txt')


