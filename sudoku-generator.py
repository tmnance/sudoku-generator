#!/usr/bin/python
import math
import random
import time
import sys
import getopt


measured_elapsed_times = []


def getRandomRangeWithExclusions(exclude_numbers=[]):
    # casting as set also uniques the exclude_numbers list
    numbers = list(set([1, 2, 3, 4, 5, 6, 7, 8, 9]) - set(exclude_numbers))
    if len(numbers) > 1:
        random.shuffle(numbers)
    return numbers


class SudokuSolver:
    def __init__(self):
        self.found_solutions = []

    def checkHasSingleSolution(self, base_grid):
        self.found_solutions = []
        self.findSolutions(base_grid)
        return (len(self.found_solutions) == 1)

    def getAllSolutionCount(self, base_grid):
        self.found_solutions = []
        self.findSolutions(base_grid, True)
        return len(self.found_solutions)

    def findSolutions(self, base_grid, find_all_solutions = False, depth = 0):
        padding_prefix = ('|   ' * (depth))
        # print(padding_prefix + 'findSolutions()')
        padding_prefix = ('|   ' * (depth + 1))

        if not find_all_solutions and len(self.found_solutions) > 1:
            # more than one solution, can stop testing
            return False

        grid = base_grid.getCopy()

        # fill out all single solution positions
        num_replaced = None
        fewest_possibility_xy = None
        while num_replaced is not 0:
            # each time we replace, try all remaining empty positions again
            num_replaced = 0
            fewest_possibilities = 10
            for (x, y) in grid.findValueAllXY(None):
                eligible_values = grid.getXYEligibleValues(x, y)
                num_eligible_values = len(eligible_values)
                if num_eligible_values == 0:
                    # no solution
                    # print(padding_prefix + '>> None :1: no solution <<')
                    return
                elif num_eligible_values == 1:
                    # only one potential value, go ahead and set it
                    grid.setXYValue(x, y, eligible_values[0])
                    if fewest_possibilities > 0:
                        fewest_possibilities = 0
                        fewest_possibility_xy = None
                    num_replaced += 1
                elif num_eligible_values < fewest_possibilities:
                    fewest_possibilities = num_eligible_values
                    fewest_possibility_xy = [x, y]

        if fewest_possibility_xy is None:
            # totally filled, good to go
            self.found_solutions.append(grid)
            # print(padding_prefix + '>> True :2: totally filled, good! <<')
        else:
            # process just the first multi-solution position in this pass
            num_pass = 0
            num_fail = 0
            (x, y) = fewest_possibility_xy

            # print(padding_prefix + '@@ check eligible values', grid.getXYEligibleValues(x, y), '@@')
            for eligible_value in grid.getXYEligibleValues(x, y):
                # attempt a recursive check assuming this value
                grid.setXYValue(x, y, eligible_value)
                self.findSolutions(grid, find_all_solutions, depth + 1)
                if not find_all_solutions and len(self.found_solutions) > 1:
                    # multiple solutions found, can exit now
                    break


