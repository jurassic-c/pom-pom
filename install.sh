#!/bin/bash

U=$(whoami)

if [ $U != "root" ]
then
	echo "Error: This script must be run as root"
	exit 1
fi

DLDIR=$(dirname $0)
if [ ! -d /opt ]
then
	mkdir /opt
fi

cp -r $DLDIR /opt/PomPom
chmod +x /opt/PomPom/main.py
cp /opt/PomPom/pom_pom.desktop /usr/share/applications/
echo "Done"
