import math
import h5py
import community
import numpy as np
import networkx as nx
from numpy import linalg
from copy import deepcopy
from gprofiler import GProfiler
from pyminer.common_functions import make_file, cmd, cp

def get_big_spearman(temp_dir, 
                     infile, 
                     ID_list,
                     columns,
                     do_hdf5,
                     usable_indices=None,
                     block_size=5000):
    print(infile)
    print(ID_list)
    euc_call = "mat_to_adj_list.py -time -transpose -hdf5_out -i '"+infile+"'"
    if do_hdf5: 
        euc_call += " -hdf5 -ids "+ID_list
        euc_call += ' -col_ids '+columns
    euc_call += ' -block_size '+str(int(block_size))
    euc_call += ' -rho_dict_dir '+temp_dir+'/sample_clustering_and_summary/rho_dicts/'
    if usable_indices is not None:
        euc_call += ' -row_subset '+temp_dir+'/used_indices.txt'
        usable_indices_str = usable_indices[:]
        make_file('\n'.join(list(map(str,usable_indices_str))),temp_dir+'/used_indices.txt')
    euc_call += " -euclidean_dist "
    cmd(euc_call)
    neg_euc_hdf5_file = temp_dir+"/sample_clustering_and_summary/rho_dicts/neg_euc_dist.hdf5"
    return(neg_euc_hdf5_file)






##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
def group_list_to_sample_k_table(labels, sample_names):
    num_clust = len(list(set(labels)))
    #print(labels)
    #print(len(labels))
    #sys.exit()
    f_list = None
    #print(dir(af))
    sample_k_table = []
    for i in range(0,len(sample_names)):
        sample_k_table.append([sample_names[i],labels[i]])
    sample_k_lists = []
    for i in range(num_clust):
        sample_k_lists.append([])
    #print(sample_k_lists)
    for i in range(0,len(sample_names)):
        sample_k_lists[labels[i]].append(sample_names[i])
    return(sample_k_table, sample_k_lists)


def sample_k_lists_to_cluster_indices(sample_k_lists, sample_id_hash):
    cluster_indices = []
    for i in range(0,len(sample_k_lists)):
        cluster_indices.append(sorted([sample_id_hash[k] for k in sample_k_lists[i]]))
        #print(i,len(cluster_indices[-1]))
    return(cluster_indices)


def get_weighted_medoid_dist_mat(center_indices, in_mat=None, in_h5=None, max_connections = 2):
    if in_mat is None and in_h5 is not None:
        f=h5py.File(in_h5,'r')
        in_mat=f["infile"]
    n_cols = len(center_indices)
    medoid_dist_mat = np.zeros((in_mat.shape[0],n_cols))
    for i in range(len(center_indices)):
        ## this is negative log2(sq_euc), so undo the log & square again
        medoid_dist_mat[:,i]=(2**(-1*in_mat[:,center_indices[i]]))
    print("sq euc dist")
    print(medoid_dist_mat)
    ## inverse sq euc dist
    medoid_dist_mat=1/medoid_dist_mat
    print("inverse sq euc dist")
    print(medoid_dist_mat)
    rowsums = np.sum(medoid_dist_mat,axis=1)
    print(rowsums.shape)
    print("relative inverse sq euc dist")
    medoid_dist_mat=medoid_dist_mat/rowsums[:,None]
    print(medoid_dist_mat)
    for i in range(medoid_dist_mat.shape[0]):
        temp_max = max(medoid_dist_mat[i,:])
        medoid_dist_mat[np.where(medoid_dist_mat[i,:]<temp_max)]=0
        medoid_dist_mat[np.where(medoid_dist_mat[i,:]==temp_max)]=1
    #medoid_dist_mat=1-medoid_dist_mat
    #rowsums = np.sum(medoid_dist_mat,axis=1)
    #print(medoid_dist_mat)
    #print(rowsums)
    #medoid_dist_mat=medoid_dist_mat/rowsums[:,None]
    if in_h5 is not None:
        f.close()
    return(medoid_dist_mat)


# f.close()
# weighted_medoid_mat = get_weighted_medoid_dist_mat(clust_res.cluster_centers_indices_,
#                                                        in_h5=neg_euc_hdf5_file)

# sns.distplot(np.max(weighted_medoid_mat,axis = 1))
# plt.show()
# sns.distplot(np.std(weighted_medoid_mat,axis = 1))
# plt.show()