class SudokuGrid:
    def __init__(self):
        # initialize empty 9x9 grid
        self.grid_matrix = [[None for x in range(9)] for x in range(9)]

    def getCopy(self):
        copy = SudokuGrid()
        # ensure the copy grid is not using same pointers as original
        copy.grid_matrix = [list(row) for row in self.grid_matrix]
        return copy

    def resetSubGrid(self, subgrid_x, subgrid_y):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        # reset 3x3 subgrid at macro position subgrid_x, subgrid_y
        for (x, y) in [(x, y) for x in range(3) for y in range(3)]:
            x += min_x
            y += min_y
            self.grid_matrix[y][x] = None
        return self

    def setXYValue(self, x, y, new_value):
        self.grid_matrix[y][x] = new_value
        return self

    def setSubgridValues(self, subgrid_x, subgrid_y, new_values):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        for (x, y) in [(x, y) for x in range(3) for y in range(3)]:
            x += min_x
            y += min_y
            new_value = new_values.pop()
            self.grid_matrix[y][x] = new_value
        return self

    def getXYValue(self, x, y):
        return self.grid_matrix[y][x]

    def getRowUsedValues(self, row_num):
        return self.grid_matrix[row_num]

    def getColUsedValues(self, col_num):
        return [row[col_num] for row in self.grid_matrix]

    def getXYSelfSubGridUsedValues(self, x, y):
        subgrid_x = math.floor(x / 3)
        subgrid_y = math.floor(y / 3)
        return self.getSubGridUsedValues(subgrid_x, subgrid_y)

    def getXYEligibleValues(self, x, y):
        # TODO: [TN 3/6/16] instead of recalculating this every time accessed have a way to store it
        #   and update when necessary
        exclude_numbers = set(
            self.getRowUsedValues(y) +
            self.getColUsedValues(x) +
            self.getXYSelfSubGridUsedValues(x, y)
        )
        values = list(set([1, 2, 3, 4, 5, 6, 7, 8, 9]) - exclude_numbers)
        return values

    def getSubGridUsedValues(self, subgrid_x, subgrid_y):
        values = []
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        for (x, y) in [(x, y) for x in range(3) for y in range(3)]:
            x += min_x
            y += min_y
            values.append(self.grid_matrix[y][x])
        return values

    def findSubGridValueXY(self, subgrid_x, subgrid_y, value):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        for (x, y) in [(x, y) for x in range(3) for y in range(3)]:
            x += min_x
            y += min_y
            if self.grid_matrix[y][x] == value:
                return [x, y]
        return None

    def findValueAllXY(self, value):
        found_xy = []
        for (x, y) in [(x, y) for x in range(9) for y in range(9)]:
            if self.grid_matrix[y][x] == value:
                found_xy.append([x, y])
        return found_xy

    def findNotValueAllXY(self, value):
        not_found_xy = []
        for (x, y) in [(x, y) for x in range(9) for y in range(9)]:
            if self.grid_matrix[y][x] != value:
                not_found_xy.append([x, y])
        return not_found_xy

    def _formatGridDisplayValue(self, value):
        if value == None:
            value = '.'
        elif value == True and str(value) == 'True':
            value = 'T'
        elif value == False and str(value) == 'False':
            value = 'F'
        else:
            value = str(value)
        return value

    def displayGrid(self, is_pretty_output = True):
        output = ''

        if is_pretty_output:
            horiz_spacer_row = "-------+-------+-------\n"
            for (i, row) in enumerate(self.grid_matrix):
                output += ' '
                for (j, value) in enumerate(row):
                    value = self._formatGridDisplayValue(value)
                    output += value + ' '
                    if ((j + 1) % 3 == 0 and j < 8):
                        output += '| '
                output += "\n"
                if ((i + 1) % 3 == 0 and i < 8):
                    output += horiz_spacer_row
        else:
            output = ''.join(
                [''.join(
                    self._formatGridDisplayValue(value) for value in row
                ) for row in self.grid_matrix]
            )

        print(output)

    def test(self):
        # verify if valid grid
        # check each row complete
        for row_num in range(9):
            values = list(set(self.getRowUsedValues(row_num) + [None]))
            values.remove(None)
            if len(values) != 9:
                return False
        # check each col complete
        for col_num in range(9):
            values = list(set(self.getColUsedValues(col_num) + [None]))
            values.remove(None)
            if len(values) != 9:
                return False
        # check each subgrid complete
        for (subgrid_x, subgrid_y) in [(x, y) for x in range(3) for y in range(3)]:
            values = list(set(self.getSubGridUsedValues(subgrid_x, subgrid_y) + [None]))
            values.remove(None)
            if len(values) != 9:
                return False
        return True


