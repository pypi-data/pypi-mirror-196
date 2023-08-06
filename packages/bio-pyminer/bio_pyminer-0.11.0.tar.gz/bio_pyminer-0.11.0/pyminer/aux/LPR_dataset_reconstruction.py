import sys
import os
import argparse
import networkx as nx
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
from random import shuffle, seed
import pandas as pd
import seaborn as sns
import sklearn
import pickle
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, LinearRegression
##############################################################
## basic function library
def process_dir(in_dir):
    ## process the output dir
    if in_dir[-1]!='/':
        in_dir+='/'
    if not os.path.isdir(in_dir):
        os.makedirs(in_dir)
    return(in_dir)


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
#########################################################################

def get_all_dirs(in_dir):
    return([dI for dI in os.listdir(in_dir) if os.path.isdir(os.path.join(in_dir,dI))])


def is_good_candidate(candidate_data, biomarker_data):
    ## checks candidate against previous marker to make sure it's not redundant data
    is_good = True
    for i in range(len(biomarker_data)):
        if np.allclose(biomarker_data[i], candidate_data):
            print("found redundant gene")
            is_good = False
    return(is_good)

def get_biomarkers(all_com, com_dict, biomarker_n, norm_array, id_hash):
    final_markers = []
    for com in all_com:
        temp_com_data = com_dict[com]
        temp_genes = temp_com_data[0]
        temp_lpr = temp_com_data[1]
        marker_genes = [temp_genes[0]]
        marker_lpr = [temp_lpr[0]]
        biomarker_data = [norm_array[id_hash[temp_genes[0]],:]]
        print('getting biomarkers of:',com)
        for i in range(1,len(temp_lpr)):
            if len(marker_genes) == biomarker_n:
                break
            candidate_gene = temp_genes[i]
            candidate_data = norm_array[id_hash[candidate_gene],:]
            if is_good_candidate(candidate_data, biomarker_data):
                marker_genes.append(candidate_gene)
                biomarker_data.append(candidate_data)
                marker_lpr.append(temp_lpr[i])
        for marker in marker_genes:
            final_markers.append(marker)
            print(marker)
    return(final_markers)


def get_lpr_biomarkers(lpr_table, biomarker_n, norm_array, id_hash):
    ## log all of the communities and their members
    com_dict = {}
    for i in range(len(lpr_table)):
        ## go through all of the lines in the input table (post-filtering)
        temp_gene = lpr_table[i][0]
        temp_com = lpr_table[i][1]
        temp_lpr = lpr_table[i][2]
        temp_pr = lpr_table[i][3]
        if temp_com not in com_dict:
            ## set up the community lists we haven't gotten to this community yet
            print('\tsetting up',temp_com)
            ## gene, lpr, pr
            com_dict[temp_com] = [[],[],[]]
        temp_com_entry = com_dict[temp_com]
        ## append the new entries
        temp_com_entry[0].append(temp_gene)
        temp_com_entry[1].append(temp_lpr)
        temp_com_entry[2].append(temp_pr)
    print("sorting them by lpr")
    all_com = sorted(list(set(com_dict.keys())))
    for com in all_com:
        ## get the sorted order
        temp_com_data = com_dict[com]
        new_order = list(np.argsort(np.array(temp_com_data[1])))[::-1]
        print('\t',com)
        #print('\t\t',max(temp_com_data[1]))
        for i in range(0,len(temp_com_data)):
            temp_com_data[i] = np.array(temp_com_data[i])
            temp_com_data[i] = temp_com_data[i][new_order]
    return(get_biomarkers(all_com, com_dict, biomarker_n, norm_array, id_hash))


def get_min_max_norm(data_array):
    print('normalizing array')
    min_vect = np.min(data_array, axis = 1)
    data_array -= np.transpose(np.array([min_vect]))
    max_post_min = np.max(data_array, axis = 1)
    data_array /= np.transpose(np.array([max_post_min]))
    return(min_vect, max_post_min, data_array)


def fit_model(Xs, Ys, verbose = True):
    #temp_model = SVR(kernel = 'linear')
    #temp_model = Ridge(alpha = 0.1)
    temp_model = LinearRegression()
    temp_model.fit(Xs, Ys)
    if verbose:
        print('\tpred:  ', temp_model.score(Xs, Ys))
        # print('\tpred:  ', temp_model.predict(Xs))
        # print('\tactual:',Ys)
    return(temp_model)


