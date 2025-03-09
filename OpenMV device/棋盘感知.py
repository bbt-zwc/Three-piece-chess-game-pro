# Find Rects Example
#
# 这个例子展示了如何使用april标签代码中的四元检测代码在图像中找到矩形。 四元检测算法以非常稳健的方式检测矩形，并且比基于Hough变换的方法好得多。 例如，即使镜头失真导致这些矩形看起来弯曲，它仍然可以检测到矩形。 圆角矩形是没有问题的！
# (但是，这个代码也会检测小半径的圆)...

import pyb
from pyb import LED
import sensor, image, time, math, display, ustruct
from machine import UART

LED(1).on()
LED(1).off()
LED(2).on()
LED(2).off()
LED(3).on()
LED(3).off()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time=2000)
lcd = display.SPIDisplay()
clock = time.clock()
uart = UART(3, 115200)  # OpenMV RT 注释掉这一行，用下一行UART(1)
uart.init(115200, bits=8, parity=None, stop=1)



#########定义发送数据处理########
def sending_data_1(ca, cb, cc, cd, ce, cf, cg, ch):
    global uart;
    data = ustruct.pack("<bbhhhhhhhhb",
                        0x2C,
                        0x12,
                        int(ca),
                        int(cb),
                        int(cc),
                        int(cd),
                        int(ce),
                        int(cf),
                        int(cg),
                        int(ch),
                        0x5B)
    uart.write(data);  # 88888888


def sending_data_2(cca, ccb, ccc, ccd, cce, ccf, ccg, cch, cci):
    global uart;
    data = ustruct.pack("<bbhhhhhhhhhb",
                        0x2B,
                        0x66,
                        int(cca),
                        int(ccb),
                        int(ccc),
                        int(ccd),
                        int(cce),
                        int(ccf),
                        int(ccg),
                        int(cch),
                        int(cci),
                        0x5C)
    uart.write(data);  # 999999999


#########定义接收数据处理########
def Receive_Prepare():
    global state
    global data
    # 假设tx是用于存储接收数据的列表，应该在函数外部定义
    # tx = []  # 在这里定义tx列表
    if state == 0:
        data[0] = uart.read()
        if data[0] == 0xFF:  # 帧头
            state = 1
        else:
            state = 0
            data.clear()  # 如果tx是列表，则应该在这里清空
    elif state == 1:
        data[1] = uart.read()  # 确保这里执行赋值操作
        state = 2
    elif state == 2:
        data[2] = uart.read()
        state = 3
    elif state == 3:
        data[3] = uart.read()
        state = 4
    elif state == 4:
        data[4] = uart.read()
        state = 5
    elif state == 5:
        data[5] = uart.read()
        if data[5] == 0xFE:
            state = 6
        else:
            state = 0
            data.clear()  # 如果tx是列表，则应该在这里清空
    else:
        state = 0
        # data.clear()  # 如果tx是列表，则应该在这里清空
    uart.read(data)


