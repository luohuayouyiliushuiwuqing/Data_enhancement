# coding:utf-8
import cv2
import os
import glob
import numpy as np


def convert_to_jpg(input_dir, output_dir, prefix="image_"):
    """
    批量将图片转换为JPG格式并重新命名

    参数:
    input_dir: 输入图片所在目录
    output_dir: 输出JPG图片目录
    prefix: 输出文件的前缀
    """
    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 支持的图片格式
    image_extensions = ['*.png', '*.bmp', '*.gif', '*.tiff', '*.jpeg', '*.jpg']
    image_files = []

    # 收集所有图片文件
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, ext)))

    # 去重（防止同一文件被多次处理）
    image_files = list(set(image_files))

    if not image_files:
        print(f"在目录 {input_dir} 中未找到任何图片文件")
        return

    # 处理每张图片
    for i, img_path in enumerate(image_files, 1):
        try:
            # 读取图片
            # 使用cv2.IMREAD_UNCHANGED保留透明度通道（如果有）
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

            if img is None:
                print(f"无法读取图片: {img_path}")
                continue

            # 生成新文件名
            new_filename = f"{prefix}{i:04d}.jpg"  # 格式如：image_0001.jpg
            output_path = os.path.join(output_dir, new_filename)

            # 转换并保存为JPG
            # JPG不支持透明度，需要处理Alpha通道
            if img.shape[-1] == 4:  # 检查是否有Alpha通道
                # 将透明背景转换为白色
                alpha_channel = img[:, :, 3]
                rgb_channels = img[:, :, :3]

                # 白色背景
                background = np.ones_like(rgb_channels, dtype=np.uint8) * 255

                # 组合图片
                alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
                alpha_factor = np.concatenate((alpha_factor, alpha_factor, alpha_factor), axis=2)

                img = (rgb_channels * alpha_factor + background * (1 - alpha_factor)).astype(np.uint8)

            # 保存为JPG，质量设置为95
            cv2.imwrite(output_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            print(f"已转换: {os.path.basename(img_path)} -> {new_filename}")

        except Exception as e:
            print(f"处理 {os.path.basename(img_path)} 时出错: {str(e)}")

    print(f"转换完成，共处理 {len(image_files)} 个文件")


if __name__ == "__main__":
    # # 设置输入和输出目录
    # input_directory = "./input_images"  # 输入图片所在目录
    # output_directory = "./output_jpgs"  # 输出JPG图片目录
    # file_prefix = "photo_"  # 输出文件前缀
    #
    # # 执行转换
    # convert_to_jpg(input_directory, output_directory, file_prefix)

    # 设置输入和输出目录
    input_directorys = "/home/igs/yhj_demo/Data_enhancement/OriginalData/Drone/DroneDetectionDataset/Crawled images"  # 输入图片所在目录
    output_directory = "./output_jpgs"  # 输出JPG图片目录
    i = 0
    for input_dir in os.listdir(input_directorys):
        convert_to_jpg(os.path.join(input_directorys, input_dir), output_directory, "photo_{}_".format(i))
        i = i + 1
