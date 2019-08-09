#!/usr/bin/python3
# 2019 s1 9414 Assignment3: Nine-Board Tic-Tac-Toe
# Group: g017862
# Member 1: Wenxun Peng zID:5195349
# Member 2: Le Wang zID:z5148417
# 26/04/19
########################################################################################################################
# Data structure: tree
# You can see there is a GameTree class in our code. The tree contains board, win_situation(if one board has one line),
# depth, children, oppo_move(the location that opponent may move), player(who plays), children(sub_tree).
# In addition, there are two functions which are used to calculate value of heuristic and add children respectively.
#
# AlphaBeta algorithm:
# In our code, we used AlphaBeta algorithm to reduce the number or traversals. We set the initial value of alpha as
# -infinite and beta as infinite. The depth of searching is 5. When arrival leaf nodes, calculate the heuristic value
# and return to the optimal value. Meanwhile, the program will not generate redundant sub trees when alpha larger than
# beta(always choose the best situation for player)
# Heuristic:
# we divide the game into two parts global board and each small board
# for each small board: Eval(s) = 3*X2(s) + X1(s) - (3*O2(s) + O1(s))
# global board: sum(each small board)
########################################################################################################################
import socket
import sys
import numpy as np

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
# the state to print
S = ['.', 'X', 'O']
curr = 0  # this is the current board to play in
# the max depth we can use the a-b algorithm
max_depth = 5


# print a row
# This is just ported from game.c
def print_board_row(boards, a, b, c, i, j, k):
    # The marking script doesn't seem to like this either, so just take it out to submit
    print("", S[boards[a][i]], S[boards[a][j]], S[boards[a][k]], end = " | ")
    print(S[boards[b][i]], S[boards[b][j]], S[boards[b][k]], end = " | ")
    print(S[boards[c][i]], S[boards[c][j]], S[boards[c][k]])


# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(boards, 1,2,3,1,2,3)
    print_board_row(boards, 1,2,3,4,5,6)
    print_board_row(boards, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(boards, 4,5,6,1,2,3)
    print_board_row(boards, 4,5,6,4,5,6)
    print_board_row(boards, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(boards, 7,8,9,1,2,3)
    print_board_row(boards, 7,8,9,4,5,6)
    print_board_row(boards, 7,8,9,7,8,9)
    print()


##################################
#  Alpha-beta prunning algorithm #
##################################

# A tree to accomplish Alpha-beta algorithm
class GameTree:
    def __init__(self, boards, oppo_move, depth, player):
        self.boards = boards
        # opponent move
        self.oppo_move = oppo_move
        self.depth = depth
        # the tree depth
        self.player = player
        self.children = []
    
    # judge whether win or not, the every board is:
    #########
    # 1 2 3 #
    # 4 5 6 #
    # 7 8 9 #
    #########

    # when the player win, then return true
    def win_situation(self, player):

        for i in range(1, 10):
            if (player==self.boards[i][1]==self.boards[i][2]==self.boards[i][3] or
            player==self.boards[i][4]==self.boards[i][5]==self.boards[i][6] or
            player==self.boards[i][7]==self.boards[i][8]==self.boards[i][9] or
            player==self.boards[i][1]==self.boards[i][4]==self.boards[i][7] or
            player==self.boards[i][2]==self.boards[i][5]==self.boards[i][8] or
            player==self.boards[i][3]==self.boards[i][6]==self.boards[i][9] or
            player==self.boards[i][1]==self.boards[i][5]==self.boards[i][9] or
            player==self.boards[i][3]==self.boards[i][5]==self.boards[i][7]):
                return True
        return False

    # calculate the heuristic and return it
    def heuristic(self):
        # three situations: player 1 wins, player 2 wins and just return the heuristic
        if self.win_situation(1)== True :      # player 1 wins, return +inf
            print_board(self.boards)
            return float('inf')
        elif self.win_situation(2) == True :       # player 2 wins, return -inf
            print_board(self.boards)
            return -float('inf')
        else:                                # calculate heuristic here
            heuristic = self.max_depth_heuristic()   
            print_board(self.boards)
            print(f"The heuristic of this board is {heuristic}")
            return heuristic
    
    def max_depth_heuristic(self):
        # since we are player 1, we just calculate our win situation
        # using the tutorial 5 eval function to calculate every boards
        # Eval(s) = 3*X2(s) + X1(s) - (3*O2(s) + O1(s))
        board_heuristic = []    # every board heuristic
        player = 1
        player2 = 2
        count1 = 0
        count2 = 0
        every_heuristic = 0

        for i in range(1, 10):
            # rows
            for b in range(1, 10):
                if self.boards[i][b] == player:
                    count1 += 1
                elif self.boards[i][b] == player2:
                    count2 += 1
                if b == 3 or b == 6 or b == 9:
                    if count1 == 2:
                        every_heuristic = 3 + every_heuristic
                    if count1 == 1:
                        every_heuristic += 1
                    if count2 == 2:
                        every_heuristic = every_heuristic - 3
                    if count2 == 1:
                        every_heuristic -= 1
                    count1 = 0
                    count2 = 0

            # columns
            for c in range(1, 4):
                # player 1
                if self.boards[i][c] == player:
                    count1 += 1
                if self.boards[i][c+3] == player:
                    count1 += 1
                if self.boards[i][c+6] == player:
                    count1 += 1
                # player 2
                if self.boards[i][c] == player2:
                    count2 += 1
                if self.boards[i][c+3] == player2:
                    count2 += 1
                if self.boards[i][c+6] == player2:
                    count2 += 1
                # count the number
                if count1 == 2:
                    every_heuristic = 3 + every_heuristic
                if count1 == 1:
                    every_heuristic += 1
                if count2 == 2:
                    every_heuristic = every_heuristic - 3
                if count2 == 1:
                    every_heuristic -= 1
                count1 = 0
                count2 = 0

            # diagonals ([1,5,9],[3,5,7])
            # [1,5,9]
            if self.boards[i][1] == player:
                count1 += 1
            if self.boards[i][5] == player:
                count1 += 1
            if self.boards[i][9] == player:
                count1 += 1
            if self.boards[i][1] == player2:
                count2 += 1
            if self.boards[i][5] == player2:
                count2 += 1
            if self.boards[i][9] == player2:
                count2 += 1
            if count1 == 2:
                every_heuristic = 3 + every_heuristic
            if count1 == 1:
                every_heuristic += 1
            if count2 == 2:
                every_heuristic = every_heuristic - 3
            if count2 == 1:
                every_heuristic -= 1
            count1 = 0
            count2 = 0

            # [3,5,7]                       
            if self.boards[i][3] == player:
                count1 += 1
            if self.boards[i][5] == player:
                count1 += 1
            if self.boards[i][7] == player:
                count1 += 1
            if self.boards[i][3] == player2:
                count2 += 1
            if self.boards[i][5] == player2:
                count2 += 1
            if self.boards[i][7] == player2:
                count2 += 1
            if count1 == 2:
                every_heuristic = 3 + every_heuristic
            if count1 == 1:
                every_heuristic += 1
            if count2 == 2:
                every_heuristic = every_heuristic - 3
            if count2 == 1:
                every_heuristic -= 1
            count1 = 0
            count2 = 0
            board_heuristic.append(every_heuristic)
            every_heuristic = 0
        # this function can be changed to get a better performance
        total_heuristic = sum(board_heuristic)
        # for k in range(len(board_heuristic)):
        #   print(f'every board is {board_heuristic[k]}\n')
        # total_heuristic = 2*board_heuristic[0] + board_heuristic[1] + 2*board_heuristic[2] + \
        # board_heuristic[3] + 2*board_heuristic[4] + board_heuristic[5] + 2*board_heuristic[6] +
        # board_heuristic[7]+2*board_heuristic[8]
        return total_heuristic

    # append children to the this tree
    def append_children(self):
        next_depth = self.depth + 1
        if self.player == 1:
            next_player = 2
        else:
            next_player = 1
        
        for i in range(1, 10):
            if self.boards[self.oppo_move][i] == 0:
                # children are all the situation that next move in the board
                next_boards = boards.copy()
                next_boards[self.oppo_move][i] = next_player
                child_tree = GameTree(next_boards, i, next_depth, next_player)
                self.children.append(child_tree)
        assert boards is not None
        return self.children


class AlphaBeta:
    def __init__(self, boards):
        global curr
        # initial player and depth
        root = GameTree(boards, curr, 0, 2)
        self.tree = root
        return
    
    # judge whether get the max search depth
    # the max depth of a-b prunning algorithm
    def getMaxDepth(self, depth):
        global max_depth
        if depth == max_depth:
            return True
        else:
            return False

    # MIN value
    def min_value(self, the_boards, alpha, beta):
        # if get the max depth, then return the value to estimate which is the best, otherwise, continuing to a-b search 
        if self.getMaxDepth(the_boards.depth):
            return the_boards.heuristic()
        curr_value = float('inf')    # beta is inf
        # if we will lose, then directly return the -inf
        # or if we will win, then directly return the inf
        if the_boards.heuristic() == float('inf'):
            return float('inf')
        if the_boards.heuristic() == -float('inf'):
            return -float('inf')

        children = the_boards.append_children()
        # child is the child boards
        for child in children:
            next_value = self.max_value(child, alpha, beta)
            curr_value = min(curr_value, next_value)
            beta = min(beta, next_value)
            # prunning
            if beta <= alpha:
                break
        return curr_value

    # MAX value
    def max_value(self, the_boards, alpha, beta):
        if self.getMaxDepth(the_boards.depth):
            return the_boards.heuristic()
        curr_value = -float('inf')  # alpha is -inf
        if the_boards.heuristic() == float('inf'):
            return float('inf')
        if the_boards.heuristic() == -float('inf'):
            return -float('inf')

        children = the_boards.append_children()
        # child is the child boards
        for child in children:
            next_value = self.min_value(child, alpha, beta)
            curr_value = max(curr_value, next_value)
            alpha = max(alpha, next_value)
            # prunning
            if beta <= alpha:
                break
        return curr_value

    def alpha_beta_search(self):
        alpha = -float('inf')
        beta = float('inf')
        children = self.tree.append_children()
        best_board = None
        for child in children:
            # the first is calculating minimal value
            value = self.min_value(child, alpha, beta)

            if value > alpha:
                alpha = value
                best_board = child
        # in fact, it can return a value, but for checking the result, return the board situation there. 
        return best_board


# choose a move to play
def play():
    global curr
    # print_board(boards)
    # just play a random move for now
    # n = np.random.randint(1,9)
    alphabeta_tree = AlphaBeta(boards)
    best_node = alphabeta_tree.alpha_beta_search()
    if best_node == None:
        for i in range(1, 10):
            if boards[curr][i] == 0:
                return i

    # return a value that determine which number we move
    best_board = best_node.boards
    for i in range(1, 10):
        for j in range(1, 10):
            if not best_board[i][j] == boards[i][j]:
                next_move = j
                break
    print_board(boards)
    print(f'We next move is: {next_move}')
    print_board(best_board)

    place(curr, next_move, 1)
    return next_move


# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()


