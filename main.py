from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QComboBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
import sys

import StartGame


class MainWindow(QWidget):
    MainWindowHeight = 900
    MainWindowWidth = 900

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(self.MainWindowHeight, self.MainWindowWidth)
        self.initButtons()
        self.setMaximumHeight(self.MainWindowHeight)
        self.setMaximumWidth(self.MainWindowWidth)
        self.setMinimumHeight(self.MainWindowHeight)
        self.setMinimumWidth(self.MainWindowWidth)
        self.setWindowTitle("Snake Game")
        self.setWindowIcon(QIcon("images/snake-icon.jpg"))

        self.lbl = QLabel(self)
        self.lbl.setText("SNAKE GAME")
        self.lbl.setStyleSheet("color: gold; font-size: 50px; font-family: Lucida Handwriting;")
        self.lbl.move(280, 150)

        oImage = QImage("images/snake-start.png")
        sImage = oImage.scaled((QSize(900, 900)))
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(pallete)

        #za broj igraca
        self.lblNumPlayers = QLabel(self)
        self.lblNumPlayers.setText("Select number of players")
        self.lblNumPlayers.setStyleSheet("color: gold; font-size: 18px; font-family: Lucida Handwriting;")
        self.lblNumPlayers.move(200, 610)

        self.comboPlayers = QComboBox(self)
        self.comboPlayers.setStyleSheet("color: gold; background-color:#3B1E08 ; font-size: 27px; font-family: Lucida Handwriting;")
        #self.comboPlayers.addItem("1")
        self.comboPlayers.addItem("2")
        self.comboPlayers.addItem("3")
        self.comboPlayers.addItem("4")
        self.comboPlayers.move(290, 650)

        #za broj zmija
        self.lblNumPlayers = QLabel(self)
        self.lblNumPlayers.setText("Select number of snakes")
        self.lblNumPlayers.setStyleSheet("color: gold; font-size: 18px; font-family: Lucida Handwriting;")
        self.lblNumPlayers.move(470, 610)

        self.comboSnakes = QComboBox(self)
        self.comboSnakes.setStyleSheet("color: gold; background-color:#3B1E08 ; font-size: 27px; font-family: Lucida Handwriting;")
        self.comboSnakes.addItem("1")
        self.comboSnakes.addItem("2")
        self.comboSnakes.addItem("3")
        self.comboSnakes.addItem("4")
        self.comboSnakes.move(550, 650)

        self.center()
        self.show()

    def initButtons(self):
        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setCursor(Qt.PointingHandCursor)
        self.startButton.setText("Start Game")
        self.startButton.setGeometry(150, 700, 250, 80)
        self.startButton.setStyleSheet(
            "background-color :gold;border:  none;font-family: Lucida Handwriting;font-size: 25px;border-radius:35px")
        self.startButton.clicked.connect(self.closeMainApp_OpenStartApp)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setCursor(Qt.PointingHandCursor)
        self.exitButton.setText("Quit")
        self.exitButton.setGeometry(500, 700, 250, 80)
        self.exitButton.setStyleSheet(
            "background-color :gold;border:  none;font-family: Lucida Handwriting;font-size: 25px;border-radius:35px")

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def closeMainApp_OpenStartApp(self):
        numPlayers = int(self.comboPlayers.currentText())
        numSnakes = int(self.comboSnakes.currentText())
        self.close()
        self.Open = StartGame.Window(numPlayers, numSnakes)
        self.Open.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
