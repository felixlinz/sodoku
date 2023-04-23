import csv
from colored import fg, bg, attr


class Board:
    def __init__(self, file):
        self.file = file
        self.sodictionary = self.sodictionarymaker(
            self.file
        )  # list that can be meddled with
        self._sodictionary = self.sodictionarymaker(
            self.file
        )  # list that can't be meddled with
        self.make_possible_solutions()  # determines the inital possible_solutions for each element in mutable list, can be run after every solved number
        self.unsolved = self.unsolvedd(
            self.sodictionary
        )  # creates initial mutable list of unsolved fields, also updatable after each iteration
        self.solved = []  # container for what has been solved
        self.frontier = []

    def sodictionarymaker(
        self, file
    ):  # reads csv file of unsolved sudoku, creates list, listed dicts or list of listed dicts
        sodictionary = []  # creating containers for all use cases
        with open(file, "r") as rowfield:
            reader = csv.reader(rowfield)
            for c, row in enumerate(reader):
                ri = []
                for cc, element in enumerate(row):
                    square = self.whichsquare(c, cc)
                    ri.append(
                        {
                            "value": int(element),
                            "row": int(c),
                            "column": int(cc),
                            "square": int(square),
                            "possible_solutions": [],
                            "tried": set(),
                        }
                    )
                sodictionary.append(ri)
        return sodictionary  # returns a list of dictionaries

    def square(self, row, column):  # returns list of values for square in question
        square = self.whichsquare(
            row, column
        )  # determines square where value in question is located
        thisSlist = []
        for element in self.sodictionary:
            for row in element:  # loops through all listed dictionaries
                if (
                    row["square"] == square
                ):  # checks if number ist part of square in question
                    thisSlist.append(row["value"])
        return thisSlist

    def column(self, column):
        # returns a list of all the numbers in a given column
        return [row[column]["value"] for row in self.sodictionary]

    def row(self, row):
        # returns a list of all the numbers in a given row
        return [element["value"] for element in self.sodictionary[row]]

    def unsolvedd(self, dictlist):
        # returns a list of all the currently unsolved cells, in listed dictionaries
        return [
            {
                "row": item["row"],
                "column": item["column"],
                "square": item["square"],
                "possible_solutions": item["possible_solutions"],
                "tried": item["tried"],
            }
            for element in dictlist
            for item in element
            if item["value"] == 0
        ]

    def whichsquare(
        self, row, column
    ):  # detirmes which of the 9 squares a cell is based in, based on row and colummn input
        square_row = (row // 3) * 3
        square_column = (column // 3) * 3
        return square_row // 3 * 3 + square_column // 3

    def make_possible_solutions(
        self,
    ):  # iterates over a given list of listed dictionaries and redetermines all the possibillities for each empty square
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # all sudoku numbers

        for row in self.sodictionary:
            for dict in row:
                a = dict["row"]
                b = dict["column"]
                possible_solutions = list(
                    set(numbers)   # subtracts all the possible sudoku numbers from sets of the cells row, column and square
                    - set(self.row(a))
                    - set(self.column(b))
                    - set(self.square(a, b))
                )

                dict["possible_solutions"] = possible_solutions  # appends updated possible_solutions onto each field

    def update(self, row, column, value):
        # use this to change specific cells of the board, automatically regenerates new possible_solutions for every cell
        self.sodictionary[row][column]["value"] = value
        self.sodictionary[row][column]["tried"].add(value)
        self.make_possible_solutions()
        self.unsolved = self.unsolvedd(self.sodictionary)

    def nukeexplored(self, row, column):
        # resets the initial unsolved fields that succed a cell, inputted via row, column
        for node in self.solved:
            drow, dcolumn = node["row"], node["column"]
            if drow == row:
                if dcolumn > column:
                    self.sodictionary[drow][dcolumn]["value"] = 0
            elif drow > row:
                self.sodictionary[drow][dcolumn]["value"] = 0
        for e, node in enumerate(self.solved):
            if node["row"] == row:
                if node["column"] >= column:
                    del self.solved[e:]
                    break
            elif node["row"] > row:
                del self.solved[e:]

    def printboard(self, aspect="value"):
        # prints the board, if you don't intend to print the values of the cell,
        # you can specify the aspect as "square", "row", "column", "possible_solutions" or "tried"
        GREEN = fg("green")
        RED = fg("red")
        RESET = attr("reset")
        board = [[item[f"{aspect}"] for item in row] for row in self.sodictionary]
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
                if int(self._sodictionary[i][e]["value"]) == 0:
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

    def save(self):
        with open("saved_sudoku.csv", "w") as board:
            writer = csv.writer(board)
            for row in self.sodictionary:
                writer.writerow([item["value"] for item in row])



def main():
    sudoku = Board(getsudoku())
    while len(sudoku.unsolved) != 0:
        if check_correctness(sudoku):
            solve(sudoku).printboard()
            break
        else:
            print("Specified Sudoku Board didn't add up, try again")
            sudoku = Board(getsudoku())


def getsudoku():
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


def solve(sudoku):
    """
    Solves a given sudoku puzzle and returns the solved sudoku object.

    Args:
        sudoku (Sudoku): A Sudoku object to be solved.

    Returns:
        Sudoku: The solved Sudoku object.

    """
    unsolved_length = len(sudoku.unsolved)
    while len(sudoku.solved) < unsolved_length:  # Loops through whole sudoku
        for i, row in enumerate(sudoku.sodictionary):
            for e, field in enumerate(row):
                if field["value"] == 0:
                    if nodes(sudoku, i, e):
                        node = sudoku.frontier.pop()
                        sudoku.update(i, e, node["value"])
                        sudoku.solved.append(node)
                        flag = True
                        break
                    else:
                        try:
                            altnode = sudoku.frontier.pop()
                        except IndexError:
                            raise IndexError("No Possible Solution, perhaps check your input")
                        lastrow, lastcolumn = altnode["row"], altnode["column"]
                        altvalue = altnode["value"]
                        sudoku.nukeexplored(lastrow, lastcolumn)
                        sudoku.update(lastrow, lastcolumn, altvalue)
                        sudoku.solved.append(altnode)
                        flag = True
                        break
            if flag:
                flag = False
                break
    return sudoku


def nodes(sudoku, row, column):
    nodeslist = []
    # optionen = list(set(sudoku.sodictionary[row][column]["possible_solutions"]) - set(sudoku.sodictionary[row][column]["tried"]))
    if len(sudoku.sodictionary[row][column]["possible_solutions"]) > 0:
        for option in sudoku.sodictionary[row][column]["possible_solutions"]:
            possibility = {
                "value": option,
                "row": row,
                "column": column,
            }
            nodeslist.insert(0, possibility)
        sudoku.frontier.extend(nodeslist)
        return True
    else:
        return False

def check_correctness(sudoku):
    for row in sudoku.sodictionary:
        for item in row:
            if len(item["possible_solutions"]) == 0 and item["value"] == 0:
                return False
    for i in range(9):
        for value in sudoku.row(i):
            if value != 0 and sudoku.row(i).count(value)>1:
                return False
    for i in range(9):
        for e in range(9):
            for value in sudoku.square(i,e):
                if value != 0 and sudoku.square(i,e).count(value)>1:
                    return False
    for i in range(9):
        for value in sudoku.column(i):
            if value != 0 and sudoku.column(i).count(value)>1:
                return False
    return True


if __name__ == "__main__":
    main()