#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement 
@File    ：findNone.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/6 12:59 
"""
import os
import shutil
if __name__ == '__main__':

    data_base_path = "/home/igs/yhj_demo/Data_enhancement/OriginalData/HQR"

    if not os.path.exists(os.path.join(data_base_path, "Nonelabel_img")):
        os.makedirs(os.path.join(data_base_path, "Nonelabel_img"))

    img_base_path = os.path.join(data_base_path, "JPEGImages")
    label_base_path = os.path.join(data_base_path, "YOLOLabels")
    # img_base_path = "/home/igs/yhj_demo/Data_enhancement/Drone_val/images/val"
    # label_base_path = "/home/igs/yhj_demo/Data_enhancement/Drone_val/labels/val"

    img_list = os.listdir(img_base_path)
    label_list = os.listdir(label_base_path)

    count = 0

    for img_name in img_list:
        img_path = os.path.join(img_base_path, img_name)
        txt_name = img_name.replace(".jpg", ".txt")
        label_path = os.path.join(label_base_path, txt_name)
        if os.path.exists(label_path) is False:
            # print(img_path)
            shutil.move(img_path, os.path.join(f"{data_base_path}/Nonelabel_img", img_name))
            # os.remove(img_path)
            count += 1
    print(count)
