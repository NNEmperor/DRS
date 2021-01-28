from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QPainter
import StartGame


class Tournament_class(QWidget):
    def __init__(self, q):
        super().__init__()
        self.initUI()
        self.queue = q

    def initUI(self):
        self.setWindowTitle('Snake game')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(400, 150, 700, 512)

        oImage = QImage("images/zmija.jpg")
        sImage = oImage.scaled((QSize(700, 512)))
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(pallete)

        self.lbl = QLabel(self)
        self.lbl.setText("SNAKE TOURNAMENT")
        self.lbl.setStyleSheet("color:#3B1E08 ; font-size: 50px; font-family: Lucida Handwriting;")
        self.lbl.move(65, 80)

        labelP1 = QLabel('Player 1', self)
        labelP1.setStyleSheet('font-size: 20px;height: 28px;width: 260px;font-family: Lucida Handwriting;')
        labelP1.move(180, 220)

        self.textboxP1 = QLineEdit(self)
        self.textboxP1.move(280, 220)
        self.textboxP1.resize(120, 30)
        self.textboxP1.setStyleSheet('font-size: 20px;height: 28px;width: 260px;background-color:gold;font-family: Lucida Handwriting;')

        labelP2 = QLabel('Player 2', self)
        labelP2.setStyleSheet('font-size: 20px;height: 28px;width: 260px;font-family: Lucida Handwriting;')
        labelP2.move(180, 260)

        self.textboxP2 = QLineEdit(self)
        self.textboxP2.move(280, 260)
        self.textboxP2.resize(120, 30)
        self.textboxP2.setStyleSheet('font-size: 20px;height: 28px;width: 260px;background-color:gold;font-family: Lucida Handwriting;')

        labelP3 = QLabel('Player 3', self)
        labelP3.setStyleSheet('font-size: 20px;height: 28px;width: 260px;font-family: Lucida Handwriting;')
        labelP3.move(180, 300)

        self.textboxP3 = QLineEdit(self)
        self.textboxP3.move(280, 300)
        self.textboxP3.resize(120, 30)
        self.textboxP3.setStyleSheet('font-size: 20px;height: 28px;width: 260px;background-color:gold;font-family: Lucida Handwriting;')

        labelP4 = QLabel('Player 4', self)
        labelP4.setStyleSheet('font-size: 20px;height: 28px;width: 260px;font-family: Lucida Handwriting;')
        labelP4.move(180, 340)

        self.textboxP4 = QLineEdit(self)
        self.textboxP4.move(280, 340)
        self.textboxP4.resize(120, 30)
        self.textboxP4.setStyleSheet('font-size: 20px;height: 28px;width: 260px;background-color:gold;font-family: Lucida Handwriting;')

        #self.textboxP1.setText("A")
        #self.textboxP2.setText("B")
        #self.textboxP3.setText("C")
        #self.textboxP4.setText("D")

        self.button = QPushButton('Start Tournament', self)
        self.button.setToolTip('Click to start tournament!')
        self.button.setStyleSheet(
            'color: gold;background-color:#3B1E08 ;font-size: 20px;height: 28px;width: 260px;'
            'font-family:Lucida Handwriting;border-radius:25px')
        #self.button.move(190, 380)
        self.button.setGeometry(190, 380, 250, 50)
        self.button.clicked.connect(self.tournament)

        self.labelP5 = QLabel('You must enter all fields', self)
        self.labelP5.setStyleSheet('font-size: 20px;height: 28px;width: 260px;color:red')
        self.labelP5.move(190, 440)
        self.labelP5.hide()

        self.labelP = QLabel('Player names must be unique', self)
        self.labelP.setStyleSheet('font-size: 20px;height: 28px;width: 260px;color:red')
        self.labelP.move(190, 460)
        self.labelP.hide()

        self.show()

    def checkstatus(self, text):
        if text == "":
            print("Empty Value Not Allowed")
            return False
        else:
            print(" Your Text : ", text)
            return True

    def check_equal(self, name, list):
        for i in range(3):
            if name == list[i]:
                return True

        return False
        """result = False;
        if len(list) > 0:
            result = all(elem ==  for elem in list)
        if result:
            print("All Elements in List are Equal")
            return True
        else:
            print("All Elements in List are Not Equal")
            return False
        """

    def tournament(self):
        if self.checkstatus(self.textboxP1.text()) and self.checkstatus(self.textboxP2.text()) and self.checkstatus(self.textboxP3.text()) and self.checkstatus(self.textboxP4.text()):
            print("ok")
            self.labelP5.hide()
            p1 = self.textboxP1.text()
            p2 = self.textboxP2.text()
            p3 = self.textboxP3.text()
            p4 = self.textboxP4.text()
            list_usernames = [p1, p2, p3, p4]
            if not self.check_equal(p1, [p2, p3, p4]) and not self.check_equal(p2, [p1, p3, p4]) and not self.check_equal(p3, [p1, p2, p4]) and not self.check_equal(p4, [p1, p2, p3]):
                self.labelP.hide()
                self.close()
                self.Open = StartGame.Window(2, 1, True, list_usernames, self.queue)
                self.Open.show()
            else:
                self.labelP.show()

        else:
            self.labelP5.show()
            self.labelP.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Tournament_class()
    sys.exit(app.exec_())
