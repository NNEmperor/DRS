from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import StartGame


class Snake(QFrame):
    WIDTH = 0
    HEIGHT = 0

    def __init__(self, position, direction, width, height, team):
        self.Position = position

        self.Direction = direction

        self.current_x_head = position[0][0]
        self.current_y_head = position[0][1]

        self.Grow_snake = False

        self.Team = team

        # sirina i visina za pomeranje zmije
        self.WIDTH = width
        self.HEIGHT = height

        self.turns_left = len(self.Position)

    #comment
    def suicide(self):
        for i in range(1, len(self.Position)):
            if self.Position[i] == self.Position[0]:
                return True
        return False

    def move_snake(self):

        # if direction is left change its position
        if self.Direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head

            # if it goes beyond left wall
            if self.Position[0][0] < 0:
                self.current_x_head = self.WIDTH - 1

        # if direction is right change its position
        if self.Direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            # if it goes beyond right wall
            if self.current_x_head == self.WIDTH:
                self.current_x_head = 0

        # if direction is down change its position
        if self.Direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            # if it goes beyond down wall
            if self.current_y_head == self.HEIGHT:
                self.current_y_head = 0

        # if direction is up change its position
        if self.Direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            # if it goes beyond up wall
            if self.current_y_head < 0:
                self.current_y_head = self.HEIGHT

                # changing head position
        head = [self.current_x_head, self.current_y_head]
        # inset head in snake list
        self.Position.insert(0, head)

        # if snake grow is False
        if not self.Grow_snake:
            # pop the last element
            self.Position.pop()
        else:
            # make grow_snake to false
            self.Grow_snake = False
