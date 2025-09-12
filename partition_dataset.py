# coding=utf-8
# vim:set fileencoding=utf-8:

import os
import shutil
import random

if __name__ == '__main__':
    base_path = "/home/igs/yhj_demo/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Basic_Data/VisDrone2019-DET-val"

    # 定义数据路径
    new_image_folder = os.path.join(base_path, "JPEGImages")
    new_label_folder = os.path.join(base_path, "YOLOLabels")

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
    total_count = len(image_files)

    if total_count == 0:
        print("错误：在JPEGImages文件夹中未找到任何.jpg文件！")
        exit(1)

    # 按照 7:3 划分训练集和验证集
    train_size = int(0.7 * total_count)

    # 随机选择训练集样本（核心随机分配部分）
    train_images = random.sample(image_files, train_size)
    # 验证集为不在训练集中的样本
    val_images = [img for img in image_files if img not in train_images]

    print(f"数据集划分完成：总样本数 {total_count}，训练集 {len(train_images)}，验证集 {len(val_images)}")

    # 复制文件到训练集
    for image in train_images:
        label_name = image.replace('.jpg', '.txt')
        label_path = os.path.join(new_label_folder, label_name)

        # 复制图片
        shutil.copy(
            os.path.join(new_image_folder, image),
            os.path.join(train_image_folder, image)
        )

        # 处理标签文件
        dest_label = os.path.join(train_label_folder, label_name)
        if os.path.exists(label_path):
            shutil.copy(label_path, dest_label)
        else:
            # 创建空标签文件
            with open(dest_label, 'w', encoding='utf-8') as f:
                pass

    # 复制文件到验证集
    for image in val_images:
        label_name = image.replace('.jpg', '.txt')
        label_path = os.path.join(new_label_folder, label_name)

        # 复制图片
        shutil.copy(
            os.path.join(new_image_folder, image),
            os.path.join(val_image_folder, image)
        )

        # 处理标签文件
        dest_label = os.path.join(val_label_folder, label_name)
        if os.path.exists(label_path):
            shutil.copy(label_path, dest_label)
        else:
            # 创建空标签文件
            with open(dest_label, 'w', encoding='utf-8') as f:
                pass

    print("数据集划分完成！训练集和验证集已准备好。")