def rm_go_terms(genes, species):
    mitochondrial = ["GO:0044429","GO:0006390","GO:0005739","GO:0005743",
                     "GO:0070125","GO:0070126","GO:0005759","GO:0032543",
                     "GO:0044455","GO:0005761"]
    ribosome = ["GO:0005840","GO:0003735","GO:0022626","GO:0044391","GO:0006614",
                "GO:0006613","GO:0045047","GO:0000184","GO:0043043","GO:0006413",
                "GO:0022613","GO:0043604","GO:0015934","GO:0006415","GO:0015935",
                "GO:0072599","GO:0071826","GO:0042254","GO:0042273","GO:0042274",
                "GO:0006364","GO:0022618","GO:0005730","GO:0005791","GO:0098554",
                "GO:0019843"]
    ribo_mito_go = mitochondrial + ribosome
    gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)
    #results = gp.gconvert(ribo_mito_go,organism="hsapiens", target="ENSG")
    results = gp.gconvert(ribo_mito_go,organism=species, target="ENSG")
    ref_genes = gp.gconvert(genes, organism=species, target="ENSG")
    ## first go to the annotation file, and read that in.
    if args.species == 'mmusculus':
        if os.path.isfile(infile_original_dir+'annotations.tsv'):
            annotations = read_table(infile_original_dir+'annotations.tsv')
            ensg_idx = 3
    else:
        if os.path.isfile(infile_original_dir+'human_orthologues.tsv'):
            annotations = read_table(infile_original_dir+'human_orthologues.tsv')
            ensg_idx = 4
    ## catelogue the results
    ensg_mito_ribo_dict=process_dict(results,3)
    # if args.species!="hsapiens":
    #     ensg_mito_ribo_dict = convert_dict_to_dict(all_mito_ribo_genes,)
    all_mito_ribo_genes = list(ensg_mito_ribo_dict.keys())
    print('\tfound',len(all_mito_ribo_genes),'mito or ribo genes')
    print('\t\t',all_mito_ribo_genes[:3])
    final_clust_gene_ids = []
    final_clust_gene_idxs = []
    for i in range(1,len(annotations)):
        temp_gene = annotations[i][ensg_idx]
        #temp_idx = clust_gene_idxs[i]
        if quick_search(ensg_mito_ribo_dict,temp_gene):
            pass
            #print('\texcluding:',annotations[i][1])
            ## here we don't include the mito and ribo genes in the final list
        else:
            # temp_original_id = str(annotations[i][1]).replace("ENTREZGENE_ACC:","")
            # print(temp_original_id)
            # if args.species != "hsapiens":
            #     pass
            # if quick_search(usable_id_hash,temp_original_id):
            #     final_clust_gene_ids.append(temp_original_id)
            #     final_clust_gene_idxs.append(id_hash[temp_original_id])
            # else:
            if int(annotations[i][0])-1 in usable_indices:
                #print("\tproblem mapping",temp_original_id,"but we'll include it")
                final_clust_gene_ids.append(ID_list[int(annotations[i][0])-1])
                final_clust_gene_idxs.append(int(annotations[i][0])-1)
    clust_gene_ids = list(set(final_clust_gene_ids))
    clust_gene_idxs = list(set(final_clust_gene_idxs))
    usable_indices = clust_gene_idxs
    return(usable_indices)



############################################################################################################################
class louvain_clust_object():
    def __init__(self, affinity, labels, sample_names):
        self.affinity_matrix_ = affinity
        self.labels_ = labels
        self.sample_k_table, self.sample_k_lists = group_list_to_sample_k_table(labels, sample_names)
        self.cluster_indices = sample_k_lists_to_cluster_indices(self.sample_k_lists, {value:key for key, value in enumerate(sample_names)})
        self.cluster_centers_indices_= []
        self.cluster_centers_ =  []
        self.get_cluster_center_indices()
    def get_cluster_center_indices(self):
        #print(self.cluster_indices)
        for i in range(len(self.cluster_indices)):
            temp_indices = np.array(self.cluster_indices[i])
            temp_indices = np.array(sorted(temp_indices.tolist()),dtype=int)
            temp_subset = self.affinity_matrix_[temp_indices,:]
            temp_subset = temp_subset[:,temp_indices]
            temp_sum = np.sum(self.affinity_matrix_[temp_indices,:],axis = 1)
            print(temp_sum)
            temp_center_index = np.argmax(temp_sum)
            print(temp_center_index)
            temp_center = temp_indices[temp_center_index]
            self.cluster_centers_indices_.append(temp_center)
            print("\t\tnew cluster center:",self.cluster_centers_indices_[-1])
        self.cluster_centers_ = np.zeros((len(self.cluster_centers_indices_),self.affinity_matrix_.shape[1]))
        for i in range(len(self.cluster_centers_)):
            #print(self.cluster_centers_indices_[i])
            self.cluster_centers_[i,:]=self.affinity_matrix_[self.cluster_centers_indices_[i],:]
        #self.cluster_centers_ = np.array(self.affinity_matrix_[self.cluster_centers_indices_])


