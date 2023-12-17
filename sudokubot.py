#!/usr/bin/python
'''
'''

from __future__ import print_function
import argparse as ap
from copy import deepcopy as dc
import csv
import time
import collections
import re
import sys

# argparse
parser = ap.ArgumentParser(
    prog = 'sudokubot.py',
    description='Reads a sudoku CSV file and produces all solutions to it, if any.'
    )

sl = [1,2,3,4,5,6,7,8,9]
uber_seeds = [[0,0],[3,0],[6,0],[0,3],[3,3],[6,3],[0,6],[3,6],[6,6]]
parser.add_argument('board_file')
args = parser.parse_args()
Cell = collections.namedtuple("Cell", "val x y uber")

# define SudokuFrame as a 9x9 array of Cell namedtuples 
class SudokuFrame:
    def __init__(self,board_file):
        self.solve_edge = []
        self.sb = [[0]*9 for i in range(9)]
        self.nines = []
        self.sorted_nines = []
        self.algo = "brute"
        self.start_time = 0.0
        self.solve_times = []
        with open(board_file, "r") as bf:
            for y, line in enumerate(iter(bf.readline, '')):            
                raw_row = list(map(int,line.strip('\n').split(',')))
                for x, cell_val in enumerate(raw_row):
                    self.sb[x][y] = Cell(int(cell_val), int(x), int(y), self.calc_uber_cell(x,y))
                if y == 8:
                    break
        init_flag = self.calc_nines()

    def calc_nines(self):
        self.nines = []
        self.sorted_nines = []
        sum_nonzero = 0
        # okay, also, self.nines is being appended every loop.  Don't need to do that.  
        # self.nines just needs to be intialized on read.  Move that up.
        for y in range(9):
            sum_nonzero = len([x for x in range(9) if self.sb[x][y].val > 0])
            self.nines.append(Cell(sum_nonzero, "r", 0, y))
            if sum_nonzero < 9:
                self.sorted_nines.append(Cell(sum_nonzero, "r", 0, y)) 
            sum_nonzero = 0
        for x in range(9):
            sum_nonzero = len([y for y in range(9) if self.sb[x][y].val > 0])
            self.nines.append(Cell(sum_nonzero, "c", 0, x))
            if sum_nonzero < 9:
                self.sorted_nines.append(Cell(sum_nonzero, "c", 0, x))
            sum_nonzero = 0
        for u in range(9):
            xx, yy = uber_seeds[u]
            for y in range(yy, yy+3):
                for x in range(xx, xx+3):
                    if self.sb[x][y].val > 0:
                        sum_nonzero += 1
            self.nines.append(Cell(sum_nonzero, "u", 0, u))
            if sum_nonzero < 9:
                self.sorted_nines.append(Cell(sum_nonzero, "u", 0, u))
            sum_nonzero = 0
        self.sorted_nines = sorted(self.sorted_nines, reverse = True)
        return()

    def calc_uber_cell(self, x, y):
        return int(x/3) + ((int(y/3)) * 3)

    def calc_solve_edge(self):
        new_solve_edge_set = 0
        # list comprehension here?  lots going on
        if self.algo == "brute":
            for y in range(9):
                for x in range(9):        
                    if not new_solve_edge_set:
                        if self.sb[x][y].val == 0:
                            self.solve_edge = [x,y]
                            new_solve_edge_set = 1
                            break
        elif self.algo == "f9":
            #Cell: fill level val, paradigm initial, 0, paradigm number

            if (len(self.sorted_nines)):
                val = self.sorted_nines[0].val
                initial = self.sorted_nines[0].x
                inumber = self.sorted_nines[0].uber
                if initial == "r":
                    for x in range(9):
                        y = int(inumber)
                        if ((self.sb[x][y].val == 0) and (new_solve_edge_set == 0)):
                            self.solve_edge = [x,y]
                            new_solve_edge_set = 1
                            break
                elif initial == "c":
                    for y in range(9):
                        x = int(inumber)
                        if ((self.sb[x][y].val == 0) and (new_solve_edge_set == 0)):
                            self.solve_edge = [x,y]
                            new_solve_edge_set = 1
                            break
                elif initial == "u":
                    start_coord = uber_seeds[int(inumber)]
                    for y in range(start_coord[1], start_coord[1] + 3):
                        for x in range(start_coord[0], start_coord[0] + 3):
                            if ((self.sb[x][y].val == 0) and (new_solve_edge_set == 0)):
                                self.solve_edge = [x,y]
                                new_solve_edge_set = 1
                                break
        return (new_solve_edge_set)


    def describe_solve_edge_values(self):
        edge_x = self.sb[self.solve_edge[0]][self.solve_edge[1]].x
        edge_y = self.sb[self.solve_edge[0]][self.solve_edge[1]].y
        edge_uber = self.sb[self.solve_edge[0]][self.solve_edge[1]].uber
        return(edge_x,edge_y,edge_uber)

    def possibles(self):
        possibles = []
        edge_x, edge_y, edge_uber = self.describe_solve_edge_values()
        row = []
        for i in range(9):
            row.append(self.sb[i][edge_y].val)    
        row_remains = [i for i in sl if i not in row]
        column = []
        for i in range(9):
            column.append(self.sb[edge_x][i].val)
        column_remains = [i for i in sl if i not in column]
        uber_list = []
        start_coord = uber_seeds[edge_uber]
        for j in range(start_coord[1], start_coord[1] + 3):
            for i in range(start_coord[0], start_coord[0] + 3):
                uber_list.append(self.sb[i][j].val)
        uber_remains = [i for i in sl if i not in uber_list]
        possibles = [i for i in row_remains if i in column_remains]
        possibles = [i for i in possibles if i in uber_remains]
        return possibles

    def draw(self):
        board_string = "\r"
        space_line = "||   |   |   ||   |   |   ||   |   |   ||\n"

        for y in range(0,9):
            if not y % 3:
                if not y == 0:
                    board_string += (space_line)
                board_string += ('=' * 41) + ('\n')
            board_string += (space_line)
            for x in range(0,9):
                if not x % 3:
                    board_string += ('|')
                pval = self.sb[x][y].val
                if pval == 0:
                    pval=" "
                board_string += ('| {0} '.format(str(pval)))
            board_string += ('||\n')
        board_string += (space_line)
        board_string += ('=' * 41) + ('\n')
        print(board_string)
    
    def add_cell(self, add_val):
        global solve_times
        edge_x,edge_y,edge_uber = self.describe_solve_edge_values()
        self.sb[edge_x][edge_y] = self.sb[edge_x][edge_y]._replace(val = add_val)
        self.nines[edge_y] = self.nines[edge_y]._replace(val = int(self.nines[edge_y].val) + 1)
        self.nines[edge_x + 9] = self.nines[edge_x + 9]._replace(val = int(self.nines[edge_x + 9].val) + 1)
        self.nines[edge_uber + 18] = (self.nines[edge_uber + 18].
            _replace(val = int(self.nines[edge_uber + 18].val) + 1))
        self.calc_nines()
        new_solve_edge_set = self.calc_solve_edge()
        if not new_solve_edge_set:
            lap = time.time()
            print('Solve discovered in ', (lap-self.start_time)*10**3, 'ms')
            self.draw()


