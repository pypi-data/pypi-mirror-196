import os
import ray
import h5py
import shutil
import fileinput
import numpy as np
import pandas as pd
import seaborn as sns
import multiprocessing
import statsmodels.api as sm
from copy import deepcopy
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pyminer.common_functions import read_table, get_bins, process_dir, make_file, ray_dict_of_array_slices_to_array, strip_split, ray_get_indices_from_list, find_random_file
from pyminer.pyminer_common_stats_functions import no_p_spear
from pyminer.pyminer_clust_funcs import *
from pyminer.pyminer_get_dispersion import do_over_dispers_feat_select
from pyminer.pyminer_gprofiler_converter import convert_to_ensg, convert_to_human
from scipy.sparse import issparse
try:
    from scipy.sparse import dok_array as dok_mat
    from scipy.sparse import lil_array as lil_mat
except:
    from scipy.sparse import dok_matrix as dok_mat
    from scipy.sparse import lil_matrix as lil_mat

##########################################
##########################################
## for when we're ready to read the distance matrix back in
# print('reading in the negative Euclidean distance matrix from the hdf5 file')
# cp(neg_euc_hdf5_file+' '+neg_euc_hdf5_file+'_copy')
# neg_euc_hdf5_file_copy = neg_euc_hdf5_file+'_copy'
# spear_h5f = h5py.File(neg_euc_hdf5_file_copy, 'r+')
# full_expression = spear_h5f["infile"]


@ray.remote
def ray_all_nb_regs(in_mat, temp_indices, exog):
    out_dict = {}
    for i in range(in_mat.shape[0]):
        out_dict[temp_indices[i]]=ray_single_nb_reg(in_mat[i,:],exog)
    return(out_dict)


def ray_single_nb_reg(endog, exog, epsilon=1e-3):
    ## exog must have intercept already added! (via sm.add_constant)
    if np.var(endog)==0:
        return(endog)
    #nb_mod = sm.GLM(endog, exog, family=sm.families.NegativeBinomial())
    nz_indices = np.where(endog>0)[0]
    ## fit the regression using the indices that actually show expression of this gene
    # print("endog.iloc[nz_indices]")
    # print(endog[nz_indices])
    # print("exog.iloc[nz_indices]")
    # print(exog.iloc[nz_indices])
    nb_mod = sm.GLM(endog[nz_indices], exog.iloc[nz_indices], family=sm.families.Gaussian())
    try:
        nb_res = nb_mod.fit()
    except:# sm.tools.sm_exceptions.PerfectSeparationError:
        return(endog)
    ## with this implementation, the residuals are only for the genes which showed non-zero expression
    all_predict = nb_res.resid_pearson
    offset = np.min([np.mean(endog[nz_indices] ), ])
    mean_within_expressed = np.mean(endog[nz_indices] )
    all_offset_residuals = np.zeros(endog.shape[0])
    all_offset_residuals[nz_indices] = all_predict+mean_within_expressed
    temp_min = np.min(all_offset_residuals)
    if temp_min<0:
        all_offset_residuals[nz_indices] = mean_within_expressed-temp_min+epsilon
    return(all_offset_residuals)


def ray_fit_all_nb_reg(in_mat, technical_table, threads=None):
    if threads is None:
        threads = multiprocessing.cpu_count()
    ray_calls=[]
    original_idx_list = list(range(in_mat.shape[0]))
    temp_indices = ray_get_indices_from_list(threads, original_idx_list)
    for i in range(len(temp_indices)):
        temp_call = ray_all_nb_regs.remote(np.array(in_mat[temp_indices[i],:]), temp_indices[i], technical_table)
        ray_calls.append(temp_call)
    #print(ray_calls)
    ray_sults = ray.get(ray_calls)
    #print(ray_sults)
    ray_array = ray_dict_of_array_slices_to_array(ray_sults)
    #ray.shutdown()
    return(ray_array)


def ray_single_nb_reg_for_all(endog, exog, all_measures, all_exog, epsilon=1e-3):
    ## exog must have intercept already added! (via sm.add_constant)
    # print(endog.shape)
    # print(exog.shape)
    # print(all_measures.shape)
    if np.var(endog)==0:
        return(np.zeros(all_measures.shape[0]))
    #nb_mod = sm.GLM(endog, exog, family=sm.families.NegativeBinomial())
    ## fit the regression using the indices that actually show expression of this gene
    nz_indices = np.where(endog>0)[0]
    nb_mod = sm.GLM(endog[nz_indices], exog[nz_indices,:], family=sm.families.Gaussian())
    try:
        nb_res = nb_mod.fit()
        #print(nb_mod)
    except:# sm.tools.sm_exceptions.PerfectSeparationError:
        return(all_measures)#np.zeros(all_measures.shape[0]))
    all_predict = all_measures - np.array(nb_res.predict(all_exog))
    # print("all_predict.shape")
    # print(all_predict.shape)
    # print(all_predict)
    ## find the non-zeros
    all_nz_indices = np.where(endog>0)[0]
    mean_within_expressed = np.mean(endog[nz_indices])
    all_offset_residuals = np.zeros(all_predict.shape)
    all_offset_residuals[all_nz_indices] = all_predict[all_nz_indices]+mean_within_expressed
    #all_offset_residuals = all_predict + np.mean(endog)
    # print("all_offset_residuals.shape")
    # print(all_offset_residuals.shape)
    # print(all_offset_residuals)
    return(all_offset_residuals)


def ray_single_nb_reg_local(endog, exog, cluster_lists, weighted_medoid_mat):
    ## this is for one gene, training a model at the per-cluster level
    ## then predicting each cell's value based on each cluster's model
    ## prediction_mat is cells in rows, & each cluster's model based prediction in 
    ## 
    prediction_mat = np.zeros((endog.shape[0],len(cluster_lists)))
    for i in range(len(cluster_lists)):
        # print(endog.shape)
        # print(exog.shape)
        # print(len(cluster_lists[i]))
        prediction_mat[:,i] = ray_single_nb_reg_for_all(endog[cluster_lists[i]],
                                                        exog[cluster_lists[i]],
                                                        endog,
                                                        exog)
        #print(prediction_mat[:,i])
    weighted_predictions = prediction_mat * weighted_medoid_mat
    final_prediction = np.sum(weighted_predictions,axis=1)
    if np.isnan(final_prediction[0]):
        print("prediction_mat")
        print(prediction_mat)
        print("weighted_predictions")
        print(weighted_predictions)
        print("final_prediction")
        print(final_prediction)
    return(final_prediction)


@ray.remote
def ray_all_nb_regs_local(in_mat, 
                          temp_indices, 
                          exog, 
                          cluster_lists, 
                          weighted_medoid_mat):
    out_dict = {}
    for i in range(in_mat.shape[0]):
        out_dict[temp_indices[i]]=ray_single_nb_reg_local(in_mat[i,:], 
                                                          exog, 
                                                          cluster_lists, 
                                                          weighted_medoid_mat)
        if np.any(np.isnan(out_dict[temp_indices[i]])):
            print(sum(np.isnan(out_dict[temp_indices[i]])))
            print(out_dict[temp_indices[i]])
            print("in_mat[i,:]")
            print(in_mat[i,:])
            print("exog")
            print(exog)
            prediction_mat = np.zeros((in_mat[i,:].shape[0],len(cluster_lists)))
            for i in range(len(cluster_lists)):
                # print(endog.shape)
                # print(exog.shape)
                # print(len(cluster_lists[i]))
                prediction_mat[:,i] = ray_single_nb_reg_for_all(in_mat[i,:][cluster_lists[i]],
                                                                exog[cluster_lists[i]],
                                                                in_mat[i,:],
                                                                exog)
                print(prediction_mat[:,i])
            weighted_predictions = np.dot(prediction_mat, weighted_medoid_mat.transpose())
            print("weighted_predictions")
            print(weighted_predictions)
            final_prediction = np.sum(weighted_predictions,axis=1)
            print("final_prediction")
            print(final_prediction)
            print(sum(np.isnan(final_prediction)))
    return(out_dict)