############################################################################################################################
def normalize_subset_of_am(am_subset,temp_global_nan_min,temp_global_nan_max,percentile,offset=0,epsilon=1e-10, expected_neighbors=200):
    if abs(temp_global_nan_min)>abs(temp_global_nan_max):
        ## it's an affinity matrix, so we'll multiply by -1
        print("looks like an affinity matrix; we'll mult by -1 to make them positive distances")
        print("original mat:",am_subset[:,:])
        am_subset[:,:] *= -1
        old_min = deepcopy(temp_global_nan_min)
        old_max = deepcopy(temp_global_nan_max)
        temp_global_nan_min = deepcopy(old_max) * -1
        temp_global_nan_max = deepcopy(old_min) * -1
    ## from here on we have a normal Euclidean distance matrix
    print("\tcurrent matrix:",am_subset[:,:])
    print("\ttemp_global_nan_min",temp_global_nan_min)
    print("\ttemp_global_nan_max",temp_global_nan_max)
    #print("\tnumber of infinites:",np.sum(np.isinf(am_subset[:,:])))
    #### subtract the global min.
    ## This gets a Euc mat that has the lowest value equal to the nearest distance
    #### Add one & inverse
    ## This gets us the inverted Euc dist mat where 1 is equivalent to closest distance in the whole matrix
    ## Then the rest is simply inversely proportional to the Euclidean distance 
    am_subset[:,:] = 1/((am_subset[:,:]-temp_global_nan_min)+1)
    #print(am_subset[:,:])
    print("\tnanmin:",np.nanmin(am_subset[:,:]))
    print("\tnanmax:",np.nanmax(am_subset[:,:]))
    ## need to add a little bit of noise to prevent univariate distributions & things getting messed up from ties
    temp_noise_offset = np.random.random(am_subset[:,:].shape)*epsilon
    temp_noise_offset+=np.min(temp_noise_offset)
    am_subset[:,:]+=temp_noise_offset[:,:]
    ## now calculate the cutoff to use
    cutoff = np.nanpercentile(am_subset[:,:], (percentile)*100, axis = 1)-epsilon
    print("\tusing cutoff of:",cutoff)
    ## func3
    for i in range(am_subset.shape[0]):
        passing_idxs = np.where(am_subset[i,:] > cutoff[i])[0]
        if len(passing_idxs)>expected_neighbors:
            ## TODO - haven't run into this yet, but could be a problem
            ## in this case, there was likely a lot of ties for the most similar
            ## So in this case, we just have to pick some at random to keep
            ## but could be worth experimenting with log squared euclidean distances
            ## in the future in case this is actually floating point errors
            #print("got some ties for similarities")
            num_to_drop = len(passing_idxs)-expected_neighbors
            #print(len(passing_idxs),"passing, need to drop:",num_to_drop)
            #sample_idxs_to_drop
            #print(am_subset[i,:])
        elif len(passing_idxs)==0:
            ## if there are a ton of ties at the top, then the top X percentile 
            ## could all be equal to the cutoff, so that when you subtract it, there's nothing left
            ## Only one dataset ever has had this... Strange, but we should be ready and account for it
            # print("nothing passed:")
            # print("need to reset the cutoff")
            # print("nanmax:",np.nanmax(am_subset[i,:]))
            # print("original_cutoff:",cutoff[i])
            temp_max = np.nanmax(am_subset[i,:])
            max_idxs = np.where(am_subset[i,:]==temp_max)[0]
            am_subset[i,:]=0
            am_subset[i,max_idxs]=temp_max
            equal_to_max_vals = am_subset[i,max_idxs]
            # print("max_vals:",equal_to_max_vals)
            # print("cutoff:",cutoff[i])
            # print(equal_to_max_vals>cutoff[i])
            # print(equal_to_max_vals-cutoff[i])
            print(am_subset[i,:])
        else:
            am_subset[i,:]-=cutoff[i]
        #am_subset[i,:]-=cutoff[i]
    # print("number of passing idxs")
    # print(np.sum(am_subset[:,:]>0,axis=1))
    # print(np.min(np.sum(am_subset[:,:]>0,axis=1)))
    am_subset[am_subset[:,:]<0] = 0
    # print("number of passing idxs")
    # print(np.sum(am_subset[:,:]>0,axis=1))
    # print(np.min(np.sum(am_subset[:,:]>0,axis=1)))
    ## set the 'diagonal' to zero since this shouldn't be included in the maximum calculation
    for i in range(am_subset.shape[0]):
        am_subset[i,i+offset]=0
    #####
    # print("number of passing idxs")
    # print(np.sum(am_subset[:,:]>0,axis=1))
    # print(np.min(np.sum(am_subset[:,:]>0,axis=1)))
    temp_max = np.nanmax(am_subset[:,:],axis=1)
    for i in range(am_subset.shape[0]):
        if temp_max[i]==0:
            print("temp_max is zero..")
            print(np.nanmax(am_subset[i,:]))
        idxs_equal_to_temp_max = np.where(am_subset[i,:]>=temp_max[i])[0]
        num_ge_max = len(idxs_equal_to_temp_max)
        if num_ge_max>expected_neighbors:
            pass
            #print("WARNING: it appears as though we had some ties for similarity:",num_ge_max, temp_max[i])
            #print(am_subset[i,idxs_equal_to_temp_max])
            #print(am_subset[i,:])
        ## it's strange, but is theoretically possible that there could be ties, so we'll handle that
        am_subset[i,:] /= temp_max[i]
    ## set the 'diagonal' to zero
    for i in range(am_subset.shape[0]):
        am_subset[i,i+offset]=0
    #print("final subset")
    #print(am_subset[:,:])
    return(am_subset)

def make_symmetric(am):
    am[:,:] = am[:,:]+np.transpose(am[:,:])
    am[:,:] /= 2
    return(am)


