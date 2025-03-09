import pyb
from pyb import LED
import sensor, image, time, math, display, ustruct
from machine import UART

# LED(1).on()
# LED(1).off()
LED(2).on()
# LED(2).off()
# LED(3).on()
# LED(3).off()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time=1000)
lcd = display.SPIDisplay()
clock = time.clock()
uart = UART(3, 115200)  # OpenMV RT 注释掉这一行，用下一行UART(1)，P4(TX)，P5(RX)
uart.init(115200, bits=8, parity=None, stop=1)


#########定义发送数据处理########
def sending_data_1(ca, cb, cc, cd, ce, cf, cg, ch, ci, cj, ck):
    global uart;
    data = ustruct.pack("<bhhhhhhhhhhb",
                        0x2C,
                        int(ca),
                        int(cb),
                        int(cc),
                        int(cd),
                        int(ce),
                        int(cf),
                        int(cg),
                        int(ch),
                        int(ci),
                        int(cj),
                        int(ck),
                        0x5B)
    uart.write(data);  # 11个数据,最后一个是标志位，倒数第二个是角度


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
        data.clear()  # 如果tx是列表，则应该在这里清空
    uart.read(data)


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


#########定义棋盘感知########
def Perceived_chessboard(ab,degrees):
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

    white_threshold = [60, 100, -20, 20, -20, 20]
    black_threshold = [0, 40, -20, 20, -20, 20]

    if(43 <= degrees and degrees <= 47):
        a31 = 22
        b31 = 122
        a32 = 106
        b32 = 122
        a33 = 106
        b33 = 38
        a34 = 22
        b34 = 38
    elif (0 <= degrees <= 43)or(47 <= degrees <= 90):
        a31 = ab[0]
        b31 = ab[1]
        a32 = ab[2]
        b32 = ab[3]
        a33 = ab[4]
        b33 = ab[5]
        a34 = ab[6]
        b34 = ab[7]
    else:
        a31 = 22
        b31 = 122
        a32 = 106
        b32 = 122
        a33 = 106
        b33 = 38
        a34 = 22
        b34 = 38

    a35 = (a31 + a32 + a33 + a34) / 4
    b35 = (b31 + b32 + b33 + b34) / 4
    x15 = a35
    y15 = b35
    c = 22  # 检测框边长
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
    # d = bytearray([0x2B, 0x66, d1, d2, d3, d4, d5, 0x5C])
    # 将这些数字连接成一个字符串，然后将其转换为整数
    number_d = ([d1, d2, d3, d4, d5, d6, d7, d8, d9])
    b = ''.join(map(str, number_d))
    # 返回值第一个字符串，第二个列表
    return b, number_d


#################定义下棋策略################

#############定义装置2执黑先行################
def play_chess1(b):  # 装置2执黑先行主程序
    # 胜利组合
    WIN_COMBINATIONS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    # 打印棋盘
    def print_board(board):
        for i in range(3):
            print(f"{board[i * 3]} | {board[i * 3 + 1]} | {board[i * 3 + 2]}")
            if i < 2:
                print("--+---+--")

    # 检查游戏结果
    def check_winner(board):
        for (x, y, z) in WIN_COMBINATIONS:
            if board[x] == board[y] == board[z] != 0:
                return board[x]  # 返回获胜方
        if 0 not in board:
            return 0  # 平局
        return -1  # 游戏继续

    # 局面评分函数：为AI和玩家各自的棋子提供评分
    def evaluate_board(board):
        score = 0
        for (x, y, z) in WIN_COMBINATIONS:
            line = [board[x], board[y], board[z]]
            if line.count(2) == 3:
                score += 100
            elif line.count(2) == 2 and line.count(0) == 1:
                score += 10
            elif line.count(1) == 3:
                score -= 100
            elif line.count(1) == 2 and line.count(0) == 1:
                score -= 10
        return score

    # 极小极大算法（含α-β剪枝）与局面评分
    def minimax(board, depth, alpha, beta, is_maximizing):
        result = check_winner(board)
        if result != -1:
            if result == 2:
                return 100 - depth
            elif result == 1:
                return -100 + depth
            else:
                return 0
        if depth == 0:
            return evaluate_board(board)
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = 2
                    score = minimax(board, depth - 1, alpha, beta, False)
                    board[i] = 0
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = 1
                    score = minimax(board, depth - 1, alpha, beta, True)
                    board[i] = 0
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    # 电脑选择最佳位置
    def best_move(board):
        best_score = -float('inf')
        move = -1
        for i in range(9):
            if board[i] == 0:
                board[i] = 2
                score = minimax(board, 5, -float('inf'), float('inf'), False)
                board[i] = 0
                if score > best_score:
                    best_score = score
                    move = i
        return move

    # 输赢状态，黑胜2，白胜1，平局0，其它3
    result0 = 3
    # 用户输入棋盘状态
    board_str = b
    if len(board_str) != 9 or not board_str.isdigit():
        print("输入的格式不正确，请输入9位数字。")
        return
    board = [int(x) for x in board_str]
    print("当前棋盘状态：")
    print_board(board)
    result = check_winner(board)
    if result != -1:
        ai_move = -1
        if result == 2:
            print("黑棋（电脑）已经获胜！")
            result0 = 2
        elif result == 1:
            print("白棋（你）已经获胜！")
            result0 = 1
        elif result == 0:
            print("平局！")
            result0 = 0
    else:
        ai_move = best_move(board)
        board[ai_move] = 2
        print(f"电脑选择了位置：{ai_move + 1}")
        print_board(board)
        result = check_winner(board)
        if result == 2:
            print("黑棋（电脑）已经获胜！")
            result0 = 2
        elif result == 1:
            print("白棋（你）已经获胜！")
            result0 = 1
        elif result == 0:
            print("平局！")
            result0 = 0
        else:
            print("游戏继续，请输入你的下一步。")
    return ai_move + 1, result0  # 返回ai（2）下棋位置和输赢情况


