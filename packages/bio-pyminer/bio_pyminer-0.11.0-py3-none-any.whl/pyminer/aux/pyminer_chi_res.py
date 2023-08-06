#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
import pandas as pd
from scipy.stats.contingency import margins
from scipy.stats import chi2,chi2_contingency
import seaborn as sns
from matplotlib import pyplot as plt

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
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-input_file", "-i","-infiles",
    help="the file containing the contingency table")
parser.add_argument("-out",
    help="directory for output")
parser.add_argument("-negative_control","-neg_ctrl","-neg","-n",
    help="the name of the treatment that is the negative control. This changes the stats from a test of independence to a goodness of fit relative to the negative control.")
    
args = parser.parse_args()
########################################################
if args.out[-1] != '/':
    args.out+='/'
########################################################

########################################################################
## statistics functions 
def residuals(observed, expected):
     return (observed - expected) / np.sqrt(expected)

def stdres(observed, expected):
     n = observed.sum()
     rsum, csum = margins(observed)
     v = csum * rsum * (n - rsum) * (n - csum) / n**3
     return (observed - expected) / np.sqrt(v)

def adj_res(observed,expected=None):
    ## https://journals.sagepub.com/doi/pdf/10.1177/0013164403251280
    n=observed.sum()
    rsum, csum =  margins(observed)
    #print("margins\n",rsum,csum)
    if type(expected)!=type(None):
    	F=expected
    else:
	    F=rsum*csum/n
    #print("F\n",F)
    res = (observed-F)/np.sqrt(F)
    z_adj_res = res/np.sqrt((1-rsum/n)*(1-csum/n))
    return(z_adj_res)

def res_to_p(residual, dof):
	chi = residual**2
	p = 1 - chi2.cdf(chi, dof)
	return(p)

def cont_to_p_independent(observed,leave_out = None):
    if leave_out != None:
        row_vect = np.arange(np.shape(observed)[0]).tolist()
        ## remove the left out index
        row_vect.pop(leave_out)
        row_vect = np.array(row_vect)
        observed = observed[row_vect,:]
    chi2, p, dof, expected = chi2_contingency(observed)
    #print("traditional expected\n",expected)
    adjusted_residuals = adj_res(observed)
    p = res_to_p(adjusted_residuals,dof)
    p = correct_pvalues_for_multiple_testing(p)
    return(p, adjusted_residuals)

def cont_to_p_relative(observed,col_index,leave_out = None):
    ## if we need to leave out a row, leave it out
    if leave_out != None:
        row_vect = np.arange(np.shape(observed)[0]).tolist()
        ## remove the left out index
        row_vect.pop(leave_out)
        row_vect = np.array(row_vect)
        observed = observed[row_vect,:]
    ## calculate the column sums
    csum = np.sum(observed,axis=0)
    ## calculate the expected relative proportions and counts
    col_expected_proportions = observed[:,col_index]/csum[col_index]
    expected = np.zeros(np.shape(observed))
    for i in range(0,np.shape(observed)[1]):
        expected[:,i]=col_expected_proportions * csum[i]
    ## make the minimum expected value 1...
    num_expected_zero = np.sum(expected == 0)
    if num_expected_zero >0:
        print('\tWARNING: we found',num_expected_zero,'fields that had an expected value == 0. P-values may be a bit wonky...')
        expected[expected == 0] = 1
    #print("\n\nexpected\n",expected)
    ## calculate the chi-square table and dof
    chi_table = ((observed - expected)**2)/expected
    ## degree of freedom is calculate as per usual with one except. We subtract the number of cells from the negative control, because we already know their values.
    dof = observed.size - sum(observed.shape) + observed.ndim - 1 - observed.shape[1]
    #print("\n\nchi table\n",chi_table)
    ## calculate the residuals
    adjusted_residuals = adj_res(observed,expected=expected)
    #print("\n\nadjusted_residuals\n",adjusted_residuals)
    p = res_to_p(adjusted_residuals,dof)
    p = correct_pvalues_for_multiple_testing(p)
    return(p, adjusted_residuals)

