#!/usr/bin/env python3
############################################################################

import fileinput
import argparse

############################################################################

## basic function library
def read_file(tempFile,linesOraw,quiet=False):
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

def strip_split(in_line):
	in_line = in_line.strip()
	in_line = in_line.split('\t')
	return(in_line)

#################################################



parser = argparse.ArgumentParser()
parser.add_argument('-in_adj_list',
	help = """the input adjacency list which will be subset for the given subsetting variables""")
parser.add_argument('-subset_ids',
	help = """the IDs from the adjacency list which need to be subset out""")
parser.add_argument('-out_adj_list',
	help = """the path to the desired output adjacency list""")
parser.add_argument('-any_in_subset',
    help = """if either nodes of the adjacency pair is in the subset of interest, put that relationship in the output adj list.""",
    action = 'store_true',
    default = False)
args = parser.parse_args()

#################################################

subset_vars = read_file(args.subset_ids,'lines')

first = True
output = ''
for line in fileinput.input(args.in_adj_list):
	if first:
		"""
		this is for appending the header of the adjacency list
		granted - this is an assumption...
		"""
		output += line
		first = False

	temp_line = strip_split(line)
	
	if args.any_in_subset:
	    if temp_line[0] in subset_vars or temp_line[1] in subset_vars:
	        output += line
	else:
	    if temp_line[0] in subset_vars and temp_line[1] in subset_vars:
		    output += line

## make sure there isn't a dangling new line
if output[-2:]=='\n':
	output=output[:-2]


make_file(output,args.out_adj_list)