def ray_fit_all_nb_reg_local(in_mat, 
                             technical_table, 
                             cluster_lists, 
                             weighted_medoid_mat, 
                             threads=None):
    if threads is None:
        threads = multiprocessing.cpu_count()
    ray_calls=[]
    original_idx_list = list(range(in_mat.shape[0]))
    temp_indices = ray_get_indices_from_list(threads, original_idx_list)
    for i in range(len(temp_indices)):
        temp_call = ray_all_nb_regs_local.remote(np.array(in_mat[temp_indices[i],:]),
                                                 temp_indices[i],
                                                 technical_table,
                                                 cluster_lists,
                                                 weighted_medoid_mat)
        ray_calls.append(temp_call)
    #print(ray_calls)
    ray_sults = ray.get(ray_calls)
    ray_array = ray_dict_of_array_slices_to_array(ray_sults)
    #ray.shutdown()
    return(ray_array)


def do_batch_correction(in_mat, technical_table, bin_size = 5000):
    nrows = in_mat.shape[0]
    bin_size = min([bin_size,math.ceil(nrows/2)])
    ## get bins
    all_bins = get_bins(nrows, bin_size=bin_size)
    ## set up the output file
    ##
    ray.init()
    exog = sm.add_constant(technical_table)
    #ray.init()
    ray_exog = ray.put(exog)
    out_mat = np.zeros(in_mat.shape)
    for i in range(len(all_bins)-1):
        start=all_bins[i]
        end=all_bins[i+1]
        out_mat[start:end,:]=ray_fit_all_nb_reg(np.array(in_mat[start:end,:]),
                                                        ray_exog)
    ray.shutdown()
    return(out_mat)



# complex_scores = get_all_clust_complex_scores(tech_dict, 
#                                                       in_mat, 
#                                                       genes, 
#                                                       cells, 
#                                                       clust_res.cluster_indices)

# ray.shutdown()
# temp_res = do_batch_correction(in_mat[:,temp_clust_idxs],
#                                                  temp_complex_scores)

# for j in range(in_mat.shape[0]):
#     print(in_mat[j,temp_clust_idxs])
#     dummy_res = ray_single_nb_reg(in_mat[j,temp_clust_idxs],temp_complex_scores)



def fine_tune_technical_correction_with_clusters(in_mat,
                                               tm_dict,
                                               genes,
                                               cells,
                                               clust_lists,
                                               out_h5):
    complex_scores = get_all_clust_complex_scores(tm_dict, 
                                                      in_mat, 
                                                      genes, 
                                                      cells, 
                                                      clust_lists)
    f = h5py.File(out_h5,"w")
    out_mat = f.create_dataset("infile",
                           (len(genes),len(cells)),
                            dtype=np.float32)
    ## go through each cluster
    for i in range(len(clust_lists)):
        temp_clust_idxs = clust_lists[i]
        temp_complex_scores = pd.DataFrame(complex_scores[i])
        #print(temp_complex_scores)
        # pd.plotting.scatter_matrix(pd.DataFrame(temp_complex_scores))
        # plt.show()
        out_mat[:,temp_clust_idxs] = do_batch_correction(in_mat[:,temp_clust_idxs],
                                                         temp_complex_scores)
    f.close()
    return(out_h5)


def process_temp_complex_scores(temp_complex_scores, percent=0.90):#0.95):
    # Separating out the features
    n_features = temp_complex_scores.shape[1]
    x = temp_complex_scores.values# Separating out the target
    x = StandardScaler().fit_transform(x)
    print(x)
    print(n_features)
    pca = PCA(n_components=n_features)
    principalComponents = pca.fit_transform(x)
    print("percent explained:")
    print(pca.explained_variance_ratio_)
    n_components = np.min(np.where(np.cumsum(pca.explained_variance_ratio_)>percent)[0])
    print("found ",n_components+1," significant components")
    component_result = principalComponents[:,list(range(n_components+1))]
    print(component_result)
    return(component_result)


def do_local_batch_correction(in_mat, clust_lists, complex_scores, weighted_medoid_mat, out_h5, bin_size = 5000):
    nrows = in_mat.shape[0]
    bin_size = min([bin_size,math.ceil(nrows/2)])
    ## get bins
    all_bins = get_bins(nrows, bin_size=bin_size)
    ## set up the output file
    ##
    all_complex_scores = pd.DataFrame(complex_scores[0])#[0] b/c technical needs to be global vars, so this is based on a "single cluster" style analysis
    temp_complex_scores = process_temp_complex_scores(all_complex_scores)
    exog = sm.add_constant(temp_complex_scores)
    f = h5py.File(out_h5,"w")
    out_mat = f.create_dataset("infile",
                           (len(genes),len(cells)),
                            dtype=np.float32)
    ray.init()
    ray_exog = ray.put(exog)
    for i in range(len(all_bins)-1):
        start=all_bins[i]
        end=all_bins[i+1]
        out_mat[start:end,:] = ray_fit_all_nb_reg_local(in_mat[start:end,:], 
                                                        ray_exog,
                                                        clust_lists,
                                                        weighted_medoid_mat,
                                                        threads=None)
    ray.shutdown()
    f.close()
    return(out_mat)




def fine_tune_technical_correction_with_clusters_local_weight(in_mat,
                                               tm_dict,
                                               genes,
                                               cells,
                                               clust_lists,
                                               out_h5,
                                               weighted_medoid_mat,
                                               bin_size=5000):
    global_complex_scores = get_all_clust_complex_scores(tm_dict, 
                                                          in_mat, 
                                                          genes, 
                                                          cells, 
                                                          [list(range(in_mat.shape[1]))])
    print(global_complex_scores)
    # complex_scores = get_all_clust_complex_scores(tm_dict, 
    #                                                   in_mat, 
    #                                                   genes, 
    #                                                   cells, 
    #                                                   clust_lists)
    #(in_mat, clust_lists, complex_scores, weighted_medoid_mat, out_h5, bin_size = 5000)
    do_local_batch_correction(in_mat,
                                         clust_lists,
                                         global_complex_scores,
                                         weighted_medoid_mat,
                                         out_h5)
    
    return(out_h5)


def get_peicemeal_colsums(in_mat):

    return()



def gm_mean(x):
    keep_idxs = np.where(x > 0)[0]
    if len(keep_idxs)==0:
        return(0)
    elif len(keep_idxs)==1:
        return(x[keep_idxs])
    else:
        x=x[keep_idxs]
        gm=np.exp(np.sum(np.log(x)) / x.shape[0])
        return(gm)



def new_calcFactorRLE(data):
    #   Scale factors as in Anders et al (2010)
    #   Mark Robinson
    #   Created 16 Aug 2010
    # gm <- exp(rowMeans(log(data)))
    # return(apply(data, 2, function(u) median((u/gm)[gm > 0])))
    sparse_convert = False
    if issparse(data):
        sparse_convert=True
    gm = np.zeros(data.shape[0])
    for i in range(data.shape[0]):
        if sparse_convert:
            gm[i] = gm_mean(data[i,:].toarray().flatten())
        else:
            gm[i] = gm_mean(data[i,:])
    keep_rows = np.where(gm>0)[0]
    gm = gm[keep_rows]
    size_factor = np.zeros(data.shape[1])
    for i in range(data.shape[1]):
        if sparse_convert:
            data_subset = data[:,i].toarray().flatten()
        else:
            data_subset = data[:,i]
        #print("1")
        data_subset = data_subset[keep_rows]
        #print("2")
        active_subset_idxs = np.where(data_subset>0)[0]
        #print("3")
        #print(active_subset_idxs.shape)
        data_subset = data_subset[active_subset_idxs]
        #print("4")
        #print(data_subset)
        size_factor[i] = np.median(data_subset/gm[active_subset_idxs])
    return(size_factor)


# def calcFactorQuantile(data, lib.size, p=0.75):
#     #   Generalized version of upper-quartile normalization
#     #   Mark Robinson and Gordon Smyth
#     #   Created 16 Aug 2010. Last modified 12 Sep 2020.
#     f = np.ones(data.shape[1])
#     ## go through the columns & calculate the 
#     for (j in seq_len(ncol(data))) f[j] <- quantile(data[,j], probs=p)
#     if(min(f)==0) warning("One or more quantiles are zero")
#     return(f / lib.size)