def normalize_am(am, percentile, min_neighbors = 5, global_percentile = False):
    ## First convert the eye to nans
    temp_global_nan_min = 99999999999999
    temp_global_nan_max = -99999999999999
    total_vars = am.shape[0]
    percentile = min([percentile,1-(min_neighbors/total_vars)])
    expected_neighbors = math.ceil(total_vars*(1-percentile))
    print("\neach cell will have",expected_neighbors,"neighbors\n")
    print('input matrix shape:',am.shape)
    print("\tfinding global min")
    print(am[:,:])
    for i in range(am.shape[0]):
        if i%10000==0 and i!=0:
            print('\t\t',round(100*i/am.shape[0],2),"%")
        am[i,i]=np.nan
        temp_local_min = np.nanmin(am[i,:])
        temp_local_max = np.nanmax(am[i,:])
        temp_global_nan_min = min([temp_local_min,temp_global_nan_min])
        temp_global_nan_max = max([temp_local_max,temp_global_nan_max])
    print("temp_global_nan_min:",temp_global_nan_min)
    print("temp_global_nan_max:",temp_global_nan_max)
    #print("normalizing to min")
    print("\tnormalizing affinity matrix")
    counter=0
    interval = 10000
    while counter+interval< am.shape[0]:
        print("\t\t",round((counter+interval)/am.shape[0]*100,2),"%")
        #########
        ## func2
        am[counter:(counter+interval),:] = normalize_subset_of_am(np.array(am[counter:(counter+interval),:]),temp_global_nan_min,temp_global_nan_max,percentile,offset=counter, expected_neighbors=expected_neighbors)
        counter+=interval
    am[counter:,:] = normalize_subset_of_am(np.array(am[counter:,:]),temp_global_nan_min,temp_global_nan_max,percentile,offset=counter, expected_neighbors=expected_neighbors)
    print("\tfinal network matrix:")
    print(am)
    return(am)


def get_current_edges(cur_row, cur_index,epsilon=1e-10):
    cur_row = np.array(cur_row)
    indices = np.where(cur_row != 0)[0]
    all_edges = []
    for index in indices:
        #if index > cur_index:
        if not np.isnan(cur_row[index]):
            all_edges.append((cur_index,index,{"weight":cur_row[index]}))
        else:
            all_edges.append((cur_index,index,{"weight":epsilon}))
    return(all_edges)


def do_louvain_primary_clustering(am, 
                                  sample_names,
                                  percentile = 0.95, 
                                  flexible_percentile = True, 
                                  flexible_cap = 200, 
                                  comp_length_cutoff = 4, 
                                  out_dir = None,
                                  resolution=1.0):
    """
    Takes in the full affinity matrix and performs louvain modularity on it.
    Percentile is the the X percentile of affinities to 
    """
    # cur_vars=set(vars().keys()).union(set(globals().keys()))
    # print("\n\nmemory check:")
    # for element in cur_vars:
    #     temp_type=eval('type('+element+')')
    #     if temp_type==np.ndarray:
    #         temp_shape=eval(element+'.shape')
    #         print("\t",temp_shape,element,temp_type)
    print("\n\nDoing Louvain clustering:")
    print("\tconverting affinity matrix into local weighted network")
    print("\tinitial matrix:")
    print(type(am))
    print(am)
    if flexible_percentile:
        ## this dynamically changes the percentile such that it will do the percentile, unless there are sufficiently large number of cells
        ## at which point, it'll cap the number of edges to the flexible cap number of edges
        equivalent_percentile_for_flexible = 1-(flexible_cap/am.shape[0])
        print("1-(",flexible_cap,'/',am.shape[0],"):",equivalent_percentile_for_flexible)
        if flexible_cap<am.shape[0]:
            percentile = max([percentile,equivalent_percentile_for_flexible])
    print("\nlocally weighted affinity matrix percentile cutoff:",percentile,'% (',int(am.shape[0]-percentile*am.shape[0]),'cells)','\n')
    ## normalize the affinity matrix (and reconvert it to positive range if needed)
    am = normalize_am(am, percentile = percentile)
    print("\tconverting into network")
    ## convert to a network graph
    G = nx.Graph()
    G.add_nodes_from(list(range(am.shape[0])))
    for i in range(am.shape[0]):
        if i%5000==0 and i != 0:
            print("\t\t",round(i/am.shape[0]*100,2),"%")
        G.add_edges_from(get_current_edges(am[i,:],i))
    print("\tdoing the modularity now")
    partition = community.best_partition(G, resolution=resolution)
    labels = []
    for i in range(len(partition.keys())):
        labels.append(partition[i])
    if out_dir is not None:
        pos = nx.spring_layout(G)
        node_size = 2.5
        edge_width = 2.5/np.sqrt(nx.number_of_edges(G))
        print("\n"*10,"saving cell ebmedding graph","\n\n\n")
        save_dict(G,os.path.join(out_dir,"cell_embedding.graphpkl"))
    af = louvain_clust_object(affinity = am, labels = labels, sample_names = sample_names)
    return(af)





