
# 项目结构说明

### 文件结构

```
├── classes.txt               # COCO 标签文件
├── coco128                   # COCO128 数据集
├── coco_164                  # COCO 图像 164 数据集
├── count_labels.py           # 标签计数脚本
├── create_none_labels.py     # 创建空标签文件脚本
├── create_rk_dataset.py      # 创建 RKNN 校验数据集脚本
├── data_augmentation.py      # 数据增强脚本
├── findNone.py               # 移动空背景图片脚本
├── one_in_ten.py             # 10 取 1 图片脚本
├── optimized_tag.py          # 删除大的目标标签脚本
├── motion_blur_data          # 运动模糊图像和优化后的标签文件夹
├── motionblur_img_txt.py     # 生成运动模糊图像和优化后的标签脚本
├── partition_dataset.py      # 划分数据集脚本
├── person.jpeg               # 示例图片
├── README.zh-CN.md           # 中文说明文档
├── rename_img_labels.py      # 重命名图像和对应的标签文件脚本
├── save_video.py             # 摄像头拍摄视频脚本
├── split_imgs_file.py        # 拆分图片文件到多个目录脚本
└── video                     # 视频文件夹

crop_image_from_yolo_txt.py   # 要根据YOLO格式的txt文件裁剪图像并保存
xmltoyolo.py                  # voc xml to yolo
```

### 详细说明

- **classes.txt**: 包含 COCO 数据集的类别标签。
- **coco128**: COCO128 数据集文件夹。
- **coco_164**: COCO 图像 164 数据集文件夹。
- **count_labels.py**: 统计标签文件中各类别标签的数量。
- **create_none_labels.py**: 创建空的标签文件，通常用于没有目标对象的图像。
- **create_rk_dataset.py**: 创建用于 RKNN 模型校验的数据集。
- **data_augmentation.py**: 实现数据增强功能，如图像旋转、缩放、翻转等。
- **findNone.py**: 查找并移动没有目标对象的背景图片。
- **one_in_ten.py**: 从每 10 张图片中随机选取 1 张，用于减少数据集规模。
- **optimized_tag.py**: 删除标签文件中过大的目标标签，通常用于去除噪声或错误标注。
- **motion_blur_data**: 包含运动模糊处理后的图像和优化后的标签文件。
- **motionblur_img_txt.py**: 生成运动模糊图像并更新对应的标签文件。
- **partition_dataset.py**: 将数据集划分为训练集、验证集和测试集。
- **person.jpeg**: 示例图片文件。
- **README.zh-CN.md**: 项目的中文说明文档。
- **rename_img_labels.py**: 批量重命名图像文件和对应的标签文件。
- **save_video.py**: 通过摄像头拍摄视频并保存。
- **split_imgs_file.py**: 将图片文件拆分到多个目录中，通常用于数据集的分布式处理。
- **video**: 存放视频文件的文件夹。
- **crop_image_from_yolo_txt**:要根据YOLO格式的txt文件裁剪图像并保存