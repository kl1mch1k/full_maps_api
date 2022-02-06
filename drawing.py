import os
import sys
import time

import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui_file import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        ## Изображение
        self.setupUi(self)
        self.pixmap = QPixmap()
        self.map_locale = [37.530887, 55.703118]
        self.map_scale = 0.001
        self.map_type = 'map'
        self.comboBox.activated.connect(self.changeLayout)
        self.getImage()
        self.updateScreen()

    def getImage(self):
        params = {'ll': ','.join([str(i) for i in self.map_locale]),
                  'spn': ','.join((str(self.map_scale),str(self.map_scale) )),
                  'l': self.map_type}
        map_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_bytes = QtCore.QByteArray(response.content)
        # self.map_file = "map.png"
        # with open(self.map_file, "wb") as file:
        #     file.write(response.content)

    def keyPressEvent(self, event):
        print(self.map_scale)
        if event.key() == QtCore.Qt.Key_PageUp and self.map_scale * 2 < 90:
            self.map_scale *= 2
        if event.key() == QtCore.Qt.Key_PageDown:
            self.map_scale /= 2
        if event.key() == QtCore.Qt.Key_Up and self.map_locale[1] + self.map_scale < 85:
            self.map_locale[1] += self.map_scale
        if event.key() == QtCore.Qt.Key_Down and self.map_locale[1] - self.map_scale > -85:
            self.map_locale[1] -= self.map_scale
        if event.key() == QtCore.Qt.Key_Left and self.map_locale[0] - self.map_scale > -180 :
            self.map_locale[0] -= self.map_scale
        if event.key() == QtCore.Qt.Key_Right and self.map_locale[0] + self.map_scale < 180:
            self.map_locale[0] += self.map_scale
        self.updateScreen()

    def updateScreen(self):
        self.getImage()
        self.pixmap.loadFromData(self.map_bytes)
        self.image.setPixmap(self.pixmap)

    def changeLayout(self):
        self.map_type = {'Схема':'map', 'Спутник': 'sat', 'Гибрид': 'sat,skl'}[self.comboBox.currentText()]
        self.updateScreen()

    # def closeEvent(self, event):
    #     self.running = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
