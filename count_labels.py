#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement 
@File    ：count_labels.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/6 18:28 
"""
import os

# 定义标签文件夹路径
train_label_folder = '/home/igs/yhj_demo/Data_enhancement/Drone_val/labels/0321_val'

# 目标数量统计
total_objects = 0

# 遍历所有标签文件
for label_file in os.listdir(train_label_folder):
    if label_file.endswith('.txt'):
        label_path = os.path.join(train_label_folder, label_file)

        # 读取文件内容并统计行数（即目标数量）
        with open(label_path, 'r') as f:
            lines = f.readlines()
            total_objects += len(lines)

print(f"训练集（train）中的总目标数量: {total_objects}")