##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################






#################################################################################
#################################################################################
#################################################################################
##############    <functions for performing k-means clustering>   ###############
#################################################################################
##############################################################################
####################### find k means for all samples #########################

##############################################################################
#########      functions for performing k-means clustering    ################

def linear_normalization(in_matrix,axis=1):
    in_matrix = in_matrix - np.transpose( np.array( [np.min(in_matrix, axis=axis)] ) )
    in_matrix = in_matrix / np.transpose( np.array( [np.max(in_matrix, axis=axis)] ) )
    print(np.min(in_matrix, axis=axis))
    print(np.max(in_matrix, axis=axis))
    return(in_matrix)

##################
def convert_to_prob(vect):
    ## calculate probabilities based on standard deviation 
    probabilities = vect - min(vect)
    probabilities = probabilities / max(probabilities)
    probabilities = probabilities / sum(probabilities)
    if np.sum(np.isnan(probabilities)) > 0:
        probabilities = np.ones(np.shape(probabilities))
        probabilities = probabilities / np.sum(probabilities)
    return(probabilities)



########################
def unknown_k_means_sample(sample_names, expression_matrix, ID_list, temp, sample_k_known=False, prob = False, first_prob = True):
    ## expressoin matrix format:
    ##        sample1, sample2, sample3 ...
    ## var1[[  1.0   ,   1.5  ,   2.0  ],
    ## var2 [  0.2   ,   1.5  ,   2.0  ],
    ## var3 [  1.0   ,   1.5  ,   2.0  ]]

    ## because the kmeans2 function from scipy clusters based on rows, 
    ## the expression matrix will be transposed

    ## samples are now in rows, and expression values are now in columns

    #### constant ####
    # go_past_for_local_min is the variable which is used for seeing how far in 
    # k selection we should go past a local minimum

    # expression_matrix = np.transpose(expression_matrix)
    # expression_matrix = expression_matrix.astype('float32')
    
    ## this variable is for testing passed a local minimum of the f(k) function
    stopping_length = 10
    
    if expression_matrix.shape[0] <= stopping_length:
        print('expression_matrix is too small to subdivide')
        
        output_cluster_annotations = list(zip(sample_names, [0]*len(sample_names)))
        for i in range(0,len(output_cluster_annotations)):
            output_cluster_annotations[i]=list(output_cluster_annotations[i])
        #output_cluster_annotations, out_var_group_list_of_lists, f_list, optimal_centroid_indices
        return(output_cluster_annotations, [sample_names], [1],[0])
    
    
    ## find the variable with the greatest number of interactions (or total expression)
    row_std = np.std(expression_matrix, axis = 1)
    print(expression_matrix)
    print(row_std)
    max_row_std = np.max(row_std)
    if prob or first_prob:
        probabilities = convert_to_prob(row_std)
        print(row_std)
        print(np.sum(row_std))
        print(len(sample_names))
        print(len(probabilities))
        centroid_initialization_index = np.random.choice ( list( range(0,len(sample_names)) ) , size = 1, replace = False, p = probabilities ) 
    else:
        centroid_initialization_index = sample(list(np.where(row_std == max_row_std)[0]), 1)
    print('first centroid index:',centroid_initialization_index)
    centroid_indices = list(centroid_initialization_index[:])
    
    temp_centroids, variable_labels = kmeans2(expression_matrix, expression_matrix[centroid_indices,:], minit='matrix', iter=10)
    
    print('\ncentroid_indices for k =',len(centroid_indices))
    print(centroid_indices)
    print('\n\n')
    
    ## initialize with k = 1
    Sk = None
    Ak = None
    temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, [list(variable_labels)], expression_matrix)
    f_list = [temp_f]
    centroid_distances_matrix = np.array(get_all_distances_from_a_centroid(expression_matrix[centroid_indices[-1]], expression_matrix))
    
    print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)


    
    while k_stopping_function(f_list, num_vars = len(sample_names)):
        ## len(f_list) must be at least the length of the stopping_length +1 for k=1
        ## then the first time that min(f(k)) is not within the stopping length, 
        ## then stop and return the optimal k

        ## first thing to do is find out all the current distances from all centroids
        if len(centroid_indices)>1:
            centroid_distances_matrix = np.hstack((centroid_distances_matrix, np.array(get_all_distances_from_a_centroid(expression_matrix[centroid_indices[-1]], expression_matrix))))
        
        ## find the index of the next centroid based on the current distance matrix
        if prob:
            next_centroid = get_next_centroid_index(centroid_distances_matrix, existing_centroids = centroid_indices, prob = True)
        else:
            next_centroid = get_next_centroid_index(centroid_distances_matrix, existing_centroids = centroid_indices)
        if next_centroid in centroid_indices:
            ## this means that the newly of the remaining points, there are now ties
            ## with already existing centroids for farthest away from other centroids
            print('already established centroid was picked again')
            break
        print(centroid_indices)
        centroid_indices.append(next_centroid)
        print('\ncentroid_indices for k =',len(centroid_indices))
        print(centroid_indices)
        print('\n\n')
        
        temp_centroids, variable_labels = kmeans2(expression_matrix, expression_matrix[centroid_indices,:], minit='matrix', iter=10)
        
        ## this function will take variable labels of format [0,1,1,0,0,2]
        ## and change it to: 
        ## [[0,3,4], ## centroid 0
        ##    [1,2],   ## centroid 1
        ##     [5]]     ## centroid 2
        variable_labels = rearrange_variable_labels(variable_labels)
       # print('variable_labels\n',variable_labels)
        if len(variable_labels) < len(centroid_indices):
            ## this means that two centroids have converged during the k-means clustering, indicating
            ## that the number of centroids is already oversaturated
            print("centroids converged, stopping due to overfit")
            break
        
        
        temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, variable_labels, expression_matrix)
        f_list.append(temp_f)
        print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)
        
    print(k_stopping_function(f_list, num_vars = len(sample_names)))
    if not k_stopping_function(f_list, num_vars = len(sample_names)):
        
        print(f_list)
    if not sample_k_known:
        optimal_k_index = get_estimated_k_from_f_list(f_list)
        print('optimal k =',optimal_k_index+1)
    elif sample_k_known:
        print('sample k known')
        optimal_k_index = int(pre_determined_sample_k-1)
    print('optimal k index:',optimal_k_index)
