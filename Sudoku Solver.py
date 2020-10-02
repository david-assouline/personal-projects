import time

board = [
    [0,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def board_generator():
    """ optional function. gives user the option to generate sudoku board through user input, row by
    row, left to right. If this function is disabled, sudoku board values must be entered through
    list variable 'board' """

    global board
    board = []
    print("Enter all of the board's values going from left to right on a row by row basis, press enter"
          " after each entry.\n""")
    for _ in range(9):
        temprow = []
        for j in range(9):
            x = (int(input("--> ")))
            while x > 9:
                print("You must enter a value between 0 and 9")
                x = (int(input("--> ")))
            else:
                temprow.append(x)

        board.append(temprow)


def print_board(board):
    """prints a semi-formatted version of the sudoku 3x3 board"""

    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- " * 14)

        for x in range(9):
            if x % 3 == 0 and x != 0:
                print("  |  ", end="")

            if x == 8:
                print(board[i][x])
            else:
                print(str(board[i][x]) + " ", end="")


def isvalid(board, number, position):

    # checks if row is valid
    for i in range(9):
        if board[position[0]][i] == number and position[1] != i:
            return False

    # checks if column is valid
    for i in range(9):
        if board[i][position[1]] == number and position[0] != i:
            return False

    # checks if box is valid
    xbox = position[1] // 3
    ybox = position[0] // 3

    for i in range(ybox * 3, ybox * 3 + 3):
        for x in range(xbox * 3, xbox * 3 + 3):
            if board[i][x] == number and (i, x) != position:
                return False

    return True


def find_empty(board):
    for i in range(9):
        for x in range(9):
            if board[i][x] == 0:
                return i, x  # returns row then column

    return None


def solve(board):

    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if isvalid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


# board_generator()
print_board(board)
start_time = time.time()
solve(board)
print("*" * 30)
print("*" * 30)
print_board(board)
print("Elapse time: {} seconds".format(time.time() - start_time))
