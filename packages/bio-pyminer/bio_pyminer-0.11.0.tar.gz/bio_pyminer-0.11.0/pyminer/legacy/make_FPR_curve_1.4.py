#!/usr/bin/env python3

##import dependency libraries
import fileinput
import sys,subprocess,time,glob,os
from operator import itemgetter
import gc
gc.enable()


## check for numpy dependency
try:
    import numpy as np
except:
    print('\n\nnumpy is a dependency for this script\nit can be installed from:\nWindows:\nhttp://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy\nMac:\nhttp://sourceforge.net/projects/numpy/files/NumPy/\nLinux:\nhttps://launchpad.net/~scipy/+archive/ppa\n\n\n')
    
import numpy as np

## check for matplotlib
if '-no_graphs' in sys.argv:
    no_matplot_lib=True
    no_graphs=True
    pass
else:
    print('\n\nmatplotlib is a dependency for graphs produced by this script\nit can be installed from:\nhttp://matplotlib.org/downloads.html\n\n\n')
    from matplotlib import use
    use('Agg')
    no_matplot_lib=False
    import matplotlib.pyplot as plt
    no_graphs=False

##
##if '-mpi' in sys.argv():
##    try:
##        __import__(mpi4py)
##        


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
###############


def get_all_freqs(FPR_list):
    all_MIC_list=[]
    all_freq=[]
    for M in FPR_list:## run through all MICs
        if M in all_MIC_list:## if that particular MIC value has already been anotated
            all_freq[all_MIC_list.index(M)]+=1## add 1 to the frequency list
        else:## otherwise
            all_MIC_list.append(M)## add that MIC value to list of all MICs
            all_freq.append(1)## and initialize the frequency at 1
    return(all_MIC_list,all_freq)

def get_bin_feqs(bin_list,MIC_list,MIC_freqs):
    global num_comparisons
    if len(MIC_list)!=len(MIC_freqs):
        sys.exit('len(MIC_list)!=len(MIC_freqs)')
    L=len(bin_list)
    temp_freq=[]
    for i in range(0,len(bin_list)):
        temp_freq+=[0]
    for M in range(0,len(MIC_list)):
        for b in range(0,len(bin_list)):
            if MIC_list[M]>bin_list[b]:
                print(MIC_list[M],'<',bin_list[b])
                temp_freq[b]+=MIC_freqs[M]
##    for i in range(0,len(temp_freq)):
##        temp_freq[i]=temp_freq[i]
    
    return(temp_freq)



########################################################################################################
if '-h' in sys.argv or '--help' in sys.argv:
    sys.exit("""
""")

if '-infile' in sys.argv:
    ## calculate how many comparisions were made
    infile=sys.argv[sys.argv.index('-infile')+1]
    var_count=0
    print('figuring out how many comparisions were made in total')
    if '-microarray' in sys.argv:
        microarray=True
    else:
        microarray=False
    
    for line in fileinput.input(infile):
        if microarray and line[0]=='!':## checks for '!' comment in line, otherwise, the line should be a variable in the microarray
            pass
        else:
            var_count+=1
    fileinput.close()
    num_comparisons=var_count*var_count

if '-FPR_mine1' in sys.argv:
    in_mine1=sys.argv[sys.argv.index('-FPR_mine1')+1]
else:
    sys.exit('-FPR_mine1 is a required argument for this program\nuse"-h" or "--help" for usage instructions')

if '-FPR_mine2' in sys.argv:
    in_mine2=sys.argv[sys.argv.index('-FPR_mine2')+1]
else:
    in_mine2=False

if '-group1_name' in sys.argv:
    name1=sys.argv[sys.argv.index('-group1_name')+1]
else:
    name1='group1'

if '-group2_name' in sys.argv:
    name2=sys.argv[sys.argv.index('-group2_name')+1]
else:
    name2='group2'

if '-dpi' in sys.argv:
    dpi_in=int(sys.argv[sys.argv.index('-dpi')+1])
else:
    dpi_in=360
if '-MIC_interval' in sys.argv:
    interval=float(sys.argv[sys.argv.index('-MIC_interval')+1])
else:
    interval=0.005
