#################定义下棋策略################

#############定义装置2执黑先行################
def play_chess1(b):# 装置2执黑先行主程序
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
        if result == 2:
            print("黑棋（电脑）已经获胜！")
            result0 = 2
        elif result == 1:
            print("白棋（你）已经获胜！")
            result0 = 1
        elif result == 0:
            print("平局！")
            result0 = 0
        return
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
def play_chess2(b):# 人2执黑先行主程序
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
    result0 = 3
    # 用户输入棋盘状态
    board_input = b
    # 将输入转换为棋盘数组
    board = [int(char) for char in board_input]
    print("当前棋盘状态：")
    print_board(board)
    # 检查游戏是否有胜负
    result = check_winner(board)
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

    return ai_move+1,result0  # 返回ai（1）下棋位置和输赢情况

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
            d = pos1
            f = pos2
            g = f"{c}{d}{f}"
            return  g# 如果作弊，不更新棋盘
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
    new_board = b  # 转换字符串为列表
    g = compare_boards(initial_board, new_board)
    return g

#################定义纠错+下棋################
def check_play():
    input_b = input("请输入新的棋盘状态（如000000000）: ")
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
    #第一个数：0没变，1正常下，2作弊，3异常
    #第四个数：0平局，1白胜，2黑胜，3其它
    #print(int(c[0]), d, h, j)
    return int(c[0]), d, h, j

# 主程序，不管谁先行都是黑色，黑2白1空0
initial_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 初始棋盘
#initial_board = [1, 2, 2, 2, 2, 1, 1, 1, 0]  # 测试棋盘
n3,n4 = 2,0 # 人机先行判断初始条件
while (True):
    s = check_play()
    print(s,s[1])