def do_depth_normalization(data, size_factors = None):
    if size_factors is None:
        size_factors = new_calcFactorRLE(data)
    for i in range(data.shape[1]):
        if size_factors[i]<=0:
            pass
        else:
            data[:,i]=data[:,i]/size_factors[i]
    return(data)


def standardize_dispersion(disp_subset):
    centered = disp_subset["mean_var_residuals"]-np.mean(disp_subset["mean_var_residuals"])
    standardized_resids = centered/np.std(centered)
    return(standardized_resids)



def do_disp_feat_select(in_mat, genes, keep_genes=None, censor_genes = [], z_resid=0.5):
    if keep_genes is None:
        keep_genes = []
        for temp_gene in genes:
            if temp_gene not in censor_genes:
                keep_genes.append(temp_gene)
    disp_table = do_over_dispers_feat_select(in_mat=in_mat, ID_list = genes)
    #print(keep_genes)
    disp_subset = disp_table[disp_table["gene"].isin(keep_genes)]
    #print("disp_subset")
    #print(disp_subset)
    centered = disp_subset["mean_var_residuals"]-np.mean(disp_subset["mean_var_residuals"])
    #print("centered")
    #print(centered)
    standardized_resids = centered/np.std(centered)
    #print("standardized_resids")
    #print(standardized_resids)
    keep_idxs = np.where(standardized_resids>=z_resid)[0]
    #print(keep_idxs)
    keep_genes = disp_subset.iloc[keep_idxs]["gene"]
    return(keep_genes)


def get_underdispersed(in_mat, genes, z_resid=0):
    disp_table = do_over_dispers_feat_select(in_mat=in_mat, ID_list = genes)
    standardized_resids = standardize_dispersion(disp_table)
    keep_idxs = np.where(standardized_resids<=z_resid)[0]
    #print(keep_idxs)
    keep_genes = disp_subset.iloc[keep_idxs]["gene"]
    return(keep_genes)


def get_tm_genes_from_dict(tm_dict):
    censor_gene_lists = list(tm_dict.values())
    censor_genes=[]
    for temp_list in censor_gene_lists:
        censor_genes+=temp_list
    return(censor_genes)


def min_count_norm(temp_mat, percentile_sum=0.9):
    colsums = np.sum(temp_mat, axis=1)
    target_depth=np.percentile(colsums,percentile_sum*100)
    print("target_depth:",target_depth)
    loading_factors=colsums/target_depth
    return(do_depth_normalization(temp_mat, size_factors=loading_factors))


def do_log_offset(temp_mat, log_offset):
    ## thinking about using log(x+c) with a higher c than 1 b/c of this paper
    ## which recommends c=1.6 to 25 
    ## https://www.biorxiv.org/content/10.1101/2021.06.24.449781v2
    ## "which implies a choice of c in the range of 25 to 1.6"
    print("offsetting")
    print(temp_mat)
    temp_mat += log_offset
    print("logging")
    temp_mat = np.log2(temp_mat)
    print(temp_mat)
    print("un-offsetting")
    temp_mat = temp_mat-np.log2(log_offset)
    print(temp_mat)
    print("checking for floating point errors")
    ## sometimes there are floating point errors that cause less than zero
    for i in range(temp_mat.shape[0]):
        temp_mat[i,:]=temp_mat[i,:]-np.nanmin(temp_mat[i,:])
        temp_mat[i,np.isnan(temp_mat[i,:])]=0
    print(temp_mat)
    #print("done")
    return(temp_mat)


def add_correlated_genes(additional_sig_genes, all_tech_genes):
    #pd.DataFrame({"genes":genes,"number_of_significant":out_num_sigs,"percent_sig":out_percent_sigs})
    sig_subset = additional_sig_genes[additional_sig_genes["number_of_significant"]>0]
    print(sig_subset)
    print(additional_sig_genes.head())
    a=sig_subset["genes"]
    a=list(sig_subset["genes"])+all_tech_genes
    a=set(list(sig_subset["genes"])+all_tech_genes)
    a=sorted(set(list(sig_subset["genes"])+all_tech_genes))
    a=list(sorted(set(list(sig_subset["genes"])+all_tech_genes)))
    all_tech_and_correlated=sorted(list(set(list(sig_subset["genes"])+all_tech_genes)))
    return(all_tech_and_correlated)


def rm_technical_and_perform_var_stabilization(in_mat,
                                               tm_dict,
                                               genes,
                                               z_resid=1.5,
                                               feat_select_method="disp",
                                               clust_lists = None,
                                               log_offset=12):
    print("rm_technical_and_perform_var_stabilization")
    ## first do an RLE-ish normalization
    ## first find the under-dispersed genes:
    all_tech_genes = get_tm_genes_from_dict(tm_dict)
    print("depth adjusting")
    in_mat = min_count_norm(in_mat)
    global_complex_scores = get_all_clust_complex_scores(tm_dict, 
                                                          in_mat, 
                                                          genes, 
                                                          [list(range(in_mat.shape[1]))])## cluster indices - but doing it globally here
    ############################################
    non_heme_tech = [gene for gene in all_tech_genes if gene not in tm_dict["hemoglobin"]]
    print("in_mat before cors")
    print(in_mat)
    additional_sig_genes = get_within_cluster_correlations_with_technical(do_log_offset(deepcopy(in_mat), log_offset),
                                                                         [list(range(in_mat.shape[1]))],
                                                                         global_complex_scores,
                                                                         genes)
    print("in_mat after cors")
    print(in_mat)
    all_tech_and_correlated_genes = add_correlated_genes(additional_sig_genes, all_tech_genes)
    if len(all_tech_and_correlated_genes)>0:#len(non_heme_tech)>0:
        ########################
        # ## Tm only
        # print("calculating Tm size factors")
        # global_cell_size_factors = new_calcFactorRLE(in_mat[get_gene_indices(non_heme_tech,genes),:])
        # print("normalizing matrix based on Tm size factors")
        # in_mat = do_depth_normalization(in_mat, size_factors=global_cell_size_factors)
        ########################
        ## Tm + correlated only
        print("calculating Tm size factors")
        global_cell_size_factors = new_calcFactorRLE(in_mat[get_gene_indices(non_heme_tech,genes),:])
        print("normalizing matrix based on Tm size factors")
        in_mat = do_depth_normalization(in_mat, size_factors=global_cell_size_factors)
        ########################
        ## Tm & other split norm
        # global_cell_size_factors = new_calcFactorRLE(in_mat[get_gene_indices(non_heme_tech,genes),:])
        # print("normalizing matrix based on Tm size factors")
        # in_mat[get_gene_indices(non_heme_tech,genes),:] = do_depth_normalization(in_mat[get_gene_indices(non_heme_tech,genes),:], size_factors=global_cell_size_factors)
        # all_other_genes = [gene for gene in genes if gene not in all_tech_genes]
        # all_other_cell_size_factors = new_calcFactorRLE(in_mat[get_gene_indices(all_other_genes,genes),:])
        # in_mat[get_gene_indices(all_other_genes,genes),:] = do_depth_normalization(in_mat[get_gene_indices(all_other_genes,genes),:], size_factors=all_other_cell_size_factors)
    else:
        underdispersed_genes = get_underdispersed(in_mat,
                                         genes,
                                         z_resid=0.5)
        global_cell_size_factors = new_calcFactorRLE(in_mat[get_gene_indices(underdispersed_genes,genes),:])
        in_mat = do_depth_normalization(in_mat, size_factors=global_cell_size_factors)
    #in_mat = do_depth_normalization(in_mat)
    sparse_convert=False
    if issparse(in_mat):
        sparse_convert = True
        print("   will convert from sparse")
    print("log2(count+offset) transforming")
    print(type(in_mat))
    print(in_mat)
    print(in_mat.shape)
    try:
        out_mat = do_log_offset(in_mat, log_offset)
    except:
        print("hit error trying to do it in memmory, so will do it on the fly row-by-row")
        for i in range(in_mat.shape[0]):
            #in_mat[i,:]=np.arccosh(in_mat[i,:]+1)
            if sparse_convert:
                temp_line = in_mat[i,:].toarray().flatten()
            else:
                temp_line = in_mat[i,:]
            in_mat[i,:]=np.log2(temp_line+log_offset) - np.log2(log_offset)
            #in_mat[i,np.where(in_mat[i,:]<0)] = 0
        out_mat = in_mat
    # sns.clustermap(lin_norm_mat(in_mat[get_gene_indices(all_tech_genes,genes),:]))
    # plt.show()
    if clust_lists is None:
        clust_lists=[list(range(in_mat.shape[1]))]
    # global_complex_scores = get_all_clust_complex_scores(tm_dict, 
    #                                                       in_mat, 
    #                                                       genes, 
    #                                                       cells, 
    #                                                       clust_lists)
    censor_gene_lists = list(tm_dict.values())
    censor_genes=[]
    for temp_list in censor_gene_lists:
        censor_genes+=temp_list
    keep_genes = [gene for gene in genes if gene not in censor_genes]
    # if feat_select_method=="disp":
    #     keep_genes = do_disp_feat_select(in_mat,
    #                                      genes,
    #                                      keep_genes=keep_genes,
    #                                      z_resid=0.5)
    print("double done")
    return(out_mat, keep_genes)





