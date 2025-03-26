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

path = "/home/igs/yhj_demo/RknnProjects/Projects/rknn_model_zoo/datasets/new_data/dataset_outdoor"

files = os.listdir(path)

# 写入文件
with open("/home/igs/yhj_demo/RknnProjects/Projects/rknn_model_zoo/datasets/new_data/dataset_outdoor.txt", 'w') as f:
    for file in files:
        f.write(f"{os.path.join('/home/igs/yhj_demo/RknnProjects/Projects/rknn_model_zoo/datasets/new_data/dataset_outdoor',file)}\n")
