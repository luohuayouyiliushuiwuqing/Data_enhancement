#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：rknn_model_zoo 
@File    ：create_rk_dataset.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/3 13:45 
"""
import os
import random
import shutil

data_path = "/home/igs/yhj_demo/PythonProject/HBoxData/HQR/JPEGImages"

rk_data_path = "H"

if not os.path.exists(rk_data_path):
    os.makedirs(rk_data_path)

files = []
for file in os.listdir(data_path):
    if file.endswith(".jpg"):
        files.append(file)

score = 400 / len(files)

print(len(files), score)
with open(f"{rk_data_path}.txt", 'w') as f:
    for file in files:
        ra = random.randint(1, 100)
        if ra < score * 100:
            f.write(f"./{rk_data_path}/{file}\n")
            shutil.copy(os.path.join(data_path, file), os.path.join(rk_data_path, file))
