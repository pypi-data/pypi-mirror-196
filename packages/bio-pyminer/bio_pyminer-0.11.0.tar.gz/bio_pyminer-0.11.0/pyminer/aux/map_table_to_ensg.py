#!/usr/bin/env python3
import pickle, scipy, sys,  fileinput, gc, os
import numpy as np
import matplotlib.pyplot as plt

gc.enable()
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

def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))
############################################################################################
##############################################################
import argparse
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


args = parser.parse_args()
################################################################

######## process the annotation file ########
annotations = read_table(args.annotation_file)
ensg_mapping_dict = {}
for i in range(1,len(annotations)):
    temp_id = annotations[i][1]
    if "ENTREZGENE_ACC" in temp_id:
	    temp_id = temp_id.replace("ENTREZGENE_ACC:","")
	    temp_id = str(float(temp_id))
    temp_ensg_id = annotations[i][3]
    if temp_ensg_id == "None":
    	pass
    else:
	    if temp_id in ensg_mapping_dict:
	    	temp_mapping_vect = ensg_mapping_dict[temp_id]
	    	temp_mapping_vect.append(temp_ensg_id)
	    else:
	    	ensg_mapping_dict[temp_id] = [temp_ensg_id]

#############################################

def get_out_lines(in_line):
	global ensg_mapping_dict
	temp_gene = in_line[0]
	if temp_gene not in ensg_mapping_dict:
		return()
	else:
		ensg_list = ensg_mapping_dict[temp_gene]
		out_lines = []
		for temp_ens in ensg_list:
			temp_line = [temp_ens]+in_line[1:]
			out_lines.append(temp_line)
	return(out_lines)

input_table = read_table(args.input)
output = [input_table[0]]



for i in range(1,len(input_table)):
	output += get_out_lines(input_table[i])

write_table(output,args.output)