if '-FPR_target' in sys.argv:
    target=float(sys.argv[sys.argv.index('-FPR_target')+1])
else:
    target=0.001

#############################################################################################################

temp=str(in_mine1).split('/')
temp=('/').join(temp[:-1])+'/'

########################


global_min1=1
global_max1=0

global_min2=1
global_max2=0

print('making bins')
## make bins
bins=[]
b=1
while b>0:
    bins.append(b)
    b-=interval

########################


FPR1_count=[]
for b in range(0,len(bins)):
    FPR1_count.append(0)
if in_mine2:
    FPR2_count=FPR1_count[:]

print('indexing all MIC values for File1')
for line in fileinput.input(in_mine1):
    temp_line=line.split('\t')
    try:
        float(temp_line[2])
    except:
        pass
    else:
        for b in range(0,len(bins)):
            temp_MIC=float(temp_line[2])
            if temp_MIC < global_min1:
                global_min1=temp_MIC
            if temp_MIC > global_max1:
                global_max1=temp_MIC
            if temp_MIC > bins[b]:
                FPR1_count[b]+=1
fileinput.close()

print('finished binning File1\n')

if in_mine2:
    print('indexing all MIC values for File2')
    for line in fileinput.input(in_mine2):
        temp_line=line.split('\t')
        try:
            float(temp_line[2])
        except:
            pass
        else:
            for b in range(0,len(bins)):
                temp_MIC=float(temp_line[2])
                if temp_MIC < global_min2:
                    global_min2=temp_MIC
                if temp_MIC > global_max2:
                    global_max2=temp_MIC
                if temp_MIC > bins[b]:
                    FPR2_count[b]+=1
    print('finished binning File2\n')

gc.collect()## collect all 'o that gaahhbage

########################
## these variables are for finding the MIC corresponding to the target FPR
FPRtargetMIC1=9999999
FPRtargetMIC2=9999999
FPRtargetFPR1=9999999
FPRtargetFPR2=9999999
FPRtargetDif1=9999999
FPRtargetDif2=9999999

FPR1_status=False
FPR2_status=False

#########################
## generate stats on FPRs at different levels
print('finding best MIC to match the desired FPR')
if in_mine2:
    unified_FPR=[['MIC','Total_count_'+name1,'FPR_'+name1,'log10(FPR)_'+name1,'Total_count_'+name2,'FPR_'+name2,'log10(FPR)_'+name2]]
    for MIC in range(0,len(bins)):
        unified_FPR.append([bins[MIC],FPR1_count[MIC],FPR1_count[MIC]/num_comparisons,np.log10(FPR1_count[MIC]/num_comparisons),FPR2_count[MIC],FPR2_count[MIC]/num_comparisons,np.log10(FPR2_count[MIC]/num_comparisons)])
        ## compare FPR at a given MIC & FPR to target & update 'best matches'
        if FPR1_count[MIC]/num_comparisons<target and bins[MIC] < FPRtargetMIC1:
            FPRtargetIndex1=MIC
            FPRtargetMIC1=bins[MIC]
            FPRtargetDif1=FPR1_count[MIC]/num_comparisons-target
            FPRtargetFPR1=FPR1_count[MIC]/num_comparisons
        ## compare FPR at a given MIC & FPR to target & update 'best matches'
        if FPR2_count[MIC]/num_comparisons<target and bins[MIC] < FPRtargetMIC2:
            FPRtargetIndex2=MIC
            FPRtargetMIC2=bins[MIC]
            FPRtargetDif2=FPR2_count[MIC]/num_comparisons-target
            FPRtargetFPR2=FPR2_count[MIC]/num_comparisons
##
else:
    unified_FPR=[['MIC','Total_count_'+name1,'FPR_'+name1,'log10(FPR)_'+name1]]
    for MIC in range(0,len(bins)):
        unified_FPR.append([bins[MIC],FPR1_count[MIC],FPR1_count[MIC]/num_comparisons,np.log10(FPR1_count[MIC]/num_comparisons)])
        ## compare FPR at a given MIC & FPR to target & update 'best matches'
        if FPR1_count[MIC]/num_comparisons<target and bins[MIC] < FPRtargetMIC1:
            FPRtargetIndex1=MIC
            FPRtargetMIC1=bins[MIC]
            FPRtargetDif1=FPR1_count[MIC]/num_comparisons-target
            FPRtargetFPR1=FPR1_count[MIC]/num_comparisons