def do_first_round_clust(in_mat, 
                         genes,
                         cells,
                         keep_genes,
                         scratch_dir,
                         clean_dir = False):
    ## write the subset of the matrix 
    first_clust_out_dir = process_dir(scratch_dir)
    first_clust_input_h5 = first_clust_out_dir+"/first_round_input.hdf5"
    f=h5py.File(first_clust_input_h5, "w")
    dset = f.create_dataset("infile",
                           (len(genes),len(cells)),
                           dtype=np.float32)
    for i in range(in_mat.shape[0]):
         dset[i,:] = in_mat[i,:]
    f.close()
    ID_list = first_clust_out_dir+"/ID_list.txt"
    columns = first_clust_out_dir+"/columns.txt"
    make_file('\n'.join(genes),ID_list)
    make_file('\n'.join(["gene"]+cells),columns)
    ## note that the get_big_spearman actually gets the Euclidean dist of Spear corrs
    euc_dist_file = get_big_spearman(scratch_dir, 
                                     first_clust_input_h5, 
                                     ID_list,
                                     columns,
                                     do_hdf5=True,
                                     usable_indices=keep_genes,
                                     block_size=5000)
    working_euc_dist_file = euc_dist_file+"_copy"
    cp(euc_dist_file,working_euc_dist_file)
    f=h5py.File(working_euc_dist_file,"r+")
    first_clust_res = do_louvain_primary_clustering(f["infile"], 
                                                      sample_names = cells,
                                                      percentile = 0.95, 
                                                      flexible_percentile = True, 
                                                      flexible_cap = 200, 
                                                      comp_length_cutoff = 4, 
                                                      out_dir = None,
                                                      resolution=.75)
    f.close()
    ## clean up dir?
    if clean_dir:
        for f in os.listdir(scratch_dir):
            temp_file = os.path.join(scratch_dir, f)
            if os.path.isdir(temp_file):
                shutil.rmtree(temp_file)
            elif os.path.isfile(temp_file):
                os.remove(temp_file)
        return(first_clust_res, None)
    else:
        return(first_clust_res, euc_dist_file)


## get the scratch dir


## first subset the matrix for each of the complexs that we know are from the batch effect & the orphan genes


## calculate the complex scores


## remove the complex related genes


def map_IDs_to_ensg():

    return()

def map_to_mouse_to_get_refs():

    return()

def get_complex_IDs_in_ref():
    return()


## 
def get_complex_dict_from_table(technical_file="/home/scott/bin/sc_norm_bench_v2/data/unified_technical_mmusculus_chromium_v3.tsv"):
    technical_table = read_table(technical_file)
    tm_terms = []
    first = True
    tm_dict = {}
    tr_dict = {}
    for line in technical_table:
        if first:
            first=False
        else:
            if line[0]=="Tm":
                if line[1] in tm_dict:
                    tm_dict[line[1]]=tm_dict[line[1]]+[line[2]]
                else:
                    tm_dict[line[1]]=[line[2]]
            else:
                if line[1] in tr_dict:
                    tr_dict[line[1]]=tr_dict[line[1]]+[line[2]]
                else:
                    tr_dict[line[1]]=[line[2]]
    return(tm_dict)



# all_tm_genes=[]
# tm_gene_dict_for_this_dataset={}
# for tm_complex in tm_complex_names:
#     temp_complex_genes=get_complex_IDs_in_ref(tm_complex_dict[tm_complex], ID_list)
#     tm_gene_dict_for_this_dataset[tm_complex]=temp_complex_genes
#     all_tm_genes+=tm_gene_dict_for_this_dataset[tm_complex]


## do the clustering without tm genes
# * note that this could be replaced with something like a "meta-cell" like object, *
# * but it should be kinda big so there's still some measurable variance *


def lin_norm_row(in_row):
    in_row -= np.min(in_row)
    temp_max = np.max(in_row)
    if temp_max > 0:
        in_row /= max(in_row)
    return(in_row)


def lin_norm_mat(in_mat):
    for i in range(in_mat.shape[0]):
        in_mat[i,:]=lin_norm_row(in_mat[i,:])
    return(in_mat)


### once the clustering is done
def get_complex_scores(temp_clust_mat_subset, do_lin_norm = True):
    temp_maxs = np.max(temp_clust_mat_subset,axis=1)
    print("temp_maxs")
    print(temp_maxs)
    nz_idxs = np.where(temp_maxs>0)[0]
    print(nz_idxs)
    if len(nz_idxs)==0:
        ## if there is no expression of this complex
        return(np.zeros(temp_clust_mat_subset.shape[1]))
    if do_lin_norm:
        temp_clust_mat_subset=temp_clust_mat_subset[nz_idxs,:]
        temp_clust_mat_subset=lin_norm_mat(temp_clust_mat_subset)
    return(lin_norm_row(np.sum(temp_clust_mat_subset,axis=0)))


def get_gene_indices(temp_genes, gene_ref):
    gene_ref_array = np.array(gene_ref)
    pertinent_indices = []
    for temp_gene in temp_genes:
        if temp_gene in gene_ref:
            cur_idx = np.where(gene_ref_array==temp_gene)[0].tolist()
            pertinent_indices+=cur_idx
    pertinent_indices=sorted(pertinent_indices)
    return(pertinent_indices)


#def get_all_clust_complex_scores(tech_dict, in_mat, genes, cells, sample_k_indices):
def get_all_clust_complex_scores(tech_dict, in_mat, genes, sample_k_indices):
    all_tm_complexes=list(tech_dict.keys())
    all_complex_scores = np.zeros((in_mat.shape[1],len(all_tm_complexes)))
    all_results = []
    for temp_clust_indices in sample_k_indices:
        temp_clust_mat = in_mat[:,temp_clust_indices]
        complex_scores={}
        print(temp_clust_mat.shape)
        for i in range(len(all_tm_complexes)):
            tm_complex=all_tm_complexes[i]
            print(tm_complex)
            temp_genes = tech_dict[tm_complex]
            print(temp_genes)
            temp_idxs = get_gene_indices(temp_genes, genes)
            print(temp_idxs)
            temp_scores = np.zeros(len(temp_clust_indices))
            if len(temp_idxs)>0:
                print(temp_clust_mat.shape)
                temp_scores=get_complex_scores(temp_clust_mat[np.array(temp_idxs),:])
            print(temp_scores)
            complex_scores[tm_complex]=temp_scores
        all_results.append(complex_scores)
    return(all_results)


