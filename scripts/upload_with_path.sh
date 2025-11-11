#!/bin/bash
set -e

# =====================
# 配置
# =====================
LOCAL_DIR="/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV_0915_Split/compressed"   # 本地压缩包所在目录
REMOTE_USER="ubuntu"
REMOTE_HOST="117.50.171.216"
REMOTE_DIR="/data"
FILES="${LOCAL_DIR}/archive_*.tar.zst*"   # 本地要上传的文件
TIMEOUT=1000                             # 单个文件上传最长时间（秒）

# =====================
# 上传函数（带重试）
# =====================
upload_file() {
    local file="$1"
    echo "==== upload to server: $file ===="

    # 无限重试直到传输成功
    until timeout "$TIMEOUT" rsync -avP --append-verify "$file" \
        ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/; do
        echo "$file Transmission interruption or freezing, try again..."
        sleep 5
    done

    echo "$file Upload completed"
}

# =====================
# 主流程
# =====================
for f in $FILES; do
    if [ -f "$f" ]; then
        upload_file "$f"
    else
        echo "file $f is none, ignore"
    fi
done

echo "? all files uploaded successfully"
