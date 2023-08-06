#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
try:
    from pyminer.common_functions import *
except:
    from common_functions import *
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

def cmd(in_message, com=True):
    print(in_message)
    time.sleep(.25)
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)



##############################################################

##########################################################################
parser = argparse.ArgumentParser()

## global arguments
parser.add_argument(
    '-file_list','-in','-i','-input',
    dest='file_list',
    help = "files that contain the input file adj lists",
    nargs = '+'#,
    )#type=argparse.FileType('r'))

parser.add_argument(
    '-out_dir','-out','-o',
    type=str)

parser.add_argument(
    '-percent_cutoff','-p',
    type = float,
    default = 0.33333)

args = parser.parse_args()
################################################################
file_list = args.file_list
out_dir = args.out_dir
if out_dir[-1]!='/':
    out_dir += '/'

if os.path.isdir(out_dir):
    pass
else:
    cmd('mkdir '+out_dir)

edge_delim = '|'

count_cutoff = args.percent_cutoff * len(file_list)
print('\n\n\ncount cutoff',count_cutoff,'\n\n\n')

##############################################################
def get_unique(temp_line):
    global edge_delim
    temp_line = sorted(temp_line)
    temp_line = edge_delim.join(temp_line)
    return(temp_line)

def get_file_adj_idset(f):
    print('\t\tgetting edge IDs from',f)
    ## gets a list of unique IDs for all edges of 
    temp_adj_pairs =[]
    first = True
    for line in fileinput.input(f):
        if first:
            first=False
        else:
            temp_line=strip_split(line)
            if len(temp_line)==1:## possible orphan nodes shouldn't be there, but just in case
                pass
            else:
                ## order the two nodes alphabetically so that each pair
                ## can only appear once. Because this is for undirected
                ## co-expression networks, it shouldn't make a difference
                ## and it will cut the run time in half
                unique_id = get_unique(temp_line)
                temp_adj_pairs.append(unique_id)
    fileinput.close()
    print('\t\t',len(temp_adj_pairs))
    return(temp_adj_pairs)

def dictify(in_list):
    return({key:idx for idx, key in enumerate(in_list)})

def quick_search(in_dict,term):
    try:
        in_dict[term]
    except:
        return(False)
    else:
        return(True)

#####################################################################

## go through each file getting the full list of all neighbors
all_adj_pairs = [] ## all adj pairs is the list of all edges with a unique identifier
print('cateloguing all of the edges:')
for f in file_list:
    print('\t',f)
    all_adj_pairs += get_file_adj_idset(f)
    print('\trunning total:',len(all_adj_pairs))

## make it unique
all_adj_pairs = sorted(list(set(all_adj_pairs)))

print('\n\nfound',len(all_adj_pairs),'edges in total\n\n')

## the boolean matrix of whether an edge is present in a given dataset
## rows for each edge and columns are each network
adj_bool_mat = np.zeros((len(all_adj_pairs), len(file_list)),dtype=int)


## go through each file again now looking for each of the full edge list
print('\n\ncateloguing the number of times each edge appears:')
for i in range(0,len(file_list)):
    f = file_list[i]
    print('\t',f)
    temp_adj_dict = dictify(get_file_adj_idset(f))
    print('\t\tfound',len(list(temp_adj_dict.keys())),'edges in this adj list')
    for j in range(0,len(all_adj_pairs)):
        if quick_search(temp_adj_dict, all_adj_pairs[j]):
            adj_bool_mat[j,i]=1
        else:
            pass#print(all_adj_pairs[j])

## count how many datasets each edge is in
adj_count = np.sum(adj_bool_mat, axis = 1)

################################################
## make the output files
filtered_node_dict = {}
print("making the output files")
out_count = [["node_1","node_2", "edge_count"]]
filtered_out_adj = [["node_1","node_2"]]
for i in range(0,len(all_adj_pairs)):
    temp_edge = all_adj_pairs[i]
    temp_edge = temp_edge.split(edge_delim)
    if adj_count[i]>count_cutoff:
        filtered_out_adj.append(temp_edge[:])
        ## enter them into the dictionary for the output ID_list.txt
        filtered_node_dict[temp_edge[0]] = None
        filtered_node_dict[temp_edge[1]] = None
    temp_edge += [adj_count[i]]
    out_count.append(temp_edge)


write_table(out_count,out_dir+'full_adj_list_counts.txt')
write_table(filtered_out_adj,out_dir+'filtered_adj_list.txt')
make_file('\n'.join(sorted(list(filtered_node_dict.keys()))),out_dir+'ID_list.txt')

## write the boolean matrix
bool_out = [['edge']+file_list]
for i in range(0,len(all_adj_pairs)):
    temp_edge = [all_adj_pairs[i]]+adj_bool_mat[i,:].tolist()
    bool_out.append(temp_edge)

write_table(bool_out,out_dir+'boolean_adj_list_table.txt')