#    if not no_graphs:
#        plt.clf()
#        plt.plot(np.arrange(1,len(flist)),f_list,'o-')
#        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    optimal_centroid_indices = centroid_indices[:optimal_k_index+1]
    #print(optimal_centroid_indices)
    
    final_centroids, final_variable_labels = kmeans2(expression_matrix, expression_matrix[optimal_centroid_indices,:], minit='matrix', iter=10)
    
    ## convert the final variable labels into a list of lists containing the variable names
    rearranged_var_labels = rearrange_variable_labels(final_variable_labels)
    out_var_group_list_of_lists = []
    for r in rearranged_var_labels:
        out_var_group_list_of_lists.append(list(sample_names[var] for var in r))
    
    
        
    output_cluster_annotations = list(map(list,zip(sample_names, final_variable_labels)))
    
    
    if sample_k_known:
        copy_centroids=optimal_centroid_indices[:]
        print(list(map(str,copy_centroids)))
        #process_dir(temp+'/sample_clustering_and_summary/')
        #make_file('\n'.join(list(map(str,copy_centroids))),temp+'/sample_clustering_and_summary/centroid_indices.txt')
    
    return(output_cluster_annotations, out_var_group_list_of_lists, f_list, optimal_centroid_indices)

########################################################################

#####################

def get_all_distances_from_a_centroid(centroid, in_mat):
    euclidean_distances = []
    for i in range(0, in_mat.shape[0]):
        ## get the euclidean distance of each variable from given centroid
        temp_dist=linalg.norm(in_mat[i] - centroid)
        euclidean_distances.append(temp_dist**2)
#        euclidean_distances.append(temp_dist)
    return(np.transpose(np.array([np.array(euclidean_distances)])))

######################


def get_next_centroid_index(distance_list, existing_centroids = [], prob = False, multiply_by_min = True):
    ## this function calculates the sum of the squares of the euclidean distances from
    ## the all of the current centroids for all variables, then returns the index of the
    ## variable with the maximum sum of the square euclidean distances from all centroids
    
    #print('distance_list')
    #print(distance_list)
    
    temp_dist_mat=np.array(distance_list)
    #row_sum=np.sum(temp_dist_mat * temp_dist_mat, axis=1)
    row_sum=np.sum(temp_dist_mat, axis=1)
    #print(temp_dist_mat)
    if multiply_by_min:
        row_max=np.amax(temp_dist_mat,axis=1)
        row_min=np.amin(temp_dist_mat,axis=1)
        #print(row_min)
        row_range_plus1=(row_max-row_min)+1
        #print(row_range_plus1)
    
        
        all_distances=row_sum*row_min
    else:
        all_distances=row_sum

    
    #print(all_distances)
    #sys.exit()

    ## add all subsequent squared distances

    if prob:
        ## calculate probabilities based on standard deviation 
        probabilities = convert_to_prob(all_distances)
        max_indices = np.random.choice ( list( range(0, np.shape(distance_list)[0] ) ) , size = 1, replace = False, p = probabilities ) 
        
        num_max_indices = 1
    else:
        max_indices = np.where(all_distances == np.max(all_distances))[0]
        num_max_indices = np.shape(max_indices)[0]
        print('\n\tnumber equal to max',num_max_indices)
    
    
    final_candidate_next_centroids = []
    if num_max_indices > 1:
        max_indices = list(max_indices)
        final_candidate_next_centroids = []
        for i in range(0,num_max_indices):
            if max_indices[i] not in existing_centroids:
                final_candidate_next_centroids.append(max_indices[i])
        if final_candidate_next_centroids == []:
            return(sample(max_indices,1)[0])
        else:
            return(sample(final_candidate_next_centroids,1)[0])
        
    else:
        return(sample(list(max_indices),1)[0])


##################

