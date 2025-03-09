# Find Rects Example
#
# 这个例子展示了如何使用april标签代码中的四元检测代码在图像中找到矩形。 四元检测算法以非常稳健的方式检测矩形，并且比基于Hough变换的方法好得多。 例如，即使镜头失真导致这些矩形看起来弯曲，它仍然可以检测到矩形。 圆角矩形是没有问题的！
# (但是，这个代码也会检测小半径的圆)...

import pyb
from pyb import LED
import sensor, image, time, math, display, ustruct
from machine import UART

LED(1).on()
# LED(1).off()
LED(2).on()
# LED(2).off()
LED(3).on()
# LED(3).off()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time=2000)
lcd = display.SPIDisplay()
clock = time.clock()
uart = UART(3, 115200)  # OpenMV RT 注释掉这一行，用下一行UART(1)
uart.init(115200, bits=8, parity=None, stop=1)

#########定义棋盘旋转########
def Chessboard_rotation():
    i1 = 0
    i2 = 0
    i3 = 0
    a21 = 0
    b21 = 0
    a22 = 0
    b22 = 0
    a23 = 0
    b23 = 0
    a24 = 0
    b24 = 0
    a1 = 22
    b1 = 122
    a2 = 106
    b2 = 122
    a3 = 106
    b3 = 38
    a4 = 22
    b4 = 38
    while (True):
        clock.tick()
        img = sensor.snapshot()
        thresholds = (20,60,20,65,10,50)
        img.binary([thresholds])
        roi100 = [0, 16, 128, 128]
        for r in img.find_rects(roi100, threshold=50000):
            img.draw_rectangle(r.rect(), color=(255, 0, 0))
            for p in r.corners(): img.draw_circle(p[0], p[1], 5, color=(0, 255, 0))
            rrr = r.corners()
            a11 = rrr[0][0]
            b11 = rrr[0][1]
            a12 = rrr[1][0]
            b12 = rrr[1][1]
            a13 = rrr[2][0]
            b13 = rrr[2][1]
            a14 = rrr[3][0]
            b14 = rrr[3][1]
            lcd.write(img)  # LCD显示图像。
            if (i1 >= 5):
                i2 = 1
                i1 = 0
                a31 = a21 / 5
                b31 = b21 / 5
                a32 = a22 / 5
                b32 = b22 / 5
                a33 = a23 / 5
                b33 = b23 / 5
                a34 = a24 / 5
                b34 = b24 / 5
                a21 = 0
                b21 = 0
                a22 = 0
                b22 = 0
                a23 = 0
                b23 = 0
                a24 = 0
                b24 = 0
                ab = [a31, b31, a32, b32, a33, b33, a34, b34]
                print(a31, b31, a32, b32, a33, b33, a34, b34)
            elif (i1 < 6):
                a21 += a11
                b21 += b11
                a22 += a12
                b22 += b12
                a23 += a13
                b23 += b13
                a24 += a14
                b24 += b14
                i1 += 1
                i2 = 0

            if (i2 == 1):
                i3 = 1
                slope = (b31 - b33) / (a31 - a33)
                print(slope)
                angle_atan = math.atan(slope)
                degrees = int(math.degrees(angle_atan))
                if(degrees<0):
                    degrees = degrees+90
                print(f"{angle_atan} 弧度 等于 {degrees} 度")

                img.draw_string(10, 10, str(degrees), color=(0, 0, 255))
                lcd.write(img)  # LCD显示图像。
        if (i3 == 1):
            break
    return ab, degrees

    # print("FPS %f" % clock.fps())
while(1):
    img = sensor.snapshot()
    lcd.write(img)  # LCD显示图像。
    ab, degrees = Chessboard_rotation()
    print(ab, degrees)