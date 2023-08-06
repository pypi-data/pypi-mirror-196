#!python
import os
import re
import gc
import ray
import h5py
import psutil
import argparse
import numpy as np
import networkx as nx
from copy import deepcopy
import matplotlib
from matplotlib import pyplot as plt
try:
    from pyminer.common_functions import *
    #from pyminer.pyminer_common_stats_functions import *
    #from pyminer.pyminer_common_stats_functions import no_p_spear, get_Z_cutoff, get_empiric_FPR, get_linear_triangle#, get_empiric_log_odds_FPR
except:
    from common_functions import *
    #from pyminer_common_stats_functions import *
    #from pyminer_common_stats_functions import no_p_spear, get_Z_cutoff, get_empiric_FPR, get_linear_triangle#, get_empiric_log_odds_FPR

##############################################################






def set_atts(G, list_of_na_files=[]):
    if len(list_of_na_files)>0:
        for f in list_of_na_files:
            temp_attr_table = read_table(f)
            for i in range(1,len(temp_attr_table[0])):
                temp_attr_name = temp_attr_table[0][i]
                temp_attr_name = temp_attr_name.replace('/','|')
                print('\nsetting the node attribute:',temp_attr_name,'\n')
                temp_attr_dict = empty_node_dict.copy()
                print(list(temp_attr_dict.keys())[:5])
                for n in range(1,len(temp_attr_table)):
                    temp_node = process_node(temp_attr_table[n][0])
                    if temp_node in temp_attr_dict:
                        temp_attr_dict[temp_node] = temp_attr_table[n][i]
                    else:
                        ## this means that we couldn't find the node from the
                        ## attr list in the graph
                        if args.verbose:
                            print(temp_node,"not in temp_attr_dict")
                        pass
                try:
                    print("temp_attr_name",temp_attr_name)
                    set_node_attributes(G,temp_attr_dict,name = temp_attr_name)
                except:
                    set_node_attributes(G,temp_attr_name,temp_attr_dict)
    return(G)


def extract_name_and_batch_info(cells, G):
    print(cells[:5])
    name_dict = {}
    batch_dict = {}
    for node in G.nodes():
        name_dict[node]=cells[node]
        if "||" in cells[node]:
            temp_batch, temp_bcode = cells[node].split("||")
            batch_dict[node]=temp_batch
    nx.set_node_attributes(G, name_dict, name = "name")
    nx.set_node_attributes(G, batch_dict, name = "batch")
    return(G)


def annotate_clusters(G, cluster_table):
    clust_dict = {row:"cluster_"+str(int(cluster_table[row][1])) for row in G.nodes()}
    nx.set_node_attributes(G, clust_dict, "cluster")
    return(G)


def update_spectral(pos, clust_dict):
    #print(clust_dict)
    all_clust = sorted(list(set(clust_dict.values())))
    #print(all_clust)
    clust_node_dict = {clust:[] for clust in all_clust}
    #print(clust_node_dict)
    clust_pos_dict = {clust:np.zeros((2)) for clust in all_clust}
    #print(clust_pos_dict)
    print("\tlogging")
    for node, clust in  clust_dict.items():
        temp_clust_list = clust_node_dict[clust]
        temp_clust_list.append(node)
        clust_node_dict[clust] = temp_clust_list
        ##
        temp_clust_loc = clust_pos_dict[clust]
        temp_clust_loc = temp_clust_loc + pos[node]
        clust_pos_dict[clust] = temp_clust_loc
    print("\taverageing")
    for clust in all_clust:
        clust_pos_dict[clust] = clust_pos_dict[clust]/len(clust_node_dict[clust])
    print("\tupdating")
    new_pos={node:clust_pos_dict[clust]+(-.5+np.random.random(2))/1e4 for node, clust in clust_dict.items()}
    return(new_pos)


####################################
def get_empty_node_dict(G):
    empty_node_dict = {}
    all_nodes = G.nodes()
    for n in all_nodes:
        empty_node_dict[n]=0
    return(empty_node_dict)