def build_model(temp_gene, biomarkers, id_list, id_hash, norm_array):
    #print(temp_gene)
    y_array = norm_array[id_hash[temp_gene],:]
    biomarker_x_idxs = [id_hash[x] for x in biomarkers]
    x_array = np.zeros((len(biomarker_x_idxs),norm_array.shape[1]))
    for i in range(len(biomarker_x_idxs)):
        mark_idx = biomarker_x_idxs[i]
        x_array[i,:] = norm_array[mark_idx,:]
    x_array = np.transpose(x_array)
    y_array = np.transpose(y_array)
    model = fit_model(x_array, y_array)#x_array[:,0])
    return(model)



def get_model(lpr_table, out_dir, data_file, biomarker_n = 1):
    ## read in the data file
    in_table = read_table(data_file)
    sample_names = in_table[0][1:]
    data_array = np.zeros((len(in_table)-1,len(sample_names)))
    id_list = []
    for i in range(1,len(in_table)):
        id_list.append(in_table[i][0])
        data_array[i-1,:] = in_table[i][1:]
    id_hash = {value:key for key, value in enumerate(id_list)}
    ## get the min_max norm & keep the stats for normalizing a hold-out
    min_vect, max_vect, norm_array = get_min_max_norm(data_array)
    ## read the LPR file
    lpr_table = read_table(lpr_table)[1:]## cut off the header
    ## to save time, we'll give the ax to everything that has 0 LPR
    working_lpr_table = []
    for i in range(0,len(lpr_table)):
        if lpr_table[i][2] != 0.:
            working_lpr_table.append(lpr_table[i])
    ## get the biomarkers
    biomarker_ids = get_lpr_biomarkers(working_lpr_table, biomarker_n, norm_array, id_hash)
    ## and random IDs for comparison
    id_list_copy = deepcopy(id_list)
    shuffle(id_list_copy)
    random_ids = id_list_copy[:len(biomarker_ids)]
    print(random_ids)
    print(biomarker_ids)
    ## take in the 
    all_models_dict = {}
    random_models_dict = {}
    for i in range(len(id_list)):
        temp_gene = id_list[i]
        print('actual')
        all_models_dict[temp_gene] = {'min':min_vect[i],
                                      'max_post_min':max_vect[i],
                                      'x_genes':biomarker_ids,
                                      'model':build_model(temp_gene, 
                                                          biomarker_ids, 
                                                          id_list, 
                                                          id_hash, 
                                                          norm_array)}
        print('random')
        random_models_dict[temp_gene] = {'min':min_vect[i],
                                         'max_post_min':max_vect[i],
                                         'x_genes':biomarker_ids,
                                         'model':build_model(temp_gene, 
                                                             random_ids, 
                                                             id_list, 
                                                             id_hash, 
                                                             norm_array)}
    return(all_models_dict, random_models_dict, biomarker_ids, random_ids)






#########################################################################
def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-community_table','-com_table',
        help = "The file with the community analysis by PyMINEr.")
    parser.add_argument(
        '-out_dir','-o',
        help = "the output directory")
    parser.add_argument(
        '-input_dataset','-i',
        type = str,
        help = "the sample level Z-scores created by PyMINEr. This is the sample_var_enrichment_Zscore.txt file in the sample_clustering_and_summary directory")
    parser.add_argument(
        '-model_file','-model','-mod','-m',
        type = str,
        help = "If we're using an independent model previously built to test on a hold-out dataset, or to synthesize a new dataset from the markers only.")
    parser.add_argument(
        '-n',
        type = int,
        default = 1,
        help = "the number of unique markers to use for each module.")


    args = parser.parse_args()
    return(args)
#########################################################################

if __name__ == '__main__':
    ## do dodecahedral
    seed(1234567789)
    args = parse_args(sys.argv)
    ## first generate or load the model
    if args.model_file == None:
        model, random_model, biomarkers, random_ids = get_model(lpr_table = args.community_table,
                                                                data_file = args.input_dataset, 
                                                                out_dir = args.out_dir,
                                                                biomarker_n = args.n)
        print('\n\nsaving model!')
        save_dict(model, os.path.join(args.out_dir,'top_'+str(args.n)+'_model.pkl'))
        save_dict(random_model, os.path.join(args.out_dir,'random_'+str(args.n)+'_model.pkl'))
    else:
        model = load_dict(args.model_file)



    
