from PyQt5.QtWidgets import *
from .start_ecolopes_design import Ui_Form
from threading import Thread
import subprocess
import os
import clipboard


class StartEcolopesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.start_ecolopes_widget = Ui_Form()
        self.start_ecolopes_widget.setupUi(self)

        thread = Thread(target= lambda : subprocess.run([os.getcwd() + r"\core\ECLPS_vox_gen_hops\00_run_venv.bat"]), args=(), daemon=False)
        thread.start()

        self.start_ecolopes_widget.pushButton_exit.clicked.connect(lambda : self.close())

        self.start_ecolopes_widget.pushButton.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/gen_random_cubes"))
        self.start_ecolopes_widget.pushButton_2.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_read_rgb"))
        self.start_ecolopes_widget.pushButton_3.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_read_data_layer"))
        self.start_ecolopes_widget.pushButton_4.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_read_meta"))
        self.start_ecolopes_widget.pushButton_5.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_write_geom"))
        self.start_ecolopes_widget.pushButton_6.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_write_datapoint_format_filter"))
        self.start_ecolopes_widget.pushButton_7.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_list_data_layers"))
        self.start_ecolopes_widget.pushButton_8.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_write_datapoint_format"))
        self.start_ecolopes_widget.pushButton_9.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_clean_new"))
        self.start_ecolopes_widget.pushButton_10.clicked.connect(lambda : clipboard.copy("http://127.0.0.1:5478/vox_list"))

    