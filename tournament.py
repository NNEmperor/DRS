from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QPainter
import StartGame


class Tournament_class(QWidget):
    def __init__(self):
        super().__init__()
        # self.setStyleSheet('background-color: rgb(53, 188, 220)')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Snake game')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(400, 150, 700, 512)
        #self.pipe = main_pipe2

        oImage = QImage("images/zmija.jpg")
        sImage = oImage.scaled((QSize(700, 512)))
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(pallete)

        self.lbl = QLabel(self)
        self.lbl.setText("SNAKE TOURNAMENT")
        self.lbl.setStyleSheet("color: rgb(50, 22, 166); font-size: 50px; font-family: Lucida Handwriting;")
        self.lbl.move(80, 80)

        labelP1 = QLabel('Player 1', self)
        labelP1.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')
        labelP1.move(190, 220)

        self.textboxP1 = QLineEdit(self)
        self.textboxP1.move(280, 220)
        self.textboxP1.resize(120, 30)
        self.textboxP1.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')

        labelP2 = QLabel('Player 2', self)
        labelP2.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')
        labelP2.move(190, 260)

        self.textboxP2 = QLineEdit(self)
        self.textboxP2.move(280, 260)
        self.textboxP2.resize(120, 30)
        self.textboxP2.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')

        labelP3 = QLabel('Player 3', self)
        labelP3.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')
        labelP3.move(190, 300)

        self.textboxP3 = QLineEdit(self)
        self.textboxP3.move(280, 300)
        self.textboxP3.resize(120, 30)
        self.textboxP3.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')

        labelP4 = QLabel('Player 4', self)
        labelP4.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')
        labelP4.move(190, 340)

        self.textboxP4 = QLineEdit(self)
        self.textboxP4.move(280, 340)
        self.textboxP4.resize(120, 30)
        self.textboxP4.setStyleSheet('font-size: 20px;height: 28px;width: 260px;')

        self.button = QPushButton('Start Tournament', self)
        self.button.setToolTip('Click to start tournament!')
        self.button.setStyleSheet(
            'color: black; background-color: rgb(118, 122, 255);font-size: 20px;height: 28px;width: 260px;')
        self.button.move(190, 380)
        self.button.clicked.connect(self.tournament)

        self.show()

   # @pyqtSlot()
    def tournament(self):

        # potrebno poslati ili pozvati unutar StartGame igrice
        list_usernames = [self.textboxP1.text(), self.textboxP2.text(), self.textboxP3.text(), self.textboxP4.text()]
        self.close()
        self.Open = StartGame.Window(2, 1, True, list_usernames)
        self.Open.show()
        #self.pipe.send(list_usernames)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Tournament_class()
    sys.exit(app.exec_())
