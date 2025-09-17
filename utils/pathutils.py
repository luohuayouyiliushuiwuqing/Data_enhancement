#!/usr/bin/env python
# coding=utf-8
# vim:set fileencoding=utf-8:
import os

# 图像文件夹可能的名称
img_possible_names = ["images", "JPEGImages"]
# 标签文件夹可能的名称
label_possible_names = ["labels", "YOLOLabels"]


def get_valid_path(base_path, possible_names):
    """获取存在的文件夹路径"""
    for name in possible_names:
        path = os.path.join(base_path, name)
        if os.path.exists(path) and os.path.isdir(path):
            return path, name
    raise FileNotFoundError(f"在{base_path}下未找到任何一个文件夹: {possible_names}")
