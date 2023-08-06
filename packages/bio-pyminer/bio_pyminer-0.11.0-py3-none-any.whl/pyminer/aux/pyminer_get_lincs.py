#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput, random
import numpy as np
from gprofiler import GProfiler
from copy import deepcopy
import pandas as pd
import requests
import json
import argparse
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

all_calls = []
def cmd(in_message, com=True):
    global all_calls
    if type(in_message)==list:
        in_message = ' '.join(in_message)
    print(in_message)
    all_calls.append(in_message)
    time.sleep(.25)
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)

def check_infile(infile):
    if os.path.isfile(infile):
        return
    else:
        sys.exit(str('could not find '+infile))

def outfile_exists(outfile):
    if os.path.isfile(outfile):
        statinfo = os.stat(outfile)
        if statinfo.st_size!=0:
            return(True)
        else:
            return(False)
    else:
        return(False)


####################################################################################

###################################################################

###################################################################


def upperGenes(genes, cell_cycle_final_dict):
    # The app uses uppercase gene symbols. So it is crucial to perform upperGenes() step.
    out_genes = []
    for gene in genes:
        if gene not in cell_cycle_final_dict:
            out_genes.append(gene.upper())
    return(out_genes) 

def get_lincs(up,down,cell_cycle_final_dict):
    ## convert to gene symbols
    # gene-set search example
    url = 'http://amp.pharm.mssm.edu/L1000CDS2/query'
    data = {"upGenes":up,
    "dnGenes":down}
    data['upGenes'] = upperGenes(data['upGenes'],cell_cycle_final_dict)
    data['dnGenes'] = upperGenes(data['dnGenes'],cell_cycle_final_dict)
    config = {"aggravate":True,"searchMethod":"geneSet","share":False,"combination":True,"db-version":"latest"}
    metadata = [{"key":"Tag","value":"PyMINEr_"+str(random.randint(0,int(1e6)))}]
    payload = {"data":data,"config":config,"meta":metadata}
    headers = {'content-type':'application/json'}
    r = requests.post(url,data=json.dumps(payload),headers=headers)
    #print(r)
    resGeneSet = r.json()
    return(resGeneSet)
###################################################################

def parse_hit(hit,keep):
    out_list = []
    for k in keep:
        if k in hit:
            out_list.append(str(hit[k]))
        else:
            out_list.append('N/A')
    return(out_list)

def get_human_symbol_names(original_name_vect,human_symbol_dict):
    temp_ids = []
    for temp_id in original_name_vect:
        temp_ids+=human_symbol_dict[temp_id]
    return(temp_ids)

def parse_group_name(file_name):
    file_name = file_name.split('/')
    file_name = file_name[-1]
    file_name = file_name.split('.')
    file_name = file_name[:-1]
    file_name = '.'.join(file_name)
    return(file_name)

def parse_up_down_files(up_file,down_file,human_symbol_dict):
    up_original_ids = read_file(up_file)
    down_original_ids = read_file(down_file)
    up_ids = get_human_symbol_names(up_original_ids,human_symbol_dict)
    down_ids = get_human_symbol_names(down_original_ids,human_symbol_dict)
    up_name = parse_group_name(up_file)
    down_name = parse_group_name(down_file)
    return(up_original_ids,down_original_ids,up_ids,down_ids,up_name,down_name)

###################################################################

def add_pubchem(tx_table):
    ## first get the right column
    tx_table_title = np.array(tx_table[0])
    col_idx = np.where(tx_table_title=="pubchem_id")[0][0]
    all_links = ["pubchem_link"]
    for i in range(len(tx_table)):
        if i > 0:
            temp_line = tx_table[i]
            chem_id = temp_line[col_idx]
            try:
                int(chem_id)
            except:
                temp_link = "N/A"
            else:
                temp_link = "https://pubchem.ncbi.nlm.nih.gov/compound/"+str(chem_id)+"#section=Biological-Test-Results"
            all_links.append(temp_link)
    ## splice it back in
    for i in range(len(tx_table)):
        tx_table[i]=tx_table[i][:col_idx]+[all_links[i]]+tx_table[i][col_idx:]
    return(tx_table)


