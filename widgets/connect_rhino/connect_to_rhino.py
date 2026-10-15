import os, sys, subprocess
from dotenv import load_dotenv, find_dotenv, get_key, set_key
from PyQt5.QtWidgets import *

def ConnnectToRhino3D():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    rhino_3d_path = get_key(dotenv_path, "RHINO3D_PATH")
    if len(rhino_3d_path) > 0:
        try:
            if os.name == "nt":
                os.startfile(rhino_3d_path)
                print("start")
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, rhino_3d_path])

        except Exception as ex:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Rhino3D path incorrect!")
            msg.setWindowTitle("Connect to Rhino3D")
            msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Rhino3D path required")
        msg.setWindowTitle("Connect to Rhino3D")
        msg.exec_()
