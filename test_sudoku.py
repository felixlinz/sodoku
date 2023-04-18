import pytest
from sudoku import Board
from sudoku import solve
from sudoku import nodes
from sudoku import check_correctness

sodoku = Board("sudokutest.csv")
test = Board("saved_sudoku.csv")
broken = Board("broken.csv")

def test_whichquare():
    assert sodoku.whichsquare(0,0) == 0
    assert sodoku.whichsquare(8,8) == 8
    assert sodoku.whichsquare(0,7) == 2
    assert sodoku.whichsquare(7,0) == 6
    assert sodoku.whichsquare(4,5) == 4

def test_square():
    assert sodoku.square(5,5) == [0, 0, 4, 8, 0, 1, 3, 0, 0]
    assert sodoku.square(4,8) == [0, 0, 7, 3, 4, 6, 0, 0, 0]
    assert sodoku.square(1,2) == [0, 7, 4, 0, 0, 0, 0, 0, 0]

def test_row():
    assert sodoku.row(0) == [0,7,4,0,0,0,0,0,0]
    assert sodoku.row(6) == [7,0,0,0,0,0,0,0,0]
    assert sodoku.row(4) == [2,5,9,8,0,1,3,4,6]

def test_column():
    assert sodoku.column(5) == [0, 6, 0, 4, 1, 0, 0, 0, 0]
    assert sodoku.column(8) == [0, 3, 8, 7, 6, 0, 0, 0, 0]

def test_makeoptions():
    assert sodoku.sodictionary[0][0]["possible_solutions"] == [1, 5, 6, 9]
    assert sodoku.sodictionary[6][8]["possible_solutions"] == [1, 2, 4, 5, 9]

def test_update():
    assert sodoku.sodictionary[0][7]["possible_solutions"] == [1, 5]
    sodoku.update(0,8,5)
    assert sodoku.sodictionary[0][8]["value"] == 5
    assert sodoku.sodictionary[0][7]["possible_solutions"] == [1]
    sodoku.update(0,8,0)
    assert sodoku.sodictionary[0][8]["value"] == 0

def test_nukeexplored():
    sodoku.update(6,1,1)
    sodoku.update(0,0,9)
    assert sodoku.sodictionary[6][1]["value"] == 1
    sodoku.solved.append({'value': 6, 'row': 6, 'column': 1})
    sodoku.nukeexplored(4,0)
    assert sodoku.sodictionary[6][1]["value"] == 0
    assert sodoku.sodictionary[0][0]["value"] == 9
    sodoku.update(6,1,0)
    sodoku.update(0,0,0)

def test_check_correctness():
    assert check_correctness(sodoku) == True
    assert check_correctness(broken) == False

def test_nodes():
    assert nodes(sodoku, 0, 0) == True
    assert nodes(test, 8, 8) == False
    assert sodoku.frontier == [{'value': 9, 'row': 0, 'column': 0}, {'value': 6, 'row': 0, 'column': 0}, {'value': 5, 'row': 0, 'column': 0}, {'value': 1, 'row': 0, 'column': 0}]

def test_solve():
    assert solve(sodoku).sodictionary[6][5]["value"] == test.sodictionary[6][5]["value"]
    assert solve(sodoku).sodictionary[8][8]["value"] == test.sodictionary[8][8]["value"]
    with pytest.raises(IndexError):
        solve(broken)
