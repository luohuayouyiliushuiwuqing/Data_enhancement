#!/bin/bash
set -e

BASE_DIR="/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV_Split"   # 修改为你的目录
OUT_PREFIX="archive"
NPROC=4                             # 并行任务数（建议设为 CPU 核心数）

export BASE_DIR OUT_PREFIX

# 把函数写成一行，xargs 调用
compress_folder() {
    folder="$1"
    name=$(basename "$folder")
    echo "tar $name to ${OUT_PREFIX}_${name}.tar.xz"
    tar -cJf "${OUT_PREFIX}_${name}.tar.xz" -C "$BASE_DIR" "$name"
}

export -f compress_folder

# 遍历 folder_* 并行压缩
find "$BASE_DIR" -maxdepth 1 -type d -name "folder_*" \
  | xargs -n1 -P"$NPROC" -I{} bash -c 'compress_folder "$@"' _ {}


#for f in archive_*.tar.xz; do
#    tar -xJf "$f" -C /your/data/path
#done
