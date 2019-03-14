############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import random, copy, sys, bisect, string, math


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    list = []
    l = []
    i = 1
    for row in range(rows):
        for col in range(cols):
            l.append(i)
            i = i + 1
        list.append(l)
        l = []
    list[rows - 1][cols - 1] = 0
    return TilePuzzle(list)


class TilePuzzle(object):
    # Required
    def __init__(self, board):
        self.board = board

    def goal_state(self):
        c = 0
        for list in self.board:
            for l in list:
                c = c + 1
        rowlen = len(self.board)
        collen = c / len(self.board)
        list = []
        l = []
        i = 1
        for x in range(rowlen):
            for y in range(collen):
                l.append(i)
                i = i + 1
            list.append(l)
            l = []
        list[rowlen - 1][collen - 1] = 0
        return list

    def is_solved(self):
        return self.board == self.goal_state()

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        row = col = j = i = c = 0
        for list in self.board:
            for l in list:
                c = c + 1
                if (l == 0):
                    row = i
                    col = j
                j = j + 1
            j = 0
            i = i + 1
        rowlen = len(self.board)
        collen = c / len(self.board)

        if (direction == "up"):
            if (row > 0):
                tmp = self.board[row - 1][col]
                self.board[row - 1][col] = self.board[row][col]
                self.board[row][col] = tmp
                return True

        if (direction == "down"):
            if (row < rowlen - 1):
                tmp = self.board[row + 1][col]
                self.board[row + 1][col] = self.board[row][col]
                self.board[row][col] = tmp
                return True

        if (direction == "left"):
            if (col > 0):
                tmp = self.board[row][col - 1]
                self.board[row][col - 1] = self.board[row][col]
                self.board[row][col] = tmp
                return True

        if (direction == "right"):
            if (col < collen - 1):
                tmp = self.board[row][col + 1]
                self.board[row][col + 1] = self.board[row][col]
                self.board[row][col] = tmp
                return True
        return False

    def scramble(self, num_moves):
        if (num_moves == 0):
            return
        if (self.perform_move(random.choice(("up", "down", "left", "right"))) == True):
            self.scramble(num_moves - 1)
        else:
            self.scramble(num_moves)

    def copy(self):
        return copy.deepcopy(TilePuzzle(self.board))

    def sucessors(self):
        moves = ["up", "down", "left", "right"]
        for mve in moves:
            p = self.copy()
            move = p.perform_move(mve)
            if (move == True):
                yield (mve, p)

    def iddfs_helper(self, limit, solution, visited,flag):
        # if the board is solved, return the moves
        # print "recursive call #: ", c, "limit: ", limit
        solution = []
        if (self.is_solved()):
            yield solution
        elif (limit == 0):
            yield "cutoff"

    # Required
    def find_solutions_iddfs(self):
        solutions = []
        visited = []
        flag = True
        visited.append(self.board)
        # iterate through the limit i
        while flag:
            solutions = self.iddfs_helper(i, solutions, visited, flag)
            for solution in solutions:
                yield solution

    # Required
    def find_solution_a_star(self):
        pass


b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
p = TilePuzzle(b)
solutions = p.find_solutions_iddfs()
print next(solutions)

"""
p=create_tile_puzzle(3, 3)
q = p.copy()
p.perform_move("left")
print p.get_board() == q.get_board()
p=TilePuzzle([[0, 1], [2, 3]])
print p.is_solved()
p = create_tile_puzzle(3, 3)
p.scramble(10)
p.perform_move("right")
print p.get_board()
p = create_tile_puzzle(2,4)
print p.get_board()
"""


############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    pass


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    pass


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    pass


class DominoesGame(object):
    # Required
    def __init__(self, board):
        pass

    def get_board(self):
        pass

    def reset(self):
        pass

    def is_legal_move(self, row, col, vertical):
        pass

    def legal_moves(self, vertical):
        pass

    def perform_move(self, row, col, vertical):
        pass

    def game_over(self, vertical):
        pass

    def copy(self):
        pass

    def successors(self, vertical):
        pass

    def get_random_move(self, vertical):
        pass

    # Required
    def get_best_move(self, vertical, limit):
        pass


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
