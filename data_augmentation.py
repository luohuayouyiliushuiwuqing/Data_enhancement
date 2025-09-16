import os
import shutil
import time

import albumentations as A
import cv2

"""
该脚本主要实现了利用albumentations工具包对yolo标注数据进行增强
给定一个存放图像和标注文件的主目录，在主目录下自动生成增强的图像和标注文件
"""

BEGIN_TIME = time.strftime("%m%d%H", time.localtime())
print(BEGIN_TIME)


# 读取并解析YOLO格式的标注文件
def read_yolo_annotation(label_files, label_list):
    yolo_b_boxes = open(label_files).read().splitlines()
    bboxes = []
    class_labels = []

    # 解析每个标注
    for b_box in yolo_b_boxes:
        b_box = b_box.split(" ")
        m_box = list(map(float, b_box[1:5]))  # YOLO格式的边界框
        m_class = b_box[0]
        bboxes.append(m_box)
        class_labels.append(label_list[int(m_class)])

    return bboxes, class_labels


# 保存增强后的图像和标注文件
def save_augmented_image_and_labels(transformed_image, transformed_bboxes, transformed_class_labels, label_list,
                                    new_name, enhance_images_files, enhance_labels_files):
    # 保存增强后的图像
    if not os.path.exists(enhance_images_files):
        os.makedirs(enhance_images_files)
    cv2.imwrite(os.path.join(enhance_images_files, new_name.replace(".txt", ".jpg")), transformed_image)

    # 保存增强后的标注文件
    if not os.path.exists(enhance_labels_files):
        os.makedirs(enhance_labels_files)

    # print(new_name)

    new_txt_file = open(os.path.join(enhance_labels_files, new_name), "w")
    for box, label in zip(transformed_bboxes, transformed_class_labels):
        new_class_num = label_list.index(label)
        box = list(box)
        # 格式化坐标精度为5位小数
        box = [str(round(coord, 5)) for coord in box]
        box.insert(0, str(new_class_num))
        new_txt_file.write(" ".join(box) + "\n")
    new_txt_file.close()


# 进行数据增强并保存图像和标注
def apply_data_augmentation(old_images_files, old_labels_files, label_list, enhance_images_files, enhance_labels_files):
    transform = A.Compose([
        A.GaussNoise(std_range=(0.1, 0.2), p=0.1),  # 10-20% of max value
        # A.RandomCrop(240, 320,p=0.1),
        A.HorizontalFlip(p=0.1),  # 水平翻转
        A.VerticalFlip(p=0.1),  # 垂直翻转
        A.RandomBrightnessContrast(p=0.1),  # 随机亮度和对比度变化
        # A.ShiftScaleRotate(p=0.1),
        A.Morphological(scale=(2, 6), p=0.1),
        A.ZoomBlur(p=0.1),
        # A.ConstrainedCoarseDropout(p=0.1),
    ], bbox_params=A.BboxParams(format='yolo', min_area=1024, min_visibility=0.2, label_fields=['class_labels']))

    mid_name = "_Augmentation" + BEGIN_TIME  # 文件名后缀

    label_files_name = os.listdir(old_labels_files)

    for name in label_files_name:
        label_file_path = os.path.join(old_labels_files, name)

        # 读取并解析YOLO标注
        bboxes, class_labels = read_yolo_annotation(label_file_path, label_list)

        # 读取图像
        image_path = os.path.join(old_images_files, name.replace(".txt", ".jpg"))
        if not os.path.exists(image_path):
            continue

        image = cv2.imread(image_path)
        # 图像增强
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            transformed_image = cv2.cvtColor(transformed['image'], cv2.COLOR_BGR2RGB)
            transformed_bboxes = transformed['bboxes']
            transformed_class_labels = transformed['class_labels']
        except Exception as e:
            # print(f"增强失败: {e}")
            continue

        # 文件名处理
        a, b = os.path.splitext(name)
        new_name = a + mid_name + b

        # 保存增强后的图像和标注
        save_augmented_image_and_labels(transformed_image, transformed_bboxes, transformed_class_labels, label_list,
                                        new_name, enhance_images_files, enhance_labels_files)


# 主函数，设置路径并执行增强过程
def main():
    root = "0321_val"

    # 原始图像和标注文件路径
    old_images_files = os.path.join(root, "images")
    old_labels_files = os.path.join(root, "labels")

    # 增强后的图像和标注文件保存路径
    enhance_images_files = os.path.join(root, "enhance", "images")
    enhance_labels_files = os.path.join(root, "enhance", "labels")

    label_list = ['Drone']

    # 执行数据增强
    apply_data_augmentation(old_images_files, old_labels_files, label_list, enhance_images_files, enhance_labels_files)


if __name__ == '__main__':
    main()
