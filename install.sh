#!/bin/bash

echo "Installing python virtual environment..."

cd ~ && virtualenv newways --python=3.10
source ~/newways/bin/activate
pip install -r ~/API-scrap-and-analysis/requirements.txt

echo "Python virtual environment has been installed successfully in ~/newways."
echo "Installing chromedriver..."

CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"
TEMP_DIR="/tmp/chromedriver_download"

mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

curl -O "$CHROMEDRIVER_URL"
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/

cd -
rm -rf "$TEMP_DIR"

echo "Chromedriver has been installed successfully."