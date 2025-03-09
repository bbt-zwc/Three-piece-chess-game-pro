def compare_boards(initial, new):
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
        return  # 如果作弊，不更新棋盘
    else:
        for i in range(9):
            if initial[i] != new[i]:
                if initial[i] == 0 and (new[i] == 1 or new[i] == 2):
                    changed_from_zero = True
                elif initial[i] != 0 and new[i] != 0:
                    print("棋盘异常")
                    return

        if new == initial:
            print("没有变化")
        elif changed_from_zero:
            print("下棋正常进行中")

    # 更新棋盘
    initial[:] = new
    print("更新后的棋盘:", initial)


# 示例使用
initial_board = [0] * 9  # 初始全为0
print("初始棋盘:", initial_board)

while True:
    # 输入新的棋盘状态
    input_string = input("请输入新的棋盘状态（9个数字，如000010000），输入'q'退出: ")

    if input_string.lower() == 'q':
        break  # 退出循环

    if len(input_string) != 9 or any(c not in '012' for c in input_string):
        print("无效输入，请输入9个数字（仅0, 1, 2）。")
        continue

    new_board = list(map(int, input_string))  # 转换字符串为列表
    compare_boards(initial_board, new_board)
