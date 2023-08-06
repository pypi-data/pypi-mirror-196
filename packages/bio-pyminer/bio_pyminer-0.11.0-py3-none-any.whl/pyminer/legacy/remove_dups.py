#!/usr/bin/env python3
##############################
import fileinput as fi
import sys

#########################################################
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

###############
##############

def prep_line(line, delim = '\t'):
    temp_line = line.strip('\n')
    temp_line = temp_line.split(delim)
    return(temp_line)

def useable_line(temp_line):
    global valid_variable, remove
    if both:
        both_in_valid_variable = (temp_line[0] in valid_variable) and (temp_line[1] in valid_variable)
    else:
        both_in_valid_variable = (temp_line[0] in valid_variable) or (temp_line[1] in valid_variable)
    if both:
        if (temp_line[0] not in valid_variable) and (temp_line[1] not in valid_variable):
            both_not_in_valid_variable = True
        else:
            both_not_in_valid_variable = False
    else:
        if (temp_line[0] not in valid_variable) or (temp_line[1] not in valid_variable):
            both_not_in_valid_variable = True
        else:
            both_not_in_valid_variable = False
    if not remove:
        return(both_in_valid_variable)
    else:
        return(both_not_in_valid_variable)
        

#########################################################
remove=False
remove_duplicates=True
both = False

all_inclusive=True
#all_inclusive=False
pr_cutoff = 1.25#0.75
#filter_file = '/home/scott/mouse_GFP_tdTomato_results_1/John_subset/combined_names_only.txt'
#filter_file = '/home/scott/scRNAseq/human/pyminer/no_splice_ribo_mito_subcomps/filter_out_genes.txt'
#filter_file = '/home/scott/scRNAseq/human/pyminer/T2D/t2d_genes_only.txt'
#filter_file_clean=filter_file.split('/')
#filter_file_clean=filter_file_clean[-1]
#filter_file = '/home/scott/mouse_GFP_tdTomato_results_1/PyMINEr/pos_cor/page_ranks.txt'
#relationship_file = '/home/scott/scRNAseq/human/pyminer/T2D/control_final_relationship_summary.tsv'
#relationship_file = '/home/scott/scRNAseq/human/pyminer/T2D/control_final_relationship_summary_t2d_genes_only.txt_degree2.txt.tsv'
#relationship_file = '/media/scott/extra_data3/RNAseq/human_results_pooled/all_human_merged_results/pyminer/control_final_relationship_summary.tsv'


if '-infile' in sys.argv:
    relationship_file=sys.argv[sys.argv.index('-infile')+1]
#	relationship_file = '/media/scott/extra_data3/RNAseq/human_results_pooled/all_human_merged_results/pyminer/control_final_relationship_summary_dedup.tsv'
else:
	sys.exit('need a file to filter, use -infile <file>')


out_relationship_file=relationship_file[:-4]+'_dedup.tsv'
#else:
#    out_relationship_file=relationship_file[:-4]+'_cutoff_'+str(pr_cutoff)+'.tsv'



##########################################################
## figure out which variables pass the page rank threshold
## log those valid variables into valid_variable hash
valid_variable = {}
valid_pairs = []

first=True
#for line in fi.input(filter_file):
for line in fi.input(relationship_file):
    if first:
        first=False
    else:
        temp_line = prep_line(line)
        if all_inclusive:
            valid_variable[temp_line[0]]=[]
            valid_variable[temp_line[1]]=[]
        else:
            if float(temp_line[1]) >= pr_cutoff:
                valid_variable[temp_line[0]]=[]
                valid_variable[temp_line[1]]=[]

fi.close()
print(len(valid_variable.keys()))

##########################################################
##
out_file = []
line_number = 0

first=True
for line in fi.input(relationship_file):
    line_number+=1
    if line_number%100000==0:
        print(line_number, 100 * len(out_file) / line_number)
    if first:
        out_file.append(line)
        first=False
    else:
        temp_line = prep_line(line)
        
        ## if both variables are in the valid variable dictionary
        if useable_line(temp_line):
            #print(temp_line[0], valid_variable[temp_line[0]],temp_line[1], valid_variable[temp_line[1]])
            if remove_duplicates:
                ## if this variable pair has been seen before, pass it, otherwise log it
                if (temp_line[1] not in valid_variable[temp_line[0]]):
    
                    temp = valid_variable[temp_line[0]]
                    temp.append(temp_line[1])
                    valid_variable[temp_line[0]] = temp
                    
                    temp = valid_variable[temp_line[1]]
                    temp.append(temp_line[0])
                    valid_variable[temp_line[1]] = temp
                    
                    out_file.append(line)    
    
                else:
                    pass
            else: ## if we aren't removing the duplicates
                out_file.append(line)

        else:
            pass

        

fi.close()

print(out_relationship_file)
make_file(out_file,out_relationship_file)


