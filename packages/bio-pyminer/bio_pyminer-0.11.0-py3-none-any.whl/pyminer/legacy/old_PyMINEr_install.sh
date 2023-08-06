#!/bin/bash

TARGET_INSTALL_DIR='/usr/local/bin/'

## install the python dependencies
sudo apt-get install python3 python3-numpy python3-scipy python3-matplotlib python3-networkx python3-h5py python3-sklearn python3-pip python3-seaborn
pip install -U gprofiler-official
pip3 install -U gprofiler-official
sudo pip install -U gprofiler-official
sudo pip3 install -U gprofiler-official
python3 -m pip install gprofiler-official

conda install numpy scipy matplotlib networkx h5py scikit-learn seaborn

## get the path of this script and other 
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/`basename "${BASH_SOURCE[0]}"`

SCRIPT=$(readlink -f $0)
ABSOLUTE_PATH=`dirname $SCRIPT`

echo ''
echo ''
echo $ABSOLUTE_PATH
## go there
cd $ABSOLUTE_PATH

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
	echo "$files["$TEMP_FILE"]}"
	## target for new symlink
	L="$TARGET_INSTALL_DIR${files["$f"]}"
	## make symlink
	sudo ln -s $TEMP_FILE $L
	sudo chmod a+x $TEMP_FILE
	sudo chmod a+x $L
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