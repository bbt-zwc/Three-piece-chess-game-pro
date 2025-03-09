# Find Rects Example
#
# 这个例子展示了如何使用april标签代码中的四元检测代码在图像中找到矩形。 四元检测算法以非常稳健的方式检测矩形，并且比基于Hough变换的方法好得多。 例如，即使镜头失真导致这些矩形看起来弯曲，它仍然可以检测到矩形。 圆角矩形是没有问题的！
# (但是，这个代码也会检测小半径的圆)...

import pyb
from pyb import LED
import sensor, image, time, math, display, ustruct
from machine import UART

LED(1).on()
#LED(1).off()
LED(2).on()
#LED(2).off()
LED(3).on()
#LED(3).off()

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time = 2000)
lcd = display.SPIDisplay()
clock = time.clock()
uart = UART(3, 115200)   #OpenMV RT 注释掉这一行，用下一行UART(1)
uart.init(115200, bits=8, parity=None, stop=1)


history = []  # 用于存储每次输入的数值

def calculate_average(history):
    """计算历史数据的平均值，并格式化为原输入形式"""
    n = len(history)
    if n == 0:
        return None
    avg = [sum(col) / n for col in zip(*history)]
    
    # 将平均值恢复成4组数对的形式
    formatted_avg = [(avg[i], avg[i + 1]) for i in range(0, len(avg), 2)]
    return formatted_avg

def is_stable(history, tolerance=2):  # tolerance 可根据需要调整，当前设置为 10
    """判断当前数值是否已经趋于稳定"""
    if len(history) < 2:
        return False
    
    # 计算最后两组数的差异
    last_values = history[-1]
    second_last_values = history[-2]
    
    # 计算差异，用于判断是否稳定
    differences = [abs(a - b) for a, b in zip(last_values, second_last_values)]
    
    # 如果所有差异在容忍度范围内，返回 True
    return all(diff <= tolerance for diff in differences)

while(True):
    clock.tick()
    img = sensor.snapshot()
    a = 0
    
    for r in img.find_rects(threshold = 20000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
        rrr = r.corners()
        #print(rrr)
        
        # 将输入值平铺成一个8个数的列表
        flattened_rrr = [rrr[i][j] for i in range(4) for j in range(2)]
            
        
        # 加入历史记录
        history.append(flattened_rrr)
        
        # 检查是否稳定
        if is_stable(history):
            # 稳定后输出平均值
            avg_values = calculate_average(history)
            a = 1
            print("数值稳定，最终平均值为：", avg_values)
            break  # 稳定后退出循环
        else:
            print("当前输入值：", flattened_rrr)
            
        print(history)
    
        lcd.write(img)  # LCD显示图像。
        
    #print("FPS %f" % clock.fps())