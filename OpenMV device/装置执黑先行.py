#########定义装置2执黑先行########
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

# 示例使用
initial_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 初始
while (True):
    input_b = input("请输入新的棋盘状态（如000000000）: ")
    n1 = input_b.count('1')
    n2 = input_b.count('2')
    list_b = list(map(int, input_b))
    if (list_b):
        a,c=play_chess1(input_b)

    print(input_b,n1,n2,list_b,a,c)