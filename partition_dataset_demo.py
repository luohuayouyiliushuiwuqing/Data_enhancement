import os
import shutil
import random

from utils.pathutils import get_valid_path, img_possible_names, label_possible_names


def copy_with_empty_label(src_img, src_label, dst_img, dst_label):
    """复制图片和标签，如果标签不存在则创建空文件"""
    shutil.copy(src_img, dst_img)
    if os.path.exists(src_label):
        shutil.copy(src_label, dst_label)
    else:
        with open(dst_label, 'w', encoding='utf-8') as f:
            pass


if __name__ == '__main__':
    base_path = "/data/DATA/CombineData/OriginalData/Urban-Surv-HV-UAV/to_server/Aviation-UAV-Drone"

    # 获取实际存在的图像和标签文件夹路径
    new_image_folder, _ = get_valid_path(base_path, img_possible_names)
    new_label_folder_Tight, _ = get_valid_path(base_path, ["YOLOLabels_Tight"])
    new_label_folder_Loose, _ = get_valid_path(base_path, ["YOLOLabels_Loose"])

    # 定义目标文件夹
    train_loose_image_folder = os.path.join(base_path, 'loose', 'images', 'train')
    val_loose_image_folder = os.path.join(base_path, 'loose', 'images', 'val')
    train_loose_label_folder = os.path.join(base_path, 'loose', 'labels', 'train')
    val_loose_label_folder = os.path.join(base_path, 'loose', 'labels', 'val')

    train_tight_image_folder = os.path.join(base_path, 'tight', 'images', 'train')
    val_tight_image_folder = os.path.join(base_path, 'tight', 'images', 'val')
    train_tight_label_folder = os.path.join(base_path, 'tight', 'labels', 'train')
    val_tight_label_folder = os.path.join(base_path, 'tight', 'labels', 'val')

    # 创建训练集和验证集文件夹
    os.makedirs(train_loose_image_folder, exist_ok=True)
    os.makedirs(val_loose_image_folder, exist_ok=True)
    os.makedirs(train_loose_label_folder, exist_ok=True)
    os.makedirs(val_loose_label_folder, exist_ok=True)

    os.makedirs(train_tight_image_folder, exist_ok=True)
    os.makedirs(val_tight_image_folder, exist_ok=True)
    os.makedirs(train_tight_label_folder, exist_ok=True)
    os.makedirs(val_tight_label_folder, exist_ok=True)

    # 计数器
    total_count = 0
    train_count = 0
    val_count = 0

    # 按 7:3 随机划分
    split_ratio = 0.7

    # 遍历图片并直接划分
    for file_name in os.listdir(new_image_folder):
        if not file_name.endswith('.jpg'):
            continue

        total_count += 1
        img_path = os.path.join(new_image_folder, file_name)
        label_name = file_name.replace('.jpg', '.txt')
        label_path_Loose = os.path.join(new_label_folder_Loose, label_name)
        label_path_tight = os.path.join(new_label_folder_Tight, label_name)

        if random.random() < split_ratio:
            dst_loose_img = os.path.join(train_loose_image_folder, file_name)
            dst_loose_label = os.path.join(train_loose_label_folder, label_name)
            copy_with_empty_label(img_path, label_path_Loose, dst_loose_img, dst_loose_label)

            dst_tight_img = os.path.join(train_tight_image_folder, file_name)
            dst_tight_label = os.path.join(train_tight_label_folder, label_name)
            copy_with_empty_label(img_path, label_path_tight, dst_tight_img, dst_tight_label)

            train_count += 1
        else:
            dst_loose_img = os.path.join(val_loose_image_folder, file_name)
            dst_loose_label = os.path.join(val_loose_label_folder, label_name)
            copy_with_empty_label(img_path, label_path_Loose, dst_loose_img, dst_loose_label)

            dst_tight_img = os.path.join(val_tight_image_folder, file_name)
            dst_tight_label = os.path.join(val_tight_label_folder, label_name)
            copy_with_empty_label(img_path, label_path_tight, dst_tight_img, dst_tight_label)

            val_count += 1

    print(f"数据集划分完成：")
    print(f"- 总样本数：{total_count}")
    print(f"- 训练集：{train_count}（占比：{train_count/total_count:.2%}）")
    print(f"- 验证集：{val_count}（占比：{val_count/total_count:.2%}）")
