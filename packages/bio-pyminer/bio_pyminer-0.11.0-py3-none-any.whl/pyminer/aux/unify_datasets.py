#!/usr/bin/env python3
##import dependency libraries
import sys,time,glob,os,pickle,fileinput, random, h5py
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
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
    for i in range(1,len(lines)):
        lines[i]=lines[i].strip()
        lines[i]=lines[i].split(delim)
        for j in range(1,len(lines[i])):
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
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-in_dir", "-i",
    help="the directory which contains the matrices to be combined into a single dataset.")
parser.add_argument("-output_file", "-o",
    help="the output file to be made after conversion.")
parser.add_argument("-hdf5", 
    help="write the output file as an hdf5 file rather than tab delimted.",
    action='store_true',
    default = False)
parser.add_argument(
    "-organism",'-species','-s',
    help='which organism are we using. (Use the -species_codes to print out a list of all supported species and their codes).',
    type = str,
    default = 'hsapiens')
parser.add_argument(
    "-species_codes",
    help="print out the species codes",
    action="store_true",
    default = False)
parser.add_argument(
    "-num_genes_downsampled",
    '-downsample',
    '-ds',
    help= "the number of genes to which expression should be downsampled to include. Samples with less than the number of indicated genes will be excluded from the final dataset.",
    type = float
    )

args = parser.parse_args()
if args.organism not in ["aaegypti","acarolinensis","agambiae","amelanoleuca","amexicanus","aplatyrhynchos","btaurus","celegans","cfamiliaris","choffmanni","cintestinalis","cjacchus","cporcellus","csabaeus","csavignyi","dmelanogaster","dnovemcinctus","dordii","drerio","ecaballus","eeuropaeus","etelfairi","falbicollis","fcatus","gaculeatus","ggallus","ggorilla","gmorhua","hsapiens","itridecemlineatus","lafricana","lchalumnae","loculatus","mdomestica","meugenii","mfuro","mgallopavo","mlucifugus","mmulatta","mmurinus","mmusculus","nleucogenys","oanatinus","oaries","ocuniculus","ogarnettii","olatipes","oniloticus","oprinceps","pabelii","panubis","pcapensis","pformosa","pmarinus","psinensis","ptroglodytes","pvampyrus","rnorvegicus","saraneus","scerevisiae","sharrisii","sscrofa","tbelangeri","tguttata","tnigroviridis","trubripes","tsyrichta","ttruncatus","vpacos","xmaculatus","xtropicalis","aclavatus","aflavus","afumigatus","afumigatusa1163","agossypii","anidulans","aniger","aoryzae","aterreus","bcinerea","bgraminis","cgloeosporioides","cgraminicola","chigginsianum","cneoformans","corbiculare","dseptosporum","fculmorum","ffujikuroi","fgraminearum","foxysporum","fpseudograminearum","fsolani","fverticillioides","ggraminis","kpastoris","lmaculans","mlaricipopulina","moryzae","mpoae","mviolaceum","ncrassa","nfischeri","pgraminis","pgraminisug99","pnodorum","pstriiformis","pteres","ptriticina","ptriticirepentis","scerevisiae","scryophilus","sjaponicus","soctosporus","spombe","sreilianum","ssclerotiorum","tmelanosporum","treesei","tvirens","umaydis","vdahliae","vdahliaejr2","ylipolytica","ztritici","aaegypti","acephalotes","adarlingi","agambiae","aglabripennis","amellifera","apisum","aqueenslandica","avaga","bantarctica","bimpatiens","bmalayi","bmori","cbrenneri","cbriggsae","celegans","cgigas","cjaponica","cquinquefasciatus","cremanei","cteleta","dananassae","derecta","dgrimshawi","dmelanogaster","dmojavensis","dpersimilis","dplexippus","dponderosae","dpseudoobscura","dpulex","dsechellia","dsimulans","dvirilis","dwillistoni","dyakuba","hmelpomene","hrobusta","iscapularis","lanatina","lcuprina","lgigantea","lloa","lsalmonis","mcinxia","mdestructor","mleidyi","mscalaris","nvectensis","nvitripennis","obimaculoides","ovolvulus","phumanus","ppacificus","rprolixus","sinvicta","smansoni","smaritima","smimosarum","spurpuratus","sratti","sscabiei","tadhaerens","tcastaneum","tkitauei","tspiralis","turticae","znevadensis","alyrata","atauschii","athaliana","atrichopoda","bdistachyon","bnapus","boleracea","brapa","bvulgaris","ccrispus","cmerolae","creinhardtii","gmax","gsulphuraria","hvulgare","lperrieri","macuminata","mtruncatula","obarthii","obrachyantha","oglaberrima","oglumaepatula","oindica","olongistaminata","olucimarinus","omeridionalis","onivara","opunctata","orufipogon","osativa","ppatens","ppersica","ptrichocarpa","sbicolor","sitalica","slycopersicum","smoellendorffii","stuberosum","taestivum","tcacao","tpratense","turartu","vvinifera","zmays"]:
    sys.exit("could not find "+args.organism+" in the species codes. Use the -species_codes argument to see what you should use for the -organism argument.")

