# importing libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from tkinter import *
from tkinter import messagebox
import random
import sys
import winsound
import Snake
import time
from threading import Thread
from network import Network
from ast import literal_eval


# creating game window
class Window(QMainWindow):
    def __init__(self, numPlayers, numSnakes):
        super(Window, self).__init__()

        # creating a board object
        self.board = Board(self, numPlayers, numSnakes)

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
        # self.board.start()

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

    NumPlayers = 0
    NumSnakes = 0

    # constructor
    def __init__(self, parent, numPlayers, numSnakes):
        super(Board, self).__init__(parent)

        # creating a timer
        self.timer = QBasicTimer()
        self.reset_timer = True

        self.NumPlayers = numPlayers
        self.NumSnakes = numSnakes
        self.winner = 0
        # snakes
        self.snakes = []
        self.scores = [0, 0, 0, 0]
        # kad se opkoli,za pozicije nove zmije
        self.new_snake = []

        for position_number in range(4):
            self.new_snake.append([[3, 2 + 2 * position_number], [2, 2 + 2 * position_number]])
            self.new_snake.append([[3, 37 - 2 * position_number], [2, 37 - 2 * position_number]])
            self.new_snake.append([[56, 2 + 2 * position_number], [57, 2 + 2 * position_number]])
            self.new_snake.append([[56, 37 - 2 * position_number], [57, 37 - 2 * position_number]])

        self.all_pos = []
        for position_number in range(4):
            self.all_pos.append([3, 2 + 2 * position_number])
            self.all_pos.append([2, 2 + 2 * position_number])
            self.all_pos.append([3, 37 - 2 * position_number])
            self.all_pos.append([2, 37 - 2 * position_number])
            self.all_pos.append([56, 2 + 2 * position_number])
            self.all_pos.append([57, 2 + 2 * position_number])
            self.all_pos.append([56, 37 - 2 * position_number])
            self.all_pos.append([57, 37 - 2 * position_number])

        # set Snakes
        for i in range(numSnakes):
            for j in range(numPlayers):
                if j == 0:
                    self.snakes.append(
                        Snake.Snake([[3, 20 + 2 * i], [2, 20 + 2 * i]], 2, Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS,
                                    j))
                if j == 1:
                    self.snakes.append(
                        Snake.Snake([[3, 17 - 2 * i], [2, 17 - 2 * i]], 2, Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS,
                                    j))
                if j == 2:
                    self.snakes.append(
                        Snake.Snake([[56, 2 + 2 * i], [57, 2 + 2 * i]], 1, Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS,
                                    j))
                if j == 3:
                    self.snakes.append(
                        Snake.Snake([[56, 37 - 2 * i], [57, 37 - 2 * i]], 1, Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS,
                                    j))

        for i in range(numPlayers):
            self.scores[i] = 0

        self.TurnCounter = 0
        self.turns = 0
        self.surpriseOn = False
        self.effectOn = False
        self.surpriseSpot = []
        self.effectSpot = []
        self.surprisePositive = True

        # wall
        self.wall = []
        for i in range(Board.WIDTHINBLOCKS):
            for j in range(Board.HEIGHTINBLOCKS):
                if i == 0 or j == 0:
                    self.wall.append([i, j])
                elif i == Board.WIDTHINBLOCKS - 1 or j == Board.HEIGHTINBLOCKS - 1:
                    self.wall.append([i, j])

        self.intervalTimer = IntervalTimer(5, self.timeout, self.msg2statusbar, self.NumPlayers, self.NumSnakes,
                                           self.snakes, self.scores)
        self.intervalTimer.start()

        # food list
        self.food = []

        # called drop food method
        for i in range((len(self.snakes) / 2).__round__()):
            self.drop_food()

        self.net = Network()
        if int(self.net.id) == 0:
            temp = str(self.food)
            self.net.client.send(str.encode(temp))
        else:
            temp = self.net.client.recv(2048).decode()
            self.food = literal_eval(temp)

        thread = Thread(target=self.process_received_move, args=())
        thread.start()

        # setting focus
        self.setFocusPolicy(Qt.StrongFocus)

        # square width method

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

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

    def colorCurrentSnake(self):
        try:
            curSnake = self.snakes[self.TurnCounter]
        except:
            return
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        if curSnake.Team == 0:
            for pos in curSnake.Position:
                color = QColor(0x3aba3a)
                if curSnake.Position[0][0] == pos[0] and curSnake.Position[0][1] == pos[1]:
                    color = QColor(0x248a49)  # BOJI GLAVU
                self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                 boardtop + pos[1] * self.square_height(), color)
        elif curSnake.Team == 1:
            for pos in curSnake.Position:
                color = QColor(0x829bf5)
                if curSnake.Position[0][0] == pos[0] and curSnake.Position[0][1] == pos[1]:
                    color = QColor(0x1d48e0)  # BOJI GLAVU
                self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                 boardtop + pos[1] * self.square_height(), color)
        elif curSnake.Team == 2:
            for pos in curSnake.Position:
                color = QColor(0xf26183)
                if curSnake.Position[0][0] == pos[0] and curSnake.Position[0][1] == pos[1]:
                    color = QColor(0xd12850)  # BOJI GLAVU
                self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                 boardtop + pos[1] * self.square_height(), color)
        elif curSnake.Team == 3:
            for pos in curSnake.Position:
                color = QColor(0xfeffad)
                if curSnake.Position[0][0] == pos[0] and curSnake.Position[0][1] == pos[1]:
                    color = QColor(0xdadb6e)  # BOJI GLAVU
                self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                 boardtop + pos[1] * self.square_height(), color)

    def paintEvent(self, event):

        # creating painter object
        painter = QPainter(self)

        # getting rectangle
        rect = self.contentsRect()

        # board top
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        # drawing snake
        for snake in self.snakes:
            if snake.Team == 0:
                for pos in snake.Position:
                    color = QColor(0x1a6b1a)
                    if snake.Position[0][0] == pos[0] and snake.Position[0][1] == pos[1]:
                        color = QColor(0x124d27)  # BOJI GLAVU
                    self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                     boardtop + pos[1] * self.square_height(), color)
            if snake.Team == 1:
                for pos in snake.Position:
                    color = QColor(0x3859d1)
                    if snake.Position[0][0] == pos[0] and snake.Position[0][1] == pos[1]:
                        color = QColor(0x0c247a)  # BOJI GLAVU
                    self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                     boardtop + pos[1] * self.square_height(), color)
            if snake.Team == 2:
                for pos in snake.Position:
                    color = QColor(0xc9224a)
                    if snake.Position[0][0] == pos[0] and snake.Position[0][1] == pos[1]:
                        color = QColor(0x990629)  # BOJI GLAVU
                    self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                                     boardtop + pos[1] * self.square_height(), color)
            if snake.Team == 3:
                for pos in snake.Position:
                    color = QColor(0xe8eb63)
                    if snake.Position[0][0] == pos[0] and snake.Position[0][1] == pos[1]:
                        color = QColor(0xc4c702)  # BOJI GLAVU
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

        if self.surpriseOn:
            color = QColor(0xFFA500)
            self.draw_square(painter, rect.left() + self.effectSpot[4][0] * self.square_width(),
                             boardtop + self.effectSpot[4][1] * self.square_height(), color)

        if self.effectOn:
            for a in self.effectSpot:
                #color = QColor(0xFFA500)
                color = QColor(255, 165, 0, 70)
                self.draw_square(painter, rect.left() + a[0] * self.square_width(),
                                 boardtop + a[1] * self.square_height(), color)

        self.colorCurrentSnake()

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
        color = QColor(255, 255, 255)

        # painting rectangle
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

        # key press event

    def process_received_move(self):
        while True:
            received = self.net.client.recv(2048).decode()
            snake = self.snakes[self.TurnCounter]

            temp = received.split(";")
            snake.Direction = int(temp[0])
            print(int(temp[0]))
            cant_move, new_team = self.is_surrounded(snake)  # poziva logiku opkoljivanja
            if cant_move:
                self.snakes.remove(snake)  # brisemo tu zmiju
                print("tim koji je opkolio: " + str(new_team))
                self.add_new_snake(new_team)
            snake.move_snake()
            self.is_food_collision()

            self.food = literal_eval(temp[1])
            self.surprisePositive = literal_eval(temp[2])
            self.effectSpot = literal_eval(temp[3])

            self.death()
            #if len(self.snakes) == 0:
            #    self.game_over()
            if self.oneTeamLeft():
                self.game_over()

    def keyPressEvent(self, event):
        if not self.GAME_OVER:
            snake = self.snakes[self.TurnCounter]
            if snake.Team != int(self.net.id):
                return

            cant_move, new_team = self.is_surrounded(snake)  # poziva logiku opkoljivanja
            if cant_move:
                print("pre klika provereno")
                self.snakes.remove(snake)  # brisemo tu zmiju
                print("tim koji je opkolio: " + str(new_team))
                self.add_new_snake(new_team)

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

                temp = str(snake.Direction) + ";" + str(self.food) + ";" + str(self.surprisePositive) + ";" + str(self.effectSpot)
                self.net.client.send(str.encode(temp))

                self.death()
                #if len(self.snakes) == 0:
                #    self.game_over()
                if self.oneTeamLeft():
                    self.game_over()
                # ----------------------------
                cant_move, new_team = self.is_surrounded(snake)  # poziva logiku opkoljivanja

                if cant_move:
                    self.snakes.remove(snake)  # brisemo tu zmiju
                    print("tim koji je opkolio: " + str(new_team))
                    self.add_new_snake(new_team)

    def add_new_snake(self, new_team):
        # dodavanje nove zmije
        position_of_snakes = []
        print("--------------------")
        for index_snake in range(len(self.snakes)):
            position_of_snakes.append(self.snakes[index_snake].Position)
            print(position_of_snakes)
            print(self.snakes[index_snake].Position)
        print("--------------------")
        print("**************************")
        print(position_of_snakes)
        print("$$$$$$$$$$$$$$$$$")
        print(position_of_snakes[0])
        for i in range(4):
            # for index_snake in range(len(self.snakes)):
            if new_team == 0:
                if [self.new_snake[0][0 + i * 4], self.new_snake[0][1 + i * 4]] not in position_of_snakes[0]:
                    self.snakes.append(
                        Snake.Snake([self.new_snake[0][0 + i * 4], self.new_snake[0][1 + i * 4]], 2,
                                    Board.WIDTHINBLOCKS, Board.HEIGHTINBLOCKS, new_team))
                    break
            if new_team == 1:
                if [self.new_snake[1][0 + i * 4], self.new_snake[1][1 + i * 4]] not in position_of_snakes[0]:
                    self.snakes.append(
                        Snake.Snake([self.new_snake[1][0 + i * 4], self.new_snake[1][1 + i * 4]], 2,
                                    Board.WIDTHINBLOCKS,
                                    Board.HEIGHTINBLOCKS, new_team))
                    break
            if new_team == 2:
                if [self.new_snake[2][0 + i * 4], self.new_snake[2][1 + i * 4]] not in position_of_snakes[0]:
                    self.snakes.append(
                        Snake.Snake([self.new_snake[2][0 + i * 4], self.new_snake[2][1 + i * 4]], 1,
                                    Board.WIDTHINBLOCKS,
                                    Board.HEIGHTINBLOCKS, new_team))
                    break
            if new_team == 3:
                if [self.new_snake[3][0 + i * 4], self.new_snake[3][1 + i * 4]] not in position_of_snakes[0]:
                    self.snakes.append(
                        Snake.Snake([self.new_snake[3][0 + i * 4], self.new_snake[3][1 + i * 4]], 1,
                                    Board.WIDTHINBLOCKS,
                                    Board.HEIGHTINBLOCKS, new_team))
                    break
        # snanew_snake_team = -1
        # u_teams.clear()  # cisti se lista timova, da ne bi posle doslo do zbrke

    def is_surrounded(self, snake):

        # izdvajanje zmija iz drugih timova
        other_teams = []

        # kom ce timu pripadati , koji su opkolili
        u_teams = []

        for s in self.snakes:
            if s.Team != snake.Team:
                other_teams.append(s)

        first_pos = False
        second_pos = False
        third_pos = False

        if snake.Direction == 2:
            #   print("udje DESNO" + str(snake.Team))
            potencijalno1 = snake.Position[0][0] + 1  # x koor +1 PRAVO
            potencijalno2 = snake.Position[0][1] + 1  # y koor dole
            potencijalno3 = snake.Position[0][1] - 1  # y koor gore
            """
            print("poz curr" + str(snake.Position[0][0]) + " po1: " + str(potencijalno1))
            print("poz curr" + str(snake.Position[0][1]) + " po2: " + str(potencijalno2))
            print("poz curr" + str(snake.Position[0][1]) + " po3: " + str(potencijalno3))
            print("--------------------------------------")
            """

            for index_snake in range(len(other_teams)):
                if [potencijalno1, snake.Position[0][1]] in other_teams[index_snake].Position:
                    first_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("1 poz")
                if [snake.Position[0][0], potencijalno2] in other_teams[index_snake].Position:
                    second_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("2 poz")
                if [snake.Position[0][0], potencijalno3] in other_teams[index_snake].Position:
                    third_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("3 poz")

            # levo kad gleda
        if snake.Direction == 1:
            potencijalno1 = snake.Position[0][0] - 1  # x koor -1 PRAVO
            potencijalno2 = snake.Position[0][1] + 1  # y koor dole
            potencijalno3 = snake.Position[0][1] - 1  # y koor gore

            """
            print("LEVO")
            print("poz curr" + str(snake.Position[0][0]) + " po1: " + str(potencijalno1))
            print("poz curr" + str(snake.Position[0][1]) + " po2: " + str(potencijalno2))
            print("poz curr" + str(snake.Position[0][1]) + " po3: " + str(potencijalno3))
            """

            for index_snake in range(len(other_teams)):
                if [potencijalno1, snake.Position[0][1]] in other_teams[index_snake].Position:
                    first_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("1 poz")
                if [snake.Position[0][0], potencijalno2] in other_teams[index_snake].Position:
                    second_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("2 poz")
                if [snake.Position[0][0], potencijalno3] in other_teams[index_snake].Position:
                    third_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("3 poz")

            # gore
        if snake.Direction == 4:
            potencijalno1 = snake.Position[0][0] + 1  # x koor +1 PRAVO
            potencijalno2 = snake.Position[0][0] - 1  # x koor -1 PRAVO
            potencijalno3 = snake.Position[0][1] - 1  # y koor dole         MOZDA -
            # potencijalno3 = snake.Position[0][1] - 1  # y koor gore

            """
            print("GORE")
            print("poz curr" + str(snake.Position[0][0]) + " po1: " + str(potencijalno1))
            print("poz curr" + str(snake.Position[0][0]) + " po2: " + str(potencijalno2))
            print("poz curr" + str(snake.Position[0][1]) + " po3: " + str(potencijalno3))

            """
            for index_snake in range(len(other_teams)):
                if [potencijalno1, snake.Position[0][1]] in other_teams[index_snake].Position:
                    first_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("1 poz")
                if [potencijalno2, snake.Position[0][1]] in other_teams[index_snake].Position:
                    second_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("2 poz")
                if [snake.Position[0][0], potencijalno3] in other_teams[index_snake].Position:
                    third_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("3 poz")

            # DOLE
        if snake.Direction == 3:
            potencijalno1 = snake.Position[0][0] + 1  # x koor +1 PRAVO
            potencijalno2 = snake.Position[0][0] - 1  # x koor -1 PRAVO
            potencijalno3 = snake.Position[0][1] + 1  # y koor dole
            # potencijalno3 = snake.Position[0][1] - 1  # y koor gore
            """
            print("DOLE")
            print("poz curr" + str(snake.Position[0][0]) + " po1: " + str(potencijalno1))
            print("poz curr" + str(snake.Position[0][0]) + " po2: " + str(potencijalno2))
            print("poz curr" + str(snake.Position[0][1]) + " po3: " + str(potencijalno3))
"""

            for index_snake in range(len(other_teams)):
                if [potencijalno1, snake.Position[0][1]] in other_teams[index_snake].Position:
                    first_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("1 poz")
                if [potencijalno2, snake.Position[0][1]] in other_teams[index_snake].Position:
                    second_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("2 poz")
                if [snake.Position[0][0], potencijalno3] in other_teams[index_snake].Position:
                    third_pos = True
                    u_teams.append(other_teams[index_snake].Team)
                    print("3 poz")

        cant_move = False
        new_team = -1

        # nakon nekog ifa koji god direction da je bio provera
        if first_pos and second_pos and third_pos:
            # self.snakes.remove(snake)  # brisemo tu zmiju
            # jeste opkoljena
            cant_move = True
            new_team = max(set(u_teams), key=u_teams.count)
            print("OPKOLJEN")

        u_teams.clear()  # cisti se lista timova, da ne bi posle doslo do zbrke
        return cant_move, new_team

    def createEndGameWindow(self):
        master = Tk()
        master.withdraw()

        pop = Toplevel(master)
        pop.title("GAME OVER")
        pop.geometry("450x250")
        pop.config(bg="#3B1E08")
        pop_label = Label(pop, text="You lost", bg="#3B1E08", fg="gold",
                          font=("Lucida Handwriting", 40))
        pop_label.pack(pady=20)

        # frame = Frame(pop, bg="#3B1E08")
        # frame.pack(pady=5)
        # dead = PhotoImage(Image.open(file="images/dead-snake.jpg"))
        # pic = Label(frame, image=dead, borderwidth=0)

        pop.mainloop()

    def death(self):
        self.count = 0
        snake = self.snakes[self.TurnCounter]
        if snake.suicide():
            if self.TurnCounter + 1 == len(self.snakes):
                self.TurnCounter = 0
            self.snakes.remove(snake)
            self.update()
            filename = 'sounds/mixkit-falling-game-over-1942.wav'
            winsound.PlaySound(filename, winsound.SND_ASYNC)
            self.update()
            self.intervalTimer.reset = True

            if not self.oneTeamLeft():
                if int(self.net.id) == snake.Team:
                    for ssnake in self.snakes:
                        if ssnake.Team == snake.Team:
                            self.count += 1
                    if self.count == 0:
                        self.createEndGameWindow()

            return
        for i in self.wall:
            # if collision found
            if i == snake.Position[0]:
                if self.TurnCounter + 1 == len(self.snakes):
                    self.TurnCounter = 0
                self.snakes.remove(snake)
                self.update()
                filename = 'sounds/mixkit-falling-game-over-1942.wav'
                winsound.PlaySound(filename, winsound.SND_ASYNC)
                self.update()
                self.intervalTimer.reset = True

                if not self.oneTeamLeft():
                    if int(self.net.id) == snake.Team:
                        for ssnake in self.snakes:
                            if ssnake.Team == snake.Team:
                                self.count += 1
                        if self.count == 0:
                            self.createEndGameWindow()

                return
        # provera da li je zmija udarila u drugu zmiju
        for s in self.snakes:
            if s.Team != snake.Team:
                for i in s.Position:
                    if i == snake.Position[0]:
                        if self.TurnCounter + 1 == len(self.snakes):
                            self.TurnCounter = 0
                        self.snakes.remove(snake)
                        self.update()
                        filename = 'sounds/mixkit-falling-game-over-1942.wav'
                        winsound.PlaySound(filename, winsound.SND_ASYNC)
                        self.update()
                        self.intervalTimer.reset = True

                        if not self.oneTeamLeft():
                            if int(self.net.id) == snake.Team:
                                for ssnake in self.snakes:
                                    if ssnake.Team == snake.Team:
                                        self.count += 1
                                if self.count == 0:
                                    self.createEndGameWindow()

                        return

        # ako zmija nije umrla potrebno je promenimo turn counter, ako je izbacena niz se "skupi"
        # tako da je sledeca na redu pod istim indeksom
        snake.turns_left = snake.turns_left - 1
        if snake.turns_left == 0:
            self.TurnCounter = (self.TurnCounter + 1) % len(self.snakes)
            self.turns = self.turns + 1
            if self.turns == 5:
                self.surpriseOn = True
                self.turns = 0
            elif self.turns == 3:
                self.surprisePositive = random.choice([True, False])
                surpriseSpot = [random.randint(3, 57), random.randint(3, 37)]
                self.effectSpot = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.effectSpot.append([surpriseSpot[0] + i, surpriseSpot[1] + j])
            elif self.turns == 1 and self.surpriseOn:
                self.effectOn = True
            elif self.turns == 2 and self.surpriseOn:
                self.surpriseOn = False
                self.effectOn = False
                self.turns = 0
                self.surprise()

            snake.turns_left = len(snake.Position)
            if snake.Grow_snake:
                snake.turns_left = snake.turns_left + 1
        self.update()
        self.intervalTimer.reset = True

    def surprise(self):
        for s in self.snakes:
            for i in s.Position:
                for j in self.effectSpot:
                    if i == j:
                        if self.surprisePositive:
                            s.Grow_snake = True
                            self.scores[s.Team] = self.scores[s.Team] + 1
                        else:
                            self.snakes.remove(s)
                            if self.TurnCounter + 1 == len(self.snakes):
                                self.TurnCounter = 0
                            self.update()
                            return

    # ako istekne 5 sekundi, potez se automatski odigra tako sto se zmija pomeri u trenutnom pravcu
    def timeout(self):
        snake = self.snakes[self.TurnCounter]
        # if snake.Team == self.net.id:
        cant_move, new_team = self.is_surrounded(snake)  # poziva logiku opkoljivanja
        if cant_move:
            self.snakes.remove(snake)  # brisemo tu zmiju
            print("tim koji je opkolio: " + str(new_team))
            self.add_new_snake(new_team)
        snake.move_snake()
        self.is_food_collision()
        # slanje tog poteza, ali mora prvo da se sinhronizuju tajmeri da bi imalo smisla
        # temp = str(snake.Direction)
        # self.net.client.send(temp.encode())
        # temp = str(self.food)
        # self.net.client.send(temp.encode())
        self.death()
        #if len(self.snakes) == 0:
        #    self.game_over()
        if self.oneTeamLeft():
            self.game_over()

    def game_over(self):
        self.GAME_OVER = True
        self.intervalTimer.cancel()
        winner_color = ''
        if self.winner == 0:
            winner_color = 'GREEN'
        elif self.winner == 1:
            winner_color = 'BLUE'
        elif self.winner == 2:
            winner_color = 'RED'
        else:
            winner_color = 'YELLOW'

        message = "Winner is team  " + winner_color
        self.msg2statusbar.emit(str("Game Ended. ") + message)
        self.setStyleSheet("background-color:#800000")
        filename = 'sounds/mixkit-completion-of-a-level-2063.wav'
        winsound.PlaySound(filename, winsound.SND_ASYNC)
        snake = self.snakes[self.TurnCounter]
        if int(self.net.id) != snake.Team:
            self.createEndGameWindow()

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
                self.scores[snake.Team] = self.scores[snake.Team] + 1
            teams_left = []
            # kod za pomeranje kada svaki igrac pomeri barem jednu zmiju
            # for snake in self.snakes:
            #    if snake.Team not in teams_left:
            #        teams_left.append(snake.Team)
            # if (self.TurnCounter + 1) % len(teams_left) == 0:
            #    self.move_food()
            if self.TurnCounter + 1 == len(self.snakes):
                if self.snakes[self.TurnCounter].turns_left == 1:
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
                        if [self.food[i][0], potencijalno] not in self.all_pos:
                            if [self.food[i][0], potencijalno] not in self.wall:
                                self.food[i][1] = potencijalno
            else:
                for j in range(random.randint(1, 3)):
                    potencijalno = (self.food[i][0] + random.choice([-1, 1])) % self.WIDTHINBLOCKS
                    # if ~self.snake.__contains__([potencijalno, self.food[i][1]]):
                    # for snake in self.snakes:
                    na_poziciji = False
                    for index_snake in range(len(self.snakes)):
                        # if [potencijalno, self.food[i][1]] not in self.snakes[index_snake].Position:
                        if [potencijalno, self.food[i][1]] in self.snakes[index_snake].Position:
                            na_poziciji = True
                    if not na_poziciji:
                        if [potencijalno, self.food[i][1]] not in self.all_pos:  # pocetne pozicije
                            if [potencijalno, self.food[i][1]] not in self.wall:
                                self.food[i][0] = potencijalno

    def oneTeamLeft(self):
        if not self.GAME_OVER:
            teams = []
            for s in self.snakes:
                if s.Team not in teams:
                    teams.append(s.Team)

            if len(teams) == 1:
                self.winner = teams[0]
                return True
            else:
                return False