def normalize_PR_dict(pr_dict):
    nodes = list(pr_dict.keys())
    original_pr = []
    for node in nodes:
        original_pr.append(pr_dict[node])
    original_pr_array = np.array(original_pr)
    original_pr_array = original_pr_array - np.min(original_pr_array)
    original_pr_array = original_pr_array / np.max(original_pr_array)
    norm_pr_dict = {}
    for i in range(0,len(nodes)):
        node = nodes[i]
        norm_pr_dict[node] = original_pr_array[i]
    return(norm_pr_dict)


def get_LPR(G, community_dict):
    ## takes in a graph, and it's partitions.
    ## Returns the dictionary of local page ranks
    ## calculate within community page-rank
    print('finding Local PageRank (LPR)')
    LPR_dict = get_empty_node_dict(G)
    all_nodes = list(LPR_dict.keys())
    ## get the list of all unique communities
    all_com_list = set(community_dict.values())
    #print(list(community_dict.keys()))
    all_com_dict = {com:[] for com in all_com_list}
    for node in all_nodes:
        temp_com = community_dict[node]
        temp_node_list = all_com_dict[temp_com]
        temp_node_list.append(node)
        all_com_dict[temp_com] = temp_node_list
    for com in all_com_list:
        temp_nodes = all_com_dict[com]
        if len(temp_nodes)>=5:
            temp_subgraph = G.subgraph(temp_nodes)
            temp_pr_dict = nx.pagerank(temp_subgraph)
            ## now normalize it within this community
            temp_pr_dict = normalize_PR_dict(temp_pr_dict)
            for node in temp_pr_dict.keys():
                LPR_dict[node] = temp_pr_dict[node]
                #print(node,temp_pr_dict[node])
    return(LPR_dict)


####################################


# from  sklearn.decomposition import SparsePCA as PCA
# pca = PCA(n_components=2)
# principalComponents = pca.fit_transform(nx.laplacian_matrix(G).toarray())

@ray.remote
def ray_bellman_ford(G, start_idxs, end_idxs, my_idxs):
    all_out_paths = []
    for idx in my_idxs:
        start = start_idxs[idx]
        end = end_idxs[idx]
        try:
            temp_paths = nx.bellman_ford_path(G, start, end, weight="inverse_weight")
        except:
            temp_paths = []
        print(temp_paths, start, end)
        all_out_paths+=temp_paths
    return(all_out_paths)


@ray.remote
def ray_get_pos(seed_pos, connected_subgraph):
    print("getting initial subgraph kamada_kawai locations")
    temp_pos = nx.drawing.layout.kamada_kawai_layout(connected_subgraph)
    #seed_pos = nx.drawing.layout.random_layout(G)
    for node, node_pos in temp_pos.items():
        seed_pos[node]=node_pos
    return(seed_pos)


