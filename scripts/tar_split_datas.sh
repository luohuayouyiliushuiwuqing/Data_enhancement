#!/bin/bash
set -e

BASE_DIR="/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV_0915_Split"   # �޸�Ϊ���Ŀ¼
OUT_PREFIX="archive"
NPROC=8                             # ������������������Ϊ CPU ��������

export BASE_DIR OUT_PREFIX NPROC

# ȷ�����Ŀ¼����
mkdir -p "$BASE_DIR/compressed"

compress_folder() {
    folder="$1"
    name=$(basename "$folder")
    out_dir="$BASE_DIR/compressed"
    out_file="$out_dir/${OUT_PREFIX}_${name}.tar.zst"

    echo "Compressing $name -> $out_file"

    # ʹ�� tar + zstd ���߳�ѹ������ xz ���죩
    tar -cf - -C "$(dirname "$folder")" "$name" \
        | zstd -T$NPROC -19 -o "$out_file"

    # ���� sha256 У��
    sha256sum "$out_file" > "$out_file.sha256"

    echo "Done: $out_file (sha256 in $out_file.sha256)"
}

export -f compress_folder

# ���� folder_* ����ѹ��
find "$BASE_DIR" -maxdepth 1 -type d -name "folder_*" \
  | xargs -n1 -P"$NPROC" -I{} bash -c 'compress_folder "$@"' _ {}