class SudokuPuzzle:
    population_pattern_order_all = [
        # no internal conflict passes
        [0, 0],
        [1, 1],
        [2, 2],
        # one internal conflict passes
        [0, 2],
        [2, 0],
        # two internal conflict passes
        [0, 1],
        [1, 0],
        # three internal conflict passes (final)
        [1, 2],
        [2, 1],
    ]
    population_pattern_order_no_conflicts = [
        # no internal conflict passes
        [0, 0],
        [1, 1],
        [2, 2],
    ]
    population_pattern_order_with_conflicts = [
        # one internal conflict passes
        [0, 2],
        [2, 0],
        # two internal conflict passes
        [0, 1],
        [1, 0],
        # three internal conflict passes (final)
        [1, 2],
        [2, 1],
    ]

    def __init__(self):
        self.start_time = time.time()
        self.seed_random_attempts = 0
        self.generate_hidden_numbers_attempts = 0
        self.solved_grid = None
        self.final_hidden_numbers_grid = None
        self._seedRandomSolvedGrid()

    def getSolvedGrid(self):
        return self.solved_grid

    def getHiddenNumbersGrid(self, difficulty = 1):
        # puzzle criteria
        # - must have one solution
        # - at least 8 of the numbers 1 - 9 need to be present
        # - avg # of clues around 27, never lower than 17 and never more than 32

        if self.final_hidden_numbers_grid is not None:
            return self.final_hidden_numbers_grid

        self.generate_hidden_numbers_attempts += 1

        # bad input, difficulty must be [1-5]
        if not (1 <= difficulty <= 5):
            return None

        # grid to store final grid with hidden numbers removed
        final_hidden_numbers_grid = self.solved_grid.getCopy()
        if difficulty == 0:
            # difficulty 0 means none hidden
            self.final_hidden_numbers_grid = final_hidden_numbers_grid
            return

        # grid to store remaining hideable numbers (discounting flagged as hidden/always shown)
        hideable_numbers_grid = self.solved_grid.getCopy()

        # flag one of each 1-9 as always visible (may later be superseded)
        for i in range(9):
            search = i + 1
            # get a random subgrid within which to always show the search number
            subgrid_show_position = random.randint(0, 8)
            (subgrid_x, subgrid_y) = SudokuPuzzle.population_pattern_order_all[subgrid_show_position]
            # flag the x, y coords of the search number within this subgrid as never hide
            (x, y) = self.solved_grid.findSubGridValueXY(subgrid_x, subgrid_y, search)
            hideable_numbers_grid.setXYValue(x, y, None)

        # difficulty mappings for [1, 2, 3, 4, 5]
        max_visible_count = [32, 30, 28, 27, 26][difficulty - 1]

        visible_count = 81

        # hardest difficulty special behavior
        if difficulty == 5:
            # remove all instances of one number
            num_to_remove = random.randint(1, 9)
            for (x, y) in final_hidden_numbers_grid.findValueAllXY(num_to_remove):
                hideable_numbers_grid.setXYValue(x, y, None)
                final_hidden_numbers_grid.setXYValue(x, y, None)
                visible_count -= 1

        # we will be checking every number we remove from now on to verify the
        #   removal still results in a single-solution grid
        solver = SudokuSolver()

        num_of_each_number_to_hide = difficulty
        # flag num_of_each_number_to_hide instances of each 1-9 as hidden
        for remove_iteration in range(num_of_each_number_to_hide):
            for search in range(9):
                search += 1
                # find randomized hideable xy positions of the search number
                hideable_xy = hideable_numbers_grid.findValueAllXY(search)
                random.shuffle(hideable_xy)

                # attempt to remove each potential xy until the removal results in single solution
                for (x, y) in hideable_xy:
                    final_hidden_numbers_grid.setXYValue(x, y, None)
                    has_single_solution = solver.checkHasSingleSolution(final_hidden_numbers_grid)
                    if has_single_solution:
                        hideable_numbers_grid.setXYValue(x, y, None)
                        visible_count -= 1
                        break
                    else:
                        # undo hiding, will retry at a different position
                        final_hidden_numbers_grid.setXYValue(x, y, search)

        # get randomized list of every remaining hideable position
        hideable_xy = hideable_numbers_grid.findNotValueAllXY(None)
        random.shuffle(hideable_xy)

        # flag to prevent neverending calculation if we somehow reach a dead end
        attempts_since_last_match = 0

        while visible_count > max_visible_count:
            # get next xy to attempt to hide
            (x, y) = hideable_xy.pop(0)
            existing_value = final_hidden_numbers_grid.getXYValue(x, y)

            # attempt to hide, will undo if unsuccessful
            final_hidden_numbers_grid.setXYValue(x, y, None)
            has_single_solution = solver.checkHasSingleSolution(final_hidden_numbers_grid)
            if has_single_solution:
                # can safely hide this xy position
                attempts_since_last_match = 0
                visible_count -= 1
            else:
                # undo hiding, will retry at a different position
                final_hidden_numbers_grid.setXYValue(x, y, existing_value)
                # add the xy back to end of queue
                hideable_xy.append([x, y])
                attempts_since_last_match += 1
                if attempts_since_last_match > len(hideable_xy):
                    # fail if we have tried every xy position and have not had a successful removal
                    break

        if attempts_since_last_match > 0 or not solver.checkHasSingleSolution(final_hidden_numbers_grid):
            # unlikely -- failed generation, try again
            return self.getHiddenNumbersGrid(difficulty)

        self.final_hidden_numbers_grid = final_hidden_numbers_grid
        return self.final_hidden_numbers_grid

    def _seedRandomSolvedGrid(self):
        is_valid = False
        self.solved_grid = SudokuGrid()

        for (subgrid_x, subgrid_y) in SudokuPuzzle.population_pattern_order_no_conflicts:
            # populate each subgrid in the overall grid
            self._seedSubGridNoConflicts(subgrid_x, subgrid_y)

        while (self.seed_random_attempts < 500 and not is_valid):
            self.seed_random_attempts += 1
            for (subgrid_x, subgrid_y) in SudokuPuzzle.population_pattern_order_with_conflicts:
                # populate each subgrid in the overall grid
                is_valid = self._seedSubGridWithConflicts(subgrid_x, subgrid_y)
                if not is_valid:
                    # failed out of this pass, try again from scratch
                    break

            if not is_valid:
                for (subgrid_x, subgrid_y) in SudokuPuzzle.population_pattern_order_with_conflicts:
                    # reset each subgrid in the overall grid
                    self.solved_grid.resetSubGrid(subgrid_x, subgrid_y)
        return self

    def _seedSubGridNoConflicts(self, subgrid_x, subgrid_y):
        eligible_values = getRandomRangeWithExclusions()
        self.solved_grid.setSubgridValues(subgrid_x, subgrid_y, eligible_values)
        return True

    def _seedSubGridWithConflicts(self, subgrid_x, subgrid_y):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3

        is_valid = False
        attempts = 0
        one_only_nums = [None for x in range(9)]

        self.solved_grid.resetSubGrid(subgrid_x, subgrid_y)

        for (i, (x, y)) in enumerate(SudokuPuzzle.population_pattern_order_all):
            x += min_x
            y += min_y

            xy_conflicts = list(set(self.solved_grid.getRowUsedValues(y) + self.solved_grid.getColUsedValues(x) + [None]))
            xy_conflicts.remove(None)

            if len(xy_conflicts) == 8:
                one_only_nums[i] = getRandomRangeWithExclusions(xy_conflicts)[0]
            elif len(xy_conflicts) == 9:
                # no way we can fill this spot, fail now
                return False
                break

        while (attempts < 50 and not is_valid):
            self.solved_grid.resetSubGrid(subgrid_x, subgrid_y)

            attempts += 1
            is_valid = True
            # copy
            self_used = list(one_only_nums)
            for (i, (x, y)) in enumerate(SudokuPuzzle.population_pattern_order_all):
                x += min_x
                y += min_y

                if one_only_nums[i] is not None:
                    new_value = one_only_nums[i]
                else:
                    xy_conflicts = self.solved_grid.getRowUsedValues(y) + self.solved_grid.getColUsedValues(x)
                    eligible_values = getRandomRangeWithExclusions(xy_conflicts + self_used)

                    if len(eligible_values) == 0:
                        # dead end
                        is_valid = False
                        break
                    new_value = eligible_values[0]

                self.solved_grid.setXYValue(x, y, new_value)
                self_used.append(new_value)

        return is_valid

    def test(self):
        return self.solved_grid.test()

    def getElapsedTime(self):
        return time.time() - self.start_time

    def displayGrid(self, grid_matrix = None, is_pretty_output = True):
        if grid_matrix is None:
            grid_matrix = self.solved_grid

        grid_matrix.displayGrid(is_pretty_output)
        return self