def find_technical_file(technology="chromium_v3",
                        species="mmusculus"):
    ## need to update this to be 
    gaurenteed_file_base_file_name = "unified_technical_mmusculus_chromium_v3.tsv"
    hypothesized_file = "unified_technical_"+str(species)+"_"+str(technology)+".tsv"
    hypothesized_file, is_same_species = find_random_file(hypothesized_file, gaurenteed_file_base_file_name = gaurenteed_file_base_file_name)
    if is_same_species:
        return(hypothesized_file, species)
    else:
        return(hypothesized_file, "mmusculus")
    #return("/home/scott/bin/sc_norm_bench_v2/data/unified_technical_mmusculus_chromium_v3.tsv", species)
    #else:
    #    return("/home/scott/bin/sc_norm_bench_v2/data/unified_technical_mmusculus_chromium_v3.tsv", "mmusculus")


# def do_feat_select(in_mat, genes, censor_genes, **kwargs):
#   return()


# def do_first_round_clust(in_mat, scratch_dir, tech_dict, **kwargs):
#   do_feat_select(,**kwargs)
#   return()



def process_tsv(in_file, as_sparse=False, as_hdf5=False, hdf5_file=None):
    ## first go through & get dims
    first = True
    nrow = -1
    genes = []
    for line in fileinput.input(in_file):
        nrow+=1
        if first:
            first = False
            temp_line=strip_split(line)
            ncol = len(temp_line)-1
            cells = temp_line[1:]
        else:
            temp_line=strip_split(line)
            genes.append(temp_line[0])
    fileinput.close()
    ## now that we have the dims, make and populate the matrix
    if as_sparse:
        full_expression = lil_mat((nrow, ncol),dtype=np.float32)
    elif as_hdf5:
        full_expression = None
    else:
        full_expression = np.zeros((nrow, ncol),dtype=np.float32)
    nrow = -2
    first = True
    for line in fileinput.input(in_file):
        nrow+=1
        if first:
            first = False
            temp_line=strip_split(line)
            ncol = len(temp_line)-1
            cells = temp_line[1:]
        else:
            #print(nrow)
            temp_line=strip_split(line)
            full_expression[nrow,:]=temp_line[1:]
    fileinput.close()
    return(full_expression, cells, genes)


def summarize_cor_mat(temp_spear_mat_subset, tech_factor_indices, z_cut=3.5, max_cut=0.9):
    all_cors = np.zeros((temp_spear_mat_subset.shape[1],len(tech_factor_indices)))
    all_sig = np.zeros((temp_spear_mat_subset.shape[1],len(tech_factor_indices)), dtype=bool)
    for i in range(len(tech_factor_indices)):
        ## the first one is the real correlation & the rest are the null shuffled versions
        temp_real_idx = tech_factor_indices[i][0]
        temp_null_idxs = tech_factor_indices[i][1:]
        real = temp_spear_mat_subset[temp_real_idx,:]
        all_cors[:,i] = real
        for j in range(temp_spear_mat_subset.shape[1]):
            temp_nulls = temp_spear_mat_subset[temp_null_idxs,j]
            dist_to_mean = real[j] - np.mean(temp_nulls)
            temp_z = dist_to_mean/np.std(temp_nulls)
            if temp_z>z_cut or real[j]>=max_cut:
            #if real[j]>np.max(temp_spear_mat_subset[temp_null_idxs,j]):
                all_sig[j,i]=True
        ## if the correlation was 1, then make it true, even if the maximum of the nulls 
        ## was also 1 - no way to say it's real or fake then. So go with the 
        ## cautious assumption that it's technical
        perfect_cor_idxs = np.where(real==1)[0]
        all_sig[perfect_cor_idxs,i]=True
    return(all_cors, all_sig)


def get_cors(technical_factors, in_mat, null_size=2500, bin_size=5000, z_cut=7.5, max_cut=0.9):
    ## first create the null distribution for technical factors
    tech_null_rows = technical_factors.shape[0]*(null_size+1)
    technical_and_null_mat=np.zeros((tech_null_rows,in_mat.shape[1]))
    counter=0
    tech_factor_indices = []
    for i in range(technical_factors.shape[0]):
        ## load the technical factors
        temp_indices = [counter]
        temp_technical = technical_factors[i,:]
        technical_and_null_mat[counter,:] = temp_technical
        counter+=1
        for i in range(null_size):
            temp_indices += [counter]
            technical_and_null_mat[counter,:] = np.random.shuffle(temp_technical)
            counter+=1
        tech_factor_indices.append(temp_indices)
    ## now go through all rows 
    nrows = in_mat.shape[0]
    bin_size = min([bin_size,math.ceil(nrows/2)])
    ## get bins
    all_bins = get_bins(nrows, bin_size=bin_size)
    ## set up the output matrix
    all_factor_cors = np.zeros((in_mat.shape[0], technical_factors.shape[0]), dtype = np.float32)
    all_factor_sig = np.zeros((in_mat.shape[0], technical_factors.shape[0]), dtype = bool)
    for i in range(len(all_bins)-1):
        start=all_bins[i]
        end=all_bins[i+1]
        print("technical_and_null_mat.shape")
        print(technical_and_null_mat.shape)
        print("in_mat[start:end,:].shape")
        print(in_mat[start:end,:].shape)
        temp_spear_mat = no_p_spear(technical_and_null_mat.T,in_mat[start:end,:].T)
        print("temp_spear_mat.shape")
        print(temp_spear_mat.shape)
        ## tech & null in rows, target genes in cols
        temp_spear_mat_subset = temp_spear_mat[:tech_null_rows,tech_null_rows:]
        temp_spear_mat_subset[np.isnan(temp_spear_mat_subset)] = 0
        print("temp_spear_mat_subset.shape")
        print(temp_spear_mat_subset.shape)
        temp_cors, temp_sig = summarize_cor_mat(temp_spear_mat_subset, tech_factor_indices, z_cut=z_cut, max_cut=max_cut)
        print(temp_cors)
        print(temp_sig)
        all_factor_cors[start:end, :]=temp_cors
        all_factor_sig[start:end, :]=temp_sig
    return(all_factor_sig)


def get_within_cluster_correlations_with_technical(in_mat,
                                                   cluster_lists,
                                                   all_complex_scores,
                                                   genes,
                                                   min_num_clusts_with_sig = None):
    if min_num_clusts_with_sig is None:
        min_num_clusts_with_sig = max([1,np.log(len(cluster_lists))])
    ##
    all_cor_res=[]
    for i in range(len(cluster_lists)):
        temp_technical_factors = process_temp_complex_scores(pd.DataFrame(all_complex_scores[i]))
        all_cor_res.append(get_cors(temp_technical_factors.T, in_mat[:,cluster_lists[i]]))
    ## now go through each of the clusters & count the number of times a gene was significantly 
    ## correlated with a technical effect
    out_num_sigs=np.zeros(in_mat.shape[0])
    for i in range(len(cluster_lists)):
        temp_sig_idxs = np.where(all_cor_res[i]==True)[0]
        out_num_sigs[temp_sig_idxs] = out_num_sigs[temp_sig_idxs]+1
    out_percent_sigs = out_num_sigs/len(cluster_lists)
    #is_sig_over_cutoff = np.zeros(in_mat.shape[0],dtype=bool)
    #is_sig_over_cutoff[sig_idxs]=True
    sig_idxs = np.where(out_num_sigs>=min_num_clusts_with_sig)[0]
    if len(sig_idxs)==0:
        return([])
    sig_genes=np.array(genes)[sig_idxs].tolist()
    print("out_percent_sigs")
    print(out_percent_sigs)
    print("out_num_sigs")
    print(out_num_sigs)
    print("len(sig_idxs)")
    print(len(sig_idxs))
    for i in range(len(cluster_lists)+1):
        print("    num sig cors:",i,":",len(np.where(out_num_sigs>=i)[0]))
    return(pd.DataFrame({"genes":genes,"number_of_significant":out_num_sigs,"percent_sig":out_percent_sigs}))


def get_censor_list_from_tech_dict(tm_dict):
    censor_gene_lists = list(tm_dict.values())
    censor_genes=[]
    for temp_list in censor_gene_lists:
        censor_genes+=temp_list
    return(censor_genes)


def update_censor_list(tm_dict, new_genes, genes):
    censor_genes = get_censor_list_from_tech_dict(tm_dict)
    keep_genes = [gene for gene in genes if gene not in censor_genes]
    additional_sig_genes = new_genes + censor_genes
    additional_sig_genes=list(set(additional_sig_genes))
    return(additional_sig_genes)


