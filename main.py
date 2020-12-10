from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
import sys

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

        self.center()
        self.show()


    def initButtons(self):
        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setCursor(Qt.PointingHandCursor)
        self.startButton.setText("Start Game")
        self.startButton.setGeometry(150, 700, 250, 80)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setCursor(Qt.PointingHandCursor)
        self.exitButton.setText("Quit")
        self.exitButton.setGeometry(500, 700, 250, 80)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
