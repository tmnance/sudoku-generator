#!/usr/bin/python
import random


def getSetNonEmptyUniqueValues(values):
    # get unique
    values = list(set(values))
    # remove None if set
    if None in values:
        values.remove(None)
    return values

def isSequence(arg):
    return (not hasattr(arg, "strip") and
        hasattr(arg, "__getitem__") or
        hasattr(arg, "__iter__"))

def getRandomRangeWithExclusions(exclude_numbers=None):
    # generate a list of 1-9
    numbers = list(range(1, 10))
    if exclude_numbers != None:
        # excluding one or more numbers
        if not isSequence(exclude_numbers):
            # convert integer to list
            exclude_numbers = [exclude_numbers]
        # get unique
        exclude_numbers = list(set(exclude_numbers))
        for exclude_number in exclude_numbers:
            numbers.remove(exclude_number)
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
            self.setXYValue(x, y, None)
        return self

    def _seedSubGrid(self, subgrid_x, subgrid_y):
        check_used = True # (subgrid_x != subgrid_y)
        min_x = subgrid_x * 3
        min_y = subgrid_y * 3
        if check_used:
            is_valid = False
            attempts = 0

            while (attempts < 100 and not is_valid):
                self._resetSubGrid(subgrid_x, subgrid_y)
                attempts += 1
                is_valid = True
                self_used = []
                for coords in Grid.population_pattern_order:
                    x = min_x + coords[0]
                    y = min_y + coords[1]
                    exclude = self.getRowUsedValues(y) + self.getColUsedValues(x) + self_used
                    # print("exclude row", y, self.getRowUsedValues(y))
                    # print("exclude col", x, self.getColUsedValues(x))
                    eligible_values = getRandomRangeWithExclusions(exclude)

                    if len(eligible_values) == 0:
                        is_valid = False
                        break
                    new_value = eligible_values[0]

                    self.setXYValue(x, y, new_value)
                    self_used.append(new_value)

            # print('attempts : ', attempts)
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # self.debug()
            return is_valid
        else:
            max_x = min_x + 3
            max_y = min_y + 3
            random = getRandomRangeWithExclusions()
            # print("_seedSubGrid : ", min_x, max_x, min_y, max_y)
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    new_value = random.pop()
                    self.setXYValue(x, y, new_value)
            return True

    def _seedRandom(self):
        print("Grid::seedRandom\n")

        is_valid = False
        attempts = 0

        while (attempts < 1000 and not is_valid):
            attempts += 1
            self._resetGridMatrix()
            for coords in Grid.population_pattern_order:
                x = coords[0]
                y = coords[1]
                is_valid = self._seedSubGrid(x, y)
                if not is_valid:
                    break


        print("Final attempts : ", attempts)
        # self._seedSubGrid(1, 2)
        # self._seedSubGrid(2, 1)

        # self._seedSubGrid(0, 0)
        # self._seedSubGrid(1, 1)
        # self._seedSubGrid(2, 2)

        # self._seedSubGrid(0, 2)
        # self._seedSubGrid(2, 0)

        # self._seedSubGrid(0, 1)
        # self._seedSubGrid(1, 0)

        # self._seedSubGrid(1, 2)
        # self._seedSubGrid(2, 1)

        # for y in list(range(0, 3)):
        #     for x in list(range(0, 3)):
        #         exclude = self.getRowUsedValues(y) + self.getColUsedValues(x)
        #         # print("exclude row", y, self.getRowUsedValues(y))
        #         # print("exclude col", x, self.getColUsedValues(x))
        #         new_value = getRandomRangeWithExclusions(exclude)[0]
        #         self.setXYValue(x, y, new_value)
        return self

    def setXYValue(self, x, y, value):
        # print("Grid::setXYValue : ", x, y, value)
        self.grid_matrix[y][x] = value
        # self.debug()
        # aaa
        return self

    def getRowUsedValues(self, row_num):
        values = self.grid_matrix[row_num]
        return getSetNonEmptyUniqueValues(values)

    def getColUsedValues(self, col_num):
        values = []
        for row in self.grid_matrix:
            values.append(row[col_num])
        return getSetNonEmptyUniqueValues(values)

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





grid = Grid()



# assign as new list
numbers = getRandomRangeWithExclusions(3)
numbers2 = getRandomRangeWithExclusions([4, 2])

print("Random numbers  : ", getRandomRangeWithExclusions())
print("Random numbers  : ", numbers)
print("Random numbers2 : ", numbers2)
grid.debug()

# print("done")