def parse_lincs_result(lincs_result,up_name,down_name, out_file_name=None, out_dir = None):
    print("going from",up_name,"to",down_name)
    orig_out_file_name = deepcopy(out_file_name)
    #print(orig_out_file_name)
    if "topMeta" not in lincs_result:
        print(lincs_result)
        return
    for line in lincs_result:
        #print(line)
        for line2 in lincs_result[line]:
            pass
            #print('\t',line2)
    top_hits = lincs_result["topMeta"]
    top_combos = lincs_result["combinations"]
    treat_titles = ['score', 'pert_desc', 'sig_id', 'pert_id', 'pubchem_id', 'drugbank_id', 'pert_dose', 'pert_dose_unit',  'cell_id', 'pert_time', 'pert_time_unit', 'DEGcount', 'overlap']
    single_treatment_table = [treat_titles]
    for hit in top_hits:
        #for hit(list(hit.keys()))
        single_treatment_table.append(parse_hit(hit,treat_titles))
    single_treatment_table = add_pubchem(single_treatment_table)
    if orig_out_file_name is None:
        out_file_name = out_dir+down_name+'_to_'+up_name+'_single_treatments.tsv'
    write_table(single_treatment_table,out_file_name)
    return(out_file_name)

####################

def get_files_from_lineage_dir(in_dir):
    out_files = []
    os.chdir(in_dir)
    for temp_file in glob.glob('*.txt'):
        print(temp_file)
        if 'gProfiler' not in temp_file:
            trial_name = parse_group_name(temp_file)
            print(trial_name)
            try:
                fake_int = int(trial_name)
            except:
                pass
            else:
                out_files.append(temp_file)
    print(out_files)
    if len(out_files)==2:
        return(out_files[0],out_files[1])
    else:
        sys.exit("couldn't find the right up and down files - try doing it the manual way")     

####################

def do_single_lincs_analysis(up_ids,down_ids,up_name,down_name, cell_cycle_final_dict, out_file_name = None, out_dir = None):
    #print("up:",up_ids)
    #print("down:",down_ids)
    lincs_result_1 = get_lincs(up_ids,down_ids,cell_cycle_final_dict)
    print(out_file_name)
    out_file_name = parse_lincs_result(lincs_result_1,up_name,down_name, out_file_name = out_file_name, out_dir = out_dir)
    return(out_file_name)

####################

def do_single_lincs_analysis_from_files(file1,
                                        file2, 
                                        cell_cycle_final_dict, 
                                        human_symbol_dict, 
                                        out_file_name = None,
                                        out_dir = None):
    ## parse them
    up_original_ids,down_original_ids,up_ids,down_ids,up_name,down_name = parse_up_down_files(file1,file2,human_symbol_dict)
    ## do the analysis going in both directions
    out_file_name_1 = do_single_lincs_analysis(up_ids,down_ids,up_name,down_name, cell_cycle_final_dict, out_file_name = out_file_name, out_dir = out_dir)
    if out_file_name is None:
        #print('\n'*5,"doing second")
        out_file_name_2 = do_single_lincs_analysis(down_ids,up_ids,down_name,up_name, cell_cycle_final_dict, out_dir = out_dir)
    else:
        out_file_name_2 = None
    return(out_file_name_1, out_file_name_2)



def do_lineage_dir(lineage,cell_cycle_final_dict, human_symbol_dict, out_dir):
    print('doing',lineage)
    out_dir = lineage
    if out_dir[-1]!='/':
        out_dir+='/'
    ## figure out which of the files are the actual gene lists
    file1,file2 = get_files_from_lineage_dir(lineage,cell_cycle_final_dict)
    out_file_name_1, out_file_name_2 = do_single_lincs_analysis_from_files(file1,file2,cell_cycle_final_dict, human_symbol_dict, out_dir = out_dir )
    return([out_file_name_1,out_file_name_2])

###################

def get_lineage_directories(in_dir):
    os.chdir(in_dir)
    lineage_dirs =[]
    for temp_file in glob.glob('*'):
        if '_vs_' in temp_file and os.path.isdir(temp_file):
            temp_full_path = os.path.abspath(temp_file)
            lineage_dirs.append(temp_full_path)
    return(lineage_dirs)

def gprof_to_symbols(results):
    symbols = []
    for i in range(1,len(results)):
        symbols.append(results[i][4])
    symbols=set(symbols)
    return(symbols)

def get_cell_cycle(human_symbol_dict):
    print("getting human symbols that are associated with the cell cycle, but are not transcription factors")
    all_symbol_list_of_lists = list(human_symbol_dict.keys())
    all_symbols_combined = []
    for l in all_symbol_list_of_lists:
        all_symbols_combined += l
    all_symbols_combined = sorted(list(set(all_symbols_combined)))
    cycle_go_terms = ["GO:0007049","GO:0000075","GO:0031576","GO:0071779","GO:0022402","GO:0051301"]
    keep_go_terms = ["GO:0140110","GO:0030545","GO:0010646","GO:0007154"]
    gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)
    cell_cycle_symbol_set = gprof_to_symbols(gp.gconvert(cycle_go_terms,organism="hsapiens", target="ENSG"))
    keep_symbol_set =  gprof_to_symbols(gp.gconvert(keep_go_terms,organism="hsapiens", target="ENSG"))
    cell_cycle_final = cell_cycle_symbol_set - keep_symbol_set
    print(cell_cycle_final)
    print("found",len(cell_cycle_final),"symbols to filter out")
    return(cell_cycle_final)


