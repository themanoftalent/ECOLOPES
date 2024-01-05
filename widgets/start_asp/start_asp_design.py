# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_asp.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(541, 626)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_code = QtWidgets.QTextEdit(Form)
        self.textEdit_code.setStyleSheet("padding:15px;border: 0;")
        self.textEdit_code.setObjectName("textEdit_code")
        self.verticalLayout.addWidget(self.textEdit_code)
        self.pushButton_clean_code = QtWidgets.QPushButton(Form)
        self.pushButton_clean_code.setStyleSheet("margin-left: 100px;margin-right: 100px;height:30px;margin-bottom:10px;margin-top:50px;")
        self.pushButton_clean_code.setObjectName("pushButton_clean_code")
        self.verticalLayout.addWidget(self.pushButton_clean_code)
        self.pushButton_submit_code = QtWidgets.QPushButton(Form)
        self.pushButton_submit_code.setStyleSheet("margin-left: 100px;margin-right: 100px;height:30px;margin-bottom:10px;")
        self.pushButton_submit_code.setObjectName("pushButton_submit_code")
        self.verticalLayout.addWidget(self.pushButton_submit_code)
        self.pushButton_exit = QtWidgets.QPushButton(Form)
        self.pushButton_exit.setStyleSheet("margin-left: 100px;margin-right: 100px;height:30px;margin-bottom:10px;margin-top:50px;")
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.verticalLayout.addWidget(self.pushButton_exit)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Start ASP"))
        self.pushButton_clean_code.setText(_translate("Form", "Clean Code"))
        self.pushButton_submit_code.setText(_translate("Form", "Submit Code"))
        self.pushButton_exit.setText(_translate("Form", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())