###############################################################
## check that we have gprofiler installed
try:
    from gprofiler import GProfiler
except:
    sys.exit('please install gprofiler; try: pip3 install gprofiler-official')
else:
    from gprofiler import GProfiler

gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)

##############################################################
##############################################################
if args.species_codes:
    print("""
Ensembl

    aaegypti — Aedes aegypti
    acarolinensis — Anolis carolinensis
    agambiae — Anopheles gambiae
    amelanoleuca — Ailuropoda melanoleuca
    amexicanus — Astyanax mexicanus
    aplatyrhynchos — Anas platyrhynchos
    btaurus — Bos taurus
    celegans — Caenorhabditis elegans
    cfamiliaris — Canis familiaris
    choffmanni — Choloepus hoffmanni
    cintestinalis — Ciona intestinalis
    cjacchus — Callithrix jacchus
    cporcellus — Cavia porcellus
    csabaeus — Chlorocebus sabaeus
    csavignyi — Ciona savignyi
    dmelanogaster — Drosophila melanogaster
    dnovemcinctus — Dasypus novemcinctus
    dordii — Dipodomys ordii
    drerio — Danio rerio
    ecaballus — Equus caballus
    eeuropaeus — Erinaceus europaeus
    etelfairi — Echinops telfairi
    falbicollis — Ficedula albicollis
    fcatus — Felis catus
    gaculeatus — Gasterosteus aculeatus
    ggallus — Gallus gallus
    ggorilla — Gorilla gorilla
    gmorhua — Gadus morhua
    hsapiens — Homo sapiens
    itridecemlineatus — Ictidomys tridecemlineatus
    lafricana — Loxodonta africana
    lchalumnae — Latimeria chalumnae
    loculatus — Lepisosteus oculatus
    mdomestica — Monodelphis domestica
    meugenii — Macropus eugenii
    mfuro — Mustela putorius furo
    mgallopavo — Meleagris gallopavo
    mlucifugus — Myotis lucifugus
    mmulatta — Macaca mulatta
    mmurinus — Microcebus murinus
    mmusculus — Mus musculus
    nleucogenys — Nomascus leucogenys
    oanatinus — Ornithorhynchus anatinus
    oaries — Ovis aries
    ocuniculus — Oryctolagus cuniculus
    ogarnettii — Otolemur garnettii
    olatipes — Oryzias latipes
    oniloticus — Oreochromis niloticus
    oprinceps — Ochotona princeps
    pabelii — Pongo abelii
    panubis — Papio anubis
    pcapensis — Procavia capensis
    pformosa — Poecilia formosa
    pmarinus — Petromyzon marinus
    psinensis — Pelodiscus sinensis
    ptroglodytes — Pan troglodytes
    pvampyrus — Pteropus vampyrus
    rnorvegicus — Rattus norvegicus
    saraneus — Sorex araneus
    scerevisiae — Saccharomyces cerevisiae
    sharrisii — Sarcophilus harrisii
    sscrofa — Sus scrofa
    tbelangeri — Tupaia belangeri
    tguttata — Taeniopygia guttata
    tnigroviridis — Tetraodon nigroviridis
    trubripes — Takifugu rubripes
    tsyrichta — Tarsius syrichta
    ttruncatus — Tursiops truncatus
    vpacos — Vicugna pacos
    xmaculatus — Xiphophorus maculatus
    xtropicalis — Xenopus tropicalis

Ensembl Genomes Fungi

    aclavatus — Aspergillus clavatus
    aflavus — Aspergillus flavus
    afumigatus — Aspergillus fumigatus
    afumigatusa1163 — Aspergillus fumigatusa1163
    agossypii — Ashbya gossypii
    anidulans — Aspergillus nidulans
    aniger — Aspergillus niger
    aoryzae — Aspergillus oryzae
    aterreus — Aspergillus terreus
    bcinerea — Botrytis cinerea
    bgraminis — Blumeria graminis f. sp. hordei DH14
    cgloeosporioides — Colletotrichum gloeosporioides
    cgraminicola — Colletotrichum graminicola
    chigginsianum — Colletotrichum higginsianum
    cneoformans — Cryptococcus neoformans
    corbiculare — Colletotrichum orbiculare
    dseptosporum — Dothistroma septosporum
    fculmorum — Fusarium culmorum UK99
    ffujikuroi — Fusarium fujikuroi
    fgraminearum — Fusarium graminearum
    foxysporum — Fusarium oxysporum
    fpseudograminearum — Fusarium pseudograminearum
    fsolani — Fusarium solani
    fverticillioides — Fusarium verticillioides
    ggraminis — Gaeumannomyces graminis
    kpastoris — Komagataella pastoris
    lmaculans — Leptosphaeria maculans
    mlaricipopulina — Melampsora larici-populina 98AG31
    moryzae — Magnaporthe oryzae
    mpoae — Magnaporthe poae
    mviolaceum — Microbotryum violaceum p1A1 Lamole
    ncrassa — Neurospora crassa
    nfischeri — Neosartorya fischeri
    pgraminis — Puccinia graminis
    pgraminisug99 — Puccinia graminis Ug99
    pnodorum — Phaeosphaeria nodorum
    pstriiformis — Puccinia striiformis f. sp. tritici PST-130 str. Race 130
    pteres — Pyrenophora teres f. teres 0-1
    ptriticina — Puccinia triticina
    ptriticirepentis — Pyrenophora tritici-repentis Pt-1C-BFP
    scerevisiae — Saccharomyces cerevisiae
    scryophilus — Schizosaccharomyces cryophilus
    sjaponicus — Schizosaccharomyces japonicus
    soctosporus — Schizosaccharomyces octosporus
    spombe — Schizosaccharomyces pombe
    sreilianum — Sporisorium reilianum SRZ2
    ssclerotiorum — Sclerotinia sclerotiorum
    tmelanosporum — Tuber melanosporum
    treesei — Trichoderma reesei
    tvirens — Trichoderma virens
    umaydis — Ustilago maydis
    vdahliae — Verticillium dahliae
    vdahliaejr2 — Verticillium dahliae JR2
    ylipolytica — Yarrowia lipolytica
    ztritici — Zymoseptoria tritici

Ensembl Genomes Metazoa

    aaegypti — Aedes aegypti
    acephalotes — Atta cephalotes
    adarlingi — Anopheles darlingi
    agambiae — Anopheles gambiae
    aglabripennis — Anoplophora glabripennis
    amellifera — Apis mellifera
    apisum — Acyrthosiphon pisum
    aqueenslandica — Amphimedon queenslandica
    avaga — Adineta vaga
    bantarctica — Belgica antarctica
    bimpatiens — Bombus impatiens
    bmalayi — Brugia malayi
    bmori — Bombyx mori
    cbrenneri — Caenorhabditis brenneri
    cbriggsae — Caenorhabditis briggsae
    celegans — Caenorhabditis elegans
    cgigas — Crassostrea gigas
    cjaponica — Caenorhabditis japonica
    cquinquefasciatus — Culex quinquefasciatus
    cremanei — Caenorhabditis remanei
    cteleta — Capitella teleta
    dananassae — Drosophila ananassae
    derecta — Drosophila erecta
    dgrimshawi — Drosophila grimshawi
    dmelanogaster — Drosophila melanogaster
    dmojavensis — Drosophila mojavensis
    dpersimilis — Drosophila persimilis
    dplexippus — Danaus plexippus
    dponderosae — Dendroctonus ponderosae
    dpseudoobscura — Drosophila pseudoobscura
    dpulex — Daphnia pulex
    dsechellia — Drosophila sechellia
    dsimulans — Drosophila simulans
    dvirilis — Drosophila virilis
    dwillistoni — Drosophila willistoni
    dyakuba — Drosophila yakuba
    hmelpomene — Heliconius melpomene
    hrobusta — Helobdella robusta
    iscapularis — Ixodes scapularis
    lanatina — Lingula anatina
    lcuprina — Lucilia cuprina
    lgigantea — Lottia gigantea
    lloa — Loa loa
    lsalmonis — Lepeophtheirus salmonis
    mcinxia — Melitaea cinxia
    mdestructor — Mayetiola destructor
    mleidyi — Mnemiopsis leidyi
    mscalaris — Megaselia scalaris
    nvectensis — Nematostella vectensis
    nvitripennis — Nasonia vitripennis
    obimaculoides — Octopus bimaculoides
    ovolvulus — Onchocerca volvulus
    phumanus — Pediculus humanus
    ppacificus — Pristionchus pacificus
    rprolixus — Rhodnius prolixus
    sinvicta — Solenopsis invicta
    smansoni — Schistosoma mansoni
    smaritima — Strigamia maritima
    smimosarum — Stegodyphus mimosarum
    spurpuratus — Strongylocentrotus purpuratus
    sratti — Strongyloides ratti
    sscabiei — Sarcoptes scabiei
    tadhaerens — Trichoplax adhaerens
    tcastaneum — Tribolium castaneum
    tkitauei — Thelohanellus kitauei
    tspiralis — Trichinella spiralis
    turticae — Tetranychus urticae
    znevadensis — Zootermopsis nevadensis

Ensembl Genomes Plants

    alyrata — Arabidopsis lyrata
    atauschii — Aegilops tauschii
    athaliana — Arabidopsis thaliana
    atrichopoda — Amborella trichopoda
    bdistachyon — Brachypodium distachyon
    bnapus — Brassica napus
    boleracea — Brassica oleracea
    brapa — Brassica rapa
    bvulgaris — Beta vulgaris subsp. vulgaris
    ccrispus — Chondrus crispus
    cmerolae — Cyanidioschyzon merolae
    creinhardtii — Chlamydomonas reinhardtii
    gmax — Glycine max
    gsulphuraria — Galdieria sulphuraria
    hvulgare — Hordeum vulgare
    lperrieri — Leersia perrieri
    macuminata — Musa acuminata
    mtruncatula — Medicago truncatula
    obarthii — Oryza barthii
    obrachyantha — Oryza brachyantha
    oglaberrima — Oryza glaberrima
    oglumaepatula — Oryza glumaepatula
    oindica — Oryza sativa indica
    olongistaminata — Oryza longistaminata
    olucimarinus — Ostreococcus lucimarinus
    omeridionalis — Oryza meridionalis
    onivara — Oryza nivara
    opunctata — Oryza punctata
    orufipogon — Oryza rufipogon
    osativa — Oryza sativa Japonica
    ppatens — Physcomitrella patens
    ppersica — Prunus persica
    ptrichocarpa — Populus trichocarpa
    sbicolor — Sorghum bicolor
    sitalica — Setaria italica
    slycopersicum — Solanum lycopersicum
    smoellendorffii — Selaginella moellendorffii
    stuberosum — Solanum tuberosum
    taestivum — Triticum aestivum
    tcacao — Theobroma cacao
    tpratense — Trifolium pratense
    turartu — Triticum urartu
    vvinifera — Vitis vinifera
    zmays — Zea mays
    """)
    sys.exit()

