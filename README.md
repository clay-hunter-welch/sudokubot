Very simple code to solve sudoku boards using two methods: 1) depth first and 2) fullest nines.  
Associated board files are to be fed in via command line.
Ex:
python3 sudokubot.py board1.1.csv

Future improvements as suggested by chatGPT:
1) SudokuFrame class should be broken down into smaller, more focused methods.
2) sudoku function could be broken down for clarity
3) Add more list comprehension to make the code cleaner and more efficient, replacing remaining for loops
4) currently there is no error handling--misformed board, no solution, etc.  Add error handling.
5) The solve times are currently stored in a global variable; clean up that functionality into a non-global solution
6) continue working to comply with PEP8
7) Bonus: I would really like to make a slow but pretty dynamic visualization of the board as it iterates,
   with clear indication of the cells being tried, the choices being made, and successes or failures when reached.
   Highlighted cells, colors, flashing cells, etc.  
