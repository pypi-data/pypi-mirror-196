#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
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
	'-input','-i',
	help = "input adj list")

parser.add_argument(
	'-output','-o',
	help = "input adj list")

parser.add_argument(
	'-annotation_file','-a',
	help = 'the annotations.tsv file created by a PyMINEr run')

parser.add_argument(
    '-convert_to_human',
    action = 'store_true',
    help = "if we're converting this adj_list to the human orthologues. Note that you'll also need to supply the human_orthologues.tsv file instead of the annotations.tsv file")


args = parser.parse_args()
################################################################




######## process the annotation file ########
annotations = read_table(args.annotation_file)
if args.convert_to_human:
    target_index = 4
else:
    target_index = 3
ensg_mapping_dict = {}
for i in range(1,len(annotations)):
    temp_id = annotations[i][1]
    if "ENTREZGENE_ACC" in temp_id:
	    temp_id = temp_id.replace("ENTREZGENE_ACC:","")
	    temp_id = str(float(temp_id))
    temp_ensg_id = annotations[i][target_index]
    if temp_ensg_id == "None":
    	pass
    else:
	    if temp_id in ensg_mapping_dict:
	    	temp_mapping_vect = ensg_mapping_dict[temp_id]
	    	temp_mapping_vect.append(temp_ensg_id)
	    else:
	    	ensg_mapping_dict[temp_id] = [temp_ensg_id]



#############################################



def get_all_ens_pairs(aliases_1,aliases_2):
	all_ensg_pairs = []
	for a1 in aliases_1:
		for a2 in aliases_2:
			all_ensg_pairs.append([a1,a2])
	return(all_ensg_pairs)

def translate_line(temp_line):
	global ensg_mapping_dict
	## check to make sure both of these genes are in the ensg dict
	if temp_line[0] not in ensg_mapping_dict or temp_line[1] not in ensg_mapping_dict:
		#print("trouble mapping:",temp_line)
		return()
	#print(temp_line[0])
	a1=ensg_mapping_dict[temp_line[0]]
	a2=ensg_mapping_dict[temp_line[1]]
	#print(a1,a2)
	return(get_all_ens_pairs(a1,a2))

def process_line(temp_line):
	global out_adj_file
	new_adj_list = translate_line(temp_line)
	if new_adj_list == None:
		## if the orthologues didn't both map sucessfully 
		return()
	else:
		for adj in new_adj_list:
			#print(adj)
			out_adj_file.write('\t'.join(adj)+'\n')


#############################################

if os.path.isfile(args.output):
	cmd('rm '+args.output)
if os.path.isfile(args.output+"_temp"):
	cmd('rm '+args.output+"_temp")

out_adj_file = open(args.output+"_temp",'a')

print('writing output ENSG adj list:')
print('\t',args.output)

first = True
for line in fileinput.input(args.input):
	if first:
		first = False
	else:
		temp_line = strip_split(line)
		process_line(temp_line)


out_adj_file.close()


## remove the last new line
cmd("head -c -1 "+args.output+"_temp"+" > "+args.output)
cmd("rm "+args.output+"_temp")