class IntervalTimer(Thread):

    def __init__(self, secs, func, statusbar, numPlayers, numSnakes, snakes, scores):
        super(IntervalTimer, self).__init__(target=func)

        self.__interval = secs
        self.__func = func
        self.__exiting = False
        self.reset = False
        self.counter = 0
        self.statusbar = statusbar
        self.numTeams = numPlayers
        self.snakes = snakes
        self.scores = scores
        self.Message1 = 0
        self.Message2 = 0
        self.Message3 = 0
        self.Message4 = 0

        self.Message = ""

    def run(self):
        while not self.__exiting:
            # time.sleep(self.__interval)
            self.reset = False
            while not self.reset:
                self.check()
                self.statusbar.emit("Time for turn: " + str(self.counter) + "  " + self.Message)
                time.sleep(1)
                self.counter = self.counter + 1
                # povecao sam tajmer da bi imali vremena da popalimo sve apps
                if self.counter == 20:
                    self.__func()
            self.counter = 0

    def cancel(self):
        self.__exiting = True

    def check(self):

        if self.numTeams == 2:
            self.Message = "teams GREEN : " + str(self.scores[0]) + " BLUE : " + str(self.scores[1])
        elif self.numTeams == 3:
            self.Message = "teams GREEN : " + str(self.scores[0]) + " BLUE : " + str(self.scores[1]) + " RED :" + str(
                self.scores[2])
        elif self.numTeams == 4:
            self.Message = "teams GREEN : " + str(self.scores[0]) + " BLUE : " + str(self.scores[1]) + " RED : " + str(
                self.scores[2]) + " YELLOW : " + str(self.scores[3])

