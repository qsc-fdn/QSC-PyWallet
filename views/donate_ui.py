# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form2(object):
    def setupUi(self, Form2):
        Form2.setObjectName("Form2")
        Form2.resize(400, 300)
        self.label = QtWidgets.QLabel(Form2)
        self.label.setGeometry(QtCore.QRect(10, 10, 241, 61))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form2)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 381, 111))
        self.label_2.setScaledContents(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form2)
        QtCore.QMetaObject.connectSlotsByName(Form2)

    def retranslateUi(self, Form2):
        _translate = QtCore.QCoreApplication.translate
        Form2.setWindowTitle(_translate("Form2", "Form"))
        self.label.setText(_translate("Form2", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">Donation address</span></p></body></html>"))
        self.label_2.setText(_translate("Form2", "<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">q000a00283951e3dc80bfad24da5b6615bea8662d72a3d4f5657e2ad6805b7c0d8b5ff12aa3ae5f</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form2 = QtWidgets.QWidget()
    ui = Ui_Form2()
    ui.setupUi(Form2)
    Form2.show()
    sys.exit(app.exec_())
