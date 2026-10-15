from PyQt5.QtWidgets import *
from modules import genatic_algorithm

def StartGa():
    try:
        genatic_algorithm.execute()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("GA started successfully!")
        msg.setWindowTitle("Start GA")
        msg.exec_()
    except Exception as ex:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("GA start error!")
        msg.setWindowTitle("Start GA")
        msg.exec_()
        print(ex)