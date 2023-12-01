#!/bin/bash

# 아래 설정에 맞게 세팅되어 있는지 확인하고 실행!!
cd ~/API-scrap-and-analysis
source ~/newways/bin/activate

python -m scrap.utils.runner -w local -m
python -m scrap.utils.runner -w metro -m

deactivate