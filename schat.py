from sudokuchat import Board as Board
from sudokuchat import solve as solve
from sudokuchat import getsudoku as getsudoku
from tabulate import tabulate


def chatsolver():
    result = test()
    return (tabulate(result, tablefmt="rounded_grid"))

def test():
    sudoku = Board(getsudoku())
    result = solve(sudoku).board
    board = []
    for row in result:
        line = []
        for cell in row:
            line.append(cell.value)
        board.append(line)
    return board

if __name__=="__main__":
    main()