#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
import random
from random import sample
from scipy.stats import gaussian_kde
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import networkx as nx
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
from copy import deepcopy
import ray
import shutil
# try:
#     from pyminer.common_functions import *
#     from pyminer.get_stats import ray_dicts_to_array
# except:
#     from ..common_functions import *
#     from ..get_stats import ray_dicts_to_array
# import pandas as pd
#############################################################

## DELETE ALL OF THESE ONCE I FIGURE OUT HOW TO IMPORT FROM DEEPER IN DIRECTORY
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

def make_table(lines,delim, num_type = float):
    #print(num_type)
    for i in range(0,len(lines)):
        lines[i]=lines[i].strip()
        lines[i]=lines[i].split(delim)
        for j in range(0,len(lines[i])):
            try:
                float(lines[i][j])
            except:
                lines[i][j]=lines[i][j].replace('"','')
            else:
                if num_type == float:
                    lines[i][j]=float(lines[i][j])
                elif num_type == int:
                    lines[i][j]=int(float(lines[i][j]))
                else:
                    lines[i][j]=num_type(lines[i][j])
    return(lines)


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return(in_path+'/')


def read_table(file, sep='\t',num_type=float):
    return(make_table(read_file(file,'lines'),sep,num_type=num_type))
    
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
#####################################################
def cp(file1,file2):
    with open(file1, 'rb') as f_in:
        with open(file2, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return()


def rm(rm_file):
    if os.path.isfile(rm_file):
        os.remove(rm_file)
    else:
        print('WARNING:',rm_file,"doesn't exist, couldn't remove it")
    return()


def process_dir(in_dir):
    ## process the output dir
    if in_dir[-1]!='/':
        in_dir+='/'
    if not os.path.isdir(in_dir):
        os.makedirs(in_dir)
    return(in_dir)



##############################################################
## this function was adopted from emre's stackoverflow answer found here:
## https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python
def correct_pvalues_for_multiple_testing(pvalues, correction_type = "Benjamini-Hochberg"):                
    """                                                                                                   
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    from numpy import array, empty
    pvalues = array(pvalues)
    n = int(pvalues.shape[0])
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        for rank, vals in enumerate(values):
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue
    elif correction_type == "Benjamini-Hochberg":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        values.reverse()
        new_values = []
        for i, vals in enumerate(values):
            rank = n - i
            pvalue, index = vals
            new_values.append((n/rank) * pvalue)
        for i in range(0, int(n)-1):
            if new_values[i] < new_values[i+1]:
                new_values[i+1] = new_values[i]
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]
    return new_pvalues

##############################################################
## DELETE ALL OF THESE ONCE I FIGURE OUT HOW TO IMPORT FROM DEEPER IN DIRECTORY
## ray functions
def get_indices(threads, num_genes):
    indices_list = []
    for t in range(threads):
        indices_list.append([])
    temp_idx = 0
    while temp_idx < num_genes:
        for t in range(threads):
            if temp_idx < num_genes:
                indices_list[t].append(temp_idx)
                temp_idx += 1
    return(indices_list)


def get_num_rows_from_dict_lists(dict_list):
    ## goes through all of the indices & returns the number of dims
    row_dims = 0
    for temp_dict in dict_list:
        for temp_key in list(temp_dict.keys()):
            #print(temp_key)
            if temp_key > row_dims:
                row_dims = temp_key
    return(row_dims+1)


def get_num_cols_from_dict_lists(dict_list):
    ## first get the dimentions
    first_key = list(dict_list[0].keys())[0]
    first = dict_list[0][first_key]
    if type(first) == list:
        col_dims = len(first)
    else:
        col_dims = 1
    return(col_dims)


def ray_dicts_to_array(dict_list):
    row_dims = get_num_rows_from_dict_lists(dict_list)
    col_dims = get_num_cols_from_dict_lists(dict_list)
    out_array = np.zeros((row_dims, col_dims))
    print(out_array)
    for temp_dict in dict_list:
        for idx, value in temp_dict.items():
            #print(idx)
            #print(value)
            out_array[idx] = value
    return(out_array)
###########################################################

##########################################################################
parser = argparse.ArgumentParser()

## global arguments
parser.add_argument(
    '-infile','-in','-i',
    dest='infile',
    help="input data matrix",
    type=str)

parser.add_argument(
	'-cluster_pkl','-clust',
	dest='cluster_pkl',
    help="clustering object created by clustering.py. This will typically be titled 'transition_prob.pkl'",
	type=str)

parser.add_argument(
    '-single_groups','-sg',
    help="group clustering results created by clustering.py. This will typically be titled '.../sample_clustering_and_summary/sample_k_means_groups.txt'",
    type=str)


parser.add_argument(
    '-mean_expression','-means',
    help="the mean expression matrix within groups. This will typically be titled: '.../sample_clustering_and_summary/k_group_means.txt'",
    type=str)


parser.add_argument(
    '-anova_summary','-aov',
    help="the summary of the ANOVAs performed by the get_stats.py program. Typically called'.../sample_clustering_and_summary/significance/groups_1way_anova_results.txt'",
    type=str)


parser.add_argument(
    "-transition_prob_file","-prob_file",'-probs',
    help = 'The file containing the cell type transition probabilities. Often called ".../sample_clustering_and_summary/final_cell_type_transition_probabilities.txt"',
    type = str)

parser.add_argument(
    "-out_dir","-output_dir","-o",
    help = 'the output directory',
    type = str)

parser.add_argument("-species", '-s',
    help="a gProfiler accepted species code. Dafault = 'hsapiens'",
    type = str,
    default = 'hsapiens')



## hdf5 options
parser.add_argument(
    '-hdf5',
    help = 'The input file is an HDF5 file',
    default = False,
    action = 'store_true')

parser.add_argument(
    "-ID_list","-ids",
    help = 'Give the row-wise IDs in this new line delimeted file. This will be used for the background',
    type = str)

parser.add_argument(
    "-columns","-cols",
    help = 'If we are using an hdf5 file, give the column-wise IDs in this new line delimeted file',
    type = str)



parser.add_argument(
    "-log",'-log2','-log_transform',
    help='do a log transformation prior to clustering',
    action = 'store_true',
    default = False)



parser.add_argument(
    '-processes', '-p',
    help = 'The number of processes to use. Default will be the number of available threads.',
    default = None,
    type = int)


args = parser.parse_args()
##########################################################################
def reorganize_single_type_table(full_table):
    ## here we will make the list of lists, get the IDhash, IDlist, etc
    max_group=-1
    ID_list = []
    ID_hash = {}
    for i in range(0,len(full_table)):
        ID_hash[full_table[i][0]]=i
        ID_list.append(full_table[i][0])
        if full_table[i][1]>max_group:## keep track of how many groups there are total
            max_group=full_table[i][1]
    
    ## the index in group_lists corresponds to the cell type group number
    ## the indices within these lists correspond to the sample index 
    group_lists=[[] for i in range(max_group+1)]
    for i in range(len(full_table)):
        group_lists[full_table[i][1]].append(i)
    return(group_lists)

def get_agglomerated_cell_types(merged_cell_types_table,single_group_ids):
    ## go through the merged cell type table, adding new sublists as we go
    all_group_ids = single_group_ids[:]
    #print(all_group_ids)
    merged_group_indices = [[i] for i in range(0,len(single_group_ids))]
    branches = []
    print(merged_group_indices)

    for i in range(0,len(merged_cell_types_table)):
        #print(merged_cell_types_table[i])
        first_merged_group_idx = int(merged_cell_types_table[i][0])
        second_merged_group_idx = int(merged_cell_types_table[i][1])
        branches.append([first_merged_group_idx,second_merged_group_idx])
        
        first_group = all_group_ids[first_merged_group_idx]
        #print(second_merged_group_idx)
        print("group#:",len(all_group_ids))
        second_group = all_group_ids[second_merged_group_idx]
        
        merged_group_indices.append(merged_group_indices[first_merged_group_idx]+merged_group_indices[second_merged_group_idx])
        print(len(merged_group_indices[-1]),merged_group_indices[-1])
        all_group_ids.append(first_group+second_group)
        #print(len(all_group_ids[-1]),all_group_ids[-1])
        #sys.exit()
    #sys.exit()
    return(merged_group_indices,all_group_ids,branches)

##########################################################################
def intify_column(in_table, column):
    for i in range(len(in_table)):
        in_table[i][column] = int(in_table[i][column])
    return(in_table)

##########################################################################
## make the output directory
args.out_dir = process_dir(args.out_dir)

## read in the files
print(args.cluster_pkl)
cluster_result_dict = import_dict(args.cluster_pkl)
cluster_result = cluster_result_dict["transition_probability"]
single_cell_type_table = read_table(args.single_groups,num_type=float)
single_cell_type_table = intify_column(single_cell_type_table,1)
for i in range(5):
    print(single_cell_type_table[i])
#transition_probs = np.array(read_table(args.transition_prob_file),dtype=float)#final_cell_type_transition_probabilities.txt
transition_probs = np.array(cluster_result.data)
single_group_lists = reorganize_single_type_table(single_cell_type_table)


colors = cluster_result_dict["color_vect"]



#######################################################
## get the linkage
min_span_tree = True
if min_span_tree:
    ## create a graph network of the transition probability matrix weighted on the probability
    ## TODO
    ## more of a note to myself: Look into maximum spanning tree instead of minimum spanning tree of inverse prob
    G=nx.Graph(1/transition_probs)
    Tree = nx.minimum_spanning_tree(G)
    T_graph = sorted(Tree.edges(data=True))
    for i in T_graph:
        print(i)
        if i[2]['weight'] > 10000:
            Tree.remove_edge(i[0],i[1])
            print("\tremoving",i)

    print('\n\nfinal graph')
    T_graph = sorted(Tree.edges(data=True))
    branches = []
    for i in T_graph:
        print(i)
        branches.append([i[0],i[1]])

    ## keep a record of the directly linked branches only. Below, we'll add to the branches object to compare the agglomerated objects
    single_merger_branches = branches[:]


    ## get all of the regular groups that are linked together
    merged_group_indices = [[i] for i in range(0,len(single_group_lists))]
    all_group_ids = single_group_lists[:]

    ## then compare the components to each other
    n_components = nx.number_connected_components(Tree)
    current_number_of_groups = len(merged_group_indices)
    print(n_components,'connected components')
    all_comps = nx.connected_components(Tree)
    new_component_indices_in_group_vect = []
    for comp in all_comps:
        merged_group_indices.append(list(comp))
        new_component_indices_in_group_vect.append(len(merged_group_indices)-1)
        print(list(comp))
        current_number_of_groups+=1

        ## put the component into a group together
        #print("single_group_lists",single_group_lists)
        temp_group = []
        for i in merged_group_indices[-1]:
            #print(i)
            #print(single_group_lists[i])
            temp_group+=single_group_lists[i]
        all_group_ids.append(temp_group)

    ## add all of the pairwise component comparisons
    for i in range(0,len(new_component_indices_in_group_vect)):
        for j in range(i,len(new_component_indices_in_group_vect)):
            if i!=j:
                branches.append([new_component_indices_in_group_vect[i], new_component_indices_in_group_vect[j]])


    ## calculate the page ranks
    full_T_graph = nx.Graph()
    for edge in T_graph:
        print(edge)
        full_T_graph.add_edge(edge[0],edge[1])
    for node in G.nodes():
        if node not in full_T_graph.nodes():
            full_T_graph.add_node(node)
    print(full_T_graph.edges())
    print(type(full_T_graph))
    pr = nx.pagerank(full_T_graph,nstart = {i:15000 for i in full_T_graph.nodes()})

    colors = cluster_result_dict["color_vect"]
    print(colors)
    color_dict = {key:value for key, value in enumerate(colors)}
    try:
        print("temp_attr_name","color")
        nx.set_node_attributes(full_T_graph,color_dict,name = "col")
    except:
        nx.set_node_attributes(full_T_graph,"col",color_dict)

    ## get the postion of the nodes
    pos = nx.spring_layout(full_T_graph)

    try:
        print("temp_attr_name","color")
        nx.set_node_attributes(full_T_graph,pos,name = "pos")
    except:
        nx.set_node_attributes(full_T_graph,"pos",pos)
    
    node_numbers = list(range(0,len(list(full_T_graph.nodes()))))
    names = {node:"sample_group_"+str(node) for node in node_numbers}
    print(names)
    try:
        nx.set_node_attributes(full_T_graph,names,name = "name")
    except:
        nx.set_node_attributes(full_T_graph,"name",names)

    print("\n\n")
    for item in full_T_graph.nodes.items():
        temp_name =item[0]
        print('\t',item)
    ## draw the graph
    #################
    ## first try
    colors_sorted_by_graph = []
    names_sorted_by_graph = []
    for node in full_T_graph.nodes():
        colors_sorted_by_graph.append(colors[node])
        names_sorted_by_graph.append(names[node])

    ###############
    ## next try for custom legend
    custom_points = []
    custom_names = []
    for node in node_numbers:
        temp_pos = pos[node]
        custom_names.append('sample_group_'+str(node))
        custom_points.append(plt.scatter(temp_pos[0],temp_pos[1], c=colors[node], label = names[node],s=1000))
    plt.clf()
    nx.draw_networkx_nodes(full_T_graph,pos, node_shape = 'o', linewidths = 0, 
                               node_size = 1000, node_color = colors_sorted_by_graph, width = 1, font_size=0,
                               label=names_sorted_by_graph)
    nx.draw_networkx_edges(full_T_graph,pos, 
            node_size = 1000, width = 1, font_size=0)
    ax=plt.gca()
    ax.legend(custom_points, custom_names, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,markerscale=1/4)
    plt.savefig(args.out_dir+'cell_type_lineage.png',
        dpi=600,
        bbox_inches='tight')
    plt.clf()
    ## save the adjacency list and graph network
    adj_list = list(full_T_graph.edges())
    for i in range(0,len(adj_list)):
        adj_list[i]=list(adj_list[i])
        adj_list[i][0]="sample_group_"+str(adj_list[i][0])
        adj_list[i][1]="sample_group_"+str(adj_list[i][1])
    adj_list = [["group1","group2"]]+adj_list

    ## log all of the edge locations 
    edge_list=[]
    for nodes in list(full_T_graph.edges()):
        node1=nodes[0]
        node2=nodes[1]
        node_1_location = pos[node1]
        node_2_location = pos[node2]
        xs = [node_1_location[0],node_2_location[0]]
        ys = [node_1_location[1],node_2_location[1]]
        edge_list.append([xs,ys])

    pos_array = np.zeros((len(node_numbers),2))
    for i in range(0,len(node_numbers)):
        pos_array[i] = pos[i]
    
    plot_dict={"x":pos_array[:,0],
    "y":pos_array[:,1],
    "pos":pos_array,
    "node_names":names,
    "colors":colors,
    "edges":edge_list}

    lineage_dict={"graph":full_T_graph,"plot":plot_dict}
    save_dict(lineage_dict,args.out_dir+"/lineage_dict.pkl")
    write_table(adj_list,args.out_dir+"/lineage_adj_list.tsv")
    #sys.exit()

else:
    ## this one does a merger based off of the linkage dendrogram created by the 
    ## transition probabilities

    merged_cell_types_table = cluster_result.dendrogram_row.linkage
    print(dir(cluster_result.dendrogram_row))
    
    
    ## get the list of lists which contains all the agglomerated cell type categories
    merged_group_indices,all_group_ids,branches = get_agglomerated_cell_types(merged_cell_types_table,single_group_lists)

# print("merged_group_indices")
# print(merged_group_indices)
# print("\nall_group_ids")
# print(len(all_group_ids))
# print("\nbranches")
# print(branches)
# sys.exit()


anova_summary_table = read_table(args.anova_summary)
global_significant_indices = []
for i in range(1,len(anova_summary_table)):
    #print(anova_summary_table[i][3])
    if anova_summary_table[i][3]<=0.05:## this is for performing the protected post-hocs
        global_significant_indices.append(True)
    else:
        global_significant_indices.append(False)
    #print(global_significant_indices[-1],anova_summary_table[i][3])


####################################################################
## read in the raw data file for doing the stats


if not args.hdf5:
    full_expression_str = read_table(args.infile)
    title = full_expression_str[0]
    full_expression_np = np.array(full_expression_str)
    row_names = full_expression_np[1:,0]
    full_expression = np.array(full_expression_np[1:,1:],dtype = float)

else:
    row_names = read_file(args.ID_list,'lines')
    title = read_file(args.columns,'lines')
    print('making a maliable hdf5 file to preserve the original data')
    cmd('cp '+args.infile+' '+args.infile+'_copy')
    import h5py
    print('reading in hdf5 file')
    infile_path = args.infile+'_copy'
    h5f = h5py.File(infile_path, 'r+')
    full_expression=h5f["infile"]

ID_list = row_names[:]
ID_hash = {name:idx for idx,name  in enumerate(ID_list)}


def ids_to_idxs(in_ids):
    global ID_hash
    temp_index_list = [ID_hash[i] for i in in_ids]
    return(temp_index_list)


if args.log:
    full_expression = np.log2(full_expression-np.min(full_expression)+1)


####################################################################
## go through all branch points and perform post-hoc tests

output_uncorrected_p_vals = np.ones((len(global_significant_indices),len(branches)))
output_corrected_p_vals = np.ones((len(global_significant_indices),len(branches)))
print(np.shape(output_uncorrected_p_vals))

print(np.shape(full_expression))


@ray.remote
def ray_get_post_hocs(indices, global_significant_indices, full_expression, group1_indices, group2_indices,  hdf5_file = None):
    if hdf5_file is not None:
        h5f = h5py.File(hdf5_file, 'r')
        full_expression=h5f["infile"]

    post_hoc_dict = {idx:None for idx in indices}
    group1_higher_dict = {idx:None for idx in indices}
    ray_count = 0
    for i in indices:
        if ray_count % 250 == 0:
            print("worker is:",ray_count/len(indices)*100," percent done")
        if global_significant_indices[i]:
            ## perform protected t-test post-hoc
            group1 = full_expression[i,group1_indices]
            group2 = full_expression[i,group2_indices]
            if np.mean(group1) > np.mean(group2):
                group1_higher_dict[i] = True
            else:
                group1_higher_dict[i] = False
            try:
                statistic,temp_p_val = ttest_ind(group1, group2,
                    equal_var=False)
                #statistic,temp_p_val = mannwhitneyu(group1, group2)
                post_hoc_dict[i] = [temp_p_val,group1_higher_dict[i]]
            except:
                post_hoc_dict[i] = [1, group1_higher_dict[i]]
                statistic, temp_p_val = (0,1)
                # statistic,temp_p_val = mannwhitneyu(group1, group2)#,
                #     #equal_var=False)
        else:
            post_hoc_dict[i] = [1,group1_higher_dict[i]]
        ray_count+=1
    
    if hdf5_file is not None:
        h5f.close()

    return(post_hoc_dict)


def get_post_hocs(i):
    global global_significant_indices, full_expression, group1_indices, group2_indices
    if global_significant_indices[i]:#True:
        ## perform protected t-test post-hoc
        group1 = full_expression[i,group1_indices]
        group2 = full_expression[i,group2_indices]
        try:
            statistic,temp_p_val = ttest_ind(group1, group2,
                equal_var=False)
            #statistic,temp_p_val = mannwhitneyu(group1, group2)
        except:
            statistic, temp_p_val = (0,1)
            # print(i)
            # print(group1,group2)
            # print(group1_mean,group2_mean)
            # statistic,temp_p_val = mannwhitneyu(group1, group2)#,
            #     #equal_var=False)
    else:
        temp_p_val = 1
    return(temp_p_val)


################################################################
from scipy.stats import ttest_ind, mannwhitneyu
branch_names = []
branch_differential_genes = []

############### NEW1 ########################
#threads = multiprocessing.cpu_count()
if args.processes == None:
    args.processes = multiprocessing.cpu_count()
threads = args.processes
indices_list = get_indices(threads, full_expression.shape[0])

ray.init()
## set up the input files
if not args.hdf5:
    ray_full_expression = ray.put(full_expression)
else:
    ## make copies of the input hdf5 file
    hdf5_file_list = []
    for t in range(threads):
        hdf5_file_list.append(args.infile+"_"+str(t))
        cp(args.infile,hdf5_file_list[-1])
############### /NEW1 ########################

for branch in range(0,len(branches)):
    branch_differential_genes.append([[],[]])
    b=branches[branch]
    #print(b)
    group1_indices = sorted(all_group_ids[b[0]])
    #print(group1_indices)
    group2_indices = sorted(all_group_ids[b[1]])
    print('\n\ncomparing group',b[0],'to',b[1],':',branch+1,"/",len(branches))
    branch_names.append(str(b[0])+'_vs_'+str(b[1]))

    ########################### OLD ##################################
    # pool = ThreadPool(threads)
    # results = pool.map(get_post_hocs,range(full_expression.shape[0]))
    # pool.close()
    # pool.join()
    ########################## /OLD ####################################
    ########################## NEW2 ###################################


    ## set up the jobs
    r_jobs = []
    for t in range(threads):
        if not args.hdf5:
            #ray_get_post_hocs(indices, global_significant_indices, full_expression, group1_indices, group2_indices,  hdf5_file = None)
            r_jobs.append(ray_get_post_hocs.remote(indices_list[t], 
                                                   global_significant_indices,
                                                   ray_full_expression,
                                                   group1_indices,
                                                   group2_indices))
        else:
            r_jobs.append(ray_get_post_hocs.remote(indices_list[t], 
                                                   global_significant_indices,
                                                   None,
                                                   group1_indices,
                                                   group2_indices,
                                                   hdf5_file = hdf5_file_list[t]))
            
    temp_results = ray.get(r_jobs)
    

    results_array = ray_dicts_to_array(temp_results)
    results = results_array[:,0].tolist()
    group1_higher_bool_array = results_array[:,1].tolist()

    ########################## /NEW ###################################
    ###################################################################

    for i in range(0,len(results)):
        output_uncorrected_p_vals[i,branch] = results[i]
ray.shutdown()

################################################################
## do the p-val correction
print('performing BH multiple comparison correction')
for i in range(0,len(branches)):
    output_corrected_p_vals[:,i] = correct_pvalues_for_multiple_testing(output_uncorrected_p_vals[:,i])

from scipy.stats import rankdata
## get enriched

previously_significant=[[] for i in range(len(single_group_lists))]
out_files = []
print('length of previously significant',len(previously_significant))
for branch in range(0,len(branches)):
    print("getting genes for",branch_names[branch])
    b=branches[branch]
    group1_indices = all_group_ids[b[0]]
    group2_indices = all_group_ids[b[1]]

    #dividing_line = len(group1_indices)
    #print(dividing_line)
    ## get significant results
    total_sig_indices = np.where(output_corrected_p_vals[:,branch]<0.05)[0]

    ## remove the genes that were significantly different at a lower branch point
    previously_significant_grp1 = previously_significant[b[0]]
    previously_significant_grp2 = previously_significant[b[1]]

    previously_significant_combined = previously_significant_grp1 + previously_significant_grp2
    previously_significant_combined = list(set(previously_significant_combined))
    previously_significant_combined.sort()
    sig_indices = []
    for i in total_sig_indices:
        if i not in previously_significant_combined:
            sig_indices.append(i)

    print(len(total_sig_indices),'differentially expressed total')
    previously_significant.append(previously_significant_grp1+previously_significant_grp2+sig_indices)
    previously_significant[b[0]]=previously_significant_grp1+previously_significant_grp2+sig_indices
    previously_significant[b[1]]=previously_significant_grp1+previously_significant_grp2+sig_indices


    if True:#31 in b or 14 in b:
        print(previously_significant_grp1[:5])
        print(previously_significant_grp2[:5])
        print(previously_significant_combined[:5])
        print(sig_indices[:5])
    print('group',len(previously_significant)-1)
        

    print('\t',len(sig_indices),'significant differences')
    for i in sig_indices:

        # group1 = full_expression[i,group1_indices]
        # group2 = full_expression[i,group2_indices]
        # group1_mean = np.mean(group1)
        # group2_mean = np.mean(group2)
        # group_merged = rankdata(np.array(group1.tolist()+group2.tolist()))
        # group1_mean = np.mean(group_merged[:dividing_line])
        # group2_mean = np.mean(group_merged[dividing_line:])
        if group1_higher_bool_array[i]:
            #print(i)
            #print(len(ID_list))
            branch_differential_genes[branch][0].append(ID_list[i])
        else:
            branch_differential_genes[branch][1].append(ID_list[i])
    num_grp_1 = len(branch_differential_genes[branch][0])
    num_grp_2 = len(branch_differential_genes[branch][1])
    print('\t\tsig_indices:',sig_indices[:5])
    print('\t\t',b[0],num_grp_1)
    print('\t\t\t',branch_differential_genes[branch][0][:min([num_grp_1,6])],'...')
    print('\t\t',b[1],num_grp_2)
    print('\t\t\t',branch_differential_genes[branch][1][:min([num_grp_2,6])],'...')

    ## write the results to file
    temp_out_dir = args.out_dir+str(b[0])+"_vs_"+str(b[1])+"/"
    cmd('mkdir '+temp_out_dir)
    # write the file for gorup1 of branch point
    temp_out_file1 = temp_out_dir+str(b[0])+'.txt'
    temp_out_file2 = temp_out_dir+str(b[1])+'.txt'
    make_file('\n'.join(branch_differential_genes[branch][0]),temp_out_file1)
    make_file('\n'.join(branch_differential_genes[branch][1]),temp_out_file2)
    out_files.append(temp_out_file1)
    out_files.append(temp_out_file2)




#############################################################
## make some plots
def draw_branches_on_exemplar_only_plot(projection):
    global single_merger_branches
    projection_x = projection[:,0]
    projection_y = projection[:,1]
    for branch in single_merger_branches:
        temp_exemplar1_idx = branch[0]
        temp_exemplar2_idx = branch[1]
        x_vect = [projection_x[temp_exemplar1_idx],projection_x[temp_exemplar2_idx]]
        y_vect = [projection_y[temp_exemplar1_idx],projection_y[temp_exemplar2_idx]]
        plt.plot(x_vect,y_vect,color = 'grey',lw=1.5,linestyle='--')


def plot_lines_to_exemplars(projection_x,projection_y,optimal_centroid_indices, color_vect):
    global single_group_lists, single_merger_branches
    for i in range(0,len(single_group_lists)):
        exemplar_x = projection_x[optimal_centroid_indices[i]]
        exemplar_y = projection_y[optimal_centroid_indices[i]]
        temp_idxs = single_group_lists[i]
        for idx in temp_idxs:
            temp_point_x = projection_x[idx]
            temp_point_y = projection_y[idx]
            plt.plot([temp_point_x,exemplar_x],[temp_point_y,exemplar_y],
                color=color_vect[i],
                lw=0.75)

        for branch in single_merger_branches:
            temp_exemplar1_idx = optimal_centroid_indices[branch[0]]
            temp_exemplar2_idx = optimal_centroid_indices[branch[1]]
            x_vect = [projection_x[temp_exemplar1_idx],projection_x[temp_exemplar2_idx]]
            y_vect = [projection_y[temp_exemplar1_idx],projection_y[temp_exemplar2_idx]]
            plt.plot(x_vect,y_vect,color = 'grey',lw=1.5,linestyle='--')


def draw_plot(plot,exemplars,color_vect,draw_connections_to_exemplars=False):
    global all_group_ids, plt
    plt.clf()
    plt.scatter(plot["x"],plot["y"],
            color=plot["c"],
            s=6)
    plt.xlabel(plot['xlab'])
    plt.ylabel(plot['ylab'])

    if draw_connections_to_exemplars:
        plot_lines_to_exemplars(plot["x"],plot["y"],exemplars,color_vect)

    #plt.show()
    # if out_plot != None:
    #     plt.savefig(temp+out_plot,
    #         dpi=args.dpi,
    #         bbox_inches='tight')

for plot in cluster_result_dict["plots"]:
    # for k in [plot].keys():
    #     print(k)
    #     print(plot[k])
    draw_plot(cluster_result_dict["plots"][plot],cluster_result_dict["exemplar_indices"],cluster_result_dict["color_vect"])
    temp_plot_out = plot.split('/')
    temp_plot_out = temp_plot_out[-1]
    plt.savefig(args.out_dir+temp_plot_out[:-4]+'_cell_type_states.png',
        dpi=600,
        bbox_inches='tight')



################################################
## get the exemplar sub-matrix
exemplar_indices = cluster_result_dict["exemplar_indices"]
exemplar_matrix = np.zeros((np.shape(full_expression)[0],len(exemplar_indices)))

mean_expression_table = read_table(args.mean_expression)
mean_expression_table = np.array(mean_expression_table[1:])
exemplar_matrix = np.array(mean_expression_table[:,1:],dtype=float)

# for i in range(0,len(exemplar_indices)):
#     exemplar_matrix[:,i] += full_expression[:,exemplar_indices[i]]


## run the PCA on just the exmplars
pca_model = PCA(n_components=2)
exemplar_pca_projection = pca_model.fit_transform(np.transpose(exemplar_matrix))

## plot them

plt.clf()
for i in range(0,len(exemplar_indices)):
    plt.scatter(exemplar_pca_projection[i,0],exemplar_pca_projection[i,1],
        color=colors[i],
        label='sample_group_'+str(i),
        s=pr[i]*1000)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

draw_branches_on_exemplar_only_plot(exemplar_pca_projection)
plt.savefig(args.out_dir+temp_plot_out[:-4]+'_.png',
            dpi=600,
            bbox_inches='tight')

def plot_2d(projection,out_plot,x_ax = '',y_ax = ''):
    global id_hash, sample_k_lists, colors, args, ax, plt
    plt.clf()
    for i in range(0,len(sample_k_lists)):
        temp_idxs = ids_to_idxs(sample_k_lists[i])
        plt.scatter(projection[temp_idxs,0],projection[temp_idxs,1],
            label='sample_group_'+str(i),
            color=colors[i],
            s=args.point_size)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(x_ax)
    plt.ylabel(y_ax)
    if out_plot != None:
        plt.savefig(temp+out_plot,
            dpi=args.dpi,
            bbox_inches='tight')

    ## get the full color vector
    out_color = np.zeros((len(list(id_hash.keys())),4))
    #print(np.shape(out_color))
    for i in range(0,len(sample_k_lists)):
        temp_idxs = ids_to_idxs(sample_k_lists[i])
        #print(colors[i])
        out_color[temp_idxs,:] = colors[i]
        #print(out_color[temp_idxs])
        #sys.exit()
    return({'x':projection[:,0],
        'y':projection[:,1],
        'c':out_color,
        'xlab':x_ax,
        'ylab':y_ax})






###############################################################
## do the pathway analysis

for out_file in out_files:
    print('gProfiler for',out_file)
    gprofile_call = 'pyminer_gprofile.py -i '+out_file+' -s '+args.species
    if args.ID_list != None:
        gprofile_call += ' -b '+args.ID_list
    cmd(gprofile_call)