def get_LPR_connected_paths(G, clust_node_dict, pos_iters = 4, threads = 6):
    gc.enable()
    clust_dict = nx.get_node_attributes(G, "cluster")
    lpr_dict = nx.get_node_attributes(G, "LPR")
    most_central_nodes = []
    central_node_dict = {}
    print("getting highest LPR node per cluster")
    for clust in sorted(list(clust_node_dict.keys())):
        temp_clust_nodes = nodesAt5 = [x for x,y in G.nodes(data=True) if y['cluster']==clust]
        temp_lpr_dict = nx.get_node_attributes(G.subgraph(temp_clust_nodes),"LPR")
        temp_high_lpr = -9999
        temp_high_node = None
        for node, lpr in temp_lpr_dict.items():
            if lpr > temp_high_lpr:
                temp_high_lpr=lpr
                temp_high_node = node
        if temp_high_node is None:
            print("\n"*10)
            print(temp_lpr_dict.items())
            print("\nnot sure what happened here...\n\n\n")
        most_central_nodes.append(temp_high_node)
        central_node_dict[clust]=temp_high_node
    all_paths = []
    start_node_list = []
    end_node_list = []
    for i in range(len(most_central_nodes)):
        for j in range(i,len(most_central_nodes)):
            if j!=i:
                start_node_list.append(most_central_nodes[i])
                end_node_list.append(most_central_nodes[j])
                #print(most_central_nodes[i], most_central_nodes[j])
                # try:
                #     temp_paths = nx.bellman_ford_path(G, most_central_nodes[i], most_central_nodes[j], weight="inverse_weight")
                # except:
                #     temp_paths = []
                # print(temp_paths)
                # all_paths += temp_paths
    #############################
    print("getting bellman_ford_paths in parallel")
    ray.init()
    ray_calls = []
    all_idxs = get_indices(threads, len(start_node_list))
    print(all_idxs)
    G_ray=ray.put(G)
    for i in range(len(all_idxs)):
        if all_idxs[i]!=[]:
            ray_calls.append(ray_bellman_ford.remote(G_ray, start_node_list, end_node_list, all_idxs[i]))
    print("\tinitializing ray calls")
    ray_out = ray.get(ray_calls)
    ray.shutdown()## this is just to liberate the G_ray obj
    gc.collect()
    all_paths = []
    for line in ray_out:
        all_paths += line
    all_paths = list(set(all_paths))
    #############################
    final_connected_nodes = list(set(all_paths))
    print(len(final_connected_nodes)," nodes in connected subgraph")
    connected_subgraph = G.subgraph(final_connected_nodes)
    # sub_g_orig = deepcopy(connected_subgraph)
    # G_original = deepcopy(G)
    pos_list = []
    #ray_connected_subgraph = ray.put(deepcopy(connected_subgraph))
    ray.init()
    ray_calls = []
    for i in range(pos_iters):
        ray_calls.append(ray_get_pos.remote(nx.drawing.layout.random_layout(G), deepcopy(connected_subgraph)))
    pos_list = ray.get(ray_calls)
    ray.shutdown()
    gc.collect()
    for i in range(len(pos_list)):
        print("getting spring embedding from initialized seeds:",i)
        pos_list[i]=nx.drawing.layout.spring_layout(G, pos = pos_list[i])
    # for temp_iter in range(pos_iters):
    #     G = deepcopy(G_original)
    #     connected_subgraph = deepcopy(connected_subgraph)
    #     temp_pos = nx.drawing.layout.kamada_kawai_layout(connected_subgraph)#kamada_kawai_layout(connected_subgraph)
    #     # seed_pos = {node:np.zeros(2) for node in clust_dict.keys()}
    #     # for node in clust_dict.keys():
    #     #     seed_pos[node]=temp_pos[central_node_dict[clust_dict[node]]]+((-.5+np.random.random(2)))
    #     seed_pos = nx.drawing.layout.random_layout(G)
    #     for node, node_pos in temp_pos.items():
    #         seed_pos[node]=node_pos
    #     print("getting spring embedding from initialized seeds")
    #     #nx.laplacian_matrix(G)
    #     pos_list.append(nx.drawing.layout.spring_layout(G, pos = seed_pos))#, fixed = list(temp_pos.keys()))
        # out_graph_plot = nx.draw(connected_subgraph,
        #                          pos2, 
        #                          node_shape = 'o', 
        #                          linewidths = 0, 
        #                          node_size = 10, 
        #                          node_color = get_color_from_var(connected_subgraph, nx.get_node_attributes(connected_subgraph,"cluster")),
        #                          width = 0.00156828259937327, 
        #                          #edge_color = "silver",
        #                          font_size=0)
        # plt.show()
    ###################################3
    for i in range(len(pos_list)):
        nx.set_node_attributes(G, pos_list[i], name = "pos_"+str(i))
    ## want to add this
    cluster_LPR_center = {node:False for node in G.nodes()}
    for node in G.nodes():
        if node in most_central_nodes:
            cluster_LPR_center[node]=True
    nx.set_node_attributes(G, cluster_LPR_center, name = "cluster_LPR_center")
    ## and the sub_graph attr too
    in_best_connected_subgraph = {node:False for node in G.nodes()}
    for node in connected_subgraph.nodes():
        in_best_connected_subgraph[node]=True
    nx.set_node_attributes(G, in_best_connected_subgraph, name = "in_best_connected_subgraph")
    for i in range(len(pos_list)):
        nx.set_node_attributes(G, pos_list[i], name = "pos_"+str(i))
    ####################################
    #return(pos_list)
    return(G)