from scipy.cluster.vq import kmeans2
def do_k_means(centroids, in_matrix, name, temp_IDs, iters = 10):
    global temp, IDlist
    
    final_centroids, variable_labels = kmeans2(in_matrix, centroids, minit='matrix', iter=iters)
    
    print(final_centroids)
    print(variable_labels)
    make_file(flatten_2D_table([['variable','group']]+list(map(list,list(zip(temp_IDs, variable_labels)))), '\t'), temp+'/'+name+'_k_groups.txt')
    #sys.exit()
    
    return

#################

def euclidean_distance(row1,row2):
    global linalg
    temp_eucl_dist = linalg.norm(row1-row2)
    return(temp_eucl_dist)


#################
from sklearn import metrics

def get_half_distance_matrix(in_array):
    ## this function returns the symetric matrix of euclidean distance between
    ## all genes based on the input array that are passed into this 
    ## function
    try:
        return(metrics.pairwise.euclidean_distances(in_array,in_array))
    except:
        distance_matrix = np.zeros((in_array.shape[0],in_array.shape[0]))
        for i in range(0,in_array.shape[0]):
            for j in range(i,in_array.shape[0]):
                if i==j:
                    pass
                else:
                    temp_dist = euclidean_distance(in_array[i,:], in_array[j,:])
                    distance_matrix[i,j] = temp_dist
                    #distance_matrix[j,i] = temp_dist
        return(distance_matrix)


#######################

def global_impact_of_k_clusters(centroids, members, interaction_matrix):
    ## centroids is a list of the centroids
    ## members is a list of the indices of each member belonging to the ith centroid
    ## the interaction matrix is given for subsetting the members out
    #print('centroids')
    #print(type(centroids))
    
    if len(members) != centroids.shape[0]:
        print('incorrect dimentions\tmembers:',len(members), '\tcentroids:', centroids.shape[0])
        sys.exit('incorrect dimentions')
    Sk=0
    Sk_vector=[]
    for i in range(0,len(members)):
        ## dummy is set because this function returns the erroneous IDs for the subset matrix
        ## this function does this because it thinks it's getting the full interaction matrix,
        ## even though in reality it is getting a subsetted matrix
        #dummy, member_subset = subset_interaction_matrix(members[i], interaction_matrix)
        member_subset = interaction_matrix[members[i],:]
        
        ## trim the centroid to only include the indices of the subset matrix
        
        #temp_centroid = centroids[i,members[i]]
        temp_centroid = centroids[i,]
        
        #print(members[i])
        distance_vector = get_all_distances_from_a_centroid(temp_centroid, member_subset)
        temp_sk = np.sum(distance_vector)
        
        Sk_vector.append(temp_sk)
        Sk += temp_sk

    return(Sk)

####################

def f_of_k(prior_Sk, prior_Ak, centroids, members, interaction_matrix):
    ## * note that if k == 1, or k == 2, the 'prior_Ak' argument is not actually used
    ## so any dumby value can be fed into the function without ill effect
    print('prior_Sk',prior_Sk)
    print('prior_Ak',prior_Ak)
    #print('centroids')
    #print(centroids)
    #print('members')
    #print(members)
    #print('interaction_matrix')
    #print(interaction_matrix)
    k = len(members)
    Nd = interaction_matrix.shape[0]
    if k == 1:
        cur_Ak = None


    ## this function should only be run on 'clusters' with at least two possible members
    if Nd == 1:
        return (None, None, None)

    ## calculate Sk 
    else:
        cur_Sk = global_impact_of_k_clusters(centroids, members, interaction_matrix)
    
    ## calculate the current Ak
    if k == 2 and Nd > 1:
        cur_Ak = 1 - ( 3 / ( 4 * Nd ) )
    elif k > 2 and Nd > 1:
        cur_Ak = prior_Ak + ( (1 - prior_Ak) / 6 )

    
    ## calculate the k evaluation function
    if k == 1 or (prior_Sk == 0 and k > 1):
        f = 1
    else:
#        print('original f(k)',cur_Sk / (cur_Ak * prior_Sk))
        f = cur_Sk / (cur_Ak * prior_Sk)

#        print('new f(k)',f)

    return(f, cur_Sk, cur_Ak)

###################

def k_stopping_function(f_list, num_vars = None, starting_length=None, stopping_length=5, delta_cutoff=10):
    ## returning True allows the k search to continue, while returning False makes it stop
    if starting_length==None:
        starting_length = int(min([np.sqrt(num_vars)+1,50])) ## this is a guess for the max number of groups to test at the beginning, barring any run-offs of local minimas
    global sample_k_known, pre_determined_sample_k
    if sample_k_known:
        if len(f_list) < pre_determined_sample_k:
            return(True)
        if len(f_list) == pre_determined_sample_k:
            return(False)
    else:
        if len(f_list)==1:
            return(True)
        if (f_list[-1] - f_list[-2]>10):
            return(False)
        if (len(f_list) < starting_length+1):
            return(True)
        if (min(f_list) in f_list[-stopping_length:]):
            return(True)

