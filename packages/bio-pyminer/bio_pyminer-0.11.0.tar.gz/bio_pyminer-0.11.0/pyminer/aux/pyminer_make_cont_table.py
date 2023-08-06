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
parser.add_argument("-out",
    help="directory for output")
    
args = parser.parse_args()
########################################################
if args.out[-1] != '/':
    args.out+='/'
########################################################

class_table=np.array(read_table(args.classes))
groups_table=np.array(read_table(args.sample_groups))

## make the group ids a bit more legible
for i in range(np.shape(groups_table)[0]):
	groups_table[i,1] = "sample_group_"+str(int(float(groups_table[i,1])))

## make sure all the ids match
class_id_hash = {key:value for key, value in class_table.tolist()}
#print(list(class_id_hash.keys())[:5])
group_table_ids = groups_table[:,0].tolist()
sg_id_hash = {key:value for key, value in groups_table.tolist()}

for cell_index in range(0,len(group_table_ids)):
	cell = group_table_ids[cell_index]
	try:
		class_id_hash[cell]
	except:
		print("couldn't find",cell,"in the classes table. If this is a header, it's fine, but if not, we're in deep doo-doo.")
		if cell_index!=0:
			sys.exit()

## make the contingency table
unique_class_ids = list(set(class_table[:,1].tolist()))
unique_class_ids = sorted(unique_class_ids)

unique_group_ids = list(set(groups_table[:,1].tolist()))
unique_group_ids = sorted(unique_group_ids)

contingency_table = np.zeros((len(unique_group_ids),len(unique_class_ids)))

group_index_hash = {key:value for value, key in enumerate(unique_group_ids)}
class_index_hash = {key:value for value, key in enumerate(unique_class_ids)}


for cell in group_table_ids:
	cell_class = class_id_hash[cell]
	cell_group = sg_id_hash[cell]
	row = group_index_hash[cell_group]
	col = class_index_hash[cell_class]
	contingency_table[row,col] += 1

contingency_table = contingency_table.tolist()
header = ['groups']+unique_class_ids
for i in range(0,len(contingency_table)):
	contingency_table[i] = [unique_group_ids[i]] + contingency_table[i]

contingency_table= [header] + contingency_table

print(np.array(contingency_table))

write_table(contingency_table,args.out+"group_class_contingency_table.txt")
