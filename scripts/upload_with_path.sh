#!/bin/bash
set -e

# =====================
# ����
# =====================
LOCAL_DIR="/media/igs/Dataset/Data_enhancement/OriginalData/Urban-Surv-HV-UAV/Aviation-HV-UAV_0915_Split/compressed"   # ����ѹ��������Ŀ¼
REMOTE_USER="ubuntu"
REMOTE_HOST="117.50.171.216"
REMOTE_DIR="/data"
FILES="${LOCAL_DIR}/archive_*.tar.zst*"   # ����Ҫ�ϴ����ļ�
TIMEOUT=1000                             # �����ļ��ϴ��ʱ�䣨�룩

# =====================
# �ϴ������������ԣ�
# =====================
upload_file() {
    local file="$1"
    echo "==== upload to server: $file ===="

    # ��������ֱ������ɹ�
    until timeout "$TIMEOUT" rsync -avP --append-verify "$file" \
        ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/; do
        echo "$file Transmission interruption or freezing, try again..."
        sleep 5
    done

    echo "$file Upload completed"
}

# =====================
# ������
# =====================
for f in $FILES; do
    if [ -f "$f" ]; then
        upload_file "$f"
    else
        echo "file $f is none, ignore"
    fi
done

echo "? all files uploaded successfully"