def get_estimated_k_from_f_list(f_list):
    global sample_k_known, pre_determined_sample_k
    if sample_k_known:
        return(pre_determined_sample_k-1)
    else:
        f_deltas=[]
        f_delta_delta=[]
        for f in range(1,len(f_list)):
            f_deltas.append(f_list[f]-f_list[f-1])
            f_delta_delta.append(f_list[f]-f_deltas[-1])
        
        #optimal_k=f_delta_delta.index(min(f_delta_delta))
#        print('f_delta_delta')
#        print(f_delta_delta)
        min_f=min(f_list)
        optimal_k_index=f_list.index(min_f)
        #next_best=min(f_list[optimal_k_index+1:])
        #if next_best < min_f*1:
        #    optimal_k_index=f_list.index(next_best)
        return(optimal_k_index)


##################

def rearrange_variable_labels(variable_labels):
    ## this function will take variable labels of format [0,1,1,0,0,2]
    ## and change it to: 
    ## [[0,3,4], ## centroid 0
    ##    [1,2],   ## centroid 1
    ##     [5]]     ## centroid 2
    max_label = max(variable_labels)
    variable_labels = np.array(variable_labels)
    new_var_labels=[]
    for i in range(0,max_label+1):## plus1 because the range function is exclusive in python, not inclusive
        new_var_labels.append(list(np.where(variable_labels == i)[0]))
    return(new_var_labels)











#########################################################

def do_unknown_k_means_clustering_iter(title, full_expression, cluster_iter = 10, performed_on_samples = False, upper_nine_k = True, cluster_prob=False):
    global sample_k_known, pre_determined_sample_k
    print("sample_k_known",sample_k_known)
    sample_k_table_list_list=[]
    sample_k_lists_list=[]
    f_list_list=[]
    optimal_centroid_indices_list=[]
    min_f=[]
    k_estimate_list = []

    ## transposed dataset to feed into k-means
    full_expression_t = np.array(np.transpose(full_expression),dtype=np.float32)

    print(cluster_iter)
    for i in range(0,cluster_iter):
        print(i)
        if i == 0:
            print(title[:5],'...',title[-5:])
            print(full_expression)
            print(np.shape(full_expression))
            # a = unknown_k_means_sample(title, full_expression_t, prob=False)
            # print(len(a))
            # for i in a:
            #     print(i)
            temp_sample_k_table, temp_sample_k_lists, temp_f_list, temp_optimal_centroid_indices = unknown_k_means_sample(title, full_expression_t, prob=False)
        else:
            temp_sample_k_table, temp_sample_k_lists, temp_f_list, temp_optimal_centroid_indices = unknown_k_means_sample(title, full_expression_t, prob=cluster_prob)
        
        sample_k_table_list_list.append(temp_sample_k_table)
        sample_k_lists_list.append(temp_sample_k_lists)
        f_list_list.append(temp_f_list)
        if bool(sample_k_known):
            min_f.append(temp_f_list[pre_determined_sample_k-1])
        else:
            min_f.append(min(temp_f_list))
        k_estimate_list.append(temp_f_list.index(min_f[-1])+1)
        
        optimal_centroid_indices_list.append(temp_optimal_centroid_indices)

    
    if performed_on_samples:
        if bool(sample_k_known):
            write_table(f_list_list,temp+'/f_lists_k_known.txt')
        else:
            write_table(f_list_list,temp+'/f_lists_k_not_known.txt')

    if upper_nine_k and not bool(sample_k_known):
        sample_k_known = True
        
        temp_k_list = k_estimate_list[:]
        temp_k_list = sorted(temp_k_list)
        pre_determined_sample_k = temp_k_list[ int(round(cluster_iter*.9, 0)) - 1 ]
        
        return( do_unknown_k_means_clustering_iter(title, full_expression, cluster_iter = cluster_iter, performed_on_samples = performed_on_samples) )
        
    ############
    print('k estimate list',k_estimate_list)
    for f in range(0,len(f_list_list)):
        print('iter',f,'k estimate',k_estimate_list[f],'f',min_f[f],f_list_list[f])

        
    
    ############
    if True:#sample_k_known:
        global_min_f = min(min_f)
        print('global_min_f',global_min_f)
        global_min_f_indices = min_f.index(global_min_f)
        print('global_min_f_indices',global_min_f_indices)
        if type(global_min_f_indices) == int:
            optimal_k_iter=global_min_f_indices
        else:
            optimal_k_iter = sample(list(global_min_f_indices),1)[0]
        f_list = f_list_list[optimal_k_iter]
        optimal_centroid_indices=optimal_centroid_indices_list[optimal_k_iter]
    
        print(optimal_centroid_indices)
        
        sample_k_table_list = sample_k_table_list_list[optimal_k_iter]
        sample_k_lists = sample_k_lists_list[optimal_k_iter]
    ############
    
    #print(full_expression[:,optimal_centroid_indices])
    

    return(sample_k_table_list, sample_k_lists, f_list, optimal_centroid_indices)

#########################################################



#############    </functions for performing k-means clustering>   ###############
#################################################################################
#################################################################################
#################################################################################
#################################################################################