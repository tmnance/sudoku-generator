#!/usr/bin/python
import random


def is_sequence(arg):
    return (not hasattr(arg, "strip") and
        hasattr(arg, "__getitem__") or
        hasattr(arg, "__iter__"))

def getRandomRangeWithExclusions(exclude_numbers=None):
    # generate a list of 1-9
    numbers = list(range(1, 11))
    if exclude_numbers != None:
        # excluding one or more numbers
        if not is_sequence(exclude_numbers):
            # convert integer to list
            exclude_numbers = [exclude_numbers]
        for exclude_number in exclude_numbers:
            numbers.remove(exclude_number)
    random.shuffle(numbers)
    return numbers


class Grid:
    def __init__(self):
        grid_row = [None] * 9
        self.grid_matrix = [grid_row] * 9

    def debug(self):
        output = "Grid::debug\n"

        header_footer_row = str('').ljust(5)
        for i in list(range(0, 9)):
            header_footer_row += str(i + 1).ljust(5)
        header_footer_row += str('').ljust(5) + "\n"

        output += header_footer_row
        for (i, row) in enumerate(self.grid_matrix):
            output += str(i + 1).ljust(5)
            for (j, col) in enumerate(row):
                output += str(col).ljust(5)
            output += str(i + 1).ljust(5)
            output += "\n"
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