#########定义棋盘感知########
def Perceived_chessboard():
    clock.tick()
    img = sensor.snapshot()
    i1 = 0
    i2 = 0
    a21 = 0
    b21 = 0
    a22 = 0
    b22 = 0
    a23 = 0
    b23 = 0
    a24 = 0
    b24 = 0
    d1, d2, d3, d4, d5, d6, d7, d8, d9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    ca, cb, cc, cd, ce, cf, cg, ch = 0, 0, 0, 0, 0, 0, 0, 0
    cca, ccb, ccc, ccd, cce, ccf, ccg, cch, cci = 0, 0, 0, 0, 0, 0, 0, 0, 0

    white_threshold = [65, 100, -25, 25, -25, 25]
    black_threshold = [0, 30, -25, 25, -25, 25]

    # 四个顶点坐标，左下角开始逆时针
    a31 = 16
    b31 = 122
    a32 = 103
    b32 = 124
    a33 = 104
    b33 = 36
    a34 = 16
    b34 = 36

    a35 = (a31 + a32 + a33 + a34) / 4
    b35 = (b31 + b32 + b33 + b34) / 4
    x15 = a35
    y15 = b35
    c = 26  # 检测框边长
    img.draw_string(int(x15), int(y15), str(5), color=(255, 255, 255))
    img.draw_rectangle(int(x15 - c / 2), int(y15 - c / 2), c, c, color=(0, 0, 255))  # 55555555555555555555号位
    roi5 = [int(x15 - c / 2), int(y15 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi5, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi5, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d5 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d5 = 2
    else:
        d5 = 0

    x11 = a34 + (a35 - a34) / 3
    y11 = b34 + (b35 - b34) / 3
    img.draw_string(int(x11), int(y11), str(1), color=(255, 255, 255))
    img.draw_rectangle(int(x11 - c / 2), int(y11 - c / 2), c, c, color=(0, 0, 255))  # 11111111111111111111号位
    roi1 = [int(x11 - c / 2), int(y11 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi1, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi1, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d1 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d1 = 2
    else:
        d1 = 0

    x13 = a33 + (a35 - a33) / 3
    y13 = b33 + (b35 - b33) / 3
    img.draw_string(int(x13), int(y13), str(3), color=(255, 255, 255))
    img.draw_rectangle(int(x13 - c / 2), int(y13 - c / 2), c, c, color=(0, 0, 255))  # 33333333333333333333号位
    roi3 = [int(x13 - c / 2), int(y13 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi3, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi3, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d3 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d3 = 2
    else:
        d3 = 0

    x17 = a31 + (a35 - a31) / 3
    y17 = b31 + (b35 - b31) / 3
    img.draw_string(int(x17), int(y17), str(7), color=(255, 255, 255))
    img.draw_rectangle(int(x17 - c / 2), int(y17 - c / 2), c, c, color=(0, 0, 255))  # 77777777777777777777号位
    roi7 = [int(x17 - c / 2), int(y17 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi7, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi7, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d7 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d7 = 2
    else:
        d7 = 0

    x19 = a32 + (a35 - a32) / 3
    y19 = b32 + (b35 - b32) / 3
    img.draw_string(int(x19), int(y19), str(9), color=(255, 255, 255))
    img.draw_rectangle(int(x19 - c / 2), int(y19 - c / 2), c, c, color=(0, 0, 255))  # 99999999999999999999号位
    roi9 = [int(x19 - c / 2), int(y19 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi9, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi9, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d9 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d9 = 2
    else:
        d9 = 0

    x12 = (x11 + x13) / 2
    y12 = (y11 + y13) / 2
    img.draw_string(int(x12), int(y12), str(2), color=(255, 255, 255))
    img.draw_rectangle(int(x12 - c / 2), int(y12 - c / 2), c, c, color=(0, 0, 255))  # 22222222222222222222号位
    roi2 = [int(x12 - c / 2), int(y12 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi2, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi2, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d2 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d2 = 2
    else:
        d2 = 0

    x14 = (x11 + x17) / 2
    y14 = (y11 + y17) / 2
    img.draw_string(int(x14), int(y14), str(4), color=(255, 255, 255))
    img.draw_rectangle(int(x14 - c / 2), int(y14 - c / 2), c, c, color=(0, 0, 255))  # 44444444444444444444号位
    roi4 = [int(x14 - c / 2), int(y14 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi4, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi4, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d4 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d4 = 2
    else:
        d4 = 0

    x16 = (x13 + x19) / 2
    y16 = (y13 + y19) / 2
    img.draw_string(int(x16), int(y16), str(6), color=(255, 255, 255))
    img.draw_rectangle(int(x16 - c / 2), int(y16 - c / 2), c, c, color=(0, 0, 255))  # 66666666666666666666号位
    roi6 = [int(x16 - c / 2), int(y16 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi6, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi6, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d6 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d6 = 2
    else:
        d6 = 0

    x18 = (x17 + x19) / 2
    y18 = (y17 + y19) / 2
    img.draw_string(int(x18), int(y18), str(8), color=(255, 255, 255))
    img.draw_rectangle(int(x18 - c / 2), int(y18 - c / 2), c, c, color=(0, 0, 255))  # 88888888888888888888号位
    roi8 = [int(x18 - c / 2), int(y18 - c / 2), c, c]
    blobs51 = img.find_blobs([white_threshold], roi=roi8, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    blobs52 = img.find_blobs([black_threshold], roi=roi8, x_stride=10, y_stride=10, invert=False, area_threshold=70,
                             pixels_threshold=170, merge=True)
    if blobs51:
        for b in blobs51:
            img.draw_rectangle(b[0:4], color=(0, 0, 0))
            img.draw_cross(b[5], b[6], color=(0, 0, 0))
        d8 = 1
    elif blobs52:
        for b in blobs52:
            img.draw_rectangle(b[0:4], color=(255, 255, 255))
            img.draw_cross(b[5], b[6], color=(255, 255, 255))
        d8 = 2
    else:
        d8 = 0
    lcd.write(img)  # LCD显示图像。
    d = bytearray([0x2B, 0x66, d1, d2, d3, d4, d5, d6, d7, d8, d9, 0x5C])
    # 将这些数字连接成一个字符串，然后将其转换为整数
    number_d = str(''.join([str(d1), str(d2), str(d3), str(d4), str(d5), str(d6), str(d7), str(d8), str(d9)]))
    return number_d


while (True):
    b = Perceived_chessboard()
    print(b)
    uart.write(b)