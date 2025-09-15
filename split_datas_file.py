# coding=utf-8
# vim:set fileencoding=utf-8:

import os
import shutil


def get_valid_path(base_path, possible_names):
    """获取存在的文件夹路径"""
    for name in possible_names:
        path = os.path.join(base_path, name)
        if os.path.exists(path) and os.path.isdir(path):
            return path, name
    raise FileNotFoundError(f"在{base_path}下未找到任何一个文件夹: {possible_names}")


base_path = "/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV_0915"
# 图像文件夹可能的名称
img_possible_names = ["images", "JPEGImages"]
# 标签文件夹可能的名称
label_possible_names = ["labels", "YOLOLabels"]

# 获取实际存在的图像和标签文件夹路径
img_path, img_folder_name = get_valid_path(base_path, img_possible_names)
label_path, label_folder_name = get_valid_path(base_path, label_possible_names)

output_base_path = base_path + "_Split"

count = 0
folder_count = 1
folder_limit = 5000

if not os.path.exists(output_base_path):
    os.makedirs(output_base_path)

back_name = "folder_back"
back_path = os.path.join(output_base_path, back_name)
back_img_path = os.path.join(back_path, img_folder_name)
if not os.path.exists(back_img_path):
    os.makedirs(back_img_path)

for filename in os.listdir(img_path):
    if filename.endswith(('.jpg')):
        if count % folder_limit == 0:
            folder_name = f"folder_{folder_count}"
            folder_path = os.path.join(output_base_path, folder_name)
            folder_img_path = os.path.join(folder_path, img_folder_name)
            folder_label_path = os.path.join(folder_path, label_folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            if not os.path.exists(folder_img_path):
                os.makedirs(folder_img_path)
            if not os.path.exists(folder_label_path):
                os.makedirs(folder_label_path)
            folder_count += 1

        src_image_path = os.path.join(img_path, filename)
        dest_image_path = os.path.join(folder_img_path, filename)

        label_name = filename.replace('.jpg', '.txt')
        src_label_path = os.path.join(label_path, label_name)
        dest_label_path = os.path.join(folder_label_path, label_name)

        if os.path.exists(src_image_path) and os.path.exists(src_label_path):
            shutil.copy(src_image_path, dest_image_path)
            shutil.copy(src_label_path, dest_label_path)
        elif os.path.exists(src_image_path) and not os.path.exists(src_label_path):
            back_dest_image_path = os.path.join(back_img_path, filename)
            shutil.copy(src_image_path, back_dest_image_path)

        count += 1
