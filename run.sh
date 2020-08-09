#!/bin/bash

cd Backend
python stage_1.py
python stage_2.py
python stage_3.py
python stage_4.py

mv stage_4.json ../Frontend/src/data

cd ../Frontend
npm start
