from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5 import uic

class CurrencyConverter(QMainWindow):

    def __init__(self):
        super(CurrencyConverter, self).__init__()
        self.initUI()


    def initUI(self):
        uic.loadUi('converter.ui', self)    
        self.center()


    def center(self):
        window_frame = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_frame.moveCenter(screen_center)
        self.move(window_frame.topLeft())

