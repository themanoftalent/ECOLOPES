from PyQt5.QtWidgets import *
from .home_design import Ui_MainWindow
from widgets.connect_graphdb.connect_graphdb import ConnectGraphDBWidget
from widgets.start_asp.start_asp import StartASPWidget
from widgets.connect_mysql.connect_mysql import MySQLSettingWidget
from widgets.import_graphdb.import_graphdb import ImportGraphDBWidget
from widgets.graphdb_to_mysql.graphdb_to_mysql import GraphDBToMySQL
from widgets.connect_to_rhino.connect_to_rhino import ConnnectToRhino3D
from widgets.start_ga.start_ga import StartGa
from widgets.process_kmeans.process_kmeans import ProcessKmeans
from widgets.sql_widget.sql_widget import SqlWidget
from widgets.start_ecolopes.start_ecolopes import StartEcolopesWidget
from dotenv import load_dotenv, find_dotenv, get_key, set_key

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.home_page = Ui_MainWindow()
        self.home_page.setupUi(self)
        
        # Button handlers
        self.home_page.pushButton_exit.clicked.connect(lambda : self.close())
        self.home_page.pushButton_start_asp.clicked.connect(lambda : StartASPWidget().show())
        self.home_page.action_graphdb.triggered.connect(lambda : ConnectGraphDBWidget().show())
        self.home_page.action_mysql.triggered.connect(lambda : MySQLSettingWidget().show())
        self.home_page.action_rhino3d.triggered.connect(self.Rhino3DSetting)
        self.home_page.pushButton_start_ga.clicked.connect(StartGa)
        self.home_page.pushButton_graphdb.clicked.connect(lambda : ImportGraphDBWidget().show())
        self.home_page.pushButton_graphdb_to_mysql.clicked.connect(GraphDBToMySQL)
        self.home_page.pushButton_connect_to_rhino.clicked.connect(ConnnectToRhino3D)
        self.home_page.pushButton_process_kmeans.clicked.connect(ProcessKmeans)
        self.home_page.pushButton_sql.clicked.connect(lambda : SqlWidget().show())
        self.home_page.pushButton_ecolopes.clicked.connect(lambda : StartEcolopesWidget().show())


    def Rhino3DSetting(self):
        file_dialog = QFileDialog()
        if file_dialog.exec_():
            if len(file_dialog.selectedFiles()) > 0:
                selected_path = file_dialog.selectedFiles()[0]
                if "rhino" in selected_path.lower():
                    dotenv_path = find_dotenv()
                    load_dotenv(dotenv_path)
                    set_key(dotenv_path, "RHINO3D_PATH", selected_path)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Rhino3D path saved successfully")
                    msg.setWindowTitle("Rhino3D Setting")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Choose a correct Rhino3D exe!")
                    msg.setWindowTitle("Rhino3D Setting")
                    msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Choose a file!")
                msg.setWindowTitle("Rhino3D Setting")
                msg.exec_()

    