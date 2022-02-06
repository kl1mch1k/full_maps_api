import os
import sys
import time

import requests
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.map_locale = [37.530887, 55.703118]
        self.map_scale = 15
        self.map_type = 'map'
        self.getImage()
        self.initUI()

    def getImage(self):
        params = {'ll': ','.join([str(i) for i in self.map_locale]),
                  'z': str(self.map_scale),
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

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap()
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.update_screen()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp and self.map_scale <= 16:
            self.map_scale += 1
        if event.key() == QtCore.Qt.Key_PageDown and self.map_scale >= 1:
            self.map_scale -= 1
        if event.key() == QtCore.Qt.Key_Up:
            self.map_locale[1] += 1
        if event.key() == QtCore.Qt.Key_Down:
            self.map_locale[1] -= 1
        if event.key() == QtCore.Qt.Key_Left:
            self.map_locale[0] -= 1
        if event.key() == QtCore.Qt.Key_Right:
            self.map_locale[0] += 1
        self.update_screen()

    def update_screen(self):
        self.getImage()
        self.pixmap.loadFromData(self.map_bytes)
        self.image.setPixmap(self.pixmap)

    # def closeEvent(self, event):
    #     self.running = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
