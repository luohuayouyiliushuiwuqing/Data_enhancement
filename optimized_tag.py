#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement 
@File    ：optimized_tag.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/6 13:47 
"""
import os

if __name__ == '__main__':
    # 数据集路径
    data_base_path = "/home/igs/yhj_demo/DroneDetectionDataset/ALL_DATA_50000"
    img_base_path = os.path.join(data_base_path, "images")
    label_base_path = os.path.join(data_base_path, "labels")

    # 设定目标尺寸阈值 (超出这个比例的目标将被删除)
    max_width = 0.5  # 相对图片宽度的最大比例
    max_height = 0.8  # 相对图片高度的最大比例

    # 获取文件列表
    img_list = os.listdir(img_base_path)
    label_list = os.listdir(label_base_path)

    for label_file in label_list:
        label_path = os.path.join(label_base_path, label_file)
        img_path = os.path.join(img_base_path, label_file.replace(".txt", ".jpg"))  # 假设图片是jpg格式

        if not os.path.exists(img_path):
            continue  # 若对应的图片不存在，则跳过

        keep_label = []  # 存储需要保留的标签

        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # 跳过格式错误的行

            _, x_center, y_center, width, height = map(float, parts)

            # 判断目标是否过大
            if width > max_width or height > max_height:
                continue  # 过滤掉过大的目标
            else:
                keep_label.append(line)

        if keep_label:
            with open(label_path, "w") as f:
                f.writelines(keep_label)  # 只保留小目标
        else:
            # 如果所有目标都过大，则删除该图片和标签
            os.remove(label_path)
            os.remove(img_path)
            print(f"Deleted {img_path} and {label_path} due to large objects.")