def reinsert_missing_row(table,index):
    temp_table=[]
    temp_table = np.zeros((table.shape[0]+1,table.shape[1]))
    #print(temp_table.shape)
    temp_table[:index,:] = table[:index,:]
    temp_table[index,:] = np.nan
    temp_table[index+1:,:] = table[index:,:]
    # for i in range(0,np.shape(table)[0]):
    #     if i != index:
    #         temp_table.append(table[i,:].tolist())
    #     else:
    #         temp_table.append([np.nan]*np.shape(table)[1])
    # temp_table = np.array(temp_table)
    return(temp_table)

def leave_one_out_chi(observed,col_index=None,gof=False):
    ## leave one out relative goodness of fit
    p_list = []
    adj_res_list = []
    ## go through each row, leaving it out
    for i in range(0,np.shape(observed)[0]):
        if gof:
            temp_p, temp_adj_res = cont_to_p_relative(observed, col_index, leave_out=i)
        else:
            temp_p, temp_adj_res = cont_to_p_independent(observed, leave_out=i)
        # print(temp_p.shape)
        # print(temp_adj_res.shape)
        temp_p = reinsert_missing_row(temp_p,i)
        temp_adj_res = reinsert_missing_row(temp_adj_res,i)
        # print(temp_p.shape)
        # print(temp_adj_res.shape)
        # sys.exit()
        p_list.append(temp_p)
        adj_res_list.append(temp_adj_res)
    ## get the maximum p-values and min abs_value
    # for i in range(0,len(adj_res_list)):
    #     print(p_list[i])
    #     print(adj_res_list[i])
    p_list = np.array(p_list)
    adj_res_list = np.array(adj_res_list)
    ## get the minimum abs residual, and maximum p-values
    p_list = np.nanmax(p_list,axis=0)
    #print("\n\nfinal p-value matrix:\n",p_list)
    adj_res_mat = np.zeros(p_list.shape)
    for i in range(0,adj_res_list.shape[1]):
        for j in range(0,adj_res_list.shape[2]):
            # print("\n")
            # print(abs(adj_res_list[:,i,j]))
            temp_argmax = np.nanargmin(abs(adj_res_list[:,i,j]))
            # print(temp_argmax,i,j)
            # print(adj_res_list[temp_argmax,i,j])
            #sys.exit()
            adj_res_mat[i,j]=adj_res_list[temp_argmax,i,j]
    # print("\nmin indices:\n",min_indices)
    # adj_res_list = adj_res_list[min_indices]
    print("\n\nfinal adj residual matrix:\n",adj_res_mat)
    print(p_list.shape,adj_res_mat.shape)
    #sys.exit()
    return(p_list,adj_res_mat)


########################################################

