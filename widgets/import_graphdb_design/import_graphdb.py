from PyQt5.QtWidgets import *
from .import_graphdb_design import Ui_Form
import webbrowser
from dotenv import find_dotenv, load_dotenv, set_key, get_key

class ImportGraphDBWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.import_graphdb_widget = Ui_Form()
        self.import_graphdb_widget.setupUi(self)

        # Env load
        self.dotenv_path = find_dotenv()
        load_dotenv(self.dotenv_path)

        #Buttons handlers
        self.import_graphdb_widget.pushButton_exit.clicked.connect(lambda : self.close())
        self.import_graphdb_widget.pushButton_upload_rdf_file.clicked.connect(self.OpenWebGraphDBImport)

    def OpenWebGraphDBImport(self):
        graphdb_url = get_key(self.dotenv_path, "GRAPHDB_URL")
        if graphdb_url.endswith("/"):
            graphdb_url = graphdb_url[:-1]
        webbrowser.open(f'{graphdb_url}/import')