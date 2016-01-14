
#Recursively unlock all files in the Drive
unlockFiles(){

# add the list of properties to be removed
 xattr -rd com.apple.FinderInfo $DRIVENAME/
 xattr -rd com.apple.quarantine $DRIVENAME/
 xattr -rd com.apple.finder.copy.source.inode#N $DRIVENAME/
 xattr -rd com.apple.finder.copy.source.volumeuuid#N $DRIVENAME/


}

# Check for locked files
checkFiles(){
  inUseFiles=$(ls -l@  $DRIVENAME/* | grep -B1 "com.apple")

  if [ "$inUseFiles" = "" ]; then
    echo "[WARNING] Device already clean. Nothing to do here"
    open "$DRIVENAME"
    exit 0;
  else
    echo "$inUseFiles"
  fi

}

#Check sudo
checkSudo()
{
 if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "This script should be run as ROOT. Try sudo"
    exit
 fi
}

echo "__________________________________________________"
echo "Abhinav.Y 2015 --abhinav56321(at)gmail.com--"
echo ""
echo "Initialize a NTFS Hard Disk on this system to fix the 'File in use Issues'"
echo "Run this script to release the Quarantine and FinderInfo locked files"
echo "Alternatively this script can be invoced as an FolderAction"
echo "Type Quit to exit the script"
echo ""
echo "__________________________________________________"


select DRIVENAME in "/Volumes"/*
do

    case "$DRIVENAME" in
        "$QUIT")
          echo "Exiting."
          break
          ;;
        *)
          echo "You picked "$DRIVENAME" "
          checkFiles;
          unlockFiles;
          ;;
    esac
done