def do_single_batch_hammer_correction(in_mat, genes, cells, tech_dict, scratch_dir):
    ## RLE norm and log transfrom
    tm_genes = get_censor_list_from_tech_dict(tech_dict)
    ## consider removing tm_genes up here!
    in_mat, b_tr_keep_genes = rm_technical_and_perform_var_stabilization(in_mat,
                                                                       tech_dict,
                                                                       genes)
    return(in_mat)
    # ##################################
    # ##################################
    # ##################################
    # ##################################
    # clust_res, neg_euc_hdf5_file = do_first_round_clust(in_mat, 
    #                                                      genes,
    #                                                      cells,
    #                                                      get_gene_indices(b_tr_keep_genes,genes),
    #                                                      os.path.join(scratch_dir,"b_tr_clust"),
    #                                                      clean_dir = True)
    # all_complex_scores = get_all_clust_complex_scores(tech_dict, 
    #                                                   in_mat, 
    #                                                   genes, 
    #                                                   cells, 
    #                                                   clust_res.cluster_indices)
    # #############################################
    # # additional_sig_genes = get_within_cluster_correlations_with_technical(in_mat,
    # #                                                                  cluster_lists,
    # #                                                                  all_complex_scores,
    # #                                                                  genes)
    # # print("originally had ",len(tm_genes)," genes in Tm")
    # # all_censor_genes = update_censor_list(tech_dict, all_cor_results, genes)
    # # tr_genes = [temp_gene for temp_gene in all_censor_genes if temp_gene not in tm_genes]
    # # print("re-doing feature selection censoring both Tm and Tr genes")
    # # print("    censoring",len(all_censor_genes),"genes")
    # ## now re-do all of the feature selection
    # # b_keep_genes = do_disp_feat_select(in_mat, genes, censor_genes = all_censor_genes, z_resid=0.5)
    # ##############################################
    # keep_genes = do_disp_feat_select(in_mat, genes, censor_genes = tm_genes, z_resid=0.5)
    # print("found",len(keep_genes),"good features in the set B, that appear to be DEG, but orthogonal to technical")
    # clust_res, neg_euc_hdf5_file = do_first_round_clust(in_mat, 
    #                                                      genes,
    #                                                      cells,
    #                                                      get_gene_indices(keep_genes,genes),#
    #                                                      scratch_dir,
    #                                                      clean_dir = False)
    # weighted_medoid_mat = get_weighted_medoid_dist_mat(clust_res.cluster_centers_indices_,
    #                                                    in_h5=neg_euc_hdf5_file)
    # out_h5=scratch_dir+"/normalized_counts_log2.hdf5"
    # out_h5_file = fine_tune_technical_correction_with_clusters(in_mat,
    #                                                                tech_dict,
    #                                                                genes,
    #                                                                cells,
    #                                                                clust_res.cluster_indices,
    #                                                                out_h5)
    # # out_h5_file = fine_tune_technical_correction_with_clusters_local_weight(in_mat,
    # #                                                                    tech_dict,
    # #                                                                    genes,
    # #                                                                    cells,
    # #                                                                    clust_res.cluster_indices,
    # #                                                                    out_h5,
    # #                                                                    weighted_medoid_mat)
    # ID_list = os.path.join(scratch_dir+"ID_list.txt")
    # columns = os.path.join(scratch_dir+"columns.txt")
    # make_file('\n'.join(genes),ID_list)
    # make_file('\n'.join(["gene"]+cells),columns)
    # if return_sparse_mat:
    #     f=h5py.File(out_h5_file,'r')
    #     out_mat = np.zeros(f["infile"].shape)
    #     for i in range(f["infile"].shape[0]):
    #         out_mat[i,:]=f["infile"][i,:]
    #     f.close()
    # return(out_h5_file)
    # ##################################
    # ##################################
    # ##################################
    # ##################################


def merge_runs(in_h5s, in_genes, in_cells):
    return()


def filter_gene_set(gene_list, keep_set):
    return()


def find_shared_genes(genes_1, genes_2):
    keep_set=set(genes_1).intersection(set(genes_2))
    return(keep_rows_1, keep_rows_2)

def rarrange_kept_rows(in_mat, keep_rows_1):
    return(in_mat)


def convert_heme_to_zeros(in_mat, genes, tech_dict):
    heme_genes = tech_dict["hemoglobin"]
    idx_lookup = {value:key for key, value in enumerate(genes)}
    for heme in heme_genes:
        in_mat[idx_lookup[heme],:]=0
    return(in_mat)


def get_dicts(results, genes, convert_idx=3):
    original_to_ensg_dict={gene:[] for gene in genes}
    ensg_to_original_dict={}
    all_ensgs = []
    ## set up the dictionary
    for i in range(1,len(results)):
        temp_gene = genes[int(results[i][0])-1]
        temp_lookup = original_to_ensg_dict[temp_gene]
        #print(results[i][convert_idx])
        if results[i][convert_idx] is None:
            original_to_ensg_dict[temp_gene] = temp_lookup + []
        else:
            original_to_ensg_dict[temp_gene] = temp_lookup + [results[i][convert_idx]]
        if results[i][convert_idx] not in ensg_to_original_dict:
            ensg_to_original_dict[results[i][convert_idx]] = []
        temp_ensg_list = ensg_to_original_dict[results[i][convert_idx]]
        ensg_to_original_dict[results[i][convert_idx]] = temp_ensg_list + [temp_gene]
    return(original_to_ensg_dict, ensg_to_original_dict)


def get_ensg_lookup(genes, species):
    gene_symbol_dict, gene_def_dict, results = convert_to_ensg(genes, species=species)
    original_to_ensg_dict, ensg_to_original_dict = get_dicts(results, genes)
    return(original_to_ensg_dict, ensg_to_original_dict )


def get_tech_to_target_species(all_tech_genes, source_species, species):
    if source_species==species:
        print(all_tech_genes[:5])
        print(species)
        gene_symbol_dict, gene_def_dict, results = convert_to_ensg(all_tech_genes, species=species)
        print(results[:5])
        original_to_target_species_ensg_dict, target_species_ensg_to_original_dict = get_dicts(results, all_tech_genes, convert_idx=3)
    else:
        gene_symbol_dict, gene_def_dict, results = convert_to_human(all_tech_genes, source_species, target_species=species)
        original_to_target_species_ensg_dict, target_species_ensg_to_original_dict = get_dicts(results, all_tech_genes, convert_idx=4)
    return(original_to_target_species_ensg_dict, target_species_ensg_to_original_dict, gene_symbol_dict)


def find_malat1(species, target_species_ensg_to_original_dict):
    symbol_dict, def_dict, results = convert_to_ensg(["malat1"], species="hsapiens")
    if results is None:
        return([])
    out_malat=[]
    if len(results)>2:
        for i in range(1,len(results)):
            if results[i][3] in target_species_ensg_to_original_dict:
                out_malat.append(results[i][3])
    return(out_malat)


def update_tech_dict(tech_dict,
                     original_to_ensg_dict,
                     ensg_to_original_dict,
                     original_to_target_species_ensg_dict,
                     target_species_ensg_to_original_dict,
                     tech_gene_to_symbol,
                     species):
    converted_tech_dict={}
    symbol_lookup_dict={}
    for temp_term in list(tech_dict.keys()):
        symbol_lookup_dict[temp_term]=[]
        print(temp_term)
        temp_gene_list = []
        for i in range(len(tech_dict[temp_term])):
            temp_start_gene = tech_dict[temp_term][i]
            target_species_ensg = original_to_target_species_ensg_dict[temp_start_gene]
            temp_map_list = []
            for j in range(len(target_species_ensg)):
                if target_species_ensg[j] in ensg_to_original_dict:
                    temp_map_list=temp_map_list+ensg_to_original_dict[target_species_ensg[j]]
            if len(temp_map_list)==0:
                temp_symbol_lookup=symbol_lookup_dict[temp_term]
                symbol_lookup_dict[temp_term]=temp_symbol_lookup+tech_gene_to_symbol[temp_start_gene]
            print("    ",temp_start_gene, temp_map_list)
            temp_gene_list=temp_gene_list+temp_map_list
            #print(temp_map_list)
        converted_tech_dict[temp_term]=temp_gene_list
    # ## this one is important especially since there's only one gene
    # if len(converted_tech_dict["MALAT1"])==0:
    #     converted_tech_dict["MALAT1"]=find_malat1(species, target_species_ensg_to_original_dict)
    # print(symbol_lookup_dict)
    print("finished")
    return(converted_tech_dict)