# global measured_elapsed_times
# start_time = time.time()
# measured_elapsed_times.append(time.time() - start_time)

argv = sys.argv[1:]
is_debug_mode = False
difficulty = 1
arg_format = 'sudoku-generator.py -d <difficulty:1-5> --debug'
try:
    opts, args = getopt.getopt(argv, 'hd:', ['debug', 'difficulty='])
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
except getopt.GetoptError:
    print(arg_format)
    sys.exit()


puzzle = SudokuPuzzle()
hidden_numbers_grid = puzzle.getHiddenNumbersGrid(difficulty)
puzzle.displayGrid()
hidden_numbers_grid.displayGrid()
hidden_numbers_grid.displayGrid(False)


if is_debug_mode:
    overall_elapsed_time = puzzle.getElapsedTime()
    print('Overall elapsed time:', round(overall_elapsed_time * 1000, 2))

    if len(measured_elapsed_times) > 0:
        average_elapsed_time = sum(measured_elapsed_times) / float(len(measured_elapsed_times))
        print('Measured elapsed len:', len(measured_elapsed_times))
        print('Measured/all percent:', str(round(100 * sum(measured_elapsed_times) / overall_elapsed_time, 2)) + '%')
        print('Total measured time: ', round(sum(measured_elapsed_times) * 1000, 2))
        print('Average elapsed time:', round(average_elapsed_time * 1000, 5))

    print('Final rand attempts: ', puzzle.seed_random_attempts)
    print('Final hide attempts: ', puzzle.generate_hidden_numbers_attempts)
    print('Test result:         ', puzzle.test())
