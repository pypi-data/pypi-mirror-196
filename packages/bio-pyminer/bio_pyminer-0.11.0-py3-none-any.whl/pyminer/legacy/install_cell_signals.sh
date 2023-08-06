#!/bin/bash

TARGET_INSTALL_DIR='/usr/local/bin/'
TARGET_LIB_DIR='/usr/local/lib/cell_signals/'

## install the python dependencies
sudo apt-get install python3 python3-numpy python3-scipy python3-matplotlib python3-networkx python3-h5py python3-sklearn python3-pip
pip install -U gprofiler-official
pip3 install -U gprofiler-official
sudo pip install -U gprofiler-official
sudo pip3 install -U gprofiler-official
python3 -m pip install gprofiler-official

conda install numpy scipy matplotlib networkx h5py scikit-learn

python3 -m pip install gprofiler-official


## get the path of this script and other 
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/`basename "${BASH_SOURCE[0]}"`

SCRIPT=$(readlink -f $0)
ABSOLUTE_PATH=`dirname $SCRIPT`

echo ''
echo 'directory that the package is in:'
echo $ABSOLUTE_PATH
## go there
cd $ABSOLUTE_PATH

echo ''
echo ''
echo 'current directory:'

echo `pwd`
echo ''
echo ''


## get the files in the bin
py_list=`find * -name "*py" -type f -exec ls {} \;`

echo ''
echo ''
echo $py_list
echo ''
echo ''

## put the bin in the install directory
for f in $py_list
do
	sudo cp $f $TARGET_INSTALL_DIR
	TEMP_FILE=$TARGET_INSTALL_DIR$f
	echo "$files["$TEMP_FILE"]}"
	## target for new symlink
	L="$TARGET_INSTALL_DIR${files["$f"]}"
	## make symlink
	#sudo ln -s $TEMP_FILE $L
	sudo chmod a+x $TEMP_FILE
	#sudo chmod a+x $L
done


## put the lib in the lib target
echo `pwd`
cd lib
lib_list=`find * -name "*protein*" -type f -exec ls {} \;`
echo $lib_list
for f in $lib_list
do
	echo $f
	cp $f $TARGET_LIB_DIR
done
cd ..
echo `pwd`


