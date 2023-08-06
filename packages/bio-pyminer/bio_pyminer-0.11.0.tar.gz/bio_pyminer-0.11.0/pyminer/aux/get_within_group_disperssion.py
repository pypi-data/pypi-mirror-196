
#!/usr/bin/env python3
##import dependency libraries
import sys,time,glob,os,pickle,fileinput, random, h5py
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from sklearn.neighbors import RadiusNeighborsRegressor as neighbors

import matplotlib.pyplot as plt
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
            table[i]=delim.join(str(table[i]))+'\n'
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



##############################################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-means", 
    help="the matrix containing the means for each variable (rows) and each group (cols)",
    type = str)
parser.add_argument("-sds", 
    help="the matrix containing the standard deiations for each variable (rows) and each group (cols)",
    type = str)
parser.add_argument("-out_dir", 
    help="the directory for output files",
    type = str)
parser.add_argument("-log", 
    help="log transform the means",
    action = 'store_true',
    default = False)
parser.add_argument("-z_cutoff", "-z",
    help="the cutoff for how many standard deviations over the mean residual should be considered overdispersed. Default = 1",
    type = float,
    default = 1.0)
args = parser.parse_args()
if args.out_dir[-1]!='/':
	args.out_dir+='/'
##############################################################
gc.enable()
## read in the means and SDs
means = np.array(read_table(args.means))
means_num = np.array(means[1:,1:],dtype = float)

if args.log:
	means_num = np.log2(1 + np.min(means_num) + means_num)

sds = np.array(read_table(args.sds))
sds_num = np.array(sds[1:,1:],dtype = float)
sds_num = sds_num**2
## convert the SDs to variance


## log the original dimentions and calculate the linear reshaping dimentions
original_dim = np.shape(means_num)
linear_dim = (original_dim[0]*original_dim[1],)

## then reshape them to do the lowess fit
linear_means = np.reshape(means_num,linear_dim)
linear_sds = np.reshape(sds_num,linear_dim)
print(linear_dim[0],'points')

## plot (a random sample of) the relationship between the coefficient of variance and means
sample_size = 50000
if linear_dim[0] > sample_size:
	print('sampling the distribution for',sample_size,'points')
	index_vect  = np.arange(linear_dim[0])
	np.random.shuffle(index_vect)
	sample = index_vect[:sample_size].tolist()
	## always include the min and max values for interpolation
	x_max_index = np.where(np.array(linear_means) == np.max(linear_means))[0][0]
	x_min_index = np.where(np.array(linear_means) == np.min(linear_means))[0][0]
	#print(sample)
	#print(type(sample))
	#sample = sample.tolist()
	if x_max_index not in sample:
		sample.append(x_max_index)
	if x_min_index not in sample:
		sample.append(x_min_index)
	#print(sample)
	print(type(sample))

	print(sample[:5],'...',sample[-5:])
	plt.scatter(linear_means[sample], linear_sds[sample], c = 'black', s = 0.5)#,xlab = 'mean',ylab = 'CV')
else:
	sample = np.arange(linear_dim[0], dtype =  int).tolist()
	plt.scatter(linear_means, linear_sds, c = 'black', s = 0.5)#,xlab = 'mean',ylab = 'CV'))#,xlab = 'mean',ylab = 'CV')
#plt.show()
#sys.exit()

## do the lowess fit. This returns the expected values of the linear_sds
print('calculating the best fit curve')

## 

neigh = neighbors(radius = 1.0, weights = 'uniform', leaf_size = 30)
mean_max = max(linear_means)
mean_min = min(linear_means)
sds_min = min(linear_sds)

## first calculate the lowess curve on the sample
lowess_estimates_sample = lowess(linear_sds[sample]-sds_min+1,linear_means[sample]-mean_min+1, delta = 0.01*mean_max)-1
lowess_estimates_sample[:,0] = lowess_estimates_sample[:,0] + mean_min
lowess_estimates_sample[:,1] = lowess_estimates_sample[:,1] + sds_min
print(lowess_estimates_sample)

## remove x ties from the lowess as this messes up the interpolation
values, indices = np.unique(lowess_estimates_sample[:,0], return_index=True)
lowess_estimates_sample = lowess_estimates_sample[indices,:]
print(lowess_estimates_sample)

## then interpolate the curve to smooth it out and provide the nearest neighbor regression with the needed coverage
from scipy.interpolate import interp1d

# ## positive control
# x = np.linspace(0, 10, num=11, endpoint=True)
# print(x)
# y = np.cos(-x**2/9.0)
# print(y)
# f2 = interp1d(x, y, kind='cubic')
# print(f2)
# xnew = np.linspace(0, 10, num=41, endpoint=True)
# print(xnew)
# print(f2(xnew))

print(np.shape(lowess_estimates_sample[:,0]))
print(np.shape(lowess_estimates_sample[:,1]))

interpolation = interp1d(lowess_estimates_sample[:,0], lowess_estimates_sample[:,1], kind='cubic')

## make the new x values evenly spaced across the spread
new_x = np.linspace(mean_min,max(linear_means), num=sample_size, endpoint = True)
print(new_x)

