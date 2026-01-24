from PyQt5.QtWidgets import *
from .sql_widget_design import Ui_Form
from dotenv import find_dotenv, load_dotenv, set_key, get_key
import sqlite3
import pandas as pd

class SqlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.sql_widget = Ui_Form()
        self.sql_widget.setupUi(self)

        self.file = None
        self.sql_widget.tableWidget.setHorizontalHeaderLabels(["vox_idx", "vox_x", "vox_y", "vox_z", "vox_z_cont", "is_new", "cls", "red", "green", "blue", "slo", "asp"])

        # Env load
        self.dotenv_path = find_dotenv()
        load_dotenv(self.dotenv_path)

        #Buttons handlers
        self.sql_widget.pushButton_exit.clicked.connect(lambda : self.close())
        self.sql_widget.pushButton_importData.clicked.connect(lambda : self.Import_Data())
        self.sql_widget.pushButton_addRow.clicked.connect(lambda : self.Add_Row())
        self.sql_widget.pushButton_removeRow.clicked.connect(lambda : self.Remove_Row())
        self.sql_widget.pushButton.clicked.connect(lambda : self.Export_Data())
    
    def Add_Row(self):
        row = self.sql_widget.tableWidget.rowCount()
        self.sql_widget.tableWidget.insertRow(row)
        for i in range(0, 12):
            self.sql_widget.tableWidget.setItem(row, i, QTableWidgetItem(""))

    def Remove_Row(self):
        self.sql_widget.tableWidget.removeRow(self.sql_widget.tableWidget.currentRow())

    def Load_Data(self, file = None):
        if file != None:
            connection = sqlite3.connect(file)
            cur = connection.cursor()
            sqlquery = "select * from vox_lvl40 LIMIT 1000"
            rows = cur.execute(sqlquery)

            index = self.sql_widget.tableWidget.rowCount()
            for row in rows:
                self.sql_widget.tableWidget.insertRow(index)

                self.sql_widget.tableWidget.setItem(index, 0, QTableWidgetItem(row[0]))
                self.sql_widget.tableWidget.setItem(index, 1, QTableWidgetItem(str(row[1])))
                self.sql_widget.tableWidget.setItem(index, 2, QTableWidgetItem(str(row[2])))
                self.sql_widget.tableWidget.setItem(index, 3, QTableWidgetItem(str(row[3])))
                self.sql_widget.tableWidget.setItem(index, 4, QTableWidgetItem(str(row[4])))
                self.sql_widget.tableWidget.setItem(index, 5, QTableWidgetItem(str(row[5])))
                self.sql_widget.tableWidget.setItem(index, 6, QTableWidgetItem(str(row[6])))
                self.sql_widget.tableWidget.setItem(index, 7, QTableWidgetItem(str(row[7])))
                self.sql_widget.tableWidget.setItem(index, 8, QTableWidgetItem(str(row[8])))
                self.sql_widget.tableWidget.setItem(index, 9, QTableWidgetItem(str(row[9])))
                self.sql_widget.tableWidget.setItem(index, 10, QTableWidgetItem(str(row[10])))
                self.sql_widget.tableWidget.setItem(index, 11, QTableWidgetItem(str(row[11])))

                index += 1
    
    def Export_Data(self):
         if self.file != None:
             d = {}
             for i in range(self.sql_widget.tableWidget.columnCount()):
                 l = []
                 for j in range(self.sql_widget.tableWidget.rowCount()):
                     it = self.sql_widget.tableWidget.item(j, i)
                     l.append(it.text() if it is not None else "")
                 h_item = self.sql_widget.tableWidget.horizontalHeaderItem(i)
                 n_column = str(i) if h_item is None else h_item.text()
                 d[n_column] = l

             df = pd.DataFrame(data=d)
             engine = sqlite3.connect(self.file)
             df.to_sql("vox_lvl40", con=engine, if_exists="replace")
        


    def Import_Data(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("SQlite files (*.sqlite)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()

            if len(selected_files) > 0:
                self.Load_Data(selected_files[0])
                self.file = selected_files[0]
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Please Choose a File!")
                msg.setWindowTitle("Choose SQLite file")
                msg.exec_()