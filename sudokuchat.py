import csv
import copy
from colored import fg, attr
from functools import wraps
import time

class Board:
    def __init__(self, file):
        self.file = file
        self.board = self.boardmaker(self.file)
        self.boardlist = self.delist(self.board)
        self._board = copy.deepcopy(self.board)
        self.make_possible_solutions()  # determines the inital possible_solutions for each element in mutable list, can be run after every solved number
        self.unsolved = self.unsolvedd()  # creates initial mutable list of unsolved fields, also updatable after each iteration
        self.solved = []  # container for what has been solved
        self.frontier = []

    def delist(self, board):
        """
        generates a version of the board that isn't nested lists
        not suitable for finding cells with coordinates but easier to iterate
        """
        nonestlist = []
        for row in board:
            nonestlist.extend(row)
        return nonestlist


    def boardmaker(self, file):  
        """
        reads csv file of unsolved sudoku, creates list, listed dicts or list of listed dicts
        """
        board = []  # creating containers for all use cases
        with open(file, "r") as rowfield:
            reader = csv.reader(rowfield)
            for c, row in enumerate(reader):
                ri = []
                for cc, element in enumerate(row):
                    if int(element) != 0:
                        ri.append(Solved_Cell(element,c,cc,self.whichsquare(c,cc)))
                    else:
                        ri.append(Unsolved_Cell(element,c,cc,self.whichsquare(c,cc)))
                board.append(ri)
        return board  # returns a list of dictionaries
    
    def whichsquare(self, row, column):  
        """
        detirmes which of the 9 squares a cell is based in, based on row and colummn input
        """
        square_row = (row// 3) * 3
        square_column = (column // 3) * 3
        return square_row // 3 * 3 + square_column // 3
    
    def square(self, square):  
        """
        returns list of values for square in question
        """
        return {cell.value for cell in self.boardlist if cell.square == square}

    def column(self, column):
        """
        returns a list of all the values in a given column
        """
        return {row[column].value for row in self.board}

    def row(self, row):
        """
        returns a list of all the values in a given row
        """
        return {element.value for element in self.board[row]}

    def unsolvedd(self):
        """
        returns a list of all the currently unsolved cells, in listed dictionaries
        """
        return [
            cell
            for row in self.board
            for cell in row
            if cell.value == 0
        ]

    def make_possible_solutions(self,): 
        """ 
        iterates over a given list of listed Cells and 
        redetermines all the possibillities for each empty square
        """
        sudoku_numbers = set(range(1,10)) # all sudoku numbers

        for row in self.board:
            for cell in row:
                a = cell.row
                b = cell.column
                possible_solutions = sudoku_numbers - self.row(a) - self.column(b) - self.square(cell.square)
                """
                    sudoku_numbers   
                    - set(self.row(a))
                    - set(self.column(b))
                    - set(self.square(cell.square))
                """

                cell.options = possible_solutions  # appends updated possible_solutions onto each field

    def update(self, row, column, value):
        """
        use this to change specific cells of the board, 
        automatically regenerates new possible_solutions for every cell
        """
        self.board[row][column].value = value
        self.make_possible_solutions()
        self.unsolved = self.unsolvedd()

    def nukeexplored(self, row, column):
        """
        resets the initial unsolved fields that succed a cell, inputted via row, column
        """
        # resetting the board
        for node in self.solved:
            if node.row == row:
                if node.column > column:
                    self.board[node.row][node.column].value = 0
            elif node.row > row:
                self.board[node.row][node.column].value = 0
        # resetting the solved list
        for e, node in enumerate(self.solved):
            if node.row == row:
                if node.column >= column:
                    del self.solved[e:]
                    break
            elif node.row > row:
                del self.solved[e:]

    def printboard(self):
        """
        prints the board, initially unsolved cells are green
        """
        GREEN = fg("green")
        RED = fg("red")
        RESET = attr("reset")
        board = [[item.value for item in row] for row in self.board]
        horz = f"{RED}═════════════{RESET}"
        vert = f"{RED}║{RESET}"
        cross = f"{RED}╬{RESET}"
        space = "             "
        schwellen = [2, 5]
        print(f"{RED}╔═══════════════╦═══════════════╦═══════════════╗{RESET}")
        for i, row in enumerate(board):
            print(vert, space, vert, space, vert, space, vert)
            print(vert, end="")
            for e, number in enumerate(row):
                if self._board[i][e].value == 0:
                    print(f"{GREEN}  {number}  {RESET}", end="")
                else:
                    print(f"  {number}  ", end="")
                if e in schwellen:
                    print(vert, end="")
            print(vert)
            if i in schwellen:
                print(vert, space, vert, space, vert, space, vert)
                print(cross, horz, cross, horz, cross, horz, cross)
        print(vert, space, vert, space, vert, space, vert)
        print(f"{RED}╚═══════════════╩═══════════════╩═══════════════╝{RESET}")

class Solved_Cell:
    """
    Object in which all the Data regarding a single cell is stored
    Completely immutable
    """
    def __init__(self, value, row, column, square):
        self._value = int(value)  
        self._row = int(row)     
        self._column = int(column)      
        self.square = square 

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def value(self):
        return self._value

class Unsolved_Cell(Solved_Cell):
    def __init__(self, value, row, column, square, options = None):
        super().__init__(value, row, column, square)
        self._options = options

    @Solved_Cell.value.setter
    def value(self, value):
        self._value = int(value)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, new_options):
        self._options = new_options

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def main():
    sudoku = Board("sudoku2.csv")
    while len(sudoku.unsolved) != 0:
        if check_correctness(sudoku):
            solve(sudoku).printboard()
            break
        else:
            print("Specified Sudoku Board didn't add up, try again")
            sudoku = Board(getsudoku())

def getsudoku():
    """
    asks the user for input and creates an 
    iterable csv file representing the sudoku
    """
    rows = 1
    print("Input Row by Row, replace empty fields with Zeroes or Whitespace")
    open("sudoku2.csv", "w")
    while rows < 10:
        row = list(input(f"Row {rows}   |").replace(" ", "0"))
        if len(row) == 9:
            rows += 1
            with open("sudoku2.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(row)
        else:
            print(f"incorrect Row input, try again row{row}")
    return "sudoku2.csv"

@timeit
def solve(sudoku):
    """
    Solves a given sudoku puzzle and returns the solved sudoku object
    using depth first search

    Args:
        sudoku (Sudoku): A Sudoku object to be solved.

    Returns:
        Sudoku: The solved Sudoku object if there is a possible solution

    """
    unsolved_length = len(sudoku.unsolved)
    # sorts the order in which the algo explores the states by reversed length of options
    # sudoku.unsolved.sort(key = lambda x: len(x.options), reverse = True)
    while len(sudoku.solved) < unsolved_length:  # Loops through whole sudoku
        for cell in sudoku.unsolved:
            if cell.value == 0:
                if nodes(sudoku, cell.row, cell.column):
                    node = sudoku.frontier.pop()
                    sudoku.update(node.row, node.column, node.value)
                    sudoku.solved.append(node)
                    flag = True
                    break
                else:
                    try:
                        # in case the previous try has run into a dead end, this explores an 
                        # alternative to the last picked option
                        altnode = sudoku.frontier.pop()
                    except IndexError:
                        raise IndexError("No Possible Solution, perhaps check your input")
                    # deletes everything that had been filled in post the step we check out
                    sudoku.nukeexplored(altnode.row, altnode.column)
                    sudoku.update(altnode.row, altnode.column, altnode.value)
                    sudoku.solved.append(altnode)
                    flag = True
                    break
            if flag:
                flag = False
                break
    return sudoku



def nodes(sudoku, row, column):
    """
    checks if there are any options where they are supposed to be

    if so, returns true and extends end of frontier 
    """
    nodeslist = []
    if sudoku.board[row][column].options:
        # checking for length is significantly quicker than checking with logic for some reason
        for option in sudoku.board[row][column].options:
            possibility = Unsolved_Cell(option, row, column,sudoku.board[row][column].square) 
            # don't remember why but this is very important
            # figure out at pleeaaase
            nodeslist.insert(0, possibility)
        sudoku.frontier.extend(nodeslist)
        return True
    else:
        return False

def check_correctness(sudoku):
    """
    checks if an inputted Sudoku adds up 
    """
    for row in sudoku.board:
        for item in row:
            # if something is unsolved and has no possible solution 
            # returns false
            if len(item.options) == 0 and item.value == 0:
                return False
    return True


if __name__ == "__main__":
    main()