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
puzzle_string = None
arg_format = 'sudoku-solver.py -p <puzzle> --debug --pretty'
try:
    opts, args = getopt.getopt(argv, 'hp:', ['puzzle=', 'debug', 'pretty'])
    for opt, arg in opts:
        if opt == '-h':
            print(arg_format)
            sys.exit()
        elif opt in ('-p', '--puzzle'):
            puzzle_string = str(arg).strip()
            if len(arg) == 81:
                # puzzle_string has proper length
                puzzle_string = arg
        elif opt == '--debug':
            is_debug_mode = True
        elif opt == '--pretty':
            is_pretty_output = True
except getopt.GetoptError:
    print(arg_format)
    sys.exit()


if puzzle_string is None:
    print('No puzzle string specified')
    sys.exit()

start_time = time.time()
input_grid = sudokupuzzle.SudokuGrid()
is_valid_input_grid = input_grid.seedFromString(puzzle_string)

if not is_valid_input_grid:
    print('Invalid puzzle string, should be something like this:')
    print('2..7..5...7...1....493.8..772..961....5..3.743.1.....9..2...76.95....4..18..6.3..')
    sys.exit()


solved_grid = None
solver = sudokupuzzle.SudokuSolver()
has_single_solution = solver.checkHasSingleSolution(input_grid)
if has_single_solution:
    solved_grid = solver.getSolutionGrid()

if solved_grid is None:
    print('Bad puzzle string, has more than one solution')
    sys.exit()
elif not solved_grid.test():
    print('Invalid grid format')
    sys.exit()


if is_debug_mode:
    if is_valid_input_grid:
        input_grid.displayGrid()
        input_grid.displayGrid(False)
        print('')
    if solved_grid != None:
        solved_grid.displayGrid()
        solved_grid.displayGrid(False)
        print('')

    elapsed_time = time.time() - start_time
    print('Overall elapsed time:', round(elapsed_time * 1000, 2))
    print('Test result:         ', solved_grid.test())
else:
    solved_grid.displayGrid(is_pretty_output)