def get_files_in_folder(in_folder):
    onlyfiles = [f for f in os.listdir(in_folder) if os.path.isfile(os.path.join(in_folder, f))]
    return(onlyfiles)


def convert_to_ensg(in_genes, gene_lookup_dict = {}, gene_symbol_dict = {}):
    ## this function will yeild a dictionary that 
    global args, gp
    temp_gene_list = []
    for g in in_genes:
        if g not in gene_lookup_dict:
            gene_lookup_dict[g] = []
        


    results = gp.gconvert(in_genes, organism = args.organism, target='ENSG',numeric_ns="ENTREZGENE_ACC")


    for r in range(1,len(results)):
        ## the original ID
        g = results[r][1]
        ## clean it up if it's an entrez gene accesssion
        g = g.replace("ENTREZGENE_ACC:","")
        ## the current orthologue list
        try:
            gene_lookup_dict[g]
        except:
            print('weird mapping event:')
            print(g,results[r])
        else:
            if results[r][4] != None:
                gene_symbol_dict[results[r][3]]=results[r][4]
            if results[r][3] != None:
                temp_list = gene_lookup_dict[g]
                temp_list += [results[r][3]]
                gene_lookup_dict[g]=temp_list
                temp_gene_list.append(results[r][3])

    new_gene_ids = []
    for k in list(gene_lookup_dict.keys()):
        new_gene_ids += gene_lookup_dict[k]
    new_gene_ids= list(set(new_gene_ids))

    for gene in new_gene_ids:
        if gene not in gene_symbol_dict:
            gene_symbol_dict[gene]="None"

    temp_gene_list = list(set(temp_gene_list))
    #print(type(gene_lookup_dict), type(gene_symbol_dict))
    return(gene_lookup_dict, gene_symbol_dict, temp_gene_list)