def update_complex_dict(tech_dict, 
                        genes, 
                        species="mmusculus", 
                        source_species="mmusculus"):
    ## no matter what we're going to need to make sure we're in ensmebl
    original_to_ensg_dict, ensg_to_original_dict = get_ensg_lookup(genes, species)
    all_tech_genes = get_censor_list_from_tech_dict(tech_dict)
    ## if the reference species is correct & already ensembl, then this should just
    ## be a dictionary of ensemble genes equaling themselves (but in lists)
    ## otherwise the below will give symmetrically look-up-able
    original_to_target_species_ensg_dict, target_species_ensg_to_original_dict, tech_gene_to_symbol = get_tech_to_target_species(all_tech_genes, source_species, species)
    updated_tech_dict = update_tech_dict(tech_dict,
                                         original_to_ensg_dict,
                                         ensg_to_original_dict,
                                         original_to_target_species_ensg_dict,
                                         target_species_ensg_to_original_dict,
                                         tech_gene_to_symbol,
                                         species)
    #updated_tech_dict=tech_dict
    return(updated_tech_dict)


def run_tm_norm(in_mat, 
                genes, 
                species="mmusculus",
                platform="chromium_v3",
                technical_file=None,
                censor_heme=True):
    if technical_file is None:
        technical_file, source_species = find_technical_file(species=species, technology=platform)
    tech_dict = get_complex_dict_from_table(technical_file=technical_file)
    tech_dict = update_complex_dict(tech_dict, genes, species=species, source_species=source_species)
    out_mat, keep_genes = rm_technical_and_perform_var_stabilization(in_mat,
                                               tech_dict,
                                               genes)
    print("continuing")
    if censor_heme:
        print("censoring heme related genes")
        out_mat = convert_heme_to_zeros(out_mat,
                                         genes,
                                         tech_dict)
    return(out_mat)


def run_batch_hammer(in_mat=None,
                     genes=None,
                     cells=None,
                     batch_table=None,
                     in_file_list=None,
                     id_list_file=None,
                     col_ids_file=None,
                     return_sparse_mat=False,
                     is_h5=False,
                     h5_mat_key="infile",
                     mask_tm = True,
                     scratch_dir = None,
                     technical_file=None,
                     species="mmusculus",
                     technology="chromium_v3",
                     censor_heme=True,
                     temp_scratch=None,
                     **kwargs):
    ## do it all on the individual datasets
    #########################################
    ## TODO: update all_datasets to have wrappers 
    ## for variable input types. Just doing tsvs for 
    ## prototyping
    all_datasets=in_file_list
    ## we assume this is in count format
    if technical_file is None:
        technical_file = find_technical_file()
    tech_dict = get_complex_dict_from_table(technical_file=technical_file)
    ## update dict ref if necessary
    in_mat = do_single_batch_hammer_correction(in_mat,
                                         genes,
                                         cells,
                                         tech_dict,
                                         temp_scratch)
    if censor_heme:
        in_mat = convert_heme_to_zeros(in_mat,
                                         genes,
                                         tech_dict)
    return(in_mat)
    # ##################################
    # ##################################
    # ##################################
    # all_output_datasets = []
    # for i in range(all_datasets):
    #     temp_scratch = process_dir(scratch_dir+"/dset_"+str(i))
    #     all_output_datasets.append(do_single_batch_hammer_correction(in_mat,
    #                                                                  genes,
    #                                                                  cells,
    #                                                                  tech_dict,
    #                                                                  temp_scratch))
    # ## once we're done doing the within batch technical correction
    # ## merge them and do it again
    # final_output_file = merge_runs(all_output_datasets)
    # if return_sparse_mat:
    #     f=h5py.File(out_h5_file,'r')
    #     out_mat = np.zeros(f["infile"].shape)
    #     for i in range(f["infile"].shape[0]):
    #         out_mat[i,:]=f["infile"][i,:]
    #     f.close()
    #     return(out_mat)
    # else:
    #     return(out_h5_file)
    # ##################################
    # ##################################
    # ##################################
    # ##################################


if __name__ == '__main__':
    technical_file="/home/scott/bin/sc_norm_bench_v2/data/unified_technical_mmusculus_chromium_v3.tsv"
    in_tsvs = ["/home/scott/Downloads/DUMMY/neuron_1k_v3.tsv","/home/scott/Downloads/DUMMY/neuron_10k_v3.tsv"]#,"/home/scott/Downloads/DUMMY/intestine_norm.tsv"]
    scratch_dir='/home/scott/Downloads/DUMMY/dummy_dir/'
    tech_dict = get_complex_dict_from_table(technical_file=technical_file)
    in_mat = None
    cells = []
    batch_vect = []
    for i in range(len(in_tsvs)):
        temp_mat, temp_cells, temp_genes = process_tsv(in_tsvs[i])
        if in_mat is None:
            in_mat = temp_mat
            genes = temp_genes
        else:
            keep_rows_1, keep_rows_2 = find_shared_genes(genes,temp_genes)
            in_mat = rarrange_kept_rows(in_mat, keep_rows_1)
            temp_mat = rarrange_kept_rows(temp_mat, keep_rows_2)
            in_mat = np.concatenate((in_mat[keep_rows,:], temp_mat), axis=1)
        cells += ["batch"+str(i)+"_"+bcode for bcode in temp_cells]
        batch_vect += ["batch"+str(i) for bcode in temp_cells]
        # in_mat_1, cells, genes = process_tsv(in_tsvs[0])
        # in_mat_2, cells, genes = process_tsv(in_tsvs[1])
    in_mat = np.concatenate(tuple(in_mat_list), axis=1)
    del(in_mat_list)




#######################################################
#######################################################
#######################################################
#######################################################
# #######################################################

# tm_genes = get_censor_list_from_tech_dict(tech_dict)
# ## consider removing tm_genes up here!
# in_mat, b_tr_keep_genes = rm_technical_and_perform_var_stabilization(in_mat,
#                                                                    tech_dict,
#                                                                    genes,
#                                                                    cells)

# ###########################################
# # keep_genes = do_disp_feat_select(in_mat,
# #                                           genes,
# #                                           censor_genes=tm_genes,
# #                                           z_resid=0.5)

# # sns.clustermap(lin_norm_mat(in_mat[get_gene_indices(keep_genes,genes),:]))
# # plt.show()

# # ######
# # non_heme_tech = [gene for gene in get_tm_genes_from_dict(tm_dict) if gene not in tm_dict["hemoglobin"]]
# # global_cell_size_factors = new_calcFactorRLE(in_mat[get_gene_indices(non_heme_tech,genes),:])
# # in_mat_norm = do_depth_normalization(in_mat, size_factors=global_cell_size_factors)
# #
# # sparse_convert=False
# # if issparse(in_mat):
# #     sparse_convert = True
# #
# #
# # for i in range(in_mat.shape[0]):
# #     #in_mat[i,:]=np.arccosh(in_mat[i,:]+1)
# #     if sparse_convert:
# #         temp_line = in_mat[i,:].toarray().flatten()
# #     else:
# #         temp_line = in_mat[i,:]
# #     in_mat[i,:]=np.log2(temp_line+12) - np.log2(12)
# #     in_mat[i,np.where(in_mat[i,:]<0)] = 0
# #
# # #######

# # keep_genes = do_disp_feat_select(in_mat,
# #                                           genes,
# #                                           censor_genes=tm_genes,
# #                                           z_resid=0.5)


# sns.clustermap(lin_norm_mat(in_mat_norm[get_gene_indices(keep_genes,genes),:]))
# plt.show()


