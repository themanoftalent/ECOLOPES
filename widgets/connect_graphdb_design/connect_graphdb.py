from PyQt5.QtWidgets import *
from .connect_graphdb_design import Ui_Form
from dotenv import find_dotenv, load_dotenv, set_key, get_key
from graphdb.rdf4j.api.repositories_api import RepositoriesApi
from graphdb.rdf4j.configuration import Configuration
from graphdb.rdf4j.api_client import ApiClient
from graphdb.rdf4j import SparqlApi
from graphdb.mime_types import RDFTypes
import requests

class ConnectGraphDBWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.connect_graphd_widget = Ui_Form()
        self.connect_graphd_widget.setupUi(self)

        # Buttons Handlers
        self.connect_graphd_widget.pushButton_exit.clicked.connect(lambda : self.close())
        self.connect_graphd_widget.pushButton_connect_to_graphdb.clicked.connect(self.ConnectToGraphDB)

    def ConnectToGraphDB(self):
        #url, done = QInputDialog.getText(self, "GraphDB URL", "Enter URL\nExample: http://localhost:7200/repositories/test/statements")
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        dialog = QDialog()
        dialog.setWindowTitle("GraphDB Connection Settings")
        dialog.setMinimumWidth(300)
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        layout.addWidget(QLabel("URL"))
        url = QLineEdit(dialog)
        layout.addWidget(url)
        layout.addWidget(QLabel("Repository"))
        repository = QLineEdit(dialog)
        layout.addWidget(repository)
        ok_button = QPushButton()
        ok_button.setText("Ok")
        ok_button.clicked.connect(lambda : dialog.accept())
        layout.addWidget(ok_button)
        url.setText(get_key(dotenv_path, "GRAPHDB_URL"))
        repository.setText(get_key(dotenv_path, "GRAPHDB_REPOSITORY"))
        dialog.exec_()

        
        is_connected, ex = self.TryConnectionToGraphDB(url=url.text(), repository=repository.text())

        if is_connected:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Connection Succeed!")
            msg.setWindowTitle("Connection Result")
            msg.exec_()

            

            set_key(dotenv_path, "GRAPHDB_URL", url.text())
            set_key(dotenv_path, "GRAPHDB_REPOSITORY", repository.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Connection Error!")
            msg.setWindowTitle("Connection Result")
            msg.exec_()

    def TryConnectionToGraphDB(self, url, repository):
        try:
            conf = Configuration()
            conf.host = url
            api_client = ApiClient(configuration=conf)
            api_client.set_default_header("Content-Type", RDFTypes.TURTLE)
            api = RepositoriesApi(api_client)
            api.get_repository_size(repository)
            return True, None
        except Exception as ex:
            print(ex)
            return False, ex

    def ImportDataToGraphDB(self):     
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)

        GRAPHDB_URL = get_key(dotenv_path, "GRAPHDB_URL")
        GRAPHDB_REPOSITROY = get_key(dotenv_path, "GRAPHDB_REPOSITORY")

        if len(GRAPHDB_URL) > 0 and len(GRAPHDB_REPOSITROY) > 0:
            file_dialog = QFileDialog()
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                
            if len(selected_files) > 0:
                is_connected = self.TryConnectionToGraphDB(GRAPHDB_URL, GRAPHDB_REPOSITROY)
                if is_connected:
                    pass
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Connection Error!")
                    msg.setWindowTitle("Connection Result")
                    msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("GraphDB Connection Required!")
            msg.setWindowTitle("Connection Result")
            msg.exec_()