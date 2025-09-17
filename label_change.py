# coding : utf-8
# vim: set fileencoding=utf-8 :
import os

# 文件夹路径
labels_base_path = "/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Basic_Data/coco_car/labels"

target_e = {"0": 0, "2": 1, "4": "3"}

txt_names = os.listdir(labels_base_path)
for txt_name in txt_names:
    txt_path = os.path.join(labels_base_path, txt_name)
    update_lines = []
    with open(txt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            if parts and parts[0] in target_e.keys():
                parts[0] = str(target_e[parts[0]])
                updated_line = " ".join(parts) + "\n"
                update_lines.append(updated_line)
    with open(txt_path, 'w') as f:
        f.writelines(update_lines)
