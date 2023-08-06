#!/bin/bash

TARGET_INSTALL_DIR='/usr/local/bin/'
TARGET_LIB_DIR='/usr/local/lib/cell_signals/'
TEMP_USER=$(who | awk '{print $1}')
#TEMP_PATH=$(sudo -Hiu $TEMP_USER env | grep PATH)
#TEMP_HOME=$(sudo -Hiu $TEMP_USER env | grep HOME | cut -c6-)

## get the path of this script and other 
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/`basename "${BASH_SOURCE[0]}"`

SCRIPT=$(readlink -f $0)
ABSOLUTE_PATH=`dirname $SCRIPT`

echo $ABSOLUTE_PATH
## go there
cd $ABSOLUTE_PATH
cd pyminer


## get the list of all scripts in the package
py_list=`find * -name "*py" -type f -exec ls {} \;`

echo $py_list

## go through the list
for f in $py_list
do
	cp $f $TARGET_INSTALL_DIR
	TEMP_FILE=$TARGET_INSTALL_DIR$f
	chmod a+x $TEMP_FILE
done

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
