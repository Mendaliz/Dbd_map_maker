import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setAttribute(Qt.WA_StaticContents)
        h = 740
        w = 740

        self.image = QImage(w, h, QImage.Format_RGB32)
        self.path = QPainterPath()
        self.clearImage()

        self.map = [[[j, i, "Констр", 1] for j in range(7)] for i in range(7)]
        self.paint_map()

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def paint_map(self):
        self.clearImage()

        self.map = [[self.paint_square(j, i, "Констр") for j in range(7)] for i in range(7)]

    def paint_square(self, x, y, text):
        self.del_square(x, y)
        x = 30 + x * 100
        y = 30 + y * 100

        qp = QPainter(self.image)
        qp.begin(self)

        my_path = QPainterPath()
        my_path.addRect(QRectF(x, y, 80, 80))

        qp.setBrush(Qt.black)
        qp.setPen(QPen(Qt.red))

        qp.drawPath(my_path)

        font = QFont()
        font.setPointSize(10)
        qp.setFont(font)
        qp.setBrush(Qt.white)
        qp.setPen(QPen(Qt.red))

        qp.drawText(x + 1, y + 1, 78, 78, Qt.AlignCenter, text)

        qp.end()
        self.update()
        return [x, y, text, 1]

    def del_square(self, x, y):
        qp = QPainter(self.image)
        qp.begin(self)

        qp.setBrush(Qt.red)
        qp.setPen(Qt.red)

        xl = 20 + x * 100
        yl = 20 + y * 100

        if self.map[y][x][-1] == 3:
            if self.image.pixelColor(xl + 20, yl - 10).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl + 10, yl - 10, xl + 90, yl - 10)
            if self.image.pixelColor(xl + 20, yl + 110).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl + 10, yl + 110, xl + 90, yl + 110)
            if self.image.pixelColor(xl - 10, yl + 20).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl - 10, yl + 10, xl - 10, yl + 90)
            if self.image.pixelColor(xl + 110, yl + 20).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl + 110, yl + 10, xl + 110, yl + 90)

            if self.image.pixelColor(xl, yl - 10).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl - 10, yl - 10, xl + 10, yl - 10)
            if self.image.pixelColor(xl + 100, yl - 10).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl + 90, yl - 10, xl + 110, yl - 10)
            if self.image.pixelColor(xl, yl + 110).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl - 10, yl + 110, xl + 10, yl + 110)
            if self.image.pixelColor(xl + 100, yl + 110).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl + 90, yl + 110, xl + 110, yl + 110)

            if self.image.pixelColor(xl - 10, yl).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl - 10, yl - 10, xl - 10, yl + 10)
            if self.image.pixelColor(xl + 110, yl).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl + 110, yl - 10, xl + 110, yl + 10)
            if self.image.pixelColor(xl - 10, yl + 100).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl - 10, yl + 90, xl - 10, yl + 110)
            if self.image.pixelColor(xl + 110, yl + 100).getRgb() == (0, 0, 0, 255):
                qp.drawLine(xl + 110, yl + 90, xl + 110, yl + 110)

        qp.setBrush(Qt.white)
        qp.setPen(Qt.white)

        qp.drawRect(xl - 9, yl - 9, 118, 118)

        qp.end()
        self.update()
        self.map[y][x][-1] = 0

    def change_text(self, x, y, text):
        if self.map[y][x][-1] == 0:
            return
        self.map[y][x][2] = text
        x = 30 + x * 100
        y = 30 + y * 100

        qp = QPainter(self.image)
        qp.begin(self)

        qp.setBrush(Qt.black)
        qp.setPen(QPen(Qt.black))

        qp.drawRect(x + 1, y + 1, 78, 78)

        font = QFont()
        font.setPointSize(10)
        qp.setFont(font)
        qp.setBrush(Qt.white)
        qp.setPen(QPen(Qt.red))

        qp.drawText(x + 1, y + 1, 78, 78, Qt.AlignCenter, text)

        qp.end()
        self.update()

    def unite_squares(self, x1, y1, x2, y2):
        x1l = x1
        y1l = y1
        x2l = x2
        y2l = y2

        for i in range(y1, y2 + 1):
            for j in range(x1, x2 + 1):
                self.map[i][j][-1] = 3

        x1 = 30 + x1 * 100
        y1 = 30 + y1 * 100
        x2 = 110 + x2 * 100
        y2 = 110 + y2 * 100

        qp = QPainter(self.image)
        qp.begin(self)

        my_path = QPainterPath()
        my_path.addRect(QRectF(x1, y1, x2 - x1, y2 - y1))

        qp.setBrush(Qt.black)
        qp.setPen(QPen(Qt.red))

        qp.drawPath(my_path)

        font = QFont()
        font.setPointSize(10)
        qp.setFont(font)
        qp.setBrush(Qt.white)
        qp.setPen(QPen(Qt.red))

        for y in range(y1l, y2l + 1):
            for x in range(x1l, x2l + 1):
                qp.drawText(self.map[y][x][0] + 1, self.map[y][x][1] + 1, 78, 78, Qt.AlignCenter, self.map[y][x][2])

        qp.end()
        self.update()

    def unite_add_text(self, x1, y1, x2, y2, text):
        qp = QPainter(self.image)
        qp.begin(self)

        qp.setPen(Qt.black)
        qp.setBrush(Qt.black)

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if self.map[y][x][-1] == 3:
                    qp.drawRect(self.map[y][x][0] + 1, self.map[y][x][1] + 1, 78, 78)

        x1l = 30 + x1 * 100
        y1l = 30 + y1 * 100
        x2l = 110 + x2 * 100
        y2l = 110 + y2 * 100

        font = QFont()
        font.setPointSize((y2l - y1l) // 5)
        qp.setFont(font)
        qp.setBrush(Qt.white)
        qp.setPen(QPen(Qt.white))

        qp.drawText(x1l + 1, y1l + 1, x2l - x1l - 2, y2l - y1l - 2, Qt.AlignCenter, text)

        qp.end()
        self.update()

    def paint_border(self):
        qp = QPainter(self.image)
        qp.begin(self)

        qp.setBrush(Qt.black)

        pen = QPen(Qt.white)
        pen.setWidth(2)
        qp.setPen(pen)

        for y in range(7):
            for x in range(7):
                if self.map[y][x][-1] == 0:
                    if x == 0:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0] - 20,
                                    self.map[y][x][1] + 100)
                    elif self.map[y][x - 1][-1] == 0:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1], self.map[y][x][0] - 20,
                                    self.map[y][x][1] + 80)
                        if y == 0:
                            up = 0
                        else:
                            up = self.map[y - 1][x - 1][-1]
                        if up == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0] - 20,
                                        self.map[y][x][1])
                        if y == 6:
                            down = 0
                        else:
                            down = self.map[y + 1][x - 1][-1]
                        if down == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] + 80, self.map[y][x][0] - 20,
                                        self.map[y][x][1] + 100)
                    if x == 6:
                        qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                    self.map[y][x][1] + 100)
                    elif self.map[y][x + 1][-1] == 0:
                        qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1], self.map[y][x][0] + 100,
                                    self.map[y][x][1] + 80)
                        if y == 0:
                            up = 0
                        else:
                            up = self.map[y - 1][x + 1][-1]
                        if up == 0:
                            qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                        self.map[y][x][1])
                        if y == 6:
                            down = 0
                        else:
                            down = self.map[y + 1][x + 1][-1]
                        if down == 0:
                            qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1] + 80, self.map[y][x][0] + 100,
                                        self.map[y][x][1] + 100)

                    if y == 0:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                    self.map[y][x][1] - 20)
                    elif self.map[y - 1][x][-1] == 0:
                        qp.drawLine(self.map[y][x][0], self.map[y][x][1] - 20, self.map[y][x][0] + 80,
                                    self.map[y][x][1] - 20)
                        if x == 0:
                            leftism = 0
                        else:
                            leftism = self.map[y - 1][x - 1][-1]
                        if leftism == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0],
                                        self.map[y][x][1] - 20)
                        if x == 6:
                            rightism = 0
                        else:
                            rightism = self.map[y - 1][x + 1][-1]
                        if rightism == 0:
                            qp.drawLine(self.map[y][x][0] + 80, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                        self.map[y][x][1] - 20)
                    if y == 6:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] + 100, self.map[y][x][0] + 100,
                                    self.map[y][x][1] + 100)
                    elif self.map[y + 1][x][-1] == 0:
                        qp.drawLine(self.map[y][x][0], self.map[y][x][1] + 100, self.map[y][x][0] + 80,
                                    self.map[y][x][1] + 100)
                        if x == 0:
                            leftism = 0
                        else:
                            leftism = self.map[y + 1][x - 1][-1]
                        if leftism == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] + 100, self.map[y][x][0],
                                        self.map[y][x][1] + 100)
                        if x == 6:
                            rightism = 0
                        else:
                            rightism = self.map[y + 1][x + 1][-1]
                        if rightism == 0:
                            qp.drawLine(self.map[y][x][0] + 80, self.map[y][x][1] + 100, self.map[y][x][0] + 100,
                                        self.map[y][x][1] + 100)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        qp.setPen(pen)

        for y in range(7):
            for x in range(7):
                if self.map[y][x][-1] != 0:
                    if x == 0:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0] - 20,
                                    self.map[y][x][1] + 100)
                    elif self.map[y][x - 1][-1] == 0:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1], self.map[y][x][0] - 20,
                                    self.map[y][x][1] + 80)
                        if y == 0:
                            up = 0
                        else:
                            up = self.map[y - 1][x - 1][-1]
                        if up == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0] - 20,
                                        self.map[y][x][1])
                        if y == 6:
                            down = 0
                        else:
                            down = self.map[y + 1][x - 1][-1]
                        if down == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] + 80, self.map[y][x][0] - 20,
                                        self.map[y][x][1] + 100)
                    if x == 6:
                        qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                    self.map[y][x][1] + 100)
                    elif self.map[y][x + 1][-1] == 0:
                        qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1], self.map[y][x][0] + 100,
                                    self.map[y][x][1] + 80)
                        if y == 0:
                            up = 0
                        else:
                            up = self.map[y - 1][x + 1][-1]
                        if up == 0:
                            qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                        self.map[y][x][1])
                        if y == 6:
                            down = 0
                        else:
                            down = self.map[y + 1][x + 1][-1]
                        if down == 0:
                            qp.drawLine(self.map[y][x][0] + 100, self.map[y][x][1] + 80, self.map[y][x][0] + 100,
                                        self.map[y][x][1] + 100)

                    if y == 0:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                    self.map[y][x][1] - 20)
                    elif self.map[y - 1][x][-1] == 0:
                        qp.drawLine(self.map[y][x][0], self.map[y][x][1] - 20, self.map[y][x][0] + 80,
                                    self.map[y][x][1] - 20)
                        if x == 0:
                            leftism = 0
                        else:
                            leftism = self.map[y - 1][x - 1][-1]
                        if leftism == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] - 20, self.map[y][x][0],
                                        self.map[y][x][1] - 20)
                        if x == 6:
                            rightism = 0
                        else:
                            rightism = self.map[y - 1][x + 1][-1]
                        if rightism == 0:
                            qp.drawLine(self.map[y][x][0] + 80, self.map[y][x][1] - 20, self.map[y][x][0] + 100,
                                        self.map[y][x][1] - 20)
                    if y == 6:
                        qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] + 100, self.map[y][x][0] + 100,
                                    self.map[y][x][1] + 100)
                    elif self.map[y + 1][x][-1] == 0:
                        qp.drawLine(self.map[y][x][0], self.map[y][x][1] + 100, self.map[y][x][0] + 80,
                                    self.map[y][x][1] + 100)
                        if x == 0:
                            leftism = 0
                        else:
                            leftism = self.map[y + 1][x - 1][-1]
                        if leftism == 0:
                            qp.drawLine(self.map[y][x][0] - 20, self.map[y][x][1] + 100, self.map[y][x][0],
                                        self.map[y][x][1] + 100)
                        if x == 6:
                            rightism = 0
                        else:
                            rightism = self.map[y + 1][x + 1][-1]
                        if rightism == 0:
                            qp.drawLine(self.map[y][x][0] + 80, self.map[y][x][1] + 100, self.map[y][x][0] + 100,
                                        self.map[y][x][1] + 100)

        qp.end()
        self.update()

    def saveImage(self, file_name, file_format):
        self.image.save(file_name, file_format)

    def sizeHint(self):
        return QSize(740, 740)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('Dbd_map_maker.ui', self)

        self.pixmap = QPixmap('m_tugnus.png')
        self.image_tugnus = self.tugnus
        self.image_tugnus.resize(100, 100)
        self.image_tugnus.setPixmap(self.pixmap)

        self.drawer = Drawer()
        self.drawer.move(110, 110)
        self.drawer.resize(740, 740)

        self.sq_text.selectAll()
        self.sq_text.setAlignment(Qt.AlignCenter)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.drawer)

        self.add_sq.clicked.connect(self.add_square)
        self.del_sq.clicked.connect(self.del_square)
        self.change_text.clicked.connect(self.change_square_text)

        self.add_sq_mul.clicked.connect(self.add_square_mul)
        self.del_sq_mul.clicked.connect(self.del_square_mul)
        self.change_text_mul.clicked.connect(self.change_square_text_mul)

        self.unite.clicked.connect(self.unite_squares)
        self.unite_add_text.clicked.connect(self.unite_squares_add_text)

        self.border.clicked.connect(self.make_border)

        self.save_map.clicked.connect(self.save_pic)
        self.new_map.clicked.connect(self.create_new)

    def add_square(self):
        x = self.sq_x.value() - 1
        y = self.sq_y.value() - 1
        text = self.sq_text.toPlainText()
        self.drawer.map[y][x] = self.drawer.paint_square(x, y, text)

    def del_square(self):
        x = self.sq_x.value() - 1
        y = self.sq_y.value() - 1
        self.drawer.del_square(x, y)

    def change_square_text(self):
        x = self.sq_x.value() - 1
        y = self.sq_y.value() - 1
        text = self.sq_text.toPlainText()
        self.drawer.change_text(x, y, text)

    def add_square_mul(self):
        x1 = self.from_x.value() - 1
        y1 = self.from_y.value() - 1
        x2 = self.to_x.value() - 1
        y2 = self.to_y.value() - 1
        text = self.mul_text.toPlainText()
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.drawer.map[y][x] = self.drawer.paint_square(x, y, text)

    def del_square_mul(self):
        x1 = self.from_x.value() - 1
        y1 = self.from_y.value() - 1
        x2 = self.to_x.value() - 1
        y2 = self.to_y.value() - 1
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.drawer.del_square(x, y)

    def change_square_text_mul(self):
        x1 = self.from_x.value() - 1
        y1 = self.from_y.value() - 1
        x2 = self.to_x.value() - 1
        y2 = self.to_y.value() - 1
        text = self.mul_text.toPlainText()
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.drawer.change_text(x, y, text)

    def unite_squares(self):
        x1 = self.from_x.value() - 1
        y1 = self.from_y.value() - 1
        x2 = self.to_x.value() - 1
        y2 = self.to_y.value() - 1
        self.drawer.unite_squares(x1, y1, x2, y2)

    def unite_squares_add_text(self):
        x1 = self.from_x.value() - 1
        y1 = self.from_y.value() - 1
        x2 = self.to_x.value() - 1
        y2 = self.to_y.value() - 1
        text = self.mul_text.toPlainText()
        self.drawer.unite_add_text(x1, y1, x2, y2, text)

    def make_border(self):
        self.drawer.paint_border()

    def save_pic(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, file_format = QFileDialog.getSaveFileName(
            self, "Save Image", r"H:\Dbd_map",
            "Картинка (*.png);;Картинка (*.jpg);;Все файлы (*)", options=options
        )
        file_format = file_format[:-1].split("*")[-1]
        self.drawer.saveImage(file_name + file_format, file_format[1:].upper())

    def create_new(self):
        self.drawer.paint_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mapMaker = MyWidget()
    mapMaker.show()
    sys.exit(app.exec_())
