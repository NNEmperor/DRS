# importing libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import sys
import winsound
import Snake
import time
from threading import Thread


# creating game window
class Window(QMainWindow):
    def __init__(self, num):
        super(Window, self).__init__()

        # creating a board object
        self.board = Board(self, num)

        # creating a status bar to show result
        self.statusbar = self.statusBar()

        # adding border to the status bar
        self.statusbar.setStyleSheet("border : 2px solid black;color:gold;background-color:#800000;font-weight: "
                                     "900;font-family: Lucida Handwriting;")

        # calling showMessage method when signal received by board
        self.board.msg2statusbar[str].connect(self.statusbar.showMessage)

        # adding board as a central widget
        self.setCentralWidget(self.board)

        # setting title to the window
        self.setWindowTitle('Snake game')
        self.setWindowIcon(QIcon("images/snake-icon.jpg"))  # IKONICA

        # setting geometry to the window
        self.setGeometry(100, 100, 600, 400)

        # starting the board object // za sada ne trb
        #self.board.start()

        oImage = QImage("images/grass_template2.jpg")  # POZADINA
        sImage = oImage.scaled((QSize(900, 900)))
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(pallete)
        # ------------------------------

        # showing the main window
        self.show()


# creating a board class
# that inherits QFrame
class Board(QFrame):
    # creating signal object
    msg2statusbar = pyqtSignal(str)

    GAME_OVER = False

    # block width and height
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    # constructor
    def __init__(self, parent, num):
        super(Board, self).__init__(parent)

        # creating a timer
        self.timer = QBasicTimer()
        self.reset_timer = True

        # snakes
        self.snakes = []
        for i in range(num):
            self.snakes.append(Snake.Snake([[2 + 2 * i, 36], [2 + 2 * i, 37]], 4, Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS))

        self.TurnCounter = 0

        # wall
        self.wall = [[0, 0], [0, 1], [0, 2], [0, 3]]
        for i in range(Board.WIDTHINBLOCKS):
            for j in range(Board.HEIGHTINBLOCKS):
                if i == 0 or j == 0:
                    self.wall.append([i, j])
                elif i == Board.WIDTHINBLOCKS - 1 or j == Board.HEIGHTINBLOCKS - 1:
                    self.wall.append([i, j])

        self.intervalTimer = IntervalTimer(5, self.next_turn, self.msg2statusbar)
        self.intervalTimer.start()

        # food list
        self.food = []

        # called drop food method
        self.drop_food()

        # setting focus
        self.setFocusPolicy(Qt.StrongFocus)

        # square width method

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

        # square height

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    # start method
    def start(self):
        # msg for status bar
        # score = current len - 2
        self.msg2statusbar.emit("SCORE: " + str(len(self.snakeTest.Position) - 2))

        # starting timer
        # self.timer.start(Board.SPEED, self)         # DA LI MENJATI???
        # self.timer.start(Board.SPEED, self)         # ZBOG HRANE---BOGINJE
        # self.timer.start(Board., self)         # DA LI MENJATI??? 2

    # paint event

    def paintEvent(self, event):

        # creating painter object
        painter = QPainter(self)

        # getting rectangle
        rect = self.contentsRect()

        # board top
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        # drawing snake
        for snake in self.snakes:
            for pos in snake.Position:
                color = QColor(0x228B22)
                if snake.Position[0][0] == pos[0] and snake.Position[0][1] == pos[1]:
                    color = QColor(0x195e32)  # BOJI GLAVU
                self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                 boardtop + pos[1] * self.square_height(), color)

        # drawing food
        for pos in self.food:
            self.draw_square_food(painter, rect.left() + pos[0] * self.square_width(),
                                  boardtop + pos[1] * self.square_height())

        color = QColor(0xA9A9A9)
        for pos in self.wall:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height(), color)

            # drawing square

    def draw_square(self, painter, x, y, color):
        # color
        # color = QColor(0x228B22)

        # painting rectangle
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

        # key press event
        """ZA HRANU"""

    def draw_square_food(self, painter, x, y):
        # color
        color = QColor(255, 0, 0)

        # painting rectangle
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

        # key press event

    def keyPressEvent(self, event):
        if not self.GAME_OVER:
            snake = self.snakes[self.TurnCounter]
            valid_move = False
            # getting key pressed
            key = event.key()
            # if left key pressed
            if key == Qt.Key_Left:
                # if direction is not right
                if snake.Direction != 2:
                    # set direction to left
                    snake.Direction = 1
                    snake.move_snake()
                    valid_move = True

            # if right key is pressed
            elif key == Qt.Key_Right:
                # if direction is not left
                if snake.Direction != 1:
                    # set direction to right
                    snake.Direction = 2
                    snake.move_snake()
                    valid_move = True

            # if down key is pressed
            elif key == Qt.Key_Down:
                # if direction is not up
                if snake.Direction != 4:
                    # set direction to down
                    snake.Direction = 3
                    snake.move_snake()
                    valid_move = True

            # if up key is pressed
            elif key == Qt.Key_Up:
                # if direction is not down
                if snake.Direction != 3:
                    # set direction to up
                    snake.Direction = 4
                    snake.move_snake()
                    valid_move = True
            # -----------------------------
            # call move snake method
            if valid_move:
                self.is_food_collision()
                self.death()
                if len(self.snakes) == 0:
                    self.game_over()

    # time event method
    def timerEvent(self, event):
        """
        # checking timer id
        if event.timerId() == self.timer.timerId():
            # call move snake method
            self.move_snake()
            # call food collision method
            self.is_food_collision()
            # call is suicide method
            self.is_suicide()
            # update the window
            self.update()
        """

    def death(self):
        snake = self.snakes[self.TurnCounter]
        if snake.suicide():
            self.snakes.remove(snake)
            self.update()
            filename = 'sounds/mixkit-falling-game-over-1942.wav'
            winsound.PlaySound(filename, winsound.SND_ASYNC)
            return
        for i in self.wall:
            # if collision found
            if i == snake.Position[0]:
                self.snakes.remove(snake)
                self.update()
                filename = 'sounds/mixkit-falling-game-over-1942.wav'
                winsound.PlaySound(filename, winsound.SND_ASYNC)
                return
        # ostaje jos provera da li je zmija udarila u drugu zmiju
        # ako zmija nije umrla potrebno je promenimo turn counter, ako je izbacena niz se "skupi"
        # tako da je sledeca na redu pod istim indeksom
        self.next_turn()

    def next_turn(self):
       # self.change_snake_color(0x228B22, self.TurnCounter)
        self.TurnCounter = (self.TurnCounter + 1) % len(self.snakes)
        self.update()
        self.intervalTimer.reset = True
       # self.change_snake_color(0xe342f5, self.TurnCounter)

    def game_over(self):
        self.GAME_OVER = True
        self.msg2statusbar.emit(str("Game Ended"))
        self.setStyleSheet("background-color : black;")
        # self.timer.stop()       #NE KORISTI SE
        self.update()

    def is_food_collision(self):
        snake = self.snakes[self.TurnCounter]
        # traversing the position of the food
        for pos in self.food:
            # if food position is similar of snake position
            if pos == snake.Position[0]:
                # remove the food
                self.food.remove(pos)
                # call drop food method
                self.drop_food()
                # grow the snake
                snake.Grow_snake = True
            self.move_food()

    # method to drop food on screen
    def drop_food(self):
        # creating random co-ordinates
        x = random.randint(3, 58)
        y = random.randint(3, 38)

        # traversing if snake position is not equal to the
        # food position so that food do not drop on snake
        for snake in self.snakes:
            for pos in snake.Position:
                # if position matches
                if pos == [x, y]:
                    # call drop food method again
                    self.drop_food()

        # append food location
        self.food.append([x, y])

    # pomeranje hrane

    def move_food(self):

        # for petlja kad bi bilo vise hrane u nizu--treba dodati u food
        for i in range(len(self.food)):
            # if (random.randint(0,4) == 0):
            if random.choice([True, False]):
                for j in range(random.randint(1, 3)):
                    potencijalno = (self.food[i][1] + random.choice([-1, 1])) % self.HEIGHTINBLOCKS
                    na_poziciji = False
                    for index_snake in range(len(self.snakes)):
                        if [self.food[i][0], potencijalno] in self.snakes[index_snake].Position:
                            na_poziciji = True
                    if not na_poziciji:
                        if [self.food[i][0], potencijalno] not in self.wall:
                            self.food[i][1] = potencijalno
            else:
                for j in range(random.randint(1, 3)):
                    potencijalno = (self.food[i][0] + random.choice([-1, 1])) % self.WIDTHINBLOCKS
                    # if ~self.snake.__contains__([potencijalno, self.food[i][1]]):
                   # for snake in self.snakes:
                    na_poziciji = False
                    for index_snake in range(len(self.snakes)):
                        #if [potencijalno, self.food[i][1]] not in self.snakes[index_snake].Position:
                        if [potencijalno, self.food[i][1]] in self.snakes[index_snake].Position:
                            na_poziciji= True
                    if not na_poziciji:
                        if [potencijalno, self.food[i][1]] not in self.wall:
                            self.food[i][0] = potencijalno


class IntervalTimer(Thread):

    def __init__(self, secs, func, statusbar):
        super(IntervalTimer, self).__init__(target=func)

        self.__interval = secs
        self.__func = func
        self.__exiting = False
        self.reset = False
        self.counter = 0
        self.statusbar = statusbar

    def run(self):
        while not self.__exiting:
            # time.sleep(self.__interval)
            self.reset = False
            while not self.reset:
                self.statusbar.emit(str(self.counter))
                time.sleep(1)
                self.counter = self.counter + 1
                if self.counter == 5:
                    self.__func()
            self.counter = 0

    def cancel(self):
        self.__exiting = True


# main method
if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    sys.exit(app.exec_())