def get_weighted_cluster_paths(G, clust_dict, pos_iters=4):
    #print(clust_dict)
    all_clust = sorted(list(set(clust_dict.values())))
    #print(all_clust)
    clust_node_dict = {clust:[] for clust in all_clust}
    print("\tlogging")
    for node, clust in  clust_dict.items():
        temp_clust_list = clust_node_dict[clust]
        temp_clust_list.append(node)
        clust_node_dict[clust] = temp_clust_list
    #########
    nx.set_node_attributes(G, get_LPR(G, clust_dict), name="LPR")
    ## get the weighted shortest paths connecting the most central nodes
    #pos_list = get_LPR_connected_paths(G, clust_node_dict, pos_iters=pos_iters)
    #return(pos_list)
    G = get_LPR_connected_paths(G, clust_node_dict, pos_iters=pos_iters)
    return(G)
    





def get_pos(G,pos_iters=4, cutoff=0.0):
    if not check_if_pos_iters_exist(G, pos_iters):
        weights = nx.get_edge_attributes(G,"weight")
        new_weights = {key:value for key, value in weights.items()}
        nx.set_edge_attributes(G, new_weights, name="weight")
        inverse_weights = {key:(1-value) for key, value in weights.items()}
        nx.set_edge_attributes(G, inverse_weights, name="inverse_weight")
        clust_dict = nx.get_node_attributes(G, "cluster")
        ########################################
        G = get_weighted_cluster_paths(G, clust_dict, pos_iters=pos_iters)
        ########################################
    return(G)




#############################################################
#############################################################



def get_color_from_var(G, in_attr_dict, filter_for_nodes=None):
    if is_categorical(in_attr_dict):
        return(get_vals_from_dict(G, get_color_from_cat(in_attr_dict), filter_for_nodes=filter_for_nodes) )#, plt.get_cmap('gist_rainbow') ) )
    else:
        return(get_vals_from_dict(G, get_color_from_float(in_attr_dict),  filter_for_nodes=filter_for_nodes))


def get_vals_from_dict(G, val_map, filter_for_nodes=None):
    if filter_for_nodes is None:
        vals = [val_map[node] for node in G.nodes()]
    else:
        vals = [val_map[node] for node in G.nodes() if node in filter_for_nodes]
    return(vals)


def get_color_from_cat(in_attr_dict):
    all_vals = []
    for n in sorted(list(in_attr_dict.keys())):
        all_vals.append(in_attr_dict[n])
    unique_entries = sorted(list(set(all_vals)))
    num_vars = len(unique_entries)
    cat_to_float_dict = {}
    for entry in enumerate(unique_entries):
        cat_to_float_dict[entry[1]]=entry[0]/(num_vars)
    ## update the in_attr_dict to be float rather than cat
    for n in in_attr_dict.keys():
        in_attr_dict[n]=cat_to_float_dict[in_attr_dict[n]]
    return(get_color_from_float(in_attr_dict))


def is_categorical(in_attr_dict):
    ## first we need to figure out if it's a float or a categorical variable
    ## the first sign that we have a categorical var is if there are strings
    ## in the attribute dict
    is_categorical_bool = False
    all_vals = []
    for n in in_attr_dict.keys():
        all_vals.append(in_attr_dict[n])
        if type(in_attr_dict[n]) == str:
            is_categorical_bool = True
    ## no we can check how variant the vector is
    ## if there are not that many unique values compared to the number of nodes
    ## then it's probably categorical
    ## by default this is set to 10%
    #num_unique = len(list(set(all_vals)))
    #if number_of_nodes(G)/10 > num_unique:
    #    is_categorical_bool = True
    return(is_categorical_bool)