#############定义人2执黑先行#################
def play_chess2(b):  # 人2执黑先行主程序
    # 胜利组合
    WIN_COMBINATIONS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    # 打印棋盘
    def print_board(board):
        for i in range(3):
            print(f"{board[i * 3]} | {board[i * 3 + 1]} | {board[i * 3 + 2]}")
            if i < 2:
                print("--+---+--")

    # 检查游戏结果
    def check_winner(board):
        for (x, y, z) in WIN_COMBINATIONS:
            if board[x] == board[y] == board[z] != 0:
                return board[x]  # 返回获胜方
        if 0 not in board:
            return 0  # 平局
        return -1  # 游戏继续

    # 局面评分函数：为AI和玩家各自的棋子提供评分
    def evaluate_board(board):
        score = 0
        for (x, y, z) in WIN_COMBINATIONS:
            line = [board[x], board[y], board[z]]
            if line.count(1) == 3:  # 白棋（AI）胜利
                score += 100
            elif line.count(1) == 2 and line.count(0) == 1:  # 白棋两子连线且黑棋未阻止
                score += 10
            elif line.count(2) == 3:  # 黑棋（玩家）胜利
                score -= 100
            elif line.count(2) == 2 and line.count(0) == 1:  # 黑棋两子连线且白棋未阻止
                score -= 10
        return score

    # 极小极大算法（含α-β剪枝）与局面评分
    def minimax(board, depth, alpha, beta, is_maximizing):
        result = check_winner(board)
        if result != -1:
            if result == 1:  # 白棋胜利
                return 100 - depth
            elif result == 2:  # 黑棋胜利
                return -100 + depth
            else:
                return 0
        if depth == 0:
            return evaluate_board(board)
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = 1  # 白棋
                    score = minimax(board, depth - 1, alpha, beta, False)
                    board[i] = 0
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = 2  # 黑棋
                    score = minimax(board, depth - 1, alpha, beta, True)
                    board[i] = 0
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    # 电脑选择最佳位置
    def best_move(board):
        best_score = -float('inf')
        move = -1
        for i in range(9):
            if board[i] == 0:
                board[i] = 1  # 白棋
                score = minimax(board, 5, -float('inf'), float('inf'), False)
                board[i] = 0
                if score > best_score:
                    best_score = score
                    move = i
        return move

    # 输赢状态，黑胜2，白胜1，平局0，其它3
    # result0 = 3
    # 用户输入棋盘状态
    board_input = b
    # 将输入转换为棋盘数组
    board = [int(char) for char in board_input]
    print("当前棋盘状态：")
    print_board(board)
    # 检查游戏是否有胜负
    result = check_winner(board)
    if result != -1:
        ai_move = -1
        if result == 2:
            print("黑棋（你）已经获胜！")
            result0 = 2
        elif result == 1:
            print("白棋（电脑）已经获胜！")
            result0 = 1
        elif result == 0:
            print("平局！")
            result0 = 0
    # AI下白棋
    else:
        result0 = 3
        ai_move = best_move(board)
        if ai_move == -1:
            print("没有可用的位置，游戏结束。")
        if ai_move != -1:
            board[ai_move] = 1  # AI执白棋（1）
            print(f"电脑选择了位置：{ai_move + 1}")
        # 打印AI落子后的棋盘
        print_board(board)
        if ai_move != -1:
            # 检查AI是否胜利
            result = check_winner(board)
            if result == 1:
                print("电脑获胜！")
                result0 = 1
            elif result == 0:
                print("平局！")
                result0 = 0
    return ai_move + 1, result0  # 返回ai（1）下棋位置和输赢情况


