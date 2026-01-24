from PyQt5.QtWidgets import *
from .start_asp_design import Ui_Form
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class StartASPWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.start_asp_widget = Ui_Form()
        self.start_asp_widget.setupUi(self)

        # Buttons Click Handle
        self.start_asp_widget.pushButton_exit.clicked.connect(lambda : self.close())
        self.start_asp_widget.pushButton_clean_code.clicked.connect(lambda : self.start_asp_widget.textEdit_code.clear())

        self.start_asp_widget.textEdit_code.setText("""# Use yours or use code below\n\nselect * where {\n\t?s ?p ?o .\n} limit 100""")
        self.start_asp_widget.textEdit_code.setStyleSheet("font-size:18px; color:gray;")