def get_color_from_float(in_attr_dict, min_express=0, max_express=1):
    if min_express != None:
        # print('setting mins to:',min_express)
        # print('setting maxs to:',max_express)
        for n in in_attr_dict.keys():
            if in_attr_dict[n] > max_express:
                #print('setting',in_attr_dict[n],'to',max_express)
                in_attr_dict[n] = max_express
            elif in_attr_dict[n] < min_express:
                #print('setting',in_attr_dict[n],'to',min_express)
                in_attr_dict[n] = min_express
            else:
                pass
    #### do linear normalization between 0 and 1
    ## get the min
    temp_min = None
    for n in in_attr_dict.keys():
        #print(n)
        #print('temp_min',temp_min)
        if temp_min == None:
            temp_min = in_attr_dict[n]
        else:
            if temp_min > in_attr_dict[n]:
                temp_min = in_attr_dict[n]
                #print('temp_min',temp_min)
            else:
                pass
    ## subtract min
    #print('temp_min',temp_min)
    for n in in_attr_dict.keys():
        in_attr_dict[n] = in_attr_dict[n]-temp_min
    ## get the max
    temp_max = None
    for n in in_attr_dict.keys():
        #print(n)
        #print('temp_max',temp_max)
        if temp_max == None:
            temp_max = in_attr_dict[n]
            #print('temp_max',temp_max)
        else:
            if temp_max < in_attr_dict[n]:
                temp_max = in_attr_dict[n]
                #print('temp_max',temp_max)
            else:
                pass
    # divide max
    #print('temp_max',temp_max)
    for n in in_attr_dict.keys():
        if temp_max == 0:
            in_attr_dict[n] = 0
        else:
            in_attr_dict[n] = in_attr_dict[n]/temp_max
    return(in_attr_dict)


#####################
## get the names of all attributes
def get_attrs(G):
    if "node" in dir(G):
        for i in iter(G.node.items()):
            first_node = i[1]
            break
    else:
        for i in iter(G.nodes.items()):
            first_node = i[1]
            break
    return(list(first_node.keys()))
#####################

def fix_ids(graph_cells, cells_dict, del_text="_Sum[0-9]*toinf_Count[0-9]*toinf_ds[0-9]*"):
    graph_cells = [re.sub(del_text, "", node) for node in graph_cells]
    out_graph_cells = []
    for temp_cell in graph_cells:
        if temp_cell in cells_dict:
            ## if they're already unified
            out_graph_cells.append(temp_cell)
        else:
            temp_try=re.sub("-", ".", temp_cell)
            if temp_try in cells_dict:
                out_graph_cells.append(temp_try)
            else:
                temp_try = re.sub("\|\|", "||X", temp_cell)
                if temp_try in cells_dict:
                    out_graph_cells.append(temp_try)
                else:
                    temp_try=temp_cell.split(".")
                    temp_try=".".join(temp_try[:-1])
                    temp_try = re.sub("\|\|", "||X", temp_try)
                    if temp_try in cells_dict:
                        out_graph_cells.append(temp_try)
                    else:
                        print("couldn't find:",temp_cell,"--last try:",temp_try)
    return(out_graph_cells)


def get_gene_dict(gene_vect, graph_cells, cells, del_text="_Sum[0-9]*toinf_Count[0-9]*toinf_ds[0-9]*"):
    gene_vect -= np.min(gene_vect)
    gene_vect /= np.max(gene_vect)
    graph_cells = [re.sub(del_text, "", node) for node in graph_cells]
    full_id_list_hash = {value:key for key, value in enumerate(cells)}
    if graph_cells[0] not in full_id_list_hash:
        graph_cells = fix_ids(graph_cells, full_id_list_hash)
    # print(gene_vect)
    # print(graph_cells[:5])
    # print(cells[:5])
    graph_cell_hash = {value:key for key, value in enumerate(graph_cells)}
    out_dict = {}
    for node in graph_cells:
        out_dict[graph_cell_hash[node]]=gene_vect[full_id_list_hash[node]]
    return(out_dict)


#############################################################

def get_cat_cmap():
    temp_colors = 'gist_rainbow'
    temp_cmap=plt.get_cmap(temp_colors)
    return(temp_cmap)

