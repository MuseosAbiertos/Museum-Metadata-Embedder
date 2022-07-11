#!/bin/bash

# Script to make a Debian deb image for gmme
# version 0.3, 2022-07-10, hvdw

if [ "$1" = "" ]
then
        printf "\n\nYou have to provide the version\n\n"
        exit
fi

# Check if running as root
if [ "$EUID" -ne 0 ]
  then printf "\n\nYou need to run this script as root with sudo\n\n"
  exit
fi

printf "\n\n PYINSTALLER STUFF\n\n"
DWD=$(pwd)
printf "Current workdir $DWD\n"

printf "\n\nGo back to root folder of souce code\n"
cd ../..
RWD=$(pwd)
printf "Current source dir $RWD\n"

printf "\nRemove possible previous build and dist folders and recreate binary\n\n"
rm -rf dist build *.spec
pyinstaller gmme.py

printf "\n\n### Finished with the pyinstaller stuff ###"
printf "\nCreate the DEBIAN .deb\n"
cd $DWD
PACKAGE_NAME="museum-metadata-embedder"
APP="gmme"
PACKAGE_VERSION="$1"
TEMP_DIR="/tmp"

rm -rf $TEMP_DIR/debian

mkdir -p $TEMP_DIR/debian/DEBIAN
mkdir -p $TEMP_DIR/debian/usr/bin
mkdir -p $TEMP_DIR/debian/usr/share/applications
mkdir -p $TEMP_DIR/debian/usr/share/$PACKAGE_NAME
mkdir -p $TEMP_DIR/debian/usr/share/doc/$PACKAGE_NAME
mkdir -p $TEMP_DIR/debian/usr/share/common-licenses/$PACKAGE_NAME
 
echo "Package: $PACKAGE_NAME" > $TEMP_DIR/debian/DEBIAN/control
echo "Version: $PACKAGE_VERSION" >> $TEMP_DIR/debian/DEBIAN/control
cat control >> $TEMP_DIR/debian/DEBIAN/control
 
cp -r $RWD/dist/gmme/* $TEMP_DIR/debian/usr/bin/
cp -r $RWD/data $TEMP_DIR/debian/usr/bin/
chmod +x $TEMP_DIR/debian/usr/bin/*
cp *.desktop $TEMP_DIR/debian/usr/share/applications/
cp -r $RWD/data $TEMP_DIR/debian/usr/share/$PACKAGE_NAME
#cp -r $RWD/exiftool $TEMP_DIR/debian/usr/share/$PACKAGE_NAME
cp copyright $TEMP_DIR/debian/usr/share/common-licenses/$PACKAGE_NAME/ # results in no copyright warning
cp copyright $TEMP_DIR/debian/usr/share/doc/$PACKAGE_NAME/
cp $RWD/LICENSE $TEMP_DIR/debian/usr/share/common-licenses/$PACKAGE_NAME/
cp $RWD/LICENSE $TEMP_DIR/debian/usr/share/doc/$PACKAGE_NAME/

printf "\nCopy/configure our Museum-Metadata-Embedder package inside the deb\n" 
cp -rp $RWD/dist/gmme/* $TEMP_DIR/debian/usr/share/$PACKAGE_NAME
#cp -rp $RWD/docs $TEMP_DIR/debian/usr/share/$PACKAGE_NAME
#cp -rp $RWD/images $TEMP_DIR/debian/usr/share/$PACKAGE_NAME

 
echo "$PACKAGE_NAME ($PACKAGE_VERSION) trust; urgency=low" > changelog
echo "  * Rebuild" >> changelog
echo " -- Museos Abiertos <admin@museosabiertos.org>  `date -R`" >> changelog
gzip -9c changelog > $TEMP_DIR/debian/usr/share/doc/$PACKAGE_NAME/changelog.gz
 
cp logo.png $TEMP_DIR/debian/usr/share/$PACKAGE_NAME/gmme-logo.png
chmod 0644 $TEMP_DIR/debian/usr/share/$PACKAGE_NAME/*.png
 
PACKAGE_SIZE=`du -bs $TEMP_DIR/debian | cut -f 1`
PACKAGE_SIZE=$((PACKAGE_SIZE/1024))
echo "Installed-Size: $PACKAGE_SIZE" >> $TEMP_DIR/debian/DEBIAN/control
 
chown -R root $TEMP_DIR/debian/
chgrp -R root $TEMP_DIR/debian/

cd $TEMP_DIR/
dpkg --build debian

arch=$(uname -m)
printf "\nBuilding for machine/architecture: $arch\n"
if [ "$arch" == 'x86_64' ];
then 
  mv debian.deb $DWD/$PACKAGE_NAME-$PACKAGE_VERSION-amd64.deb
fi
if [[ $arch =~ ^arm ]];
then
  mv debian.deb $DWD/$PACKAGE_NAME-$PACKAGE_VERSION-armhf.deb
fi


printf "\n\nAs we run as root we now need to clean up our stuff\n"
rm -rf $RWD/dist $RWD/build $RWD/*.spec
rm -r $TEMP_DIR/debian

