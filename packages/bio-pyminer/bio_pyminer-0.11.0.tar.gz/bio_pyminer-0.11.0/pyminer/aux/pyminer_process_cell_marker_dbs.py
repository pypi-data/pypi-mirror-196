#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput, random
import numpy as np
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


#############################################################

class cell_markers():
    def __init__(self, name, species):
        self.name = name
        self.species = species


########################################################
def get_cellmark_cell_types(df):
    ## gets the set of cell types for the pang db

    ## human cell types

    ## mouse cell types

    return

def process_CellMarker(infile):
    df = pd.read_csv(infile, sep='\t')
    print("\n\nCellMarker")
    print(df.head(15))
    for col in df.columns: print(col)
    print(df[["speciesType","tissueType","cellType","cellName","geneSymbol","geneID"]])

    human_df = df[df["speciesType"] == "Human"]
    mouse_df = df[df["speciesType"] == "Mouse"]

    marker_list = []
    marker_list.append(cell_markers(name = "CellMarker", 
                                    species = "hsapiens"))
    marker_list.append(cell_markers(name = "CellMarker", 
                                    species = "mmusculus"))
    return


########################################################
def get_pang_cell_types(df):
    ## gets the set of cell types for the pang db
    
    return


def process_PanglaoDB(infile):
    ## this db is 
    df = pd.read_csv(infile, sep='\t')
    print("\n\nPang")
    print(df.head(15))
    for col in df.columns: print(col)

    ## separate into human and mouse 
    human_df = df[df["species"].isin(["Mm Hs","Hs"])]
    mouse_df = df[df["species"].isin(["Mm Hs","Mm"])]

    marker_list = []
    marker_list.append(cell_markers(name = "PanglaoDB", 
                                    species = "hsapiens"))
    marker_list.append(cell_markers(name = "PanglaoDB", 
                                    species = "mmusculus"))
    return(marker_list)
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-lib_dir","-string_db_dir",
        help="This directory contains the cell_type_marker_gene_files.txt and their associated files file distributed with the package",
        type = str,
        default = "/usr/local/lib/")
    args = parser.parse_args()

    file_types_and_functions = {"CellMarker":process_CellMarker,
                                "PanglaoDB":process_PanglaoDB}

    all_files = read_table(os.path.join(args.lib_dir,"cell_type_marker_gene_files.txt"))
    all_markers = []
    for line in all_files:
        ## name of db \t file
        all_markers.append(file_types_and_functions[line[0]](line[1]))
    return



if __name__ == "__main__":
    main()