def get_num_cmap():
    # temp_colors = 'gnuplot'
    # temp_cmap=plt.get_cmap(temp_colors)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["dimgray","mediumvioletred","orangered","yellow"])
    temp_cmap=plt.get_cmap(cmap)
    return(temp_cmap)

#############################################################
@ray.remote
def ray_plot(G, pos_str, node_colors, temp_cmap, temp_out_dir, out_file_end, node_size=15, node_subset = None):
    plt.clf()
    edge_width = 1/np.sqrt(nx.number_of_edges(G))
    out_graph_plot = nx.draw(G,
                                 nx.get_node_attributes(G,pos_str), 
                                 node_shape = 'o', 
                                 linewidths = 0, 
                                 node_size = node_size, 
                                 node_color = node_colors,
                                 width = edge_width, 
                                 cmap=get_cat_cmap(),
                                 edgelist=[],
                                 #edge_color = "silver",
                                 font_size=0)
    out_file = os.path.join(temp_out_dir, out_file_end)
    plt.savefig(out_file,dpi=300,bbox_inches='tight')
    plt.clf()
    return

@ray.remote
def ray_draw(**kwargs):
    return(nx.draw(**kwargs))

#############################################################

def get_batch_dict(node_to_batch_dict):
    batch_to_node_list = {}
    for node, batch in node_to_batch_dict.items():
        if batch not in batch_to_node_list:
            batch_to_node_list[batch]=[]
        temp_list = batch_to_node_list[batch]
        temp_list.append(node)
        batch_to_node_list[batch] = temp_list
    return(batch_to_node_list)


def get_pos_min_max(temp_pos):
    min_x = 99999
    max_x = -99999
    min_y = 99999
    max_y = -99999
    for node, location in temp_pos.items():
        if location[0] > max_x:
            max_x = location[0]
        if location[0] < min_x:
            min_x = location[0]
        if location[1] > max_y:
            max_y = location[1]
        if location[1] < min_y:
            min_y = location[1]
    x_delta = (max_x-min_x)*0.025
    y_delta = (max_y-min_y)*0.025
    return(min_x-x_delta, max_x+x_delta, min_y-y_delta, max_y+y_delta)


#############################################################

def get_attrs(G):
    if "node" in dir(G):
        for i in iter(G.node.items()):
            first_node = i[1]
            break
    else:
        for i in iter(G.nodes.items()):
            first_node = i[1]
            break
    all_atts = list(first_node.keys())
    return(all_atts)


def check_if_pos_iters_exist(G, pos_iters):
    all_node_atts = get_attrs(G)
    all_pos_present=True
    for temp_iter in range(pos_iters):
        pos_str = "pos_"+str(temp_iter)
        if pos_str not in all_node_atts:
            print("\tcouldn't find",pos_str)
            all_pos_present=False
    if all_pos_present:
        print("found all the positions!")
        return(True)
    else:
        print("didn't find all the positions, will get them now")
        return(False)


#############################################################

