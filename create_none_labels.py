#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement 
@File    ：create_none_labels.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/6 18:10 
"""
import os

# 定义路径
train_image_folder = '/home/igs/yhj_demo/DroneDetectionDataset/ALL_DATA_50000/images'
train_label_folder = '/home/igs/yhj_demo/DroneDetectionDataset/ALL_DATA_50000/labels'

val_image_folder = ''
val_label_folder = '/home/igs/yhj_demo/DroneDetectionDataset/coco/new_only5000/new/coco/labels/0321_val'

# 确保标签文件夹存在
os.makedirs(train_label_folder, exist_ok=True)
os.makedirs(val_label_folder, exist_ok=True)

# 补全训练集标签
train_images = [f for f in os.listdir(train_image_folder) if f.endswith('.jpg')]
for image in train_images:
    label_name = image.replace('.jpg', '.txt')
    label_path = os.path.join(train_label_folder, label_name)

    # 如果标签文件不存在，则创建空文件
    if not os.path.exists(label_path):
        open(label_path, 'w').close()
        print(f"创建空标签文件: {label_path}")

# # 补全验证集标签
# val_images = [f for f in os.listdir(val_image_folder) if f.endswith('.jpg')]
# for image in val_images:
#     label_name = image.replace('.jpg', '.txt')
#     label_path = os.path.join(val_label_folder, label_name)
#
#     # 如果标签文件不存在，则创建空文件
#     if not os.path.exists(label_path):
#         open(label_path, 'w').close()
#         print(f"创建空标签文件: {label_path}")

print("所有缺失的标签文件已补全！")
