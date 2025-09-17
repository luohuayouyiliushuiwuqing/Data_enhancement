#!/usr/bin/env python
# 功能：统计YOLO标签文件夹中各类别目标数量
# coding=utf-8
# vim:set fileencoding=utf-8:

import os
from typing import Dict, Tuple


def read_label_file(file_path: str) -> list[str]:
    """读取单个标签文件并返回每行内容（去除空行）"""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def count_classes_in_file(file_path: str) -> Dict[str, int]:
    """统计单个标签文件中的类别数量"""
    class_counts = {}
    for line in read_label_file(file_path):
        parts = line.split()
        if parts:
            class_id = parts[0]
            class_counts[class_id] = class_counts.get(class_id, 0) + 1
    return class_counts


def merge_counts(total_counts: Dict[str, int], file_counts: Dict[str, int]) -> None:
    """合并单个文件的统计结果到总统计中"""
    for class_id, count in file_counts.items():
        total_counts[class_id] = total_counts.get(class_id, 0) + count


def count_classes_in_folder(folder_path: str) -> Tuple[Dict[str, int], int]:
    """统计文件夹中所有标签文件的类别数量"""
    total_counts = {}
    total_objects = 0

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            file_counts = count_classes_in_file(file_path)
            merge_counts(total_counts, file_counts)
            total_objects += sum(file_counts.values())

    return total_counts, total_objects


def print_results(class_counts: Dict[str, int], total_objects: int) -> None:
    """打印统计结果"""
    print(f"总目标数量: {total_objects}\n")
    print("各目标类别数量统计:")
    for class_id in sorted(class_counts.keys(), key=lambda x: int(x)):
        print(f"类别 {class_id}: {class_counts[class_id]} 个")


if __name__ == "__main__":
    train_label_folder = "/data/CombineData/OriginalData/Urban-Surv-HV-UAV/Basic_Data/coco/labels"

    class_counts, total_objects = count_classes_in_folder(train_label_folder)
    print_results(class_counts, total_objects)
