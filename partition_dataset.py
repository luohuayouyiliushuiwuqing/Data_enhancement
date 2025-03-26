# coding=utf-8
# vim:set fileencoding=utf-8:

import os
import shutil
import random

if __name__ == '__main__':
    base_path = "/home/igs/yhj_demo/Data_enhancement/Drone_mixout"

    # 定义数据路径
    new_image_folder = os.path.join(base_path, "images")
    new_label_folder = os.path.join(base_path, "labels")

    train_image_folder = os.path.join(base_path, 'coco73', 'images', 'train')
    val_image_folder = os.path.join(base_path, 'coco73', 'images', 'val')
    train_label_folder = os.path.join(base_path, 'coco73', 'labels', 'train')
    val_label_folder = os.path.join(base_path, 'coco73', 'labels', 'val')

    # 创建训练集和验证集文件夹
    os.makedirs(train_image_folder, exist_ok=True)
    os.makedirs(val_image_folder, exist_ok=True)
    os.makedirs(train_label_folder, exist_ok=True)
    os.makedirs(val_label_folder, exist_ok=True)

    # 获取所有图片文件
    image_files = [f for f in os.listdir(new_image_folder) if f.endswith('.jpg')]

    # 按照 7:3 划分训练集和验证集
    train_size = int(0.7 * len(image_files))
    random.shuffle(image_files)

    train_images = image_files[:train_size]
    val_images = image_files[train_size:]

    # 复制文件到训练集
    for image in train_images:
        label_name = image.replace('.jpg', '.txt')
        label_path = os.path.join(new_label_folder, label_name)

        shutil.copy(os.path.join(new_image_folder, image), os.path.join(train_image_folder, image))

        # 如果标签文件存在，复制它，否则创建一个空的标签文件
        if os.path.exists(label_path):
            shutil.copy(label_path, os.path.join(train_label_folder, label_name))
        else:
            open(os.path.join(train_label_folder, label_name), 'w').close()  # 创建空的 .txt 文件

    # 复制文件到验证集
    for image in val_images:
        label_name = image.replace('.jpg', '.txt')
        label_path = os.path.join(new_label_folder, label_name)

        shutil.copy(os.path.join(new_image_folder, image), os.path.join(val_image_folder, image))

        # 如果标签文件存在，复制它，否则创建一个空的标签文件
        if os.path.exists(label_path):
            shutil.copy(label_path, os.path.join(val_label_folder, label_name))
        else:
            open(os.path.join(val_label_folder, label_name), 'w').close()  # 创建空的 .txt 文件

    print("数据集划分完成！训练集和验证集已准备好。")
