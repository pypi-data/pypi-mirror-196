
import numpy as np
from sklearn.metrics import pairwise
import seaborn as sns
from matplotlib import pyplot as plt

euc = pairwise.euclidean_distances

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
    
########################################################################

group_mean_table = np.array(read_table("/home/scott/Documents/others/lauren/prelim_run/pyminer/sample_clustering_and_summary/k_group_means.txt"))
genes_used_for_clust_table = np.array(read_table("/home/scott/Documents/others/lauren/prelim_run/pyminer/sample_clustering_and_summary/genes_used_for_clustering.txt"))
indices_used_for_clust = list(map(int,map(float,sorted(genes_used_for_clust_table[:,1].tolist()))))
## per cell type means:
means = np.array(group_mean_table[1:,1:], dtype = float)
means = means[indices_used_for_clust,:]

## get the average transcript vector for each cell type pair
## avgs: [transcript vector, i, j]
avgs = np.zeros((means.shape[0],means.shape[1],means.shape[1]))
cell_type_to_cell_type_distance = euc(means.T,squared=True)

for i in range(0,means.shape[1]):
	for j in range(i,means.shape[1]):
		if i!=j:
			temp_avg = np.mean(means[:,np.array([i,j])], axis = 1)
			avgs[:,i,j] = temp_avg
			avgs[:,j,i] = temp_avg
		else:
			avgs[:,i,j] = means[:,i]
			avgs[:,j,i] = means[:,i]

## get the euclidean distance of each cell type and all cell type pair averages
cell_type_distances_x = []
dist_from_avgs_y = []
ratio_of_dist_to_avgs_and_cell_type_dist = []
w_list = []
by_first = []
by_second = []
dist_from_pair_avgs = np.zeros((means.shape[1],means.shape[1],means.shape[1]))
for w in range(0,means.shape[1]):
	for i in range(0,means.shape[1]):
		for j in range(i,means.shape[1]):
			dist_from_pair_avgs[w,i,j] = np.sum((means[:,w]-avgs[:,i,j])**2)
			if w != i and w!=j and i!=j:
				dist_from_avgs_y.append(dist_from_pair_avgs[w,i,j])
				cell_type_distances_x.append(cell_type_to_cell_type_distance[i,j])
				ratio_of_dist_to_avgs_and_cell_type_dist.append(cell_type_distances_x[-1]/dist_from_avgs_y[-1])
				w_list.append(w)
				by_first.append(i)
				by_second.append(j)



for i in range(0,len(dist_from_avgs_y)):
#	if ratio_of_dist_to_avgs_and_cell_type_dist[i] > 7.5:#dist_from_avgs_y[i] <= 5 and cell_type_distances_x[i] >= 20:
	if cell_type_distances_x[i] >= 225:
		print(w_list[i],'is explained by',by_first[i],'and',by_second[i])


sns.kdeplot(cell_type_distances_x, dist_from_avgs_y)
plt.show()
plt.clf()

sns.violinplot(ratio_of_dist_to_avgs_and_cell_type_dist)
plt.show()
plt.clf()


sns.violinplot(np.log2(np.array(ratio_of_dist_to_avgs_and_cell_type_dist)))
plt.show()
plt.clf()
