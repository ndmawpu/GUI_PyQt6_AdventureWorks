from PyQt6.QtWidgets import QApplication, QMainWindow
from controllers.MainWindowEx import MainWindowEx    

def main():
    qApp=QApplication([])
    qmainWindow=QMainWindow()
    window=MainWindowEx()
    window.setupUi(qmainWindow)
    window.show()
    qApp.exec()

if __name__ == "__main__":
    main()