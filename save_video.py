# coding: utf-8
import cv2

# 打开摄像头，参数 0 通常是默认的摄像头
cap = cv2.VideoCapture(0)

# 检查是否成功打开摄像头
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# # 获取摄像头的宽度和高度
# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# 设置视频输出的宽度和高度为 640x480
frame_width = 640
frame_height = 480

# 设置摄像头的分辨率为 640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)


# 定义视频保存的格式，输出文件名，编码格式等
fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # 视频编码格式，'XVID' 是常见格式
out = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (frame_width, frame_height))  # 20.0 是帧率

# 循环读取视频帧
while True:
    ret, frame = cap.read()

    if not ret:
        print("无法读取视频帧")
        break

    # 将当前帧写入视频文件
    out.write(frame)

    # 显示视频帧
    cv2.imshow('Camera', frame)

    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源和视频写入资源
cap.release()
out.release()
cv2.destroyAllWindows()
