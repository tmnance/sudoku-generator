#!/usr/bin/python
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

    def __init__(self, difficulty):
        self.start_time = time.time()
        if 0 <= difficulty <= 5:
            self.difficulty = difficulty
        else:
            difficulty = 1
        self._seedRandomSolvedGrid()

    def _seedRandomSolvedGrid(self):
        is_valid = False
        self.attempts = 0
        self._resetGridMatrix()

        for (subgrid_x, subgrid_y) in SudokuPuzzle.population_pattern_order_no_conflicts:
            # populate each subgrid in the overall grid
            self._seedSubGridNoConflicts(subgrid_x, subgrid_y)

        while (self.attempts < 500 and not is_valid):
            self.attempts += 1
            for (filled_grid_num, (subgrid_x, subgrid_y)) in enumerate(SudokuPuzzle.population_pattern_order_with_conflicts):
                # populate each subgrid in the overall grid
                is_valid = self._seedSubGridWithConflicts(subgrid_x, subgrid_y, filled_grid_num + 3)
                if not is_valid:
                    # failed out of this pass, try again from scratch
                    break

            if not is_valid:
                for (subgrid_x, subgrid_y) in SudokuPuzzle.population_pattern_order_with_conflicts:
                    # reset each subgrid in the overall grid
                    self._resetSubGrid(subgrid_x, subgrid_y)
        return self

    def _resetGridMatrix(self):
        # fill empty 9x9 grid
        self.grid_matrix = [[None for x in range(9)] for x in range(9)]
        return self

    def _resetSubGrid(self, subgrid_x, subgrid_y):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        for (x, y) in SudokuPuzzle.population_pattern_order_all:
            x += min_x
            y += min_y
            self.grid_matrix[y][x] = None
        return self

    def _seedSubGridNoConflicts(self, subgrid_x, subgrid_y):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        eligible_values = getRandomRangeWithExclusions()
        for (x, y) in SudokuPuzzle.population_pattern_order_all:
            x += min_x
            y += min_y
            new_value = eligible_values.pop()
            self.grid_matrix[y][x] = new_value
        return True

    def _seedSubGridWithConflicts(self, subgrid_x, subgrid_y, filled_grid_num):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3

        is_valid = False
        attempts = 0
        one_only_nums = [None for x in range(9)]

        self._resetSubGrid(subgrid_x, subgrid_y)

        for (i, (x, y)) in enumerate(SudokuPuzzle.population_pattern_order_all):
            x += min_x
            y += min_y

            xy_conflicts = list(set(self.getRowUsedValues(y) + self.getColUsedValues(x) + [None]))
            xy_conflicts.remove(None)

            if len(xy_conflicts) == 8:
                one_only_nums[i] = getRandomRangeWithExclusions(xy_conflicts)[0]
            elif len(xy_conflicts) == 9:
                # no way we can fill this spot, fail now
                return False
                break

        while (attempts < 25 and not is_valid):
            self._resetSubGrid(subgrid_x, subgrid_y)

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
                    xy_conflicts = self.getRowUsedValues(y) + self.getColUsedValues(x)
                    eligible_values = getRandomRangeWithExclusions(xy_conflicts + self_used)

                    if len(eligible_values) == 0:
                        # dead end
                        is_valid = False
                        break
                    new_value = eligible_values[0]

                # assigning directly for performance
                self.grid_matrix[y][x] = new_value
                self_used.append(new_value)

        return is_valid

    def getRowUsedValues(self, row_num):
        return self.grid_matrix[row_num]

    def getColUsedValues(self, col_num):
        # [TN 3/5/16] this function has been optimized for performance
        return [row[col_num] for row in self.grid_matrix]

    def getSubGridUsedValues(self, subgrid_x, subgrid_y):
        values = []
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        for (x, y) in SudokuPuzzle.population_pattern_order_all:
            x += min_x
            y += min_y
            values.append(self.grid_matrix[y][x])
        return values

    def _findSubGridValueXY(self, subgrid_x, subgrid_y, value):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        for (x, y) in SudokuPuzzle.population_pattern_order_all:
            x += min_x
            y += min_y
            if self.grid_matrix[y][x] == value:
                return [x, y]
        return None

    def _findValueAllXY(self, value):
        found_xy = []
        for (subgrid_x, subgrid_y) in SudokuPuzzle.population_pattern_order_all:
            found_xy.append(self._findSubGridValueXY(subgrid_x, subgrid_y, value))
        return found_xy

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
        for (subgrid_x, subgrid_y) in SudokuPuzzle.population_pattern_order_with_conflicts:
            values = list(set(self.getSubGridUsedValues(subgrid_x, subgrid_y) + [None]))
            values.remove(None)
            if len(values) != 9:
                return False
        return True

    def getElapsedTime(self):
        return time.time() - self.start_time

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

    def displayGrid(self, grid_matrix = None, is_pretty_output = True):
        output = ''

        if is_pretty_output:
            horiz_spacer_row = "-------+-------+-------\n"

            if grid_matrix is None:
                grid_matrix = self.grid_matrix

            for (i, row) in enumerate(grid_matrix):
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
                ) for row in grid_matrix]
            )

        print(output)


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


puzzle = SudokuPuzzle(difficulty)
puzzle.displayGrid()


if is_debug_mode:
    overall_elapsed_time = puzzle.getElapsedTime()
    print('Overall elapsed time:', round(overall_elapsed_time * 1000, 2))

    if len(measured_elapsed_times) > 0:
        average_elapsed_time = sum(measured_elapsed_times) / float(len(measured_elapsed_times))
        print('Measured elapsed len:', len(measured_elapsed_times))
        print('Measured/all percent:', str(round(100 * sum(measured_elapsed_times) / overall_elapsed_time, 2)) + '%')
        print('Total measured time: ', round(sum(measured_elapsed_times) * 1000, 2))
        print('Average elapsed time:', round(average_elapsed_time * 1000, 5))

    print('Final attempts:      ', puzzle.attempts)
    print('Test result:         ', puzzle.test())
