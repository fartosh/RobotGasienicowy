from socket import *
import threading
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import QMainWindow, QApplication
import sys
import urllib
import cv2
import numpy as np


class Gui(QMainWindow):
    IP_RPI = '192.168.42.1'
    palette = QtGui.QPalette()

    def __init__(self):
        QMainWindow.__init__(self)
        self.klientT = socket(AF_INET, SOCK_STREAM)
        self.klientR = socket(AF_INET, SOCK_STREAM)
        uic.loadUi('gui.ui', self)
        self.polaczPrzycisk.clicked.connect(self.polaczenie)
        self.wyjdzPrzycisk.clicked.connect(self.wyjdz)
        self.cameraView.setPixmap(QtGui.QPixmap("przyklad.jpg"))

    def polaczenie(self):
        self.klientR.connect(('192.168.42.1', 51716))
        print "polaczono R"
        self.klientT.connect(('192.168.42.1', 51717))
        #print "polaczono T"
        #self.klientT.listen(5)
        self.klientOdbior()
        #safety = True

    def klientOdbior(self):
        watek = threading.Thread(target=self.odbieranie)
        watek.start()

    def odbieranie(self):
        stream = urllib.urlopen('http://192.168.42.1:5555/?action=stream')
        print stream
        bytes=''
        while True:
            bytes += stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                print bytes
                print jpg
                #i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                #cv2.imshow('i',i)
                #if cv2.waitKey(1) ==27:
                #    exit(0)
        """while len(self.klientR.recv(32)) != 0:
            data = self.klientR.recv(128)
            wyswietlML = True
            wyswietlMR = True
            wyswietlGR = True
            wyswietlSH = True
            wyswietlAY = True

            if len(data) > 0:
            #   this.Invoke((MethodInvoker)delegate
                silnikL = ""
                silnikR = ""
                sharp = ""
                ground = ""
                yaw = ""

                self.rs232all.clear()
                for i in range(len(data)-8):
                    if data[i] == 'M' and wyswietlML:
                        if data[i+1] == 'L':
                            wyswietlML = False
                            silnikL += data[i + 2]
                            silnikL += data[i + 3]
                            silnikL += data[i + 4]
                            silnikL += data[i + 5]
                            silnikL += data[i + 6]
                            silnikL += data[i + 7]
                            for j in range(len(silnikL)):
                                if silnikL[j] == "X":
                                    silnikL[j] = ""

                self.rs232all.append("Silnik lewy: " + silnikL + '\n')

                for i in range(len(data)-8):
                    if data[i] == 'M' and wyswietlMR:
                        if data[i+1] == 'R':
                            wyswietlMR = False
                            silnikR += data[i + 2]
                            silnikR += data[i + 3]
                            silnikR += data[i + 4]
                            silnikR += data[i + 5]
                            silnikR += data[i + 6]
                            silnikR += data[i + 7]
                            for j in range(len(silnikR)):
                                if silnikR[j] == "X":
                                    silnikR[j] = ""

                self.rs232all.append("Silnik prawy: " + silnikR + '\n')

                for i in range(len(data)-8):
                    if data[i] == 'G' and wyswietlGR:
                        if data[i+1] == 'D':
                            wyswietlGR = False
                            ground += data[i + 2]
                            ground += data[i + 3]
                            ground += data[i + 4]
                            ground += data[i + 5]
                            ground += data[i + 6]
                            ground += data[i + 7]
                            for j in range(len(ground)):
                                if ground[j] == "X":
                                    ground[j] = ""

                self.rs232all.append("Czujnik ziemi: " + ground + '\n')

                for i in range(len(data)-8):
                    if data[i] == 'S' and wyswietlSH:
                        if data[i+1] == 'H':
                            wyswietlSH = False
                            sharp += data[i + 2]
                            sharp += data[i + 3]
                            sharp += data[i + 4]
                            sharp += data[i + 5]
                            sharp += data[i + 6]
                            sharp += data[i + 7]
                            for j in range(len(sharp)):
                                if sharp[j] == "X":
                                    sharp[j] = ""
                            odleglosc_od_sciany = int(sharp)

                self.rs232all.append("Sharp: " + sharp + "cm\n")

                for i in range(len(data)-8):
                    if data[i] == 'A' and wyswietlAY:
                        if data[i+1] == 'Y':
                            wyswietlAY = False
                            yaw += data[i + 2]
                            yaw += data[i + 3]
                            yaw += data[i + 4]
                            yaw += data[i + 5]
                            yaw += data[i + 6]
                            yaw += data[i + 7]
                            for j in range(len(yaw)):
                                if yaw[j] == "X":
                                    yaw[j] = ""

                self.rs232all.append("MinIMU9: " + yaw + " stopni\n")"""

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Up:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
            self.przodLabel.setPalette(self.palette)

        if key == QtCore.Qt.Key_Down:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
            self.tylLabel.setPalette(self.palette)

        if key == QtCore.Qt.Key_Left:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
            self.lewoLabel.setPalette(self.palette)

        if key == QtCore.Qt.Key_Right:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
            self.prawoLabel.setPalette(self.palette)

        if key == QtCore.Qt.Key_Escape:
            #rozlaczanie
            pass

        if key == QtCore.Qt.Key_1:
            pass

    def keyReleaseEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Up:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)
            self.przodLabel.setPalette(self.palette)

        if key == QtCore.Qt.Key_Down:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)
            self.tylLabel.setPalette(self.palette)

        if key == QtCore.Qt.Key_Left:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)
            self.lewoLabel.setPalette(self.palette)

        if key == QtCore.Qt.Key_Right:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)
            self.prawoLabel.setPalette(self.palette)

    def wyjdz(self):
        sys.exit()


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    gui = Gui()
    gui.show()

    sys.exit(qApp.exec_())

