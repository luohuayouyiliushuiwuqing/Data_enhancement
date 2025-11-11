#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：rknn_model_zoo 
@File    ：create_rk_dataset.py
@IDE     ：PyCharm 
@Author  ：高筱六和栾昊六
@Date    ：2025/3/3 13:45 
"""
import os
import random
import shutil

data_path = "/data/CombineData/OriginalData/Urban-Surv-HV-UAV/Aviation-UAV/JPEGImages"
rk_data_path = "Aviation-UAV"

# 创建目标目录（如果不存在）
if not os.path.exists(rk_data_path):
    os.makedirs(rk_data_path)

# 获取所有jpg文件
image_files = [file for file in os.listdir(data_path) if file.endswith(".jpg")]
total_files = len(image_files)
print(f"找到{total_files}个JPG文件")

# 确定需要选择的文件数量（最多400个）
num_files_to_select = min(400, total_files)

# 随机选择指定数量的文件
selected_files = random.sample(image_files, num_files_to_select)

# 复制选中的文件并记录路径
with open(f"{rk_data_path}.txt", 'w') as f:
    for file in selected_files:
        # 写入文件路径到文本
        f.write(f"./{rk_data_path}/{file}\n")
        # 复制文件到目标目录
        src_path = os.path.join(data_path, file)
        dest_path = os.path.join(rk_data_path, file)
        shutil.copy(src_path, dest_path)

print(f"已成功复制{len(selected_files)}个文件到{rk_data_path}目录")
