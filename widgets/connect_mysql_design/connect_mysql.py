from PyQt5.QtWidgets import *
from .connect_mysql_design import Ui_Form
import MySQLdb
import os
from dotenv import find_dotenv, load_dotenv, set_key, get_key


class MySQLSettingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mysql_setting_widget = Ui_Form()
        self.mysql_setting_widget.setupUi(self)

        # Widget On Load
        self.OnLoad()

        # Buttons Click Handlers
        self.mysql_setting_widget.pushButton_exit.clicked.connect(lambda : self.close())
        self.mysql_setting_widget.pushButton_try_connection.clicked.connect(self.TryMySQLConnectionUI)
        self.mysql_setting_widget.pushButton_save.clicked.connect(self.SaveMySQLConnection)

    def OnLoad(self):
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)

        server = get_key(dotenv_path, "SERVER")
        database = get_key(dotenv_path, "DATABASE")
        user = get_key(dotenv_path, "USER")
        password = get_key(dotenv_path, "PASSWORD")

        self.mysql_setting_widget.lineEdit_server.setText(server)
        self.mysql_setting_widget.lineEdit_database.setText(database)
        self.mysql_setting_widget.lineEdit_user.setText(user)
        self.mysql_setting_widget.lineEdit_password.setText(password)

    def TryMySQLConnectionUI(self):
        result, error = self.TryMySQLConnection()
        result_label = self.mysql_setting_widget.label_connection_result
      
        if  result == True:
            result_label.setText("Connection Succeed !")
            result_label.setStyleSheet("color:green;font-size:12px;")
        else:
            result_label.setText(f"Connection Error !\n{error}")
            result_label.setStyleSheet("color:red;font-size:12px;")


    def TryMySQLConnection(self):
        server = self.mysql_setting_widget.lineEdit_server.text()
        database = self.mysql_setting_widget.lineEdit_database.text()
        user = self.mysql_setting_widget.lineEdit_user.text()
        password = self.mysql_setting_widget.lineEdit_password.text()

        try:
            db = MySQLdb.connect(
                host=server,
                user=user,
                passwd=password,
                db = database
            )

           
            return True, None
        except MySQLdb.OperationalError as ex:
            return False, ex

    def SaveMySQLConnection(self):
        server = self.mysql_setting_widget.lineEdit_server.text()
        database = self.mysql_setting_widget.lineEdit_database.text()
        user = self.mysql_setting_widget.lineEdit_user.text()
        password = self.mysql_setting_widget.lineEdit_password.text()
        result_label = self.mysql_setting_widget.label_connection_result
        
        try:
            dotenv_path = find_dotenv()
            load_dotenv(dotenv_path)

            set_key(dotenv_path, "SERVER", server)
            set_key(dotenv_path, "DATABASE", database)
            set_key(dotenv_path, "USER", user)
            set_key(dotenv_path, "PASSWORD", password)
            
            result_label.setText("Save Succeed !")
            result_label.setStyleSheet("color:green;font-size:12px;")
        except Exception as ex:
            result_label.setText(f"Save Error !\n{ex}")
            result_label.setStyleSheet("color:red;font-size:12px;")