#####################################################################################
## go through all of the files and collect the gene ids and sample_ids

os.chdir(args.in_dir)


def get_sample_names(in_file):
    for line in fileinput.input(in_file):
        temp_line = strip_split(line)
        break
    fileinput.close()
    temp_line = temp_line[1:]
    top_dir = in_file.split('/')
    file_name = top_dir[-1][:-4]
    for i in range(0,len(temp_line)):
        temp_line[i]=file_name+"||"+temp_line[i]
        #print(temp_line[i])
    return(temp_line)

def get_genes(in_file):
    gene_list = []
    first = True
    for line in fileinput.input(in_file):
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            gene_list.append(temp_line[0])
    fileinput.close()
    #gene_list = int_gene_convert(gene_list)
    return(gene_list)

# def int_gene_convert(gene_list):
#     out_genes = []
#     for gene in gene_list:
#         try:
#             int(gene)
#         except:
#             out_genes.append(gene)
#         else:
#             out_genes.append(int(gene))
#     return(out_genes)
########################################################
all_files = get_files_in_folder(args.in_dir)

all_samples = []## list of lists containing each sample in each dataset
all_genes = []## list of lists containing each gene in each dataset
all_samples_linear =[]## this will be a simple linear list with each sample in the order that it will be in the output file
sample_offset = []

