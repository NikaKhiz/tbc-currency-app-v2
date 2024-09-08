from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QMessageBox
from PyQt5 import uic

SUPERUSER = {
    'username': 'admin',
    'password': 'admin'
}

CURRENCIES = {
        'GE': {
            'unit': 1,
            'USD': 0.37,
            'LIRA': 12.64,
            'RUBL': 32.66
            },
        'USD': {
            'unit': 1,
            'GE': 2.69,
            'LIRA': 34,
            'RUBL': 87.87
            },
        'RUBL': {
            'unit': 1,
            'GE': 0.031,
            'LIRA': 0.39,
            'USD': 0.011
            },
        'LIRA': {
            'unit': 1,
            'GE': 0.079,
            'USD': 0.029,
            'RUBL': 2.58,
            },
    }

currencies_list = [*CURRENCIES.keys()]

class CurrencyConverter(QMainWindow):

    def __init__(self):
        super(CurrencyConverter, self).__init__()
        self.initUI()

        # fill up currency boxes and calculate rate
        self.fill_up_currencies()
        self.calculate_current_rate(self.base_currencies_box.currentText(), self.conversion_currencies_box.currentText())


        # initially open login page 
        self.stackedWidget.setCurrentIndex(0)

        # on button click login user
        self.loginButton.clicked.connect(lambda: self.authorize(self.username_label.text(), self.password_label.text()))

        # on button click logout user
        self.logoutButton.clicked.connect(self.logout)

    # load generated ui file by qt designer and center main window 
    def initUI(self):
        uic.loadUi('converter.ui', self)    
        self.center()


    def center(self):
        window_frame = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_frame.moveCenter(screen_center)
        self.move(window_frame.topLeft())

    
    # fill up currencies lists according to provided currency list
    def fill_up_currencies(self):
        self.base_currencies_box.addItems(currencies_list)
        self.conversion_currencies_box.addItems(currencies_list)
        self.conversion_currencies_box.setCurrentIndex(1)


    # calculate rate according to given currencies 
    def calculate_current_rate(self, base_currency, conversion_currency):
        base_currency_value = CURRENCIES[base_currency]['unit']
        if base_currency != conversion_currency:
            conversion_currency_value = CURRENCIES[base_currency][conversion_currency]
        else:
            conversion_currency_value = base_currency_value
            
        rate = conversion_currency_value * base_currency_value
        self.rate_label.setText(f'Rate : {rate}')



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

    # switch from converter page to login
    def logout(self):
        self.username_label.setText('')
        self.password_label.setText('')
        self.stackedWidget.setCurrentIndex(0)
        