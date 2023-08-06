#!/usr/bin/env python3
##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import pandas as pd
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

parser.add_argument(
	'-infiles','-in','-i','-input',
    nargs="+",
	dest='infile',
    help="Shortest path output from PyMINEr. These must all be in the same format!",
	type=str)

parser.add_argument("-out_dir", "-o", "-out",
    help="the directory to place the output file(s)")

args = parser.parse_args()
##############################################################
class dataset():
    def __init__(self, in_file=None,rows=None,cols=None,array=None,out_dir=None,name=None):
        if in_file != None:
            self.table=read_table(in_file)
            self.rows, self.cols, self.array = table_to_axes_and_array(self.table)
        else:
            self.rows, self.cols, self.array, self.out_dir, self.name  = (rows, cols, array, out_dir, name)
            self.table = None
        if out_dir != None:
            ## make the output directory if it doesn't exist
            self.out_dir = out_dir
            if self.out_dir[-1]!='/':
                self.out_dir+='/'
            if not os.path.isdir(self.out_dir):
                cmd('mkdir '+self.out_dir)


    def write_array(self):
        temp_table=[self.cols]+self.array.tolist()
        ## add the header
        for i in range(1,len(temp_table)):
            ## add the gene name to the first col
            temp_table[i]=[self.rows[i]]+temp_table[i]
        write_table(temp_table,self.out_dir+self.name+'.tsv')


def table_to_axes_and_array(in_table):
    temp_array = np.array(in_table)
    rows = temp_array[:,0].tolist()
    cols = temp_array[0,:].tolist()
    num_array = np.array(temp_array[1:,1:],dtype=float)
    return(rows, cols, num_array)

def check_compatibility(dataset_list):
    first = True
    for d in dataset_list:
        if first:
            first=False
        else:
            if d.rows!=last_row or d.cols!=last_col:
                sys.exit('datasets not compatible')
        last_row = d.rows
        last_col = d.cols
    return

def make_3d_array(dataset_list):
    ## check dataset compatibility
    check_compatibility(dataset_list)
    single_shape=dataset_list[0].array.shape
    final_array = np.zeros((len(dataset_list),single_shape[0],single_shape[1]))
    for i in range(0,len(dataset_list)):
        final_array[i]+=dataset_list[i].array
    return(final_array)
####################



####################
dataset_list = []
final_merged_datasets = []
for in_file in args.infile:
    ## check that the file is there
    if not os.path.isfile(in_file):
        sys.exit("couldn't find"+in_file)
    dataset_list.append(dataset(in_file=in_file,name=in_file))
    final_array_inf = make_3d_array(dataset_list)
    final_array_noInf = final_array_inf
    final_array_noInf[np.isinf(final_array_noInf)]=np.nan
    ## get the final row and col
    rows=dataset_list[0].rows
    cols=dataset_list[0].cols
    ## do the actual merging
    final_merged_datasets.append(dataset(array=np.max(final_array_inf,axis=0),rows=rows,cols=cols,name='max_inf',out_dir=args.out_dir))
    final_merged_datasets.append(dataset(array=np.nanmax(final_array_noInf,axis=0),rows=rows,cols=cols,name='max_noInf',out_dir=args.out_dir))
    final_merged_datasets.append(dataset(array=np.median(final_array_inf,axis=0),rows=rows,cols=cols,name='median_inf',out_dir=args.out_dir))
    final_merged_datasets.append(dataset(array=np.nanmedian(final_array_noInf,axis=0),rows=rows,cols=cols,name='median_noInf',out_dir=args.out_dir))

    ## now write the results
    for fd in final_merged_datasets:
        fd.write_array()