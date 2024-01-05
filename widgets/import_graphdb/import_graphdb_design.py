# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_graphdb.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(692, 289)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_upload_rdf_file = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_upload_rdf_file.setFont(font)
        self.pushButton_upload_rdf_file.setStyleSheet("padding:20px; margin:10px")
        self.pushButton_upload_rdf_file.setObjectName("pushButton_upload_rdf_file")
        self.horizontalLayout.addWidget(self.pushButton_upload_rdf_file)
        self.pushButton_get_rdf_data_from_a_url = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_get_rdf_data_from_a_url.setFont(font)
        self.pushButton_get_rdf_data_from_a_url.setStyleSheet("padding:20px; margin:10px")
        self.pushButton_get_rdf_data_from_a_url.setObjectName("pushButton_get_rdf_data_from_a_url")
        self.horizontalLayout.addWidget(self.pushButton_get_rdf_data_from_a_url)
        self.pushButton_import_rdf_text_snippet = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_import_rdf_text_snippet.setFont(font)
        self.pushButton_import_rdf_text_snippet.setStyleSheet("padding:20px; margin:10px")
        self.pushButton_import_rdf_text_snippet.setObjectName("pushButton_import_rdf_text_snippet")
        self.horizontalLayout.addWidget(self.pushButton_import_rdf_text_snippet)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_exit = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet("margin:10px; padding:10px;")
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.verticalLayout_2.addWidget(self.pushButton_exit)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "GraphDB"))
        self.pushButton_upload_rdf_file.setText(_translate("Form", "Upload RDF File"))
        self.pushButton_get_rdf_data_from_a_url.setText(_translate("Form", "Get RDF Data From a URL"))
        self.pushButton_import_rdf_text_snippet.setText(_translate("Form", "Import RDF Text Snippet"))
        self.pushButton_exit.setText(_translate("Form", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())