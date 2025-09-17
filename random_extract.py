#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
"""
@Project ：Data_enhancement
@File    ：random_extract.py
@IDE     ：PyCharm
@Author  ：高筱六和栾昊六
@Date    ：2025/3/6 13:12
@Function：从指定数据集中随机抽取部分图像和标签文件复制到新目录
"""

import os
import shutil
import random
from typing import Optional

from utils.pathutils import get_valid_path, img_possible_names, label_possible_names


def ensure_dir(path: str) -> None:
    """确保目录存在，不存在则创建"""
    if not os.path.exists(path):
        os.makedirs(path)


def random_copy_files(src_dir: str, dst_dir: str, suffix: Optional[str], prob: float) -> None:
    """
    从源目录随机抽取文件复制到目标目录
    :param src_dir: 源目录
    :param dst_dir: 目标目录
    :param suffix: 文件后缀（如 .jpg / .txt），None 表示所有文件
    :param prob: 抽取概率（0~1）
    """
    ensure_dir(dst_dir)
    file_list = sorted(os.listdir(src_dir))

    for file_name in file_list:
        if suffix and not file_name.endswith(suffix):
            continue
        if random.random() < prob:
            src_path = os.path.join(src_dir, file_name)
            dst_path = os.path.join(dst_dir, file_name)
            shutil.copy(src_path, dst_path)


def copy_images_and_labels(base_path: str, new_name: str, prob: float) -> None:
    """随机复制 images 和 labels 文件"""
    img_src = get_valid_path(base_path, img_possible_names)
    label_src = get_valid_path(base_path, label_possible_names)

    img_dst = os.path.join(base_path, new_name, "images")
    label_dst = os.path.join(base_path, new_name, "labels")

    ensure_dir(img_dst)
    ensure_dir(label_dst)

    img_list = sorted(os.listdir(img_src))
    for img_name in img_list:
        if random.random() < prob:
            label_name = img_name.rsplit(".", 1)[0] + ".txt"
            img_path = os.path.join(img_src, img_name)
            label_path = os.path.join(label_src, label_name)

            if os.path.exists(img_path) and os.path.exists(label_path):
                shutil.copy(img_path, os.path.join(img_dst, img_name))
                shutil.copy(label_path, os.path.join(label_dst, label_name))


if __name__ == "__main__":
    data_base_path = "/data/CombineData/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV"
    extract_prob = 0.1

    # # 随机复制单独的 images（可选，独立功能）
    # random_copy_files(
    #     src_dir=os.path.join(data_base_path, "images"),
    #     dst_dir=os.path.join(data_base_path, str(extract_prob * 100), "images_back"),
    #     suffix=".jpg",
    #     prob=extract_prob,
    # )

    # 随机复制成对的 image + label（主功能）
    copy_images_and_labels(data_base_path, str(extract_prob * 100), prob=extract_prob)
