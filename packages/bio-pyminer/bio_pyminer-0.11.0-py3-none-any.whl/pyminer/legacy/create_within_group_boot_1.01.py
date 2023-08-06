#!/usr/bin/python3
import sys,subprocess,time,glob,os
from random import shuffle,seed
from operator import itemgetter
import gc
gc.enable()

## check for numpy dependency
try:
    import numpy as np
except:
    print('numpy is a dependency for this script\nit can be installed from:\nWindows:\nhttp://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy\nMac:\nhttp://sourceforge.net/projects/numpy/files/NumPy/\nLinux:\nhttps://launchpad.net/~scipy/+archive/ppa')
    sys.exit()
else:
    import numpy as np
## check for matplotlib
try:
    import matplotlib.pyplot as plt
except:
    print('matplotlib is a dependency for graphs produced by this script\nit can be installed from:\nhttp://matplotlib.org/downloads.html')
else:
    import matplotlib.pyplot as plt


######################################################################################
###############
## basic function library
def read_file(tempFile,linesOraw):
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
    print(type(table))
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

def import_dict(f):
    f=open(f,'rb')
    d=pickle.load(f)
    f.close()
    return(d)

def save_dict(d,path):
    f=open(path,'wb')
    pickle.dump(d,f)
    f.close()


def cmd(in_message):
    subprocess.Popen(in_message,shell=True).communicate()

###############

def find_table_start(table):# returns title line, variable lists, and table matrices
    global dividing_col,microarray
    if microarray:
        print('reading in microarray data')
        for i in range(0,len(table)):
            if "!series_matrix_table_begin" in table[i]:
                print('table starts at line',i+1)
                ID_list=[]
                #print((len(table[i+1:-1]),len(table[i+1][1:])))
                outmat=np.zeros((len(table[i+1:-1]),len(table[i+1][1:])))
                outmat_index=0
                for j in range(i+2,len(table)):
                    if table[j][0][0]=='!':
                        outmat=outmat[:outmat_index]
                        #print(np.shape(outmat))
                        break
                    ##print(outmat_index)

                    #print(table[j][0])
                    ID_list.append([table[j][0]])

                    ##print(np.array(table[j][1:]))
                    ##print(outmat[outmat_index])
                    ##print(ID_list[outmat_index])
                    ##print(table[j][0])
                    
                    outmat[outmat_index]+=np.array(table[j][1:])

                    
                    ##except:
                    ##    print(outmat[outmat_index])
                    ##    print(np.array(table[j][1:]))
                    ##    sys.exit()
                    outmat_index+=1
                
                print(len(ID_list),'variables detected')
                print(np.shape(ID_list),np.shape(outmat))
                outmat=outmat.astype('<U32')

                #ID_list=np.array(ID_list,dtype='<U9')
                print(np.shape(ID_list),np.shape(outmat))
                #print(ID_list)
                outmat=np.hstack((ID_list,outmat))
                
                return(ID_list,outmat)## +2 because of title row
    else:
        title_line=np.array(table[0])
        ID_list=[]
        outmat=np.zeros((len(table)-1,len(table[0][1:])))
        outmat_index=0
        for j in range(1,len(table)):
            ID_list.append(table[j][0])
            outmat[outmat_index]+=np.array(table[j][1:])
            outmat_index+=1

        print(len(ID_list),'variables detected')
        print(np.shape(ID_list),np.shape(outmat))
        outmat=outmat.astype('<U32')

        ID_list=np.array([ID_list],dtype='<U32').T

        print(type(ID_list))
        print(type(outmat))
        
        print(np.shape(ID_list),np.shape(outmat))
        
        outmat=np.hstack((ID_list,outmat))
    
        return(ID_list,outmat)

##############################################################

##########################################
## parse input arguments
if '-h' in sys.argv or '--help' in sys.argv:
    print("""

""")
    sys.exit()


if '-single_network' in sys.argv:
    single_network=True
    dividing_col=0
else:
    single_network=False

if '-dividing_col' in sys.argv:
    dividing_col=int(sys.argv[sys.argv.index('-dividing_col')+1])
else:
    if not single_network:
        sys.exit('-diving_col is a required argument when -single_network is not in use')

if '-infile' in sys.argv:
    infile=sys.argv[sys.argv.index('-infile')+1]
else:
    ##temporary
    ##infile='/media/extra_data/matrix_analysis/data/negative_control_bootstrap/within_group_bootstrap/GSE38609-GPL10558_series_matrix.txt'
    sys.exit('-infile is a required argument\n\nUse the -h or --help option for usage instructions')

if '-microarray' in sys.argv:
    microarray=True
else:
    microarray=False

if '-num' in sys.argv:
    number_of_arrays_to_return=int(sys.argv[sys.argv.index('-num')+1])
else:
    number_of_arrays_to_return=1
    #number_of_arrays_to_return=10

if '-seed' in sys.argv:## seed for randomizing
    seed(int(sys.argv[sys.argv.index('-infile')+1]))
else:
    seed(10)

#######################################
temp=str(infile).split('/')
temp=('/').join(temp[:-1])
#######################################


## reads input raw data
table=read_file(infile,'lines')
table=make_table(table,'\t')
#print(table[0:10])
## retuns ID list for variable names and 
IDlist,out_mat=find_table_start(table)
print(IDlist[:10])
#sys.exit()

n_per_group1=dividing_col
print(n_per_group1)
n_per_group2=len(out_mat[0])-dividing_col-1
print(n_per_group2)
num_vars=len(out_mat)

#### create names for output variables
##var_names=[]
##for i in range(0,num_vars):
##    var_names.append('var'+str(i+1))
##
##var_names=np.array([var_names],dtype='<U9').T
##print('var_names shape:',np.shape(var_names))

## create sample names
samples=['names']
for i in range(0,n_per_group1):
    samples.append('group1.'+str(i+1))
for i in range(0,n_per_group2):
    samples.append('group2.'+str(i+1))
samples=np.array([samples],dtype='<U32')
print('samples shape:',np.shape(samples))
print(samples)



## shuffle within group values
for i in range(0,number_of_arrays_to_return):
    ## create output matrix
    temp_boot=out_mat[:]
    
    ## Shuffle both groups
    print('shuffling array number',i)
    for row in range(0,len(temp_boot)):

        #print(out_mat[row])

        ## group 1
        shuffle(temp_boot[row][1:n_per_group1+1])
        ## group 2
        shuffle(temp_boot[row][n_per_group1+1:])

        #print(temp_boot[row])
        #sys.exit()

    print('temp_boot shape:',np.shape(temp_boot))

    print(temp_boot[:5])
    
    title_out_mat=np.vstack((samples,temp_boot))
    
    cmd('mkdir '+temp+'/boot_'+str(i+1))
    make_file(flatten_2D_table(title_out_mat,'\t'),temp+'/boot_'+str(i+1)+'/'+'within_group_boot_'+str(i+1)+'.txt')

    del title_out_mat



