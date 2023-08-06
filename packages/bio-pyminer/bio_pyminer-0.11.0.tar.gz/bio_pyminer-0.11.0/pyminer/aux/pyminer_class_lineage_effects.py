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
import networkx as nx
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

parser.add_argument("-cont_table", 
    help="the file containing the contingency table")
parser.add_argument("-residuals", 
    help="the file containing the residuals table")
parser.add_argument("-lineage_dict", 
    help="the lineage dictionary .pkl file")
parser.add_argument("-out",
    help="directory for output")
    
args = parser.parse_args()
########################################################
if args.out[-1] != '/':
    args.out+='/'
########################################################


master_lineage_dict = import_dict(args.lineage_dict)
resid_table = np.array(read_table(args.residuals))
classes = resid_table[0,1:].tolist()
resid_array = np.array(resid_table[1:,1:],dtype=float)


######################################################
## some functions for plotting
global_cmap = sns.color_palette("coolwarm", 256)
def get_norm_vect(in_vect):
    temp_max = max(abs(np.array(in_vect)))
    in_vect = list(in_vect)
    fake_vect = [-temp_max]+in_vect+[temp_max]
    fake_vect = np.array(fake_vect)
    fake_vect = fake_vect - min(fake_vect)
    fake_vect = fake_vect/max(fake_vect)
    out_vect = fake_vect[1:-1].tolist()
    return(out_vect)


######################################################

def make_master_plot(pos,edges,base_colors,name_dict):
    global plt

    for i in range(0,len(base_colors)):
        plt.scatter(pos[i,0],pos[i,1],
            s=1000,c=np.array([base_colors[i]]),label=name_dict[i])
    #plt.show()

def add_coloration(pos,colors):
    global global_cmap
    # plt.scatter(pos[:,0],pos[:,1],
    #     s=450,c="white",cmap="coolwarm")
    plt.scatter(pos[:,0],pos[:,1],
        s=400,c=colors,edgecolors="white",cmap="coolwarm",
        linewidths=2.5)
    #plt.show()

## get the positions of all the points
pos = master_lineage_dict["plot"]["pos"]
colors = master_lineage_dict["plot"]["colors"]
edges = master_lineage_dict["plot"]["edges"]
names = master_lineage_dict["plot"]["node_names"]

## first go through just plotting the 
for i in range(0,len(classes)):
    temp_class = classes[i]
    temp_res_vect = resid_array[:,i]
    temp_plot = master_lineage_dict["plot"]
    ## convert residuals to colors get_colors
    color_vect = get_norm_vect(temp_res_vect)
    make_master_plot(pos,edges,colors,names)
    add_coloration(pos,color_vect)
    #temp_plot.plot(pos,col=color_vect,cmap=global_cmap)
    plt.show()