##
out_summary='FPR target = '+str(target)+'\nbest MIC1 match = '+str(FPRtargetMIC1)+'\nTrue FPR at MIC = '+str(FPRtargetMIC1)+' = '+str(FPRtargetFPR1)
if in_mine2:
    out_summary+='\nbest MIC2 match = '+str(FPRtargetMIC2)+'\nTrue FPR at MIC = '+str(FPRtargetMIC2)+' = '+str(FPRtargetFPR2)

## check to make sure that there were MICs which landed on both sides of the cutoff.
## Otherwise it's suggested to either re-run PyMINEr on the bootstrap file with a lower MIC cutoff,
## or to change the target FPR in this program
if FPRtargetMIC1==9999999:
    out_summary+='\n\n***Note: the target FPR threshold ('+str(target)+') was not met by any MICs in your bootstrap for '+name1+'\ntry doing the boostrap again with a lower MIC cutoff, or raising the FPR threshold'
##    if not FPR1_status:
##        out_summary+='\n***Note: the true best MIC matching the target FPR for '+name1+' may be lower than reported here\nNone of the MICs tested failed to pass the target FPR threshold\nTo address this, either use a more stringent FPR target, or lower the MIC cutoff and re-run the PyMINEr analysis on the bootstrap file'
if in_mine2:
    if FPRtargetMIC2==9999999:
        out_summary+='\n\n***Note: the target FPR threshold ('+str(target)+') was not met by any MICs in your bootstrap for '+name2+'\ntry doing the boostrap again with a lower MIC cutoff, or raising the FPR threshold'
##    if not FPR2_status:
##        out_summary+='\n***Note: the true best MIC matching the target FPR for '+name2+' may be lower than reported here\nNone of the MICs tested failed to pass the target FPR threshold\nTo address this, either use a more stringent FPR target, or lower the MIC cutoff and re-run the PyMINEr analysis on the bootstrap file'
    
out_summary+='\n\n**Note: range of MICs for '+name1+' was '+str(global_min1)+' to '+str(global_max1)
if in_mine2:
    out_summary+='\n\n**Note: range of MICs for '+name2+' was '+str(global_min2)+' to '+str(global_max2)

make_file(out_summary,temp+'MIC_for_target_summary.txt')
    
make_file(flatten_2D_table(unified_FPR,'\t'),temp+'FPR_frequencies_for_MIC_bins.tsv')

###########################
FPR1=np.log10(np.array(FPR1_count)/num_comparisons)
if in_mine2:
    FPR2=np.log10(np.array(FPR2_count)/num_comparisons)
    min_FPR=min(np.min(FPR2),np.min(FPR1))
else:
    min_FPR=np.min(FPR1)

if not no_graphs:
    print('making FPR curve graph')
    #
    plt.plot([global_min1,global_min1],[0,min_FPR],ls='--',color='k',label='range for '+name1)
    plt.plot([global_max1,global_max1],[0,min_FPR],ls='--',color='k')
    #
    plt.plot(bins,FPR1,ls='--',color='k')
    plt.scatter(bins,FPR1,marker='o',color='k',edgecolors='k',label=name1)
    #
    if in_mine2:
        #
        plt.plot([global_min1,global_min1],[0,min_FPR],ls='--',color='r',label='range for '+name2)
        plt.plot([global_max1,global_max1],[0,min_FPR],ls='--',color='r')
        #
        plt.plot(bins,FPR2,ls='--',color='r')
        plt.scatter(bins,FPR2,marker='o',color='r',edgecolors='k',label=name2)
        #
    plt.plot([0,1],np.log10(np.array([target,target])),ls='--',color='b',label='FPR = log10('+str(target)+')')
    
    plt.ylabel('log10(FPR)')
    plt.xlabel('MIC cutoff')
    plt.xlim([0,1])
    plt.legend()
    output=temp+'FPR_curve.png'
    plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    

print('finished'+out_summary)