###################################################################
def collate_lincs(master_out_dir, all_output_files):
    all_combined_results = []
    title_line = None
    print("\n\n\ncollating all of the results\n")
    #print(all_output_files)
    for out_file in all_output_files:
        if out_file != None: ## i.e. no drugs or DEGs
            ## read it in
            temp_file = read_table(out_file)
            short_name = os.path.splitext(os.path.basename(out_file))[0]
            title_line = temp_file[0]
            temp_output = []
            for i in range(1,len(temp_file)):
                ## add the annotation for what the file is & append it to the results
                all_combined_results.append([short_name]+temp_file[i])
        title_line = ['input_file']+title_line
    results_df = pd.DataFrame(all_combined_results, columns = title_line)
    print(results_df)
    results_df = results_df.sort_values(by=['score'],ascending = False)
    # for i in range(5):
    #     print(all_combined_results[i])
    out_path = os.path.join(master_out_dir,'collated_LINCS_results.tsv')
    print("writing results:\n",out_path)
    results_df.to_csv(path_or_buf = out_path,sep='\t')
    return(all_combined_results)


def do_lincs_main(full_lineage, lineage_dir, up, down, human_symbol_dict, out_dir, rm_cell_cycle = False):
    master_out_dir = deepcopy(out_dir)
    ## import the symbol dictionary
    human_symbol_dict, human_def_dict = import_dict(human_symbol_dict)
    if rm_cell_cycle:
        cell_cycle_final_dict = get_cell_cycle(human_symbol_dict)
    else:
        cell_cycle_final_dict = {}
    ##################################################
    ## write the output for single treatments       
    if out_dir != None:
        if out_dir[-1]!='/':
            out_dir+='/'
    ####################################################
    all_output_files=[]
    ## import the up and down lists
    if full_lineage!=None:
        all_output_files = []
        lineage_dirs = get_lineage_directories(full_lineage)
        for lineage in lineage_dirs:
            temp_file = do_lineage_dir(lineage,cell_cycle_final_dict,human_symbol_dict, out_dir)
            if temp_file != None:
                all_output_files += temp_file
    elif lineage_dir!=None:
        do_lineage_dir(lineage_dir,cell_cycle_final_dict, human_symbol_dict, out_dir)
    else:
        ## if this is a specific analysis with a desired up or down, we won't do it bi-directionally
        ## so then we'll just read in the up and down files and run it on those
        up_original_ids,down_original_ids,up_ids,down_ids,up_name,down_name = parse_up_down_files(up,down,human_symbol_dict)
        do_single_lincs_analysis(up_ids,down_ids,up_name,down_name, cell_cycle_final_dict, out_dir = out_dir)
    #############################################################
    ## now make the combined results file 
    if all_output_files != []:
        all_out = collate_lincs(master_out_dir, all_output_files)
        #all_combined_results = [title_line]+all_combined_results
        #write_table(all_combineresults_dfd_results, out_path)
    return()
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-full_lineage", 
        help="the directory for all of the cell type pairs",
        type = str)

    parser.add_argument("-lineage_dir", 
        help="the directory for a single cell type pair created by ",
        type = str)

    parser.add_argument("-up", 
        help="a file containing genes that go up",
        type = str)

    parser.add_argument("-down", 
        help="a file containing genes that go down",
        type = str)

    parser.add_argument("-human_symbol_dict", 
        help="the pickled file created by pyminer_gprofiler_converter.py. This is typically 'human_orthologues.pkl'",
        type = str)

    parser.add_argument("-rm_cell_cycle", 
        help="If you want to remove cell-cycle related genes. Otherwise, there's a good chance you'll see lots of chemo-therapy kind of drugs, where were're really intersested in getting genes that are related to cell identity rather than simply stopping the cell cycle in cycling stem cells. Note that Transcription factors and genes involved in ligand-receptor signaling and cell-cell comunication are still retained, even if they're annotated as being related to the cell cycle. This is important because growth factors or other proteins related to cell identity are sometimes also involved in the cell cycle.",
        action = 'store_true')

    parser.add_argument("-out_dir",'-o', 
        help="the output prefix",
        type = str)

    args = parser.parse_args()
    ##############################################################
    do_lincs_main(args.full_lineage, args.lineage_dir, args.up, args.down, args.human_symbol_dict, args.out_dir, rm_cell_cycle = False)
    