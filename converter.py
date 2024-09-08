from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QMessageBox
from PyQt5 import uic

SUPERUSER = {
    'username': 'admin',
    'password': 'admin'
}

class CurrencyConverter(QMainWindow):

    def __init__(self):
        super(CurrencyConverter, self).__init__()
        self.initUI()

        # initially open login page 
        self.stackedWidget.setCurrentIndex(0)

        # on button click login user
        self.loginButton.clicked.connect(lambda: self.authorize(self.username_label.text(), self.password_label.text()))


    # load generated ui file by qt designer and center main window 
    def initUI(self):
        uic.loadUi('converter.ui', self)    
        self.center()


    def center(self):
        window_frame = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_frame.moveCenter(screen_center)
        self.move(window_frame.topLeft())


    #  switch from login page to the converter page
    def authorize(self, username, password):
        if username == SUPERUSER['username'] and password == SUPERUSER['password']:
            self.stackedWidget.setCurrentIndex(1)
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Incorrect credentials :(')
            msg.setText('Please provide valid credentials.')
            msg.setIcon(QMessageBox.Warning)

            ex = msg.exec()