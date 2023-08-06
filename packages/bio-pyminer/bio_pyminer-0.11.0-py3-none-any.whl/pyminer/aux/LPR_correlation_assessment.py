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
from scipy.stats import pearsonr
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
#########################################################################

def get_all_dirs(in_dir):
	return([dI for dI in os.listdir(in_dir) if os.path.isdir(os.path.join(in_dir,dI))])

def do_com_analysis(z_array, base_dir, com_dir, id_list, id_hash, lpr_dict):
	print('\nanalyzing:', com_dir)
	## read in the community_ids
	com_dir = os.path.join(base_dir, com_dir)
	all_com_ids = read_file(os.path.join(com_dir, 'community_ids.txt'), 'lines')

	## read in the median module z-score
	med_mod_table = np.array(read_table(os.path.join(com_dir, 'median_module_usage.tsv')))
	mod_usage_vect = np.array(med_mod_table[1:,1], dtype = np.float32)

	##############
	## get the correlation of all module ids with the median module usage
	# first subset the table for community ids

	# get the pearson r matrix
	pearson_dict = {}
	pearson_vect = []
	lpr_vect = []
	for i in range(len(all_com_ids)):
		temp_id = all_com_ids[i]
		temp_idx = id_hash[temp_id]
		r, p = pearsonr(z_array[temp_idx,:], mod_usage_vect)
		pearson_dict[temp_id] = r
		pearson_vect.append(r)
		lpr_vect.append(lpr_dict[temp_id])
		#print(r)
	lpr_vs_pearsonr = pearsonr(lpr_vect,pearson_vect)
	print("\tthis modules' correlation of lpr vs pearson is:", lpr_vs_pearsonr)
	return (lpr_vect, pearson_vect, lpr_vs_pearsonr, pearson_dict)


def write_cor_results(pearson_dict, lpr_dict, com_dict, out_dir):
	all_ids = sorted(list(pearson_dict.keys()))
	output = [['feature_id','community','LPR','pearson_r_with_mod_usage']]
	for temp_id in all_ids:
		output.append([temp_id, com_dict[temp_id], lpr_dict[temp_id], pearson_dict[temp_id]])
	write_table(deepcopy(output),os.path.join(out_dir, 'lpr_vs_pearsonr_for_mod_usage.tsv'))
	out_df = pd.DataFrame.from_records(output[1:])
	out_df = out_df.rename(index=str, columns={key:value for key, value in enumerate(output[0])})
	print(out_df)
	return(out_df)


def plot_results(results_df, out_dir):
	## do a scatter plot colored by the module
	ax = sns.lmplot(x="LPR", y="pearson_r_with_mod_usage", hue = "community", data = results_df,
		       scatter_kws=dict(s=1))
	ax._legend.remove()
	#plt.legend(loc='right')
	r, p = pearsonr(results_df["LPR"], results_df["pearson_r_with_mod_usage"])
	title_str = "r="+str(r)+"\np="+str(p)
	plt.title(title_str)
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	# sns.lmplot(x="LPR", y="pearson_r_with_mod_usage", data = results_df,
	# 	       scatter_kws=dict(s=0), ax = ax)
	# plt.plot([0,1],[0,1])
	plt.savefig(os.path.join(out_dir, 'lpr_vs_pearsonr_for_mod_usage.png'), dpi = 300,bbox_inches='tight')
	return



def get_markers(results_df, n=1):
	## get all of the communities
	list(set(results_df["community"]))
	return


def do_all_community_analysis(in_dir, out_dir, lpr_table, sample_z):
	## first get all of the directories that are for the contained communities
	all_dirs = get_all_dirs(in_dir)
	com_dirs = [temp_dir for temp_dir in all_dirs if 'community_' in temp_dir]
	print(com_dirs)

	## read in the LPR table
	lpr_table = read_table(lpr_table)
	lpr_dict = {}
	com_dict = {}
	for i in range(1,len(lpr_table)):
		lpr_dict[lpr_table[i][0]]=float(lpr_table[i][2])
		com_dict[lpr_table[i][0]]=lpr_table[i][1]

	## read in the sample_z table
	in_table_array = np.array(read_table(sample_z))
	id_list = in_table_array[1:,0].tolist()
	id_hash = {value:key for key, value in enumerate(id_list)}
	z_array = np.array(in_table_array[1:, 1:], dtype = np.float32)

	## next go through each community and get all of their stats
	lpr_vects = []
	pearson_vects = []
	lpr_vs_pear = []
	pearson_dict = {}
	for community in com_dirs:
		com_results  = do_com_analysis(z_array = z_array, 
									   base_dir = in_dir,
							           com_dir = community,
							           id_list = id_list,
							           id_hash = id_hash,
							           lpr_dict = lpr_dict)
		lpr_vects.append(com_results[0])
		pearson_vects.append(com_results[1])
		lpr_vs_pear.append(com_results[2])
		pearson_dict.update(com_results[3])

	## write the results
	results_df = write_cor_results(pearson_dict, lpr_dict, com_dict, out_dir)
	plot_results(results_df, out_dir)
	get_markers()

	return






#########################################################################
def parse_args(args):
	parser = argparse.ArgumentParser()
	parser.add_argument(
	    '-community_dir','-com_dir','-in_dir',
	    help = "The directory that contains all of the directories of the communities generated by PyMINEr. Note that this should be applied to the sample level analysis, which is not typically run by PyMINEr.")
	parser.add_argument(
	    '-community_table','-com_table',
	    help = "The file with the community analysis by PyMINEr.")
	parser.add_argument(
		'-out_dir',
		help = "the output directory")
	parser.add_argument(
	    '-sample_z',
	    type = str,
	    help = "the sample level Z-scores created by PyMINEr. This is the sample_var_enrichment_Zscore.txt file in the sample_clustering_and_summary directory")

	args = parser.parse_args()
	return(args)
#########################################################################

if __name__ == '__main__':
	## do dodecahedral
	seed(1234567789)
	args = parse_args(sys.argv)
	do_all_community_analysis(in_dir = args.community_dir, 
							  lpr_table = args.community_table,
		                      out_dir = args.out_dir,
		                      sample_z = args.sample_z)

	
