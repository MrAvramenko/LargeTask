import os
import sys
import requests

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QMainWindow, QPushButton, QComboBox



class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.scale1 = [0.002, 0.002]
        self.cords1 = [59.934556, 30.324993]
        self.setGeometry(500, 200, 850, 700)
        self.scalepl.clicked.connect(self.sc)
        self.scalemn.clicked.connect(self.sc)
        self.up.clicked.connect(self.cor)
        self.down.clicked.connect(self.cor)

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.cords1[1]},{self.cords1[0]}&spn={self.scale1[0]},{self.scale1[1]}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        os.remove(self.map_file)
    def sc(self):
        if self.sender().text() == '+':
            self.scale1 = [self.scale1[0]*0.1, self.scale1[1]*0.1]
        else:
            self.scale1 = [self.scale1[0]/0.1, self.scale1[1]/0.1]
        self.push()

    def cor(self):
        if self.sender().text() == '^':
            self.cords1 = [self.cords1[0]-self.scale1[0]*0.2, self.cords1[1]]
            self.push()

    def push(self):
        print(self.scale1)
        print(self.cords1)
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image = self.Map
        self.image.resize(581, 401)
        self.image.setPixmap(self.pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
