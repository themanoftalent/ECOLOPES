# Description: This file is the main file of the project.
#SoftAiyazilim.com



from PyQt5.QtWidgets import *
from home.home import HomePage

if __name__ == "__main__":
    app = QApplication([])
    page = HomePage()
    page.show()
    app.exec_()