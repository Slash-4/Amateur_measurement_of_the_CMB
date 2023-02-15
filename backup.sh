#!/bin/bash/
set -e -o nounset

#Path variables

LOCALDRIVEPATH=~/OneDrive
DRIVENAME="Microsof_onedrive"

if [[ $# != 1 && $# != 2 ]]; then
	echo 'Error: Expected one or two input parameters.'
	echo 'Usage: ./backup.sh <fileordirtobackup> [backupdir]'
	exit 1
fi

BACKEDUP=$1
if [[ $# == 2 ]]; then 
	TARGET=$2
else
	TARGET=$LOCALDRIVEPATH/backup/
fi

#check for compatibility
#returns true if the file described by the path doesn't exist
if [[ !  -f "$BACKEDUP"  && ! -d "$BACKEDUP" ]]; then
	echo Error: The file or directory \'"$BACKEDUP"\' does not exist.
	exit 2
fi

if [ ! -d "$TARGET" ]; then
        echo Error: The directory \'"$TARGET"\' does not exist.
        exit 2
fi

#the -ef comparator should return true if the 
#two paths point to the same place
if [[ "$BACKEDUP" -ef "$TARGET" ]]; then
	echo Error: The backed up directory and target directory are the same.
	exit 2
fi
#date should format to YYYYMMDD
TODAY=$(date '+%Y%m%d')
FILENAME=$(basename $BACKEDUP)
TARNAME=$FILENAME.$TODAY.tar

#Compress file
tar -cfz /tmp/$FILENAME.$TODAY.tar.gz $BACKEDUP &> /dev/null

rclone --vfs-cache-mode writes mount $DRIVENAME: $LOCALDRIVEPATH #& needs to open another process

#check if a tar already exist
if [ -f "$TARGET/$TARNAME" ]; then 
	#for this read command: -p  prompt,  -n 1 one character and accept \ literally,  -r store to default prompt value $REPLY
	read -p "Backup file '$TARNAME' already exists. Overwrite? (y/n)" -n 1 -r
	echo
	if  [[ !  $REPLY =~ ^y$ ]]; then
		exit 3
	fi
fi



#TODO: check connection





#TODO: encrypt 
