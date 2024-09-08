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

        # on button click clear the currency form values
        self.clearButton.clicked.connect(self.on_click_clear)

        # on button click convert given amount of currency into another and show result
        self.convertButton.clicked.connect(lambda: self.on_click_convert(self.base_currencies_box.currentText(), self.conversion_currencies_box.currentText()))


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
        self.clear_currencies_form()


    # calculate rate according to given currencies 
    def calculate_current_rate(self, base_currency, conversion_currency):
        rate = self.convert_currencies(base_currency, conversion_currency)
        self.rate_label.setText(f'Rate : {rate}')


    def convert_currencies(self, base_currency, conversion_currency):
        base_currency_value = CURRENCIES[base_currency]['unit']
        if base_currency != conversion_currency:
            conversion_currency_value = CURRENCIES[base_currency][conversion_currency]
        else:
            conversion_currency_value = base_currency_value
            
        return conversion_currency_value * base_currency_value


    # on button click convert given currency into another and show resutls
    def on_click_convert(self, base_currency, conversion_currency):
        try:
            amount = self.amount_line.text()
            if not amount:
                self.result_label.setText('Please choose amount for calculation')
                return

            amount = float(amount)
            base_currency = self.base_currencies_box.currentText()
            conversion_currency = self.conversion_currencies_box.currentText()
            conversion_rate = self.convert_currencies(base_currency, conversion_currency)
            converted_amount = amount * conversion_rate
            self.result_label.setText(f'Result : {int(amount)} {base_currency} is {converted_amount:.2f} {conversion_currency}')
        except ValueError:
            self.result_label.setText('Provide valid integer as amount.')


    # on button click return form values to initial state   
    def on_click_clear(self):
        self.clear_currencies_form()
        

    def clear_currencies_form(self):
        self.base_currencies_box.setCurrentIndex(0)
        self.conversion_currencies_box.setCurrentIndex(1)
        self.amount_line.setText('')
        self.calculate_current_rate(self.base_currencies_box.currentText(), self.conversion_currencies_box.currentText())
        self.result_label.setText('')


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
        