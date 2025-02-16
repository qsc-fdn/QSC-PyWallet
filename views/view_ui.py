# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI5.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(828, 395)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("views/images/logocircle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inner_window = QtWidgets.QTabWidget(self.centralwidget)
        self.inner_window.setTabBarAutoHide(False)
        self.inner_window.setObjectName("inner_window")
        self.history_tab = QtWidgets.QWidget()
        self.history_tab.setObjectName("history_tab")
        self.transaction_table = QtWidgets.QTableWidget(self.history_tab)
        self.transaction_table.setGeometry(QtCore.QRect(0, 0, 811, 281))
        self.transaction_table.setObjectName("transaction_table")
        self.transaction_table.setColumnCount(3)
        self.transaction_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table.setHorizontalHeaderItem(2, item)
        self.save_history = QtWidgets.QPushButton(self.history_tab)
        self.save_history.setGeometry(QtCore.QRect(0, 280, 811, 21))
        self.save_history.setObjectName("save_history")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./assets/tab_history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inner_window.addTab(self.history_tab, icon1, "")
        self.send_tab = QtWidgets.QWidget()
        self.send_tab.setObjectName("send_tab")
        self.clear_button = QtWidgets.QPushButton(self.send_tab)
        self.clear_button.setGeometry(QtCore.QRect(610, 270, 93, 28))
        self.clear_button.setObjectName("clear_button")
        self.send_button = QtWidgets.QPushButton(self.send_tab)
        self.send_button.setGeometry(QtCore.QRect(710, 270, 93, 28))
        self.send_button.setObjectName("send_button")
        self.sendto_label = QtWidgets.QLabel(self.send_tab)
        self.sendto_label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        self.sendto_label.setObjectName("sendto_label")
        self.description_label = QtWidgets.QLabel(self.send_tab)
        self.description_label.setGeometry(QtCore.QRect(20, 50, 81, 16))
        self.description_label.setObjectName("description_label")
        self.amount_label = QtWidgets.QLabel(self.send_tab)
        self.amount_label.setGeometry(QtCore.QRect(20, 80, 91, 16))
        self.amount_label.setObjectName("amount_label")
        self.send_input = QtWidgets.QLineEdit(self.send_tab)
        self.send_input.setGeometry(QtCore.QRect(120, 20, 671, 22))
        self.send_input.setObjectName("send_input")
        self.description_input = QtWidgets.QLineEdit(self.send_tab)
        self.description_input.setGeometry(QtCore.QRect(120, 50, 671, 22))
        self.description_input.setObjectName("description_input")
        self.amount_input = QtWidgets.QLineEdit(self.send_tab)
        self.amount_input.setGeometry(QtCore.QRect(120, 80, 161, 22))
        self.amount_input.setInputMask("")
        self.amount_input.setText("")
        self.amount_input.setCursorPosition(0)
        self.amount_input.setObjectName("amount_input")
        self.ots_key_index_input = QtWidgets.QLineEdit(self.send_tab)
        self.ots_key_index_input.setGeometry(QtCore.QRect(120, 110, 161, 22))
        self.ots_key_index_input.setInputMask("")
        self.ots_key_index_input.setText("")
        self.ots_key_index_input.setCursorPosition(0)
        self.ots_key_index_input.setObjectName("ots_key_index_input")
        self.ots_key_index_count_label = QtWidgets.QLabel(self.send_tab)
        self.ots_key_index_count_label.setGeometry(QtCore.QRect(10, 110, 101, 20))
        self.ots_key_index_count_label.setObjectName("ots_key_index_count_label")
        self.ots_key_index_label = QtWidgets.QLabel(self.send_tab)
        self.ots_key_index_label.setGeometry(QtCore.QRect(290, 110, 111, 20))
        self.ots_key_index_label.setText("")
        self.ots_key_index_label.setObjectName("ots_key_index_label")
        self.ots_warning_label = QtWidgets.QLabel(self.send_tab)
        self.ots_warning_label.setGeometry(QtCore.QRect(10, 140, 591, 161))
        self.ots_warning_label.setObjectName("ots_warning_label")
        self.line = QtWidgets.QFrame(self.send_tab)
        self.line.setGeometry(QtCore.QRect(10, 130, 781, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalSlider = QtWidgets.QSlider(self.send_tab)
        self.horizontalSlider.setGeometry(QtCore.QRect(290, 80, 160, 16))
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(50)
        self.horizontalSlider.setPageStep(50)
        self.horizontalSlider.setProperty("value", 50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.slider_label = QtWidgets.QLabel(self.send_tab)
        self.slider_label.setGeometry(QtCore.QRect(290, 90, 161, 17))
        self.slider_label.setObjectName("slider_label")
        self.custom_fee = QtWidgets.QRadioButton(self.send_tab)
        self.custom_fee.setGeometry(QtCore.QRect(460, 80, 151, 23))
        self.custom_fee.setObjectName("custom_fee")
        self.fee_edit = QtWidgets.QLineEdit(self.send_tab)
        self.fee_edit.setGeometry(QtCore.QRect(290, 80, 161, 22))
        self.fee_edit.setInputMask("")
        self.fee_edit.setText("")
        self.fee_edit.setCursorPosition(0)
        self.fee_edit.setObjectName("fee_edit")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./assets/tab_send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inner_window.addTab(self.send_tab, icon2, "")
        self.receive_tab = QtWidgets.QWidget()
        self.receive_tab.setObjectName("receive_tab")
        self.public_label_title = QtWidgets.QLabel(self.receive_tab)
        self.public_label_title.setGeometry(QtCore.QRect(330, 20, 161, 16))
        self.public_label_title.setObjectName("public_label_title")
        self.public_label_description = QtWidgets.QLabel(self.receive_tab)
        self.public_label_description.setGeometry(QtCore.QRect(84, 50, 671, 20))
        self.public_label_description.setText("")
        self.public_label_description.setObjectName("public_label_description")
        self.view_recovery_seed_btn = QtWidgets.QPushButton(self.receive_tab)
        self.view_recovery_seed_btn.setGeometry(QtCore.QRect(288, 270, 261, 25))
        self.view_recovery_seed_btn.setObjectName("view_recovery_seed_btn")
        self.qr_image_label = QtWidgets.QLabel(self.receive_tab)
        self.qr_image_label.setGeometry(QtCore.QRect(290, 80, 251, 181))
        self.qr_image_label.setText("")
        self.qr_image_label.setObjectName("qr_image_label")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./assets/tab_receive.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inner_window.addTab(self.receive_tab, icon3, "")
        self.verticalLayout.addWidget(self.inner_window)
        self.balance_label = QtWidgets.QLabel(self.centralwidget)
        self.balance_label.setObjectName("balance_label")
        self.verticalLayout.addWidget(self.balance_label)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 828, 22))
        self.menubar.setObjectName("menubar")
        self.menuWizard = QtWidgets.QMenu(self.menubar)
        self.menuWizard.setObjectName("menuWizard")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        mainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.actionWizard = QtWidgets.QAction(mainWindow)
        self.actionWizard.setObjectName("actionWizard")
        
        self.actionCheck_for_updates = QtWidgets.QAction(mainWindow)
        self.actionCheck_for_updates.setObjectName("actionCheck_for_updates")
        self.actionOfficial_website = QtWidgets.QAction(mainWindow)
        self.actionOfficial_website.setObjectName("actionOfficial_website")
        self.actionDocumentation = QtWidgets.QAction(mainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionQRL_whitepaper = QtWidgets.QAction(mainWindow)
        self.actionQRL_whitepaper.setObjectName("actionQRL_whitepaper")
        self.actionReport_bug = QtWidgets.QAction(mainWindow)
        self.actionReport_bug.setObjectName("actionReport_bug")
        self.actionDonate_to_development = QtWidgets.QAction(mainWindow)
        self.actionDonate_to_development.setObjectName("actionDonate_to_development")
        self.actionPreferences = QtWidgets.QAction(mainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionNetwork = QtWidgets.QAction(mainWindow)
        self.actionNetwork.setObjectName("actionNetwork")
        self.actionPlugins = QtWidgets.QAction(mainWindow)
        self.actionPlugins.setObjectName("actionPlugins")
        self.actionSign_verify_message = QtWidgets.QAction(mainWindow)
        self.actionSign_verify_message.setObjectName("actionSign_verify_message")
        self.actionEncrypt_decrypt_message = QtWidgets.QAction(mainWindow)
        self.actionEncrypt_decrypt_message.setObjectName("actionEncrypt_decrypt_message")
        self.actionPay_to_many = QtWidgets.QAction(mainWindow)
        self.actionPay_to_many.setObjectName("actionPay_to_many")
        self.actionLoad_transaction = QtWidgets.QAction(mainWindow)
        self.actionLoad_transaction.setObjectName("actionLoad_transaction")
        self.actionShow_addresses = QtWidgets.QAction(mainWindow)
        self.actionShow_addresses.setObjectName("actionShow_addresses")
        self.actionShow_coins = QtWidgets.QAction(mainWindow)
        self.actionShow_coins.setObjectName("actionShow_coins")
        self.actionHide_channels = QtWidgets.QAction(mainWindow)
        self.actionHide_channels.setObjectName("actionHide_channels")
        self.actionShow_contacts = QtWidgets.QAction(mainWindow)
        self.actionShow_contacts.setObjectName("actionShow_contacts")
        self.actionInformation = QtWidgets.QAction(mainWindow)
        self.actionInformation.setObjectName("actionInformation")
        self.actionPassword = QtWidgets.QAction(mainWindow)
        self.actionPassword.setObjectName("actionPassword")
        self.actionSeed = QtWidgets.QAction(mainWindow)
        self.actionSeed.setObjectName("actionSeed")
        self.actionPrivate_keys = QtWidgets.QAction(mainWindow)
        self.actionPrivate_keys.setObjectName("actionPrivate_keys")
        self.actionAddresses = QtWidgets.QAction(mainWindow)
        self.actionAddresses.setObjectName("actionAddresses")
        self.actionLabels = QtWidgets.QAction(mainWindow)
        self.actionLabels.setObjectName("actionLabels")
        self.actionHistory = QtWidgets.QAction(mainWindow)
        self.actionHistory.setObjectName("actionHistory")
        self.actionContacts = QtWidgets.QAction(mainWindow)
        self.actionContacts.setObjectName("actionContacts")
        self.actionFind = QtWidgets.QAction(mainWindow)
        self.actionFind.setObjectName("actionFind")
        self.actionRecently_opened = QtWidgets.QAction(mainWindow)
        self.actionRecently_opened.setObjectName("actionRecently_opened")
        self.actionOpen = QtWidgets.QAction(mainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtWidgets.QAction(mainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave_backup = QtWidgets.QAction(mainWindow)
        self.actionSave_backup.setObjectName("actionSave_backup")
        self.actionDelete = QtWidgets.QAction(mainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionQuit = QtWidgets.QAction(mainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionCheck_for_updates)
        self.menuHelp.addAction(self.actionOfficial_website)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionQRL_whitepaper)
        self.menuHelp.addAction(self.actionReport_bug)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionDonate_to_development)

        self.menuWizard.addAction(self.actionWizard)
        self.menubar.addAction(self.menuWizard.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
       
        self.retranslateUi(mainWindow)
        self.inner_window.setCurrentIndex(1)
        self.clear_button.clicked.connect(self.amount_input.clear)
        #self.clear_button.clicked.connect(self.ots_key_index_input.clear)
        self.clear_button.clicked.connect(self.send_input.clear)
        self.clear_button.clicked.connect(self.description_input.clear)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "QSC PyWallet v1.0"))
        item = self.transaction_table.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "Date"))
        item = self.transaction_table.horizontalHeaderItem(2)
        item.setText(_translate("mainWindow", "Description"))
        item = self.transaction_table.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "Amount"))
        self.save_history.setText(_translate("mainWindow", "Save history"))
        self.inner_window.setTabText(self.inner_window.indexOf(self.history_tab), _translate("mainWindow", "History"))
        self.clear_button.setText(_translate("mainWindow", "Clear"))
        self.send_button.setText(_translate("mainWindow", "Send"))
        self.sendto_label.setText(_translate("mainWindow", "Send to"))
        self.description_label.setText(_translate("mainWindow", "Description"))
        self.amount_label.setText(_translate("mainWindow", "Amount/fee"))
        self.send_input.setPlaceholderText(_translate("mainWindow", "QSC address"))
        self.description_input.setPlaceholderText(_translate("mainWindow", "Description"))
        self.amount_input.setPlaceholderText(_translate("mainWindow", "QSC"))
        self.ots_key_index_input.setPlaceholderText(_translate("mainWindow", "OTS Key Index"))
        self.ots_key_index_count_label.setText(_translate("mainWindow", "OTS Key Index"))
        self.ots_warning_label.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">OTS Key Index Warning</span></p><p><span style=\" font-size:9pt; font-style:italic;\">The OTS Key Index shall be less than 1,048,576. </span></p><p><span style=\" font-size:9pt; font-style:italic;\">With your last key you must empty your wallet. Otherwise these funds will be </span><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">lost FOREVER!</span></p></body></html>"))
        self.slider_label.setText(_translate("mainWindow", "low        medium      high"))
        self.custom_fee.setText(_translate("mainWindow", "Enable custom fee"))
        self.fee_edit.setPlaceholderText(_translate("mainWindow", "Fee"))
        self.inner_window.setTabText(self.inner_window.indexOf(self.send_tab), _translate("mainWindow", "Send"))
        self.public_label_title.setText(_translate("mainWindow", "Your Public QSC Address"))
        self.view_recovery_seed_btn.setText(_translate("mainWindow", "View recovery seed"))
        self.inner_window.setTabText(self.inner_window.indexOf(self.receive_tab), _translate("mainWindow", "Receive"))
        self.balance_label.setText(_translate("mainWindow", "Balance: "))
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.menuWizard.setTitle(_translate("mainWindow", "Wizard"))
        self.actionAbout.setText(_translate("mainWindow", "About"))
        self.actionWizard.setText(_translate("mainWindow", "Wizard"))
        self.actionCheck_for_updates.setText(_translate("mainWindow", "Check for updates"))
        self.actionOfficial_website.setText(_translate("mainWindow", "Official website"))
        self.actionDocumentation.setText(_translate("mainWindow", "Documentation"))
        self.actionQRL_whitepaper.setText(_translate("mainWindow", "QSC whitepaper"))
        self.actionReport_bug.setText(_translate("mainWindow", "Report bug"))
        self.actionDonate_to_development.setText(_translate("mainWindow", "Donate"))
        self.actionPreferences.setText(_translate("mainWindow", "Preferences"))
        self.actionNetwork.setText(_translate("mainWindow", "Network"))
        self.actionPlugins.setText(_translate("mainWindow", "Plugins"))
        self.actionSign_verify_message.setText(_translate("mainWindow", "Sign/verify message"))
        self.actionEncrypt_decrypt_message.setText(_translate("mainWindow", "Encrypt/decrypt message"))
        self.actionPay_to_many.setText(_translate("mainWindow", "Pay to many"))
        self.actionLoad_transaction.setText(_translate("mainWindow", "Load transaction"))
        self.actionShow_addresses.setText(_translate("mainWindow", "Show addresses"))
        self.actionShow_coins.setText(_translate("mainWindow", "Show coins"))
        self.actionHide_channels.setText(_translate("mainWindow", "Hide channels"))
        self.actionShow_contacts.setText(_translate("mainWindow", "Show contacts"))
        self.actionInformation.setText(_translate("mainWindow", "Information"))
        self.actionPassword.setText(_translate("mainWindow", "Password"))
        self.actionSeed.setText(_translate("mainWindow", "Seed"))
        self.actionPrivate_keys.setText(_translate("mainWindow", "Private keys"))
        self.actionAddresses.setText(_translate("mainWindow", "Addresses"))
        self.actionLabels.setText(_translate("mainWindow", "Labels"))
        self.actionHistory.setText(_translate("mainWindow", "History"))
        self.actionContacts.setText(_translate("mainWindow", "Contacts"))
        self.actionFind.setText(_translate("mainWindow", "Find"))
        self.actionRecently_opened.setText(_translate("mainWindow", "Recently opened"))
        self.actionOpen.setText(_translate("mainWindow", "Open"))
        self.actionNew.setText(_translate("mainWindow", "New/Restore"))
        self.actionSave_backup.setText(_translate("mainWindow", "Save backup"))
        self.actionDelete.setText(_translate("mainWindow", "Delete"))
        self.actionQuit.setText(_translate("mainWindow", "Quit"))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
