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


parser.add_argument("-collation_file", 
    help="the file describing cell types and datasets",
    type = str,
    default = "/media/scott/HD2/all_pancreatic_datasets/final_datasets/combined_autocrine_paracrine/cell_type_annotations.txt")
parser.add_argument("-percent_cutoff",
	default = 0.5,
	type=float)#0.65)
parser.add_argument("-out", 
    help="the output folder in which the final output enrichemnt files should go",
    type = str,
    default = "/media/scott/HD2/all_pancreatic_datasets/final_datasets/combined_autocrine_paracrine/enrichment_files/")
args = parser.parse_args()

######## process the annotation file ########
def get_annotation_dict(anno_path):
	annotations = read_table(anno_path)
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
	return(ensg_mapping_dict)

############################################

collation_file = np.array(read_table(args.collation_file))

## collect all of the cell types, and the files for their enrichment lists
cell_types = sorted(list(set(collation_file[1:,2].tolist())))
print(cell_types)

## log the datasets, associated annotation file, and enrichment list file for each net cell type
full_cell_type_dict ={cell_type:[] for cell_type in cell_types}

print(collation_file[0])
for i in range(1,np.shape(collation_file)[0]):
	temp_cell_type = collation_file[i][2]
	temp_full_list = full_cell_type_dict[temp_cell_type]
	## PMID, annotation_file, enrichment_file
	temp_pmid = collation_file[i][3]
	temp_annotation_file = collation_file[i][4]
	temp_enrichment_file = collation_file[i][5]
	print(temp_cell_type, [temp_pmid,temp_annotation_file,temp_enrichment_file])
	temp_full_list.append([temp_pmid,temp_annotation_file,temp_enrichment_file])
	full_cell_type_dict[temp_cell_type] = temp_full_list[:]

## count the number of times a cell type was found in a given dataset
cell_type_dataset_count = {}
cell_type_enriched_cutoff = {}
for cell in cell_types:
	print('\n\n\n',cell)
	for file_vect in full_cell_type_dict[cell]:
		print('\t',file_vect)
	cell_type_dataset_count[cell]=len(full_cell_type_dict[cell])
	cell_type_enriched_cutoff[cell]=len(full_cell_type_dict[cell])*args.percent_cutoff
	print('\n\t',cell_type_dataset_count[cell],cell_type_enriched_cutoff[cell])


## generate the ensembl gene dicts
dataset_ensg_dict = {}
for i in range(1,np.shape(collation_file)[0]):
	if collation_file[i][3] not in dataset_ensg_dict:
		dataset_ensg_dict[collation_file[i][3]] = get_annotation_dict(collation_file[i][4])

##########################################
def convert_enrichment_list(in_list,in_dict):
	out_list = []
	for gene in in_list:
		if gene not in in_dict:
			print('\tdifficulty mapping',gene)
		else:
			out_list += in_dict[gene]
	out_list = sorted(list(set(out_list)))
	return(out_list)

def get_all_cell_enrichment_lists(cell_enrich_list):
	global dataset_ensg_dict
	temp_cell_type_enrichment_list_of_lists = []
	for file_vect in cell_enrich_list:
		## the gene list & the ensembl look up for this dataset
		temp_cell_type_enrichment_list_of_lists.append(convert_enrichment_list(read_file(file_vect[2]),dataset_ensg_dict[file_vect[0]]))
		print('\t',temp_cell_type_enrichment_list_of_lists[-1][:2],'...')
	return(temp_cell_type_enrichment_list_of_lists)

## make each ensg enrichment list
full_cell_enrichment_lists ={}
for cell in cell_types:
	print(cell)
	full_cell_enrichment_lists[cell]=get_all_cell_enrichment_lists(full_cell_type_dict[cell])



## get the summary stats for each gene in each enrichment set
final_cell_enrichment_dict = {}
for cell in cell_types:
	## make a list of all genes that appear at all for this cell type
	temp_all_gene_lists = full_cell_enrichment_lists[cell]
	temp_unique_genes = []
	temp_all_linear_genes = []
	for gl in temp_all_gene_lists:
		temp_unique_genes+=gl
		temp_all_linear_genes+=gl
	temp_unique_genes = sorted(list(set(temp_unique_genes)))
	## catelogue the number of times that each gene shows up
	gene_enrichment_summary=[]
	final_significant_gene_list = []
	for gene in temp_unique_genes:
		gene_enrichment_summary.append([gene,temp_all_linear_genes.count(gene)])
		if gene_enrichment_summary[-1][-1] >= cell_type_enriched_cutoff[cell]:
			final_significant_gene_list.append(gene)
	write_table(gene_enrichment_summary[:],args.out+"aall_genes_count_"+cell+".txt")
	print(cell,len(final_significant_gene_list),"genes in final gene list")
	final_cell_enrichment_dict[cell]=final_significant_gene_list[:]
	make_file('\n'.join(final_significant_gene_list),args.out+cell+".txt")

## make the boolean table and background IDs
all_genes = []
include_cell_types = ["acinar","alpha","beta","delta","duct","epsilon","pp","stromal"]
for cell in include_cell_types:
	all_genes += final_cell_enrichment_dict[cell]
all_genes = sorted(list(set(all_genes)))
all_gene_idx_hash = {value:key for key, value in enumerate(all_genes)}

bool_out = np.zeros((len(all_genes),len(include_cell_types)),dtype = bool)

for col in range(len(include_cell_types)):
	cell = include_cell_types[col]
	temp_enrich = final_cell_enrichment_dict[cell]
	for gene in temp_enrich:
		row = all_gene_idx_hash[gene]
		bool_out[row,col]=True

bool_out = np.array(bool_out,dtype=str).tolist()
bool_out = [include_cell_types]+bool_out
make_file('\n'.join(all_genes[:]),args.out+'all_included_genes.txt')
out_genes = ['gene']+all_genes
for i in range(0,len(out_genes)):
	bool_out[i]=[out_genes[i]]+bool_out[i]

write_table(bool_out,args.out+'boolean_enrichment_table.tsv')

