"""
description
"""

import math

class NovelTechnique:

    def __init__(self, circles, diameter):
        super().__init__
        self.diameter = diameter
        self.distance = diameter + 20
        self.radius = diameter /2
        self.circles = circles
        self.new_pointer_pos = ()

    def filter(self, target_pos, curr_pos):
        middle = (target_pos[0] - self.radius, target_pos[1] - self.radius)
        offset = math.dist(middle, curr_pos)
        print("-----------------")
        print(middle)
        print(curr_pos)
        if offset <= self.distance:
            self.new_pointer = middle
            #print(self.new_pointer)
            print("true")
        else:
            self.new_pointer = curr_pos
            #print(self.new_pointer)
            print("false")
        return self.new_pointer

        
