#!/bin/bash

#Setup selenium
sudo apt-get update
sudo apt-get install -y chromium-browser unzip
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
pip install -U selenium

#setup spacy
pip install -U spacy
python -m spacy download en_core_web_lg

#setup tensorflow
pip install -q tensorflow-hub
pip install -q tensorflow-datasets
pip install numpy 
pip install pandas
pip install matplotlib

python ./Backend/train_mobilenet.py

#setup npm
cd Frontend
npm install npm*