for f in all_files:
    print('working on',f)
    all_samples.append(get_sample_names(f))
    print('\tfound',len(all_samples[-1]),'new samples')
    print('\t\t',all_samples[-1][:1],"...")
    all_genes.append(get_genes(f))
    print('\tfound',len(all_genes[-1]),'new genes')
    print('\t\t',all_genes[-1][:1],"...")

## make all samples linear list
for s in all_samples:
    all_samples_linear += s

## calculate the column offset for each file
previous_length = 0
for s in all_samples:
    sample_offset.append(previous_length)
    previous_length+=len(s)
    
########################################################
## now we need to get all the genes

gene_lookup_dict = {}
gene_symbol_dict = {}

print('converting all of the gene ids to ENSG')
num_datasets = len(all_genes)
individual_gene_lists = []
for g in all_genes:
    gene_lookup_dict, gene_symbol_dict, temp_gene_list = convert_to_ensg(g, gene_symbol_dict = gene_symbol_dict, gene_lookup_dict = gene_lookup_dict)
    individual_gene_lists.append(temp_gene_list)


# for g in all_genes:
#     for temp_g in g:
#         print(temp_g, gene_lookup_dict[temp_g])
        

## now organize the genes, and get ready for laying out the output table
all_gene_lists = list(gene_lookup_dict.values())
print("all_gene_lists",len(all_gene_lists))
all_ensg_genes = []
for i in range(0,len(all_gene_lists)):
    all_ensg_genes+=all_gene_lists[i]

## filtering for genes that were found in all datasets
all_repeated_genes = all_ensg_genes[:]

all_full_ensg_genes = list(set(all_ensg_genes))
all_ensg_genes = []
remove_ensg_genes = []
for gene in all_full_ensg_genes:
    for temp_genes in individual_gene_lists:

        if gene not in temp_genes:
            #print(gene,"not found in all datasets")
            remove_ensg_genes.append(gene)
            break

