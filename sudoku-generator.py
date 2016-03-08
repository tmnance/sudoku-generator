#!/usr/bin/python
import math
import random
import time
import sys
import getopt
import sudokupuzzle


argv = sys.argv[1:]
is_debug_mode = False
is_pretty_output = False
difficulty = 1
arg_format = 'sudoku-generator.py -d <difficulty:1-5> --debug --pretty'
try:
    opts, args = getopt.getopt(argv, 'hd:', ['difficulty=', 'debug', 'pretty'])
    for opt, arg in opts:
        if opt == '-h':
            print(arg_format)
            sys.exit()
        elif opt in ('-d', '--difficulty') and str(arg).isdigit():
            arg = int(arg)
            if 0 <= arg <= 5:
                # difficulty within proper range
                difficulty = int(arg)
        elif opt == '--debug':
            is_debug_mode = True
        elif opt == '--pretty':
            is_pretty_output = True
except getopt.GetoptError:
    print(arg_format)
    sys.exit()


start_time = time.time()
puzzle = sudokupuzzle.SudokuPuzzle()
hidden_numbers_grid = puzzle.getHiddenNumbersGrid(difficulty)


if is_debug_mode:
    solved_grid = puzzle.solved_grid
    solved_grid.displayGrid()
    solved_grid.displayGrid(False)
    print('')
    hidden_numbers_grid.displayGrid()
    hidden_numbers_grid.displayGrid(False)
    print('')

    elapsed_time = time.time() - start_time
    print('Overall elapsed time:', round(elapsed_time * 1000, 2))
    print('Final rand attempts: ', puzzle.seed_random_attempts)
    print('Final hide attempts: ', puzzle.generate_hidden_numbers_attempts)
    print('Test result:         ', puzzle.test())
else:
    hidden_numbers_grid.displayGrid(is_pretty_output)
