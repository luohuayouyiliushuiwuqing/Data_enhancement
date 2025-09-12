#!/bin/bash
set -e

BASE_DIR="/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV_Split"   # �޸�Ϊ���Ŀ¼
OUT_PREFIX="archive"
NPROC=4                             # ������������������Ϊ CPU ��������

export BASE_DIR OUT_PREFIX

# �Ѻ���д��һ�У�xargs ����
compress_folder() {
    folder="$1"
    name=$(basename "$folder")
    echo "tar $name to ${OUT_PREFIX}_${name}.tar.xz"
    tar -cJf "${OUT_PREFIX}_${name}.tar.xz" -C "$BASE_DIR" "$name"
}

export -f compress_folder

# ���� folder_* ����ѹ��
find "$BASE_DIR" -maxdepth 1 -type d -name "folder_*" \
  | xargs -n1 -P"$NPROC" -I{} bash -c 'compress_folder "$@"' _ {}


#for f in archive_*.tar.xz; do
#    tar -xJf "$f" -C /your/data/path
#done