remove_ensg_genes = list(set(remove_ensg_genes))

for gene in all_full_ensg_genes:
    if gene not in remove_ensg_genes:
        all_ensg_genes.append(gene)

all_ensg_genes = list(set(all_ensg_genes))

print(len(all_ensg_genes),'ENSG genes found in each dataset')
print(len(remove_ensg_genes),'found in only some datasets')
all_ensg_genes.sort()
remove_ensg_genes.sort()

## remove missing genes from other datasets
print("removing ENSG genes that weren't found in all datasets")
for gene in list(gene_lookup_dict.keys()):
    temp_list = gene_lookup_dict[gene]
    new_list = []
    for i in range(0,len(temp_list)):
        if temp_list[i] in remove_ensg_genes:
            pass
        else:
            new_list.append(temp_list[i])
    gene_lookup_dict[gene] = new_list


all_ensg_genes.sort()
print(all_ensg_genes[:5],'...')

all_ensg_positions_dict = {key:value for value, key in enumerate(all_ensg_genes)}

for i in range(0,5):
    temp_gene = all_ensg_genes[i]
    print(temp_gene, all_ensg_positions_dict[temp_gene])

##################################################################################################
## now we actually start making the output

if args.hdf5:
    ## set up the hdf5 file

    outfile = os.path.splitext(args.output_file)[0]+'.hdf5'
    cmd('rm '+outfile)
    h5_f = h5py.File(outfile, "w")

    ## set up the data matrix (this assumes float32)
    out_mat = h5_f.create_dataset("temp_infile", (len(all_ensg_genes),len(all_samples_linear)), dtype=np.float32, maxshape=(None,None))

    #out_mat = np.zeros((len(all_ensg_genes),len(all_samples_linear)))
    
else:
    out_mat = np.zeros((len(all_ensg_genes),len(all_samples_linear)))

def get_array_addition(temp_gene, f, temp_line_num):
    global gene_lookup_dict, all_ensg_positions_dict, sample_offset

    ## get the indices of the samples in the final dataset
    num_samples = np.shape(temp_line_num)[0]
    col_idxs = list(range(sample_offset[f],(num_samples+sample_offset[f])))
    
    ## get the genes & output rows that this accession/symbol corresponds to 
    target_genes = gene_lookup_dict[temp_gene]
    if target_genes == []:
        return(None,None,None)
    row_idxs = []
    for gene in target_genes:
        row_idxs.append(all_ensg_positions_dict[gene])
    num_targets = len(row_idxs)
    
    ## make an array that segregates 
    expression_sub_array = np.zeros((num_targets, num_samples))
    for row in range(0,num_targets):
        expression_sub_array+=temp_line_num/num_targets

    return(row_idxs, col_idxs, expression_sub_array)

## go through each file populating the output matrix
print('making matrix for output', len(all_ensg_genes),'genes and',len(all_samples_linear),'samples')

## clean the all_samples_linear.. I noticed that quotes sometimes screw things up
for i in range(0,len(all_samples_linear)):
    all_samples_linear[i] = all_samples_linear[i].replace('"','')

for f in range(0,len(all_files)):
    first = True
    print('\tworking on',all_files[f])
    for line in fileinput.input(all_files[f]):
        if first:
            first = False
            temp_num_samples = len(strip_split(line))-1
            count=0
        else:
            count+=1
            if temp_num_samples>2000:
                if count % 2000 == 0:
                    print('\t\t',count)
            temp_line = strip_split(line)
            #print(temp_line)
            temp_gene = temp_line[0]
            temp_line_num = np.array(temp_line[1:],dtype = float)
            ## get the gene row(s) to add these values too
            row_idxs, col_idxs, expression_sub_array = get_array_addition(temp_gene,f, temp_line_num)
            if row_idxs != None:
                for temp_row in row_idxs:
                    out_mat[temp_row,col_idxs]+=expression_sub_array[0,:]



#########################################################

def lin_norm_vect(vect,min_non_zero,epsilon=0.0):
    vect = vect-min_non_zero
    vect[np.where(vect<0.0)[0]] = -epsilon
    vect = vect/(max(vect)/1000)
    vect += epsilon
    ## fix floating point errors
    vect[np.where(vect<0.0)[0]] = 0.0
    return(vect)