#################定义检查犯规################
def check_chess(b):
    def compare_boards(initial, new):
        c, d, f = 4, 0, 0

        # 检查是否有两个数字交换了位置，且其中一个为非零
        def check_swap(initial, new):
            swap_positions = []
            for i in range(9):
                if initial[i] != new[i]:
                    swap_positions.append(i)
            if len(swap_positions) == 2:
                pos1, pos2 = swap_positions
                return (pos1 + 1, initial[pos1], pos2 + 1, initial[pos2])  # 返回1-based index 和对应的值
            return None

        # 检测状态变化
        changed_from_zero = False
        swap_result = check_swap(initial, new)
        if swap_result:
            pos1, value1, pos2, value2 = swap_result
            print(f"玩家作弊，交换了第{pos1}个数字（{value1}）和第{pos2}个数字（{value2}）的位置")
            c = 2
            if (value1 != 0):
                d = pos1
                f = pos2

            if (value1 == 0):
                d = pos2
                f = pos1

            g = f"{c}{d}{f}"
            return g  # 如果作弊，不更新棋盘
        else:
            for i in range(9):
                if initial[i] != new[i]:
                    if initial[i] == 0 and (new[i] == 1 or new[i] == 2):
                        changed_from_zero = True
                    elif initial[i] != 0 and new[i] != 0:
                        c = 3
                        print("棋盘异常")
                        return g
            if new == initial:
                c = 0
                print("没有变化")
            elif changed_from_zero:
                c = 1
                print("下棋正常进行中")
            else:
                c = 3

        # c为1表示下棋正常进行中，c为0表示没变化，c为2表示作弊，c为3表示异常，作弊从d位置移动到了f位置
        g = f"{c}{d}{f}"
        # 更新棋盘
        initial[:] = new
        print("更新后的棋盘:", initial)
        return g

    # 输入新的棋盘状态
    # input_string = input("请输入新的棋盘状态（9个数字，如000010000），输入'q'退出: ")
    new_board = list(map(int, b))  # 转换字符串为列表
    g = compare_boards(initial_board, new_board)
    return str(g)


#################定义纠错+下棋################
def check_play(b):
    input_b = b  # input("请输入新的棋盘状态（如000000000）: ")
    list_b = list(map(int, input_b))
    n1 = input_b.count('1')
    n2 = input_b.count('2')
    d, h, j = 0, 0, 3  # 输出初始值
    global n3, n4
    if (n4 == 0):  # 先判断人执黑先行还是机器执黑先行，1机器2人
        if n2 > n1:
            n3 = 2
        else:
            n3 = 1
        n4 = 1

    if (list_b):
        c = check_chess(list_b)  # 判断是否作弊
        print(c)
    if (c != None):
        if (c[0] == str(2)):  # 作弊纠正
            d = int(c[2])
            h = int(c[1])

        if (c[0] == str(1) or (c[0] == str(0) and n4 == 1)):
            n4 = 2
            if (n3 == 1):  # 装置2执黑先行
                h, j = play_chess1(input_b)  # 输出下棋参数
                if (h != 0):
                    d = n2 + 10  # 选择拿棋位置
                if (j == 3):
                    list_b[h - 1] = 2  # 刷新装置下棋之后的棋盘

            if (n3 == 2 and c[0] == str(1)):  # 人2执黑先行
                h, j = play_chess2(input_b)  # 输出下棋参数
                if (h != 0):
                    d = n1 + 15  # 选择拿棋位置
                if (j == 3):
                    list_b[h - 1] = 1  # 刷新装置下棋之后的棋盘

        if (j == 3):
            c = check_chess(list_b)  # 再判断是否作弊并刷新棋盘
            # print(n1,n2,list_b,c,h,j) # 中间量不管它

    # 输出4个数，第一个判断作弊，第二个和第三个表示电脑要把第几个位置的棋子放在第几个位置，第4个数判断谁赢
    # 第一个数：0没变，1正常下，2作弊，3异常
    # 第四个数：0平局，1白胜，2黑胜，3其它
    # print(int(c[0]), d, h, j)
    return int(c[0]), d, h, j


while (True):
    ab,degrees = Chessboard_rotation()  # 棋盘旋转判断输出坐标（四个顶点）和角度
    print(ab,degrees)
    n3, n4 = 2, 0  # 人机先行判断初始条件
    # 示例使用
    initial_board = Perceived_chessboard(ab, degrees)[1]  # 初始
    while (True):
        Perceived_chessboard(ab, degrees)
        kk = uart.read()  # 串口接收 FF 01 00 00 00 FE
        if (kk == None):
            time.sleep_ms(10)
        if (kk != None):
            print(kk)
            if (kk[1] == 1): # 下棋程序
                b = Perceived_chessboard(ab, degrees)[0]  # input("请输入新的棋盘状态（如000000000）: ")
                if (b != None):
                    s = check_play(b)
                    d = bytearray([0x2C, s[0], s[1], s[2], s[3], 0, 0, 0, 0, 0, degrees, 1, 0x5B])
                    uart.write(d)
                    print(d)

            elif (kk[1] == 2): # 棋盘复位程序
                b = Perceived_chessboard(ab, degrees)[1]  # input("请输入新的棋盘状态（如000000000）: ")
                if (b != None):
                    d = bytearray([0x2C, b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], degrees, 2, 0x5B])
                    uart.write(d)
                    print(d)
            elif (kk[1] == 3):
                # d = bytearray([0x2C, 9, 9, 9, 9, 9, 9, 9, 9, 9, 2, 0x5B])
                break
