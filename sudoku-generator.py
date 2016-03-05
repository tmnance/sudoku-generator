#!/usr/bin/python
import random
import time


measured_elapsed_times = []


def getRandomRangeWithExclusions(exclude_numbers=[]):
    # [TN 3/5/16] this function has been optimized for performance
    # numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # exclude_numbers = list(set(exclude_numbers))
    # for exclude_number in exclude_numbers:
    #     numbers.remove(exclude_number)
    # casting as set also uniques the exclude_numbers list
    numbers = list(set([1, 2, 3, 4, 5, 6, 7, 8, 9]) - set(exclude_numbers))
    if len(numbers) > 1:
        random.shuffle(numbers)
    return numbers


class Grid:
    population_pattern_order = [
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

    def __init__(self):
        self._seedRandom()

    def _resetGridMatrix(self):
        # fill empty 9x9 grid
        self.grid_matrix = [[None for x in range(9)] for x in range(9)]
        return self

    def _resetSubGrid(self, subgrid_x, subgrid_y):
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        for coords in Grid.population_pattern_order:
            x = min_x + coords[0]
            y = min_y + coords[1]
            self.grid_matrix[y][x] = None
        return self

    def _seedSubGrid(self, subgrid_x, subgrid_y):
        # no conflicts
        check_used = (subgrid_x != subgrid_y)
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        if check_used:
            is_valid = False
            attempts = 0

            while (attempts < 10 and not is_valid):
                self._resetSubGrid(subgrid_x, subgrid_y)
                attempts += 1
                is_valid = True
                self_used = []
                for coords in Grid.population_pattern_order:
                    x = min_x + coords[0]
                    y = min_y + coords[1]

                    # get unique
                    exclude = self.getRowUsedValues(y) + self.getColUsedValues(x) + self_used
                    eligible_values = getRandomRangeWithExclusions(exclude)

                    if len(eligible_values) == 0:
                        # dead end
                        is_valid = False
                        break
                    new_value = eligible_values[0]

                    # assigning directly for performance
                    self.grid_matrix[y][x] = new_value

                    self_used.append(new_value)

            # print('attempts : ', attempts)
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # self.debug()
            return is_valid
        else:
            # seed with no conflicts
            max_x = min_x + 3
            max_y = min_y + 3
            eligible_values = getRandomRangeWithExclusions()

            for coords in Grid.population_pattern_order:
                x = min_x + coords[0]
                y = min_y + coords[1]
                new_value = eligible_values.pop()
                self.grid_matrix[y][x] = new_value

            return True

    def _seedRandom(self):
        is_valid = False
        self.attempts = 0

        while (self.attempts < 1000 and not is_valid):
            self.attempts += 1
            self._resetGridMatrix()
            for coords in Grid.population_pattern_order:
                x = coords[0]
                y = coords[1]
                is_valid = self._seedSubGrid(x, y)
                if not is_valid:
                    # failed out of this pass, try again from scratch
                    break
        return self

    def getRowUsedValues(self, row_num):
        return self.grid_matrix[row_num]

    def getColUsedValues(self, col_num):
        # [TN 3/5/16] this function has been optimized for performance
        return [row[col_num] for row in self.grid_matrix]

    def debug(self):
        output = "Grid::debug\n"

        header_footer_row = '      '
        for i in list(range(0, 9)):
            header_footer_row += str(i + 1) + ' '
            if (i + 1) % 3 == 0:
                header_footer_row += '  '
        header_footer_row += "\n"

        horiz_spacer_row = "    +-------+-------+-------+\n"

        output += header_footer_row
        output += horiz_spacer_row
        for (i, row) in enumerate(self.grid_matrix):
            output += str(i + 1) + '   '
            output += '| '
            for (j, col) in enumerate(row):
                if col == None:
                    col = '.'
                output += str(col) + ' '
                if (j + 1) % 3 == 0:
                    output += '| '
            output += '  ' + str(i + 1)
            output += "\n"
            if (i + 1) % 3 == 0:
                output += horiz_spacer_row

        output += header_footer_row
        print(output)



# global measured_elapsed_times
# start_time = time.time()
# measured_elapsed_times.append(time.time() - start_time)

start_time = time.time()
###
grid = Grid()
###
overall_elapsed_time = time.time() - start_time

average_elapsed_time = 0
if len(measured_elapsed_times) > 0:
    average_elapsed_time = sum(measured_elapsed_times) / float(len(measured_elapsed_times))

print('measured elapsed len:  ', len(measured_elapsed_times))
print('overall_elapsed_time:  ', round(overall_elapsed_time * 1000, 5))
print('measured/all percent:  ', str(round(100 * sum(measured_elapsed_times) / overall_elapsed_time, 2)) + '%')
print('total measured time:   ', round(sum(measured_elapsed_times) * 1000, 5))
print('average elapsed time:  ', round(average_elapsed_time * 1000, 5))
print('')

print('Final attempts : ', grid.attempts)
grid.debug()

# print("done")

