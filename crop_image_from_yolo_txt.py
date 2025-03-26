#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement 
@File    ：crop_image_from_yolo_txt.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/7 17:48 
"""
import cv2
import numpy as np
import os


def crop_image_from_yolo_txt(image_path, txt_path, output_dir):
    """
    根据 YOLO 格式的 txt 文件裁剪图像并保存
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return

    img_height, img_width = image.shape[:2]

    # 读取 txt 文件
    with open(txt_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        # 解析每一行
        parts = line.strip().split()
        if len(parts) != 5:
            print(f"跳过无效行: {line}")
            continue

        class_id, x_center, y_center, width, height = map(float, parts)

        # 将归一化坐标转换为绝对坐标
        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height

        # 计算边界框的左上角和右下角坐标
        x1 = int(x_center - width / 2)
        y1 = int(y_center - height / 2)
        x2 = int(x_center + width / 2)
        y2 = int(y_center + height / 2)

        # 确保边界框在图像范围内
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(img_width, x2)
        y2 = min(img_height, y2)

        # 裁剪图像
        cropped_image = image[y1:y2, x1:x2]

        # 保存裁剪后的图像
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_crop_{i}.jpg")
        cv2.imwrite(output_path, cropped_image)
        # print(f"保存裁剪图像: {output_path}")


def batch_crop_images_and_labels(images_dir, labels_dir, output_dir):
    """
    批量处理 images 和 labels 文件夹中的图像和标签
    """
    # 遍历 images 文件夹中的所有图像
    for image_name in os.listdir(images_dir):
        if not image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            continue

        # 构建图像路径和对应的标签路径
        image_path = os.path.join(images_dir, image_name)
        label_name = os.path.splitext(image_name)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_name)

        # 如果标签文件存在，则处理
        if os.path.exists(label_path):
            crop_image_from_yolo_txt(image_path, label_path, output_dir)
        else:
            print(f"未找到标签文件: {label_path}")


path = "0311_val"

# 示例使用
images_train_dir = os.path.join(path, 'images/')  # 训练集图像文件夹
labels_train_dir = os.path.join(path, 'labels/')  # 训练集标签文件夹
output_train_dir = os.path.join(path, 'cropped_images/')  # 训练集裁剪图像输出文件夹

# images_val_dir = os.path.join(path, 'images/0321_val')  # 验证集图像文件夹
# labels_val_dir = os.path.join(path, 'labels/0321_val')  # 验证集标签文件夹
# output_val_dir = os.path.join(path, 'cropped_images/0321_val')  # 验证集裁剪图像输出文件夹

# 处理训练集
print("处理训练集...")
batch_crop_images_and_labels(images_train_dir, labels_train_dir, output_train_dir)

# # 处理验证集
# print("处理验证集...")
# batch_crop_images_and_labels(images_val_dir, labels_val_dir, output_val_dir)

print("处理完成！")
