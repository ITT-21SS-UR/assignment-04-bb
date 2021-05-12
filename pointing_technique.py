"""
This Script offers a new pointing technique for pointing in grid like structures.
The script needs a list of possible targets and the ratio of the targets on the screen so 4 by 6 for example.
Given a position, the filter method can then return the target of the list that is closest to the given position.
The script only works with setups where the targets are in a grid like structure so they can be represented as rows and
columns. Additionally The index of the targets in the targets list must represent them being "read" from left to right
and top to bottom.
If these requirements are met, the filter method first calculates the row and column index of targets closest to the
given position. It can then calculate the index of the closest target by combining the row and column index.
"""


class NovelTechnique:

    def __init__(self, targets, current_size):
        self.targets = targets
        self.current_size = current_size

    # checks which target is closest to the current pointer position and returns the closest target
    def filter(self, pointer_pos):
        x_values = [self.targets[i][0] for i in range(0, self.current_size[0], 1)]
        closest_x_index = self.getSmallestDifference(x_values, pointer_pos[0])
        y_values = [self.targets[i][1] for i in range(closest_x_index, len(self.targets), self.current_size[0])]
        closest_y_index = self.getSmallestDifference(y_values, pointer_pos[1])
        closest_target_index = (closest_y_index*self.current_size[0]+closest_x_index)
        return self.targets[closest_target_index]

    # calculates smallest difference from list to value and returns its index
    def getSmallestDifference(self, lst, x):
        abs_differences = [abs(i-x) for i in lst]
        return abs_differences.index(min(abs_differences))