## this function was adopted from emre's stackoverflow answer found here:
## https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python
def correct_pvalues_for_multiple_testing(pvalues, correction_type = "Benjamini-Hochberg"):                
    """                                                                                                   
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    from numpy import array, empty
    pvalues = array(pvalues)

    ## convert to linear if needed
    #print(pvalues)
    if len(np.shape(pvalues)) > 1:
    	needs_reshaping = True
    	original_shape = np.shape(pvalues)
    	new_shape = pvalues.size
    	#print(new_shape)
    	pvalues = pvalues.reshape((new_shape))
    	#print(pvalues)
    else:
    	needs_reshaping = False

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
    if needs_reshaping:
    	#print('original_shape\n',pvalues.reshape((original_shape)))
    	#print('new_pvalues\n',new_pvalues.reshape((original_shape)))
        new_pvalues = new_pvalues.reshape((original_shape))
    #print("new_pvalues\n",new_pvalues)
    return new_pvalues
########################################################




########################################################
## read in the contingency table
chi_table_str = np.array(read_table(args.input_file))
colnames = chi_table_str[0,:].tolist()
rownames = chi_table_str[:,0].tolist()
treatment_vector = chi_table_str[0,1:].tolist()
for row in range(len(rownames)):
    rownames[row] = rownames[row].replace("sample_group_","")
treatment_idx_dict = {key:value for value, key in enumerate(treatment_vector)}


chi_table_int = np.array(np.array(chi_table_str[1:,1:],dtype=float),dtype=int)
obs = chi_table_int[:]
## example
#obs = np.array([[33, 196, 136, 32], [55, 190, 71, 13], [150, 130, 75, 31]])



########################################################
## calculate the values...



if args.negative_control!=None:
	if args.negative_control not in treatment_idx_dict:
		sys.exit("couldn't find",args.negative_control,"in the contingency table!")
	neg_index = treatment_idx_dict[args.negative_control]
	## if there is a designated negative control 
	## manually calculate the chi-square based on the expected values 
	## from the negative control vector
	print("\n\np-values when relative to:",neg_index,'\n')
	p_table, temp_adj_residuals = leave_one_out_chi(obs,neg_index,gof=True)
	#print(p_table)
	#print(temp_adj_residuals)
else:
	p_table, temp_adj_residuals = leave_one_out_chi(obs,gof=False)
	#print(p_table, temp_adj_residuals)


########################################################
## make and write the output tables

def process_table(in_table):
    global colnames, rownames
    in_table = in_table.tolist()
    in_table = [colnames] + in_table
    for i in range(1,len(rownames)):
        in_table[i] = [rownames[i]] + in_table[i]
    return(in_table)
    
global_cmap = sns.color_palette("coolwarm", 256)
def do_heatmap(in_mat_str,mat_name = None, file_name = None):
    global plt, args, global_cmap
    plt.clf()
    try:
        in_mat_num = np.array(in_mat_str[1:,1:],dtype=float)
    except:
        in_mat_num = in_mat_str[1:,1:].tolist()
        for i in range(0,len(in_mat_num)):
            for j in range(0,len(in_mat_num[0])):
                in_mat_num[i][j]=eval(in_mat_num[i][j])
        in_mat_num = np.array(in_mat_num,dtype=bool)
    in_mat_df = pd.DataFrame(in_mat_num,
    	columns = in_mat_str[0,1:],
    	index=in_mat_str[1:,0],
    	copy=True)
    print(in_mat_df)
    heatmap = sns.clustermap(in_mat_df,cmap=global_cmap)
    heatmap.fig.suptitle(mat_name)
    #plt.show()
    plt.savefig(args.out+file_name+'.png', dpi=600, bbox_inches='tight')

## get rid of pesky zeros from floating point error...
tiny = np.finfo(p_table.dtype).tiny
neg_log_10_p = -np.log10(p_table+tiny)
sig_bool_table = p_table<0.05

sig_bool_table_str = np.array(process_table(sig_bool_table))
p_table_str = np.array(process_table(p_table))
neg_log_10_p_str = np.array(process_table(neg_log_10_p))
temp_adj_residuals_str = np.array(process_table(temp_adj_residuals))
print(p_table_str)
print(neg_log_10_p_str)
print(sig_bool_table_str)
print(temp_adj_residuals_str)

do_heatmap(p_table_str,mat_name = "BH corrected\np-values",file_name="bh_corrected_pvals")
do_heatmap(neg_log_10_p_str,mat_name = "-log10 BH corrected\np-values",file_name="neg_log10_BH_pvals")
do_heatmap(temp_adj_residuals_str,mat_name = "Adjusted residuals",file_name="adjusted_residuals")
do_heatmap(sig_bool_table_str,mat_name = "Significance boolean table",file_name="significance_boolean_table")
########################################################
## make some plots

write_table(p_table_str,args.out+"BH_p_table.tsv")
write_table(neg_log_10_p_str,args.out+"neg_log10_BH_p_table.tsv")
write_table(temp_adj_residuals_str,args.out+"adjusted_residuals_table.tsv")
write_table(sig_bool_table_str,args.out+"significance_boolean_table.tsv")

