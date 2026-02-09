#!/bin/bash
set -e

BASE_DIR="/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV_0915_Split"   # 修改为你的目录
OUT_PREFIX="archive"
NPROC=8                             # 并行任务数（建议设为 CPU 核心数）

export BASE_DIR OUT_PREFIX NPROC

# 确保输出目录存在
mkdir -p "$BASE_DIR/compressed"

compress_folder() {
    folder="$1"
    name=$(basename "$folder")
    out_dir="$BASE_DIR/compressed"
    out_file="$out_dir/${OUT_PREFIX}_${name}.tar.zst"

    echo "Compressing $name -> $out_file"

    # 使用 tar + zstd 多线程压缩（比 xz 更快）
    tar -cf - -C "$(dirname "$folder")" "$name" \
        | zstd -T$NPROC -19 -o "$out_file"

    # 生成 sha256 校验
    sha256sum "$out_file" > "$out_file.sha256"

    echo "Done: $out_file (sha256 in $out_file.sha256)"
}

export -f compress_folder

# 遍历 folder_* 并行压缩
find "$BASE_DIR" -maxdepth 1 -type d -name "folder_*" \
  | xargs -n1 -P"$NPROC" -I{} bash -c 'compress_folder "$@"' _ {}