def downsample_and_rank_transform(vect, num_expressed, cutoff):
    #print(vect)
    ranked_original = rankdata(vect)
    ranked_original = ranked_original - min(ranked_original)
    #print(ranked_original)
    subtract = max(ranked_original) - cutoff - 1
    #print(subtract)
    ranked_original -= subtract
    #print(ranked_original)
    flatten_to_zero_indices = np.where(ranked_original<=0)[0]
    #print(flatten_to_zero_indices)
    ranked_original[flatten_to_zero_indices] = 0.0
    #print(ranked_original)
    ## now that we know where the top n genes are, flatten the rest to zero in the original vector
    included_indices = np.where(ranked_original>0)[0]
    #flattened_vect = included_binary_vect * vect
    flattened_vect = vect[:]
    vect[flatten_to_zero_indices]=0
    min_non_zero = min(flattened_vect[included_indices])
    norm_vect = lin_norm_vect(flattened_vect,min_non_zero)
    return(norm_vect)
    #return(ranked_original)


## figure out how many genes are expressed in each of the samples
if args.num_genes_downsampled:
    print(np.shape(out_mat))
    out_mat = out_mat[:np.shape(out_mat)[0],:]
    #print(out_mat)
    sample_wise_gene_express_count = np.sum(out_mat > 0.0, axis = 0)
    print(np.shape(sample_wise_gene_express_count))
    print(sample_wise_gene_express_count)
    samples_to_keep = np.where(sample_wise_gene_express_count>=args.num_genes_downsampled)[0]
    print("samples_to_keep",samples_to_keep)
    print("sample_wise_gene_express_count",sample_wise_gene_express_count)
    print(len(samples_to_keep),(len(samples_to_keep)/len(sample_wise_gene_express_count)), "samples had enough expressed genes to keep")
    ## do the subsetting
    out_mat = out_mat[:,samples_to_keep]
    all_samples_linear = np.array(all_samples_linear)
    all_samples_linear = all_samples_linear[samples_to_keep].tolist()
    sample_wise_gene_express_count = sample_wise_gene_express_count[samples_to_keep]
    #new_sample_wise_gene_express_count = np.sum(out_mat != 0.0, axis = 0)
    #sys.exit(new_sample_wise_gene_express_count == sample_wise_gene_express_count)

    ## do the rank transformation
    from scipy.stats import rankdata
    print('rank transforming all of the samples')
    print(np.shape(out_mat))
    for i in range(0,np.shape(out_mat)[1]):
        #print(out_mat[:,i])
        out_mat[:,i] = downsample_and_rank_transform(out_mat[:,i],
            sample_wise_gene_express_count[i],
            args.num_genes_downsampled)
        #print(out_mat[:,i])
    print("col NonZero Sum",np.sum(out_mat != 0.0, axis = 0))
    print("colmax",np.max(out_mat,axis=0))
    print("colmin",np.min(out_mat,axis=0))
    print('colsum',np.sum(out_mat,axis=0))
    print(out_mat)
    #sys.exit()


## remove the unexpressed genes
print('removing unexpressed genes.\nOriginal Shape',np.shape(out_mat))
gene_express_sum = np.sum(out_mat, axis = 1)
non_zero_genes = np.where(gene_express_sum != 0.0)[0]
print('non_zero_genes',non_zero_genes)
all_ensg_genes = np.array(all_ensg_genes)
all_ensg_genes = all_ensg_genes[non_zero_genes].tolist()
out_mat = out_mat[non_zero_genes,:]
print('  New Shape:',np.shape(out_mat))

#######################################################
## quantile normalize giving each dataset equal weight
dataset_vect=[]
dataset_dict={}
for i in range(len(all_samples_linear)):
    sample = all_samples_linear[i]
    temp = sample.split("||")
    temp_dataset = temp[0]
    dataset_vect.append(temp_dataset)
    if temp[0] not in dataset_dict:
        dataset_dict[temp_dataset]=[i]
    else:
        temp_index = dataset_dict[temp_dataset]
        temp_index.append(i)
        dataset_dict[temp_dataset] = temp_index

dataset_list = list(dataset_dict.keys())
dataset_averages = np.zeros((len(all_ensg_genes),len(dataset_list)))