# define sudoku fullest nines solve recursive function
def sudoku(board_evolution):
    board_evolution = dc(board_evolution)
    possibles = board_evolution.possibles()
    if possibles:
        for test_val in possibles:
            test_board = dc(board_evolution)
            test_board.add_cell(test_val)
            test_board.calc_nines()
            sudoku(test_board)    
    return


def main():
    board_file=args.board_file
    board = SudokuFrame(board_file)
    print('Board initial state:')
    board.draw()

    solve_times = []
    board.calc_solve_edge()
    for i in range(10):
        print('running pass ', i)
        board.start_time = time.time()
        sudoku(board)
        solve_times.append(time.time() - board.start_time)
    avg_d1st_solve = sum(solve_times) / 10 * 10**3
    board.algo = "f9"
    solve_times = []
    board.calc_solve_edge()
    for i in range(10):
        board.start_time = time.time()
        sudoku(board)
        solve_times.append(time.time() - board.start_time)
    avg_f9_solve = sum(solve_times) / 10 * 10**3
    percent_faster = 100 - (100 * avg_f9_solve / avg_d1st_solve)
    print ('Avg d1st solve time: {} ms Average f9 solve time: {} ms'.format(avg_d1st_solve,avg_f9_solve))
    print ('f9 is average {} percent faster than d1st'.format(percent_faster))


main()