def run_main_cell_plotting(g, 
                           graph_id_list,
                           id_list, 
                           columns, 
                           in_file,
                           cluster_file,
                           hdf5=True,
                           node_atts=[], 
                           plot_genes=[],
                           out_dir=None,
                           pos_iters=4):
    if out_dir is not None:
        graph_pkl_out_file = os.path.join(out_dir, "cell_embed_with_plots.graphpkl")
        if os.path.isfile(graph_pkl_out_file):
            print("loading", graph_pkl_out_file)
            G=import_dict(graph_pkl_out_file)
        else:
            G=import_dict(g)
    else:
        G=import_dict(g)
    in_file = os.path.realpath(in_file)
    if not hdf5:
        in_mat, genes, cells = read_tsv(in_file)
    else:
        f = h5py.File(in_file,'r')
        in_mat = f["infile"]
        genes = read_file(id_list,'lines')
        cells = read_file(columns,'lines')[1:]
    infile_original_dir = get_file_path(in_file)
    graph_cells = read_file(graph_id_list,'lines')[1:]
    ## unify the graph cell ids
    full_id_list_hash = {value:key for key, value in enumerate(cells)}
    graph_cells = fix_ids(graph_cells, full_id_list_hash)
    if len(graph_cells)==0 not in full_id_list_hash:
        print("still didn't unify them")
        print(cells[0])
        return()
    ##
    cluster_table = read_table(cluster_file)
    G = annotate_clusters(G, cluster_table)
    G = extract_name_and_batch_info(graph_cells, G)
    G = get_pos(G, pos_iters=pos_iters)
    G_original = deepcopy(G)
    num_cpus = max([1,psutil.cpu_count(logical=False)-2])
    batch_to_node_list_dict = get_batch_dict(nx.get_node_attributes(G,"batch"))
    all_batches = list(batch_to_node_list_dict.keys())
    print("all batches:",all_batches)
    ## ray_get_indices_from_list
    for pos_iter in range(pos_iters):
        pos_str = "pos_"+str(pos_iter)
        min_x, max_x, min_y, max_y = get_pos_min_max(nx.get_node_attributes(G,pos_str))
        print(pos_str)
        G = deepcopy(G_original)
        if out_dir is not None:
            out_dir = process_dir(out_dir)
            temp_out_dir = process_dir(os.path.join(out_dir,"iter_"+str(pos_iter)))
        node_size = 15
        edge_width = 1/np.sqrt(nx.number_of_edges(G))
        print("\tplotting batch")
        out_graph_plot = nx.draw(G,
                                 nx.get_node_attributes(G,"pos_"+str(pos_iter)), 
                                 node_shape = 'o', 
                                 linewidths = 0, 
                                 node_size = node_size, 
                                 node_color = get_color_from_var(G, nx.get_node_attributes(G,"batch")),
                                 width = edge_width, 
                                 #cmap=get_cat_cmap(),
                                 #edge_color = "silver",
                                 edgelist=[],
                                 font_size=0)
        plt.xlim([min_x, max_x])
        plt.ylim([min_y, max_y])
        if out_dir is None:
            plt.show()
        else:
            out_file = os.path.join(temp_out_dir, "batch.png")
            plt.savefig(out_file,dpi=300,bbox_inches='tight')
            plt.clf()
        print("\tplotting cluster")
        out_graph_plot = nx.draw(G,
                                 nx.get_node_attributes(G,"pos_"+str(pos_iter)), 
                                 node_shape = 'o', 
                                 linewidths = 0, 
                                 node_size = node_size, 
                                 node_color = get_color_from_var(G, nx.get_node_attributes(G,"cluster")),
                                 width = edge_width, 
                                 cmap=get_cat_cmap(),
                                 edgelist=[],
                                 #edge_color = "silver",
                                 font_size=0)
        plt.xlim([min_x, max_x])
        plt.ylim([min_y, max_y])
        if out_dir is None:
            plt.show()
        else:
            out_file = os.path.join(temp_out_dir, "cluster.png")
            plt.savefig(out_file,dpi=300,bbox_inches='tight')
            plt.clf()
        ###############################
        genes = np.array(genes)
        for gene in plot_genes:
            print("\tplotting ",gene)
            idx = np.where(genes==gene)[0]
            full_gene_vect = in_mat[idx,].flatten()
            expression_dict = get_gene_dict(full_gene_vect, graph_cells, cells)
            expression_color_dict = get_color_from_var(G, expression_dict)
            out_graph_plot = nx.draw(G,
                                 nx.get_node_attributes(G,"pos_"+str(pos_iter)), 
                                 node_shape = 'o', 
                                 linewidths = 0, 
                                 node_size = node_size, 
                                 node_color = expression_color_dict,
                                 width = edge_width, 
                                 cmap=get_num_cmap(),
                                 edgelist=[],
                                 #edge_color = "silver",
                                 font_size=0)
            plt.xlim([min_x, max_x])
            plt.ylim([min_y, max_y])
            if out_dir is None:
                plt.show()
            else:
                out_file = os.path.join(temp_out_dir, gene+"_expression.png")
                plt.savefig(out_file,dpi=300,bbox_inches='tight')
                plt.clf()
            ## now do it again for every batch
            for temp_batch in all_batches:
                print("\tplotting",gene,"in",temp_batch)
                out_graph_plot = nx.draw(G,
                                 nx.get_node_attributes(G,"pos_"+str(pos_iter)), 
                                 node_shape = 'o', 
                                 linewidths = 0, 
                                 node_size = node_size, 
                                 node_color = get_color_from_var(G, expression_dict, filter_for_nodes=batch_to_node_list_dict[temp_batch]),
                                 nodelist=batch_to_node_list_dict[temp_batch],
                                 edgelist=[],
                                 width = edge_width, 
                                 cmap=get_num_cmap(),
                                 #edge_color = "silver",
                                 font_size=0)
                plt.xlim([min_x, max_x])
                plt.ylim([min_y, max_y])
                if out_dir is None:
                    plt.show()
                else:
                    out_file = os.path.join(temp_out_dir, gene+"_expression_"+temp_batch+".png")
                    plt.savefig(out_file,dpi=300,bbox_inches='tight')
                    plt.clf()
    ####################################
    if hdf5:
        f.close()
    if out_dir is not None:
        save_dict(G,graph_pkl_out_file)
    return()
    ###############




