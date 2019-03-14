############################################################
# CMPSC 442: Homework 4
############################################################

student_name = "Meng Kry"

############################################################
# Imports
############################################################

# Include your imports here, if any are used
import Queue, copy, time

############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    cells = []
    for i in range(9):
        for j in range(9):
            cells.append((i,j))
    return cells

# list of restriction for a cell
def sudoku_arcs():
    lists=[]
    for cell in sudoku_cells():
        for cell1 in sudoku_cells():
            if(cell != cell1):
                if ((cell[0]//3) == (cell1[0]//3)) and ((cell[1]//3) == (cell1[1]//3)):
                    lists.append((cell, cell1))
                elif(cell[0] == cell1[0]):
                    lists.append((cell,cell1))
                elif(cell[1] == cell1[1]):
                    lists.append((cell, cell1))
    return lists

def read_board(path):
    raw_data = open(path, 'rb')
    data = [line.split() for line in raw_data]
    raw_data.close()
    dict = {}
    for cell in sudoku_cells():
        dict[cell] = []
    row = 0
    for line in data:
        col = 0
        for str in line:
            for char in str:
                if(char != '*'):
                    dict[(row,col)].append(int(char))
                else:
                    for i in range(1,10):
                        dict[(row,col)].append(i)
                col = col + 1
        row = row + 1
    return dict

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return set(self.board[cell])

    #remove value of cell2 in the domain of cell1
    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1, cell2) in self.ARCS:
            # domainX is the domain of cell1
            domainX = list(self.get_values(cell1))
            # domainY is the domain of cell2
            domainY = list(self.get_values(cell2))
            # if the len of domainY is 1, meaning the cell is solved or given a number

            if((len(domainY) == 1) and(len(domainX) >1)):
                y = domainY[0]
                if y in domainX:
                    domainX.remove(y)
                    self.board[cell1] = domainX
                    return True
            elif(len(domainX) == 1 and len(domainY) > 1):
                x = domainX[0]
                if x in domainY:
                    domainY.remove(x)
                    self.board[cell2] = domainY
                    return True
        return False


    def infer_ac3(self):
        queue = Queue.Queue()
        for arc in self.ARCS:
            queue.put(arc)
        # queue have all the constraints for all the open cell
        while queue.qsize()> 0:
            cell1, cell2 = queue.get()
            if self.remove_inconsistent_values(cell1,cell2):
                if(len(self.get_values(cell1)) > 1):
                    for arc in self.ARCS:
                        if cell1 in arc:
                            queue.put(arc)
                elif(len(self.get_values(cell2)) > 1):
                    for arc in self.ARCS:
                        if cell2 in arc:
                            queue.put(arc)

    def is_solved(self):

        for cell in self.CELLS:
            for arc in self.ARCS:
                if cell == arc[0]:
                    if self.board[cell] == self.board[arc[1]]:
                        return False
        return True

    def print_board(self):
        for i in range(9):
            for j in range(9):
                print self.get_values((i,j)),
            print

    # find the unique value in domain of a cell compare to its neighbors and assign it to the cell
    def optimizer(self, dict):
        flag = False
        for value in dict:
            if(len(dict[value]) == 1):
                cell = dict[value][0]
                domain = self.board[cell]
                if len(domain) >1 :
                    self.board[cell] = [value]
                    flag = True
        return flag

    def optimize(self):
        flag = False
        for row in range(9):
            row_dict = {}
            col_dict = {}
            for k in range(1,10):
                row_dict[k] = []
                col_dict[k] = []

            for col in range(9):
                # get the cells in the grid
                X = row - row % 3
                Y = col - col % 3
                cells = [(X + x, Y + y) for x in range(3) for y in range(3)]

                square_dict = {}
                for k in range(1,10):
                    square_dict[k] = []

                # dict of (row,col) with value as index for cells in the grid
                for cell in cells:
                    for value in self.board[cell]:
                        square_dict[value].append(cell)

                # optimize grid
                flag = flag or self.optimizer(square_dict)

                # dict of (row,col) with value as index for cell in the row
                for value in self.board[(row,col)]:
                    row_dict[value].append((row,col))

                # dic of (col,row) with value as index for cell in the col
                for value in self.board[(col,row)]:
                    col_dict[value].append((col,row))

            # optimize row
            flag = flag or self.optimizer(row_dict)
            # optimize col
            flag = flag or self.optimizer(col_dict)

        return flag


    def infer_improved(self):
        self.infer_ac3()
        while self.optimize():
            self.infer_ac3()

    # I was doing this for infer_improved...
    def infer_with_guessing(self):
        self.infer_improved()
        if self.is_solved():
            return True
        self.print_board()
        print
        for cell in self.CELLS:
            domain = list(self.get_values(cell))
            if len(domain) > 1:
                for value in domain:
                    sudoku_copy = copy.deepcopy(self)
                    sudoku_copy.board[cell] = [value]
                    if sudoku_copy.infer_with_guessing():
                        self.board = sudoku_copy.board

        if self.is_solved() != True:
            return False

############################################################
# Test Benches:
'''
b = read_board("hw4-medium1.txt")
sudoku = Sudoku(b)
print sudoku.get_values((0, 0))
print
print sudoku.get_values((0, 1))
print
print sudoku_cells()
print
print ((0, 0), (0, 8)) in sudoku_arcs()
print ((0, 0), (8, 0)) in sudoku_arcs()
print ((0, 8), (0, 0)) in sudoku_arcs()
print ((0, 0), (2, 1)) in sudoku_arcs()
print ((2, 2), (0, 0)) in sudoku_arcs()
print ((2, 3), (0, 0)) in sudoku_arcs()
print
sudoku = Sudoku(read_board("hw4-easy.txt"))
sudoku.get_values((0, 3))
print
for col in [0, 1, 4]:
    removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
    print removed, sudoku.get_values((0, 3))
print
sudoku.infer_ac3()
print sudoku.is_solved()
sudoku.print_board()
print
sudoku = Sudoku(read_board("hw4-medium2.txt"))
sudoku.infer_improved()
print sudoku.is_solved()
sudoku.print_board()
'''
############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.`
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
