#!/bin/bash

TARGET_INSTALL_DIR='/usr/local/bin/'
TARGET_LIB_DIR='/usr/local/lib/cell_signals/'
TEMP_USER=$(who | awk '{print $1}')
TEMP_PATH=$(sudo -Hiu $TEMP_USER env | grep PATH)
TEMP_HOME=$(sudo -Hiu $TEMP_USER env | grep HOME | cut -c6-)
if [ $TEMP_HOME"/.bashrc" ]
then
	echo "running as "$TEMP_USER
	echo $TEMP_HOME"/.bashrc"
	# source $TEMP_HOME"/.bashrc"
	#[[ -r $TEMP_HOME"/.bashrc" ]] && . ~/.bashrc
 	PATH_APPENDS=$(grep 'export PATH=' $TEMP_HOME"/.bashrc" | sed -r 's/"//g')
 	#PATH_APPENDS=$($PATH_APPENDS)
 	echo $PATH_APPENDS
 	$PATH_APPENDS:$PATH
fi

echo "USER"
echo $TEMP_USER

# NEW_PATH=$(sudo -i -u $TEMP_USER echo $PATH)

# echo "NEW_PATH"
# echo $NEW_PATH

# echo "pre-PATH"
# echo $PATH
# export PATH=$(NEW_PATH):$PATH
echo "post-PATH"
echo $PATH

#$TEMP_PATH

## install the python dependencies
sudo apt-get install python3 python3-numpy python3-scipy python3-matplotlib python3-networkx>=2.3 python3-h5py python3-sklearn python3-pip python3-seaborn
pip install gprofiler-official==0.3.5
pip install umap-learn
pip3 install gprofiler-official==0.3.5
pip3 install umap-learn
pip3 install -U statsmodels
sudo pip install umap-learn
sudo pip3 install umap-learn
pip3 install python-louvain

echo "

if you have anaconda installed - this step could take a minute. Please be patient

"


conda install numpy scipy matplotlib networkx h5py scikit-learn seaborn 
conda install -c conda-forge umap-learn


## get the path of this script and other 
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/`basename "${BASH_SOURCE[0]}"`

SCRIPT=$(readlink -f $0)
ABSOLUTE_PATH=`dirname $SCRIPT`

echo ''
echo ''
echo $ABSOLUTE_PATH
## go there
cd $ABSOLUTE_PATH
cd pyminer

echo ''
echo ''
echo ''

echo `pwd`
echo ''
echo ''

## echo `ls`

## get the list of all scripts in the package
py_list=`find * -name "*py" -type f -exec ls {} \;`

echo ''
echo ''
echo $py_list
echo ''
echo ''
echo ''
echo ''

# ## set the inventory and symlinks
# declare -A files

# files=( ["PyMINEr_6.00.py"]="PyMINEr.py"
#  ["create_within_group_boot_1.01.py"]="create_within_group_boot.py" 
#  ["PyMINEr_pipeline_1.02.py"]="PyMINEr_pipeline.py" 
#  ["make_FPR_curve_1.4.py"]="FPR_curve_script.py" 
#  ["remove_dups.py"] = "remove_dups.py"
#  ["mine_R_cutoff_filter.py"] = "mine_R_cutoff_filter.py"
#  ["mat_to_adj_list.py"] = "mat_to_adj_list.py"
#  ["clustering.py"] = "clustering.py"
#  ["get_stats.py"] = "get_stats.py"
#  ["plot_network.py"] = "plot_network.py"
#  ["pyminer_gprofile.py"] = "pyminer_gprofile.py"
#  ["make_website.py"] = "make_website.py")


# ## check for symlinks, and remove if they already exist

# rm $TARGET_INSTALL_DIR"PyMINEr.py"
# rm $TARGET_INSTALL_DIR"create_within_group_boot.py"
# rm $TARGET_INSTALL_DIR"PyMINEr_pipeline.py"
# rm $TARGET_INSTALL_DIR"FPR_curve_script.py"
# rm $TARGET_INSTALL_DIR"remove_dups.py"
# rm $TARGET_INSTALL_DIR"mine_R_cutoff_filter.py"
# rm $TARGET_INSTALL_DIR"mat_to_adj_list.py"
# rm $TARGET_INSTALL_DIR"clustering.py"
# rm $TARGET_INSTALL_DIR"get_stats.py"
# rm $TARGET_INSTALL_DIR"plot_network.py"
# rm $TARGET_INSTALL_DIR"pyminer_gprofile.py"
# rm $TARGET_INSTALL_DIR"make_website.py"



# rm $TARGET_INSTALL_DIR"PyMINEr_6.00.py"
# rm $TARGET_INSTALL_DIR"create_within_group_boot_1.01.py"
# rm $TARGET_INSTALL_DIR"PyMINEr_pipeline_1.02.py"
# rm $TARGET_INSTALL_DIR"FPR_curve_script_1.4.py"
# rm $TARGET_INSTALL_DIR"mine_R_cutoff_filter.py"

## go through the list
for f in $py_list
do
	sudo cp $f $TARGET_INSTALL_DIR
	TEMP_FILE=$TARGET_INSTALL_DIR$f
	#echo "$files["$TEMP_FILE"]}"
	## target for new symlink
	#L="$TARGET_INSTALL_DIR${files["$f"]}"
	## make symlink
	#sudo ln -s $TEMP_FILE $L
	sudo chmod a+x $TEMP_FILE
	#sudo chmod a+x $L
done

## get rid of the default gprofiler so that it actually works
G="$(which gprofiler.py)"
destination="${G: :-3}""_cli.py"
echo $G
echo $destination
mv $G $destination

## get rid of the default gprofiler so that it actually works
G="$(which gprofiler.py)"
destination="${G: :-3}""_cli.py"
echo $G
echo $destination
mv $G $destination




## put the lib in the lib target
cd ..
echo `pwd`
cd lib
lib_list=`find * -name "*protein*" -type f -exec ls {} \;`
echo $lib_list
mkdir $TARGET_LIB_DIR
for f in $lib_list
do
	echo $f
	cp $f $TARGET_LIB_DIR
done
cd ..
echo `pwd`

cd $TARGET_LIB_DIR
gunzip -f *