#############################################################


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-graph",'-g',
        help="if you already have a graph object that was saved by this program, we can just use that instead of recalculating everything",
        type = str)#,
        #default = "/home/scott/bin/sc_norm_bench_v2/data/biologic_datasets/output/different_tissue_no_overlap/sc_vi/sample_clustering_and_summary/cell_embedding.graphpkl")

    parser.add_argument("-graph_cols_ids",'-g_ids',
        help="these are sorted IDs matching the order of the nodes in the graph")#,
        #default = "/home/scott/bin/sc_norm_bench_v2/data/biologic_datasets/output/different_tissue_no_overlap/sc_vi/column_IDs.txt")

    parser.add_argument("-id_list",'-id','-ID','-IDs','-ids', 
        help="these are sorted IDs matching the order of the original input dataset")#,
        #default = "/home/scott/bin/sc_norm_bench_v2/data/biologic_datasets/output/different_tissue_no_overlap/no_correction/ID_list.txt")

    parser.add_argument("-columns","-cols","-col_ids",
        help = "the column IDs of the matrix (for single cell data this is your cells). Note this requores a header line")#,
        #default="/home/scott/bin/sc_norm_bench_v2/data/biologic_datasets/output/different_tissue_no_overlap/no_correction/column_IDs.txt")

    parser.add_argument("-in_file",
        help = "the expression matrix")#,
        #default = "/home/scott/bin/sc_norm_bench_v2/data/biologic_datasets/output/different_tissue_no_overlap/no_correction/normalized_counts_log2.hdf5")

    parser.add_argument("-cluster_file",
        help = "the cluster annotation_file")#,
        #default = "/home/scott/bin/sc_norm_bench_v2/data/biologic_datasets/output/different_tissue_no_overlap/sc_vi/sample_clustering_and_summary/sample_k_means_groups.tsv")

    parser.add_argument("-hdf5",
        help="use this arg if the input is an hdf5 file",
        action="store_true")

    parser.add_argument("-node_atts",
        help = "a node attribute file for plotting",
        nargs="+")

    parser.add_argument("-plot_genes",
        help="the names of any genes that you'd like to plot (these must be exact matches with entries in the id_list)",
        nargs="+")#,
        #default = ["ENSMUSG00000054422","ENSMUSG00000038255"])

    parser.add_argument("-out_dir","-o",
        help = "the output directory",
        default = None)

    parser.add_argument("-pos_iters",
        help="number of iterations to run for different layouts",
        default=4)

    args = parser.parse_args()
    run_main_cell_plotting(g=args.graph, 
                           graph_id_list=args.graph_cols_ids,
                           id_list=args.id_list, 
                           columns=args.columns, 
                           in_file=args.in_file,
                           cluster_file=args.cluster_file,
                           hdf5=args.hdf5,
                           node_atts=args.node_atts, 
                           plot_genes=args.plot_genes,
                           out_dir = args.out_dir,
                           pos_iters = args.pos_iters)



