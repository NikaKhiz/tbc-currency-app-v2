import sys
from PyQt5.QtWidgets import QApplication
from converter import CurrencyConverter


def main():
    app = QApplication(sys.argv)
    
    converter = CurrencyConverter()
    converter.show()
    
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
