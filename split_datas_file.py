# coding=utf-8
# vim:set fileencoding=utf-8:

import os
import shutil
from pathlib import Path

from utils.pathutils import get_valid_path, img_possible_names, label_possible_names

base_path = "/data/CombineData/OriginalData/Urban-Surv-HV-UAV/Basic_Data/coco_car"

# 获取实际存在的图像和标签文件夹路径
img_path, img_folder_name = get_valid_path(base_path, img_possible_names)
label_path, label_folder_name = get_valid_path(base_path, label_possible_names)

output_base_path = os.path.join(base_path, Path(base_path).name + "_Split")

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
    if filename.endswith('.jpg'):
        if count % folder_limit == 0:
            folder_name = f"folder_{folder_count}" # 固定folder名称，方便脚本运行
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