# clust_res, neg_euc_hdf5_file = do_first_round_clust(in_mat, 
#                                                      genes,
#                                                      cells,
#                                                      get_gene_indices(keep_genes,genes),
#                                                      os.path.join(scratch_dir,"tm_norm_only"),
#                                                      clean_dir = True)


# batch_by_clust_table = pd.DataFrame({"batch":["b1" for i in range(in_mat_1.shape[1])]+["b2" for i in range(in_mat_2.shape[1])],"labels":clust_res.labels_})
# summary_table = batch_by_clust_table.groupby(["batch","labels"]).size()
# summary_table = summary_table.unstack().T
# "b1<-c("+",".join(map(str,summary_table["b1"]))+")"
# "b2<-c("+",".join(map(str,summary_table["b2"]))+")"
# PercentMaxDiff::pmd(as.matrix(cbind(b1,b2)))

# ###########################################

# clust_res, neg_euc_hdf5_file = do_first_round_clust(in_mat, 
#                                                      genes,
#                                                      cells,
#                                                      get_gene_indices(b_tr_keep_genes,genes),
#                                                      os.path.join(scratch_dir,"b_tr_clust"),
#                                                      clean_dir = True)


# all_complex_scores = get_all_clust_complex_scores(tech_dict, 
#                                                   in_mat, 
#                                                   genes, 
#                                                   cells, 
#                                                   clust_res.cluster_indices)



# additional_sig_genes = get_within_cluster_correlations_with_technical(in_mat,
#                                                                  clust_res.cluster_indices,
#                                                                  all_complex_scores,
#                                                                  genes)





# print("originally had ",len(tm_genes)," genes in Tm")
# all_censor_genes = update_censor_list(tech_dict, additional_sig_genes, genes)
# tr_genes = [temp_gene for temp_gene in all_censor_genes if temp_gene not in tm_genes]
# print("re-doing feature selection censoring both Tm and Tr genes")
# print("    censoring",len(all_censor_genes),"genes")
# ## now re-do all of the feature selection
# b_keep_genes = do_disp_feat_select(in_mat, genes, censor_genes = all_censor_genes, z_resid=0.5)
# print("found",len(keep_genes),"good features in the set B, that appear to be DEG, but orthogonal to technical")

# sns.clustermap(in_mat[get_gene_indices(b_keep_genes,genes),:])
# plt.show()


# clust_res, neg_euc_hdf5_file = do_first_round_clust(in_mat, 
#                                                      genes,
#                                                      cells,
#                                                      get_gene_indices(b_keep_genes,genes),
#                                                      scratch_dir,
#                                                      clean_dir = False)





# #######################################################################

# in_mat, keep_genes = rm_technical_and_perform_var_stabilization(in_mat,
#                                                                    tech_dict,
#                                                                    genes,
#                                                                    cells_merged)
# sns.clustermap(in_mat[get_gene_indices(keep_genes,genes),:])
# plt.show()

# clust_res, neg_euc_hdf5_file = do_first_round_clust(in_mat, 
#                                      genes,
#                                      cells_merged,
#                                      get_gene_indices(keep_genes,genes),
#                                      scratch_dir)




# weighted_medoid_mat = get_weighted_medoid_dist_mat(clust_res.cluster_centers_indices_,
#                                                        in_h5=neg_euc_hdf5_file)
# out_h5=scratch_dir+"/normalized_counts_log2.hdf5"
# out_h5_file = fine_tune_technical_correction_with_clusters(in_mat,
#                                                                    tech_dict,
#                                                                    genes,
#                                                                    cells_merged,
#                                                                    clust_res.cluster_indices,
#                                                                    out_h5)

# # out_h5_file = fine_tune_technical_correction_with_clusters_local_weight(in_mat,
# #                                                                    tech_dict,
# #                                                                    genes,
# #                                                                    cells,
# #                                                                    clust_res.cluster_indices,
# #                                                                    out_h5,
# #                                                                    weighted_medoid_mat)

# ID_list = os.path.join(scratch_dir+"ID_list.txt")
# columns = os.path.join(scratch_dir+"columns.txt")
# make_file('\n'.join(genes),ID_list)
# make_file('\n'.join(["gene"]+cells_merged),columns)

# f=h5py.File(out_h5_file,'r')
# out_mat = np.zeros(f["infile"].shape)
# for i in range(f["infile"].shape[0]):
#     out_mat[i,:]=f["infile"][i,:]


# f.close()


# disp_table = do_over_dispers_feat_select(in_mat=out_mat, ID_list = genes)
# disp_table[disp_table["bool"]=="True"]
# centered = disp_table["mean_var_residuals"]-np.mean(disp_table["mean_var_residuals"])
# standardized_resids = centered/np.std(centered)
# keep_idxs = np.where(standardized_resids>=1)[0]
# keep_genes = disp_table.iloc[keep_idxs]["gene"]



# sns.clustermap(out_mat[get_gene_indices(keep_genes,genes),:])
# plt.show()

# sns.clustermap(lin_norm_mat(out_mat[get_gene_indices(keep_genes,genes),:]) )
# plt.show()


# ##################################


# disp_table = do_over_dispers_feat_select(in_mat=out_mat_merged, ID_list = genes)
# disp_table[disp_table["bool"]=="True"]
# centered = disp_table["mean_var_residuals"]-np.mean(disp_table["mean_var_residuals"])
# standardized_resids = centered/np.std(centered)
# keep_idxs = np.where(standardized_resids>=1)[0]
# keep_genes = disp_table.iloc[keep_idxs]["gene"]

# sns.clustermap(out_mat[get_gene_indices(keep_genes,genes),:])
# plt.show()

# sns.clustermap(lin_norm_mat(do_depth_normalization(out_mat)[get_gene_indices(keep_genes,genes),:]))
# plt.show()


# #########


# disp_table = do_over_dispers_feat_select(in_mat=out_mat, ID_list = genes)
# keep_genes = list(disp_table[disp_table["bool"]=="True"]["gene"])
# merged_scratch_dir_2=process_dir(os.path.join(scratch_dir, "merged_2"))
# #merged_scratch_dir = process_dir(os.path.join(scratch_dir,"merged/"))
# merged_clust_res, out_neg_euc_dist_file = do_first_round_clust(out_mat, 
#                                          genes,
#                                          cells_merged,
#                                          get_gene_indices(keep_genes,genes),
#                                          merged_scratch_dir_2)
# batch_by_clust_table = pd.DataFrame({"batch":["b1" for i in range(in_mat_1.shape[1])]+["b2" for i in range(in_mat_2.shape[1])],"labels":merged_clust_res.labels_})
# summary_table = batch_by_clust_table.groupby(["batch","labels"]).size()
# summary_table = summary_table.unstack().T

# #############################
# disp_table = do_over_dispers_feat_select(in_mat=out_mat_merged_norm, ID_list = genes)
# keep_genes = list(disp_table[disp_table["bool"]=="True"]["gene"])
# merged_scratch_dir = process_dir(os.path.join(scratch_dir,"merged_2_norm/"))
# merged_clust_res = do_first_round_clust(out_mat_merged_norm, 
#                                          genes,
#                                          cells_merged,
#                                          get_gene_indices(keep_genes,genes),
#                                          merged_scratch_dir)

# batch_by_clust_table = pd.DataFrame({"batch":["b1" for i in range(in_mat_1.shape[1])]+["b2" for i in range(in_mat_2.shape[1])],"labels":merged_clust_res[0].labels_})
# summary_table = batch_by_clust_table.groupby(["batch","labels"]).size()
# summary_table = summary_table.unstack().T

# sns.clustermap(lin_norm_mat(out_mat[:500,:]))
# plt.show()


#     run_batch_hammer(,
#                      in_mtxs = [],
#                      technical_file=technical_file)




# clust_res, neg_euc_hdf5_file = do_first_round_clust(in_mat, 
#                                                       genes,
#                                                       cells,
#                                                       get_gene_indices(keep_genes,genes),
#                                                       os.path.join(scratch_dir,"tm_norm_only"),
#                                                       clean_dir=True)