## interpolate the lowess function
new_y = interpolation(new_x)
print(new_x,new_y)

## get the interplated lowess ready for nearest neighbor regression
train_x = np.array([[x] for x in lowess_estimates_sample[:,0].tolist()])
train_y = lowess_estimates_sample[:,1]

full_x = np.array([[x] for x in linear_means.tolist()])
#train_x = full_x[sample]
#train_y = linear_sds[sample]

print(train_x)
print(train_y)
#neigh.fit(train_x,train_y)
print(new_x)
print(new_y)
new_x = np.array([[x] for x in new_x.tolist()])

#plt.clf()
plt.scatter(new_x,new_y, c = 'red', s = 0.75)
plt.savefig(args.out_dir+'local_fit.png',dpi=600,bbox_inches='tight')
#plt.show()
#sys.exit()
neigh.fit(new_x,new_y)

## now calculate the values for everything else
bin_size = 100000
total_vars = len(linear_means)
bins = []
cur_bin = 0
while cur_bin<total_vars:
	bins.append(min(cur_bin, total_vars))
	cur_bin+=bin_size

bins.append(total_vars)
print(bins)

lowess_estimates = np.zeros((len(linear_means),))
for i in range(1,len(bins)):
	print("working on",bins[i-1],bins[i])
	# if i%50000 == 0:
	# 	print('\t',bins[i]/len(linear_means))
	lowess_estimates[bins[i-1]:bins[i]] += neigh.predict(full_x[bins[i-1]:bins[i]])
#lowess_estimates = neigh.predict(full_x)

#lowess_estimates = lowess(linear_sds[sample]+1,linear_means[sample]+1)-1#, return_sorted = False)#, frac = 1e-3, delta = 1e-10*max(linear_means))
#lowess_estimates = [x[0] for x in lowess_estimates]


#plt.scatter(linear_means[sample],lowess_estimates[sample],c='red',s=0.5)
#plt.savefig(args.out_dir+'local_fit_sample.png',dpi=600,bbox_inches='tight')
#plt.show()
#sys.exit()
## calculate the residuals
print('getting the residuals')
residuals = linear_sds - lowess_estimates

print('sample_means',linear_means[:10])
print('sample_estimates',lowess_estimates[:10])
print('sample_CVs',linear_sds[:10])
print('sample_residuals',residuals[:10])


## reshape it back into the table
resid_table = np.reshape(residuals, original_dim)

print(np.sum(np.isnan(residuals)))
nan_idx = np.where(np.isnan(residuals))[0]

print('nan means',linear_means[nan_idx])
print('nan sds',linear_sds[nan_idx])
print('nan estimates',lowess_estimates[nan_idx])
print('nan resid',residuals[nan_idx])


#print(np.nan_std(residuals))
st_dev_resid = np.std(residuals)
print('sd residuals:',st_dev_resid)

st_dev_cutoff = st_dev_resid*args.z_cutoff
print('residual cutoff for overdispersion:',st_dev_cutoff)

## plot the residuals
plt.clf()
plt.scatter(linear_means[sample],residuals[sample], c = 'black', s = 0.5)#,xlab = 'mean',ylab = 'CV')
plt.plot([min(linear_means),max(linear_means)],[0,0],c='red')
## find the significant residuals
resid_sample = residuals[sample]
mean_sample = linear_means[sample]
sig_indices = np.where(resid_sample >= st_dev_cutoff)[0]
plt.scatter(mean_sample[sig_indices], resid_sample[sig_indices], c = 'blue', s = 2)
plt.savefig(args.out_dir+'residuals.png',dpi=600,bbox_inches='tight')
#plt.show()


## determine which genes are locally overdispersed
print('calculating local overdispersion')
local_overdispersion_bool_table = resid_table >= st_dev_cutoff

print('number of overdispersed genes in each group:')
number_overdispersed_per_group = np.sum(local_overdispersion_bool_table, axis = 0)
print(number_overdispersed_per_group)



## get the boolean overdispersed table ready for writing to file
#print(np.shape(local_overdispersion_bool_table))
#print(local_overdispersion_bool_table)
local_overdispersion_bool_table = np.array(local_overdispersion_bool_table,dtype = str)
#print(local_overdispersion_bool_table)
local_overdispersion_bool_table=local_overdispersion_bool_table.tolist()
#print(local_overdispersion_bool_table[:5])

## add the gene names
gene_names = means[:,0].tolist()
for i in range(1,(np.shape(means)[0])):
 	local_overdispersion_bool_table[i-1] = [gene_names[i]] + local_overdispersion_bool_table[i-1]

## add the column names
group_names = means[0,:].tolist()
local_overdispersion_bool_table = [group_names] + local_overdispersion_bool_table


local_overdispersion_bool_table=np.array(local_overdispersion_bool_table, dtype = str)
print(local_overdispersion_bool_table)
print(np.shape(local_overdispersion_bool_table))

write_table(local_overdispersion_bool_table,args.out_dir+'/locally_overdispersed_boolean_table.txt')




