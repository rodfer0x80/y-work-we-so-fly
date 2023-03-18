#!/bin/sh

DRIVER_VERSION="v0.32.2"
DRIVER_ARCH="geckodriver-$DRIVER_VERSION-linux64.tar.gz"
GECKO_SIG="geckodriver-$DRIVER_VERSION-linux64.tar.gz.asc"
SIG_KEY="0x4360FE2109C49763186F8E21EBE41E90F6F12F6D"
DRIVERS_DIR="/opt/drivers"
DRIVER_LOCAL="$DRIVER_DIR/geckodriver"

installDriver()
{
    mkdir -p $DRIVERS_DIR || sudo mkdir -p $DRIVERS_DIR && sudo chown -R $USER:$USER $DRIVERS_DIR
    cd /tmp
    wget https://github.com/mozilla/geckodriver/releases/download/$DRIVER_VERSION/$DRIVER_ARCH
    wget https://github.com/mozilla/geckodriver/releases/download/$DRIVER_VERSION/$GECKO_SIG
    gpg --recv-keys $SIG_KEY
    gpg --verify $GECKO_SIG $DRIVER_ARCH 
    tar xf $DRIVER_ARCH
    rm -rf "./$DRIVER_ARCH" "./$GECKO_SIG"
    mv $(echo $DRIVER_LOCAL | cut -d "/" -f2) $DRIVERS_DIR
    return 0
}

test -e $DRIVER_LOCAL || installDriver
