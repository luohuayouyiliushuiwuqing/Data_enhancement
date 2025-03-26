#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement 
@File    ：rename_img_labels.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/6 18:33 
"""
import os


def rename_files(image_folder, label_folder, prefix=""):
    """
    统一修改 image_folder 和 label_folder 下的文件名，确保匹配
    """
    # 获取所有图片文件（按名字排序，保持一致性）
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.jpg')])

    for idx, image_file in enumerate(image_files, start=1):
        # 生成新文件名（6 位数字，不足补 0，例如 000001.jpg）
        new_name = f"{prefix}{idx:06d}"
        new_image_name = f"{new_name}.jpg"
        new_label_name = f"{new_name}.txt"

        # 原文件路径
        old_image_path = os.path.join(image_folder, image_file)
        old_label_path = os.path.join(label_folder, image_file.replace('.jpg', '.txt'))

        # 新文件路径
        new_image_path = os.path.join(image_folder, new_image_name)
        new_label_path = os.path.join(label_folder, new_label_name)

        # 重命名图片
        os.rename(old_image_path, new_image_path)

        # 只有在标签文件存在时才重命名，否则创建空的 .txt 文件
        if os.path.exists(old_label_path):
            os.rename(old_label_path, new_label_path)
        else:
            open(new_label_path, 'w').close()  # 创建空标签文件

        print(f"重命名: {image_file} -> {new_image_name}, 标签: {new_label_name}")


# 训练集
train_image_folder = '0321_val/images'
train_label_folder = '0321_val/labels'
rename_files(train_image_folder, train_label_folder)

# # 验证集
# val_image_folder = '/home/igs/yhj_demo/DroneDetectionDataset/coco/new_only5000/new/coco/images/0321_val'
# val_label_folder = '/home/igs/yhj_demo/DroneDetectionDataset/coco/new_only5000/new/coco/labels/0321_val'
# rename_files(val_image_folder, val_label_folder)

print("所有文件重命名完成！")
