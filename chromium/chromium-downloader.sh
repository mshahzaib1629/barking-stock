#! /bin/bash

cd $(dirname $0)

LASTCHANGE_URL="https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2FLAST_CHANGE?alt=media"

REVISION=$(curl -s -S $LASTCHANGE_URL)

CHROMIUM_DIR="chromium-data"

echo "latest revision is $REVISION"

# if [ -d "$CHROMIUM_DIR/chrome-linux" ] ; then
#   echo "chromium already installed"
#   exit
# fi

ZIP_URL="https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F$REVISION%2Fchrome-linux.zip?alt=media"

ZIP_FILE="${REVISION}-chrome-linux.zip"

echo "fetching $ZIP_URL"

rm -rf $REVISION
mkdir $CHROMIUM_DIR
pushd $CHROMIUM_DIR
curl -# $ZIP_URL > $ZIP_FILE
echo "unzipping.."
unzip $ZIP_FILE
popd
rm -f ./latest
ln -s $CHROMIUM_DIR/chrome-linux/ ./latest

# Install required dependencies for Chromium
echo "Installing required dependencies for Chromium..."
sudo apt-get update
sudo apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget libatk1.0-0 libgbm-dev

echo "Chromium and its dependencies installation completed."