## get the average sorted vector for each dataset
for d in range(len(dataset_list)):
    dataset = dataset_list[d]
    for col in dataset_dict[dataset]:
        dataset_averages[:,d]+=np.sort(out_mat[:,col],kind="mergesort")## note that these are in decending order
    dataset_averages[:,d]/=len(dataset_dict[dataset])

print("dataset averages:\n",dataset_averages)
final_quantile_master_vect = np.mean(dataset_averages,axis=1)
print("master quantile vector (highest to lowest):\n",final_quantile_master_vect[::-1])

def quantile(vect):
    global final_quantile_master_vect
    copy_master = final_quantile_master_vect[:]
    sort_order = np.argsort(vect)
    #print(sort_order)
    out = np.zeros((np.shape(vect)[0]))
    for i in range(0,np.shape(sort_order)[0]):
        temp_idx=int(sort_order[i])
        out[temp_idx]=copy_master[i]
    return(out)


## go back through the whole dataset and update the values to match the master quantile normalization vector
if True:
    print('\n\nupdating values to relfect the quantile normalized values')
    for col in range(0,np.shape(out_mat)[1]):
        if col%1000 == 0:
            print('\t',col)
        out_mat[:,col]=quantile(out_mat[:,col])
    print("col NonZero Sum",np.sum(out_mat != 0.0, axis = 0))
#########################################################

print(out_mat)
print('writing the output file')
if not args.hdf5:
    
    nrow = np.shape(out_mat)[0]+1
    ncol = np.shape(out_mat)[1]+1 
    #print(all_samples_linear)
    #print(len(all_samples_linear))
    out_str = [["gene"]+all_samples_linear] 
    #print(out_str)
    #gene_array = ["gene"]+all_ensg_genes 
    for i in range(0,len(out_mat)):        
        out_str.append([all_ensg_genes[i]]+out_mat[i].tolist())
        #print(out_str[-1])
    out_str = np.array(out_str)
        
    write_table(out_str, args.output_file)
else:
    #h5_f.close()
    ## create the final dataset with the removed samples and genes

    # outfile_final = os.path.splitext(args.output_file)[0]+'.hdf5'
    # h5_final = h5py.File(outfile_final, "w")

    # h5_final.create_dataset("infile", (len(all_ensg_genes),len(all_samples_linear)), dtype=np.float32)
    # h5_final["infile"] = np.zeros((len(all_ensg_genes),len(all_samples_linear)))
    # print(h5_final["infile"] + out_mat)

    h5_f.create_dataset("infile", (len(all_ensg_genes),len(all_samples_linear)), dtype=np.float32, maxshape=(None,None), data=out_mat)
    #h5_f["infile"] = h5_f["temp_infile"][non_zero_genes,samples_to_keep]
    #h5_f["shit_fucker"] = h5_f["infile"][:]

    # #del out_mat
    # print("col NonZero Sum",np.sum(final_out_mat != 0.0, axis = 0))
    # print("colmax",np.max(final_out_mat,axis=0))
    # print("colmin",np.min(final_out_mat,axis=0))
    # print('colsum',np.sum(final_out_mat,axis=0))
    # print(final_out_mat)


    print("col NonZero Sum",np.sum(h5_f["temp_infile"] != 0.0, axis = 0))
    print("colmax",np.max(h5_f["temp_infile"],axis=0))
    print("colmin",np.min(h5_f["temp_infile"],axis=0))
    print('colsum',np.sum(h5_f["temp_infile"],axis=0))
    print(h5_f["temp_infile"])


    print("col NonZero Sum",np.sum(h5_f["infile"] != 0.0, axis = 0))
    print("colmax",np.max(h5_f["infile"],axis=0))
    print("colmin",np.min(h5_f["infile"],axis=0))
    print('colsum',np.sum(h5_f["infile"],axis=0))
    print(h5_f["infile"])

    temp=str(args.output_file).split('/')
    temp=('/').join(temp[:-1])
    
    ## write the row and column info
    make_file('\n'.join(["variables"]+all_samples_linear),temp+'/column_IDs.txt')
    make_file('\n'.join(all_ensg_genes),temp+'/ID_list.txt')

    del h5_f["temp_infile"]
    ## close the hdf5 file
    h5_f.close()
    #h5_final.close()
    #cmd('rm '+outfile)

