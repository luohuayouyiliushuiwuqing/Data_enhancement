import os
import random

import cv2
import numpy as np


def motion_blur(image, degree=12, angle=0):
    """对图像施加运动模糊"""
    image = np.array(image)  # 转换为 numpy 数组
    kernel = np.zeros((degree, degree), dtype=np.float32)
    center = degree // 2
    angle_rad = np.deg2rad(angle)

    for i in range(degree):
        x = int(center + (i - center) * np.cos(angle_rad))
        y = int(center + (i - center) * np.sin(angle_rad))
        if 0 <= x < degree and 0 <= y < degree:
            kernel[x, y] = 1

    kernel /= np.sum(kernel)
    blurred = cv2.filter2D(image, -1, kernel)
    return blurred


def adjust_bbox(x_center, y_center, width, height, degree):
    """根据运动模糊程度调整YOLO标签框"""
    expansion_ratio = 1 + degree * 0.002  # 根据模糊程度扩展目标框
    width = min(1.0, width * expansion_ratio)
    height = min(1.0, height * expansion_ratio)
    x_center = min(1.0, max(0.0, x_center))  # 确保坐标不超出范围
    y_center = min(1.0, max(0.0, y_center))

    return x_center, y_center, width, height


# def adjust_bbox(x_center, y_center, width, height, degree):
#     """根据运动模糊程度调整YOLO标签框（保留六位小数）"""
#     expansion_ratio = 1 + degree * 0.02  # 根据模糊程度扩展目标框
#     width = min(1.0, round(width * expansion_ratio, 6))
#     height = min(1.0, round(height * expansion_ratio, 6))
#     x_center = round(min(1.0, max(0.0, x_center)), 6)  # 确保坐标不超出范围
#     y_center = round(min(1.0, max(0.0, y_center)), 6)
#
#     return x_center, y_center, width, height

def Motionblur_img_txt(img, degree, angle):
    # 应用运动模糊
    img_blurred = motion_blur(img, degree=degree, angle=angle)
    # 读取标签并修改
    with open(label_path, "r") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue

        class_id = parts[0]
        x_center, y_center, width, height = map(float, parts[1:5])
        x_center, y_center, width, height = adjust_bbox(x_center, y_center, width, height, degree)

        new_lines.append(f"{class_id} {x_center} {y_center} {width} {height}\n")
    # 生成保存文件名
    output_img_name = f"blur_{img_file.split('.')[0]}_{degree}_{angle}.jpg"
    output_label_name = f"blur_{img_file.split('.')[0]}_{degree}_{angle}.txt"
    output_img_file = os.path.join(output_img_path, output_img_name)
    output_label_file = os.path.join(output_label_path, output_label_name)
    # 保存处理后的图片和标签
    cv2.imwrite(output_img_file, img_blurred)
    with open(output_label_file, "w") as f:
        f.writelines(new_lines)


if __name__ == '__main__':

    # 数据路径
    data_base_path = "/home/igs/yhj_demo/DroneDetectionDataset/coco/new_only5000"
    img_base_path = os.path.join(data_base_path, "images")
    label_base_path = os.path.join(data_base_path, "labels")

    # 输出目录
    output_img_path = os.path.join(data_base_path, "blur", "images")
    output_label_path = os.path.join(data_base_path, "blur", "labels")
    os.makedirs(output_img_path, exist_ok=True)
    os.makedirs(output_label_path, exist_ok=True)

    # 处理所有图片和标签
    img_list = os.listdir(img_base_path)
    label_list = os.listdir(label_base_path)

    p = 30

    for img_file in img_list:
        ra = random.randint(0, 100)
        if ra < p:
            continue
        img_path = os.path.join(img_base_path, img_file)
        label_file = img_file.replace(".jpg", ".txt")  # 假设图片是 jpg 格式
        label_path = os.path.join(label_base_path, label_file)

        if not os.path.exists(label_path):
            continue  # 跳过没有标签的图片

        # 读取图片
        img = cv2.imread(img_path)

        degree = random.randint(2, 20)
        angle = random.randint(0, 360)

        Motionblur_img_txt(img, degree, angle)

    print("运动模糊图像和优化后的标签已生成!")
