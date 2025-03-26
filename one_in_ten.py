#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement 
@File    ：one_in_ten.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/6 13:12 
"""
import os
import shutil

data_base_path = "/home/igs/yhj_demo/DroneDetectionDataset/coco"

img_base_path = os.path.join(data_base_path, "images")
label_base_path = os.path.join(data_base_path, "labels")

img_list = os.listdir(img_base_path)
label_list = os.listdir(label_base_path)

img_list.sort()

img_new_path = os.path.join(data_base_path, "new", "images")
label_new_path = os.path.join(data_base_path, "new", "labels")

if not os.path.exists(img_new_path):
    os.makedirs(img_new_path)

if not os.path.exists(label_new_path):
    os.makedirs(label_new_path)

count = 0
for img_name in img_list:
    img_path = os.path.join(img_base_path, img_name)
    label_name=img_name.replace(".jpg", ".txt")
    label_path = os.path.join(label_base_path, label_name)

    if count % 10 == 0:
        shutil.copy(img_path, os.path.join(img_new_path, img_name))
        shutil.copy(label_path, os.path.join(label_new_path, label_name))

    count += 1
