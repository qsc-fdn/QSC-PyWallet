import sys
#from os import remove
import csv
import random
from datetime import datetime
#from time import time
#from multiprocessing.dummy import Pool as ThreadPool

#from hashlib import new
#from PIL import Image
import simplejson as json
from google.protobuf import message
import qrcode

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import * 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from views.view_ui import Ui_mainWindow
from views.about_ui import Ui_Form
from views.donate_ui import Ui_Form2

from models.model import *
from models import Slaves
import models.TransferTransaction
from models.utils import update_node_list
from models.GetMiniTransactionsByAddress import TableOutput
from models.aes import AESModel

from pyqrllib.pyqrllib import hstr2bin, SHAKE_128, SHAKE_256, SHA2_256
from pyqrllib.pyqrllib import hstr2bin, XmssFast, QRLDescriptor

from qsc.crypto.xmss import XMSS
#from qrl.crypto.doctest_data import *





####################################################################################################################
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
options = []
qrl_network = []
explorer_network = []
slider_values = []


class MyWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(550, 400)
        self.introPage = IntroPage()
        self.createWallet = CreateWallet()
        self.walletDetails = WalletDetails()
        self.createSeedByMouse = CreateSeedByMouse()
        self.walletDetailsExperimental = WalletDetailsExperimental()
        self.slavesJsonOptions = SlaveJsonOptions()
        self.createSlavesJson = CreateSlavesJson()
        self.openWalletFileSlaves = OpenWalletFileSlaves()
        self.openWalletFile = OpenWalletFile()
        self.restoreWallet = RestoreWallet()
        self.restoreWalletSlaves = RestoreWalletSlaves()
        self.lastPage = LastPage()
        self.mnemonicPage = MnemonicPhrase()
        self.addPage(self.introPage) #0
        self.addPage(self.createWallet) #1
        self.addPage(self.walletDetails) #2
        #self.addPage(self.createSeedByMouse) #3
        self.addPage(self.mnemonicPage) #3
        self.addPage(self.walletDetailsExperimental) #4
        self.addPage(self.openWalletFile) #5
        self.addPage(self.restoreWallet) #6
        self.addPage(self.slavesJsonOptions) #7
        self.addPage(self.createSlavesJson) #8
        self.addPage(self.openWalletFileSlaves) #9
        self.addPage(self.restoreWalletSlaves) #10
        self.addPage(self.lastPage) #11
        
        self.currentIdChanged.connect(self.next_callback)
        self.walletDetails.save_wallet_file.clicked.connect(self.saveFile)
        self.walletDetailsExperimental.save_wallet_file.clicked.connect(self.saveFileExperimental)
        self.openWalletFile.openFileBtn.clicked.connect(self.openFile)
        self.openWalletFileSlaves.openFileBtn.clicked.connect(self.openFileSlaves)
        self.finished.connect(self.onFinished)

        self.last_page_id = 0


    seed_data = []
    data = []

    def next_callback(self, page_id: int):
        if page_id == 2 and self.last_page_id == 1:
            combo_height_short = main.createWallet.combo_height
            combo_hash_short = main.createWallet.combo_hash
            if combo_height_short.currentIndexChanged or combo_hash_short.currentIndexChanged:
                options.clear()
                options.append(combo_height_short.currentIndex())
                options.append(combo_hash_short.currentIndex())
            main.thread = QThread()
            # Step 3: Create a worker object
            main.worker = Worker()
            # Step 4: Move worker to the thread
            main.worker.moveToThread(main.thread)
            # Step 5: Connect signals and slots
            main.thread.started.connect(main.worker.run)
            main.worker.finished.connect(main.thread.quit)
            main.worker.finished.connect(main.worker.deleteLater)
            main.thread.finished.connect(main.thread.deleteLater)
            # Step 6: Start the thread
            main.thread.start()

            main.button(QWizard.NextButton).setEnabled(False)
            main.button(QWizard.BackButton).setEnabled(False)
            main.button(QWizard.CancelButton).setEnabled(False)
            main.worker.update_text.connect(self.evt_set_text)
            main.thread.finished.connect(lambda: main.button(QWizard.NextButton).setEnabled(True))
            main.thread.finished.connect(lambda: main.button(QWizard.BackButton).setEnabled(True))
            main.thread.finished.connect(lambda: main.button(QWizard.CancelButton).setEnabled(True))
            main.thread.finished.connect(main.finishedThread)
        if page_id == 4 and self.last_page_id == 3:
            combo_height_short = self.createSeedByMouse.combo_height
            combo_hash_short = self.createSeedByMouse.combo_hash
            if combo_height_short.currentIndexChanged or combo_hash_short.currentIndexChanged:
                combo_height_options = {0: 8, 1: 10, 2: 12, 3: 14, 4: 16, 5: 18}
                combo_hash_options = {0: SHAKE_128, 1: SHAKE_256, 2: SHA2_256}
            seed_data = [i for i in self.seed_data if int(i) < 255]
            random.shuffle(seed_data)
            new_seed_data = [int(g) for g in seed_data[:48]]
            qaddress, mnemonic, hexseed = Model.getAddressExperimental(combo_height_options[combo_height_short.currentIndex()], combo_hash_options[combo_hash_short.currentIndex()], tuple(new_seed_data[:48]))
            self.walletDetailsExperimental.qaddress.setText(qaddress)
            self.walletDetailsExperimental.mnemonic.setText(mnemonic + "\n" + "\n")
            self.walletDetailsExperimental.hexseed.setText(hexseed)
        if page_id == 8 and self.last_page_id == 9:
            qrl_address = []
            mnemonic = []
            hexseed = []
            qrl_address.append(main.data[0].split(" ")[0])
            mnemonic.append(" ".join(main.data[0].split(" ")[1:-1]))
            hexseed.append(main.data[0].split(" ")[35])
            print(f'-> hexseed: {hexseed[0]}')
            xmss_pk = XMSS.from_extended_seed(hstr2bin(hexseed[0])).pk
            src_xmss = XMSS.from_extended_seed(hstr2bin(hexseed[0]))
            xmss_height = src_xmss.height
            xmss = XMSS.from_height(xmss_height)
            xmss_extended_seed = xmss.extended_seed
            Slaves.slave_tx_generate(xmss_pk, src_xmss, xmss_extended_seed)
        if page_id == 8 and self.last_page_id == 10:
            qrl_address = []
            mnemonic = []
            hexseed = []
            if QWizard.hasVisitedPage(main, 7):
                if main.restoreWalletSlaves.seedline_edit.text()[:6] ==  "absorb":
                    qrl_address.append(Model.recoverAddressMnemonic(main.restoreWalletSlaves.seedline_edit.text()))
                    mnemonic.append(main.restoreWalletSlaves.seedline_edit.text())
                    hexseed.append(Model.recoverHexseedMnemonic(main.restoreWalletSlaves.seedline_edit.text()))
                elif main.restoreWalletSlaves.seedline_edit.text()[:2] ==  "01":
                    qrl_address.append(Model.recoverAddressHexseed(main.restoreWalletSlaves.seedline_edit.text()))
                    mnemonic.append(Model.recoverMnemonicHexseed(main.restoreWalletSlaves.seedline_edit.text()))
                    hexseed.append(main.restoreWalletSlaves.seedline_edit.text())
            
            src_xmss = XMSS.from_extended_seed(hstr2bin(hexseed[0]))
            xmss_pk = src_xmss.pk
            print(f'-> hexseed: {hexseed[0]}')
            xmss_height = src_xmss.height
            xmss = XMSS.from_height(xmss_height)
            xmss_extended_seed = xmss.extended_seed
            Slaves.slave_tx_generate(xmss_pk, src_xmss, xmss_extended_seed)
            if len(qrl_address) == 0:
                qrl_address.append(src_xmss.qaddress)

        if page_id == 6:
            main.button(QWizard.NextButton).setEnabled(False)

        if page_id == 2 and self.last_page_id == 3:
            mnemonic = self.mnemonicPage.passphrase_edit.text()
            if mnemonic:
                print(f'-> mnemoic: {mnemonic}')
                hexseed = Model.getHexSeedMnemonic(mnemonic)
                qadress = Model.recoverAddressMnemonic(mnemonic)
                self.evt_set_text(qadress, mnemonic, hexseed)
        
        print(f'-> page id: {page_id}, last page id: {self.last_page_id}')

        self.last_page_id = page_id
    
    def finishedThread(self):
        print("Wallet generated!")

    def evt_set_text(self, qadress, mnemonic, hexseed):
        main.walletDetails.qaddress.setText(qadress)
        main.walletDetails.mnemonic.setText(mnemonic)
        main.walletDetails.hexseed.setText(hexseed)
        #print(f'-> mnemonic: {mnemonic}')
    
    def saveFile(self):
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory= 'wallet.json',
            filter=file_filter,
            initialFilter='Json file (*.json)')
        dialog = open(dialog_save_file_name[0], "w")
        dialog.write(json.dumps(AESModel.encrypt(self.walletDetails.qaddress.toPlainText() + " " + self.walletDetails.mnemonic.text().rstrip() + " " + self.walletDetails.hexseed.text(), self.createWallet.passwordline_edit.text())))
        dialog.close()

    def saveFileExperimental(self):
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory= 'wallet.json',
            filter=file_filter,
            initialFilter='Json file (*.json)')
        dialog = open(dialog_save_file_name[0], "w")
        dialog.write(json.dumps(AESModel.encrypt(self.walletDetailsExperimental.qaddress.toPlainText() + " " + self.walletDetailsExperimental.mnemonic.text().rstrip() + " " + self.walletDetailsExperimental.hexseed.text(), self.createSeedByMouse.passwordline_edit.text())))
        dialog.close()


    def openFile(self) -> int:
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory= '.json',
                filter=file_filter,
                initialFilter='Json file (*.json)')
        try:
            dialog = open(dialog_save_file_name[0], "r")
            main.data.append(bytes.decode(AESModel.decrypt(json.load(dialog), self.openWalletFile.passwordline_edit.text())))
            dialog.close()
            QMessageBox.about(self, "Success!", "Correct password!")
        except ValueError:
            QMessageBox.warning(self, "Wrong password!", "You have entered the wrong password!")

    def openFileSlaves(self) -> int:
        file_filter = 'Json file (*.json)'
        dialog_save_file_name = QFileDialog.getOpenFileName(
                parent=self,
                caption='Open file',
                directory= '.json',
                filter=file_filter,
                initialFilter='Json file (*.json)')
        try:
            dialog = open(dialog_save_file_name[0], "r")
            main.data.append(bytes.decode(AESModel.decrypt(json.load(dialog), self.openWalletFileSlaves.passwordline_edit.text())))
            dialog.close()
            QMessageBox.about(self, "Success!", "Correct password!")
        except ValueError:
            QMessageBox.warning(self, "Wrong password!", "You have entered the wrong password!")

    def onFinished(self):
        qrl_address = []
        mnemonic = []
        hexseed = []
        if QWizard.hasVisitedPage(main, 2): # walletDetails
            qrl_address.append(main.walletDetails.qaddress.toPlainText())
            mnemonic.append(main.walletDetails.mnemonic.text().rstrip())
            hexseed.append(main.walletDetails.hexseed.text())
            if main.introPage.combo.currentText() == "Mainnet":
                qrl_network.append("Mainnet")
                explorer_network.append("")
            elif main.introPage.combo.currentText() == "Testnet":
                qrl_network.append("Testnet")
                explorer_network.append("testnet-")
        elif QWizard.hasVisitedPage(main, 5): # open wallet
            qrl_address.append(main.data[0].split(" ")[0])
            mnemonic.append(" ".join(main.data[0].split(" ")[1:-1]))
            hexseed.append(main.data[0].split(" ")[35])
            if main.introPage.combo.currentText() == "Mainnet":
                qrl_network.append("Mainnet")
                explorer_network.append("")
            elif main.introPage.combo.currentText() == "Testnet":
                qrl_network.append("Testnet")
                explorer_network.append("testnet-")
        elif QWizard.hasVisitedPage(main, 6): # restore wallet
            if main.restoreWallet.seedline_edit.text()[:6] ==  "absorb":
                qrl_address.append(Model.recoverAddressMnemonic(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(main.restoreWallet.seedline_edit.text())
                hexseed.append(Model.recoverHexseedMnemonic(main.restoreWallet.seedline_edit.text()))
            elif main.restoreWallet.seedline_edit.text()[:2] ==  "01":
                qrl_address.append(Model.recoverAddressHexseed(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(Model.recoverMnemonicHexseed(main.restoreWallet.seedline_edit.text()))
                hexseed.append(main.restoreWallet.seedline_edit.text())
            if main.introPage.combo.currentText() == "Mainnet":
                qrl_network.append("Mainnet")
                explorer_network.append("")
            elif main.introPage.combo.currentText() == "Testnet":
                qrl_network.append("Testnet")
                explorer_network.append("testnet-")
        elif QWizard.hasVisitedPage(main, 3): #createSeedByMouse
            qrl_address.append(main.walletDetailsExperimental.qaddress.toPlainText())
            mnemonic.append(main.walletDetailsExperimental.mnemonic.text().rstrip())
            hexseed.append(main.walletDetailsExperimental.hexseed.text())
            if main.introPage.combo.currentText() == "Mainnet":
                qrl_network.append("Mainnet")
                explorer_network.append("")
            elif main.introPage.combo.currentText() == "Testnet":
                qrl_network.append("Testnet")
                explorer_network.append("testnet-")

        if len(qrl_address) > 0:
            mainWindow.public_label_description.setText(qrl_address[0])
            mainWindow.public_label_description.setTextInteractionFlags(Qt.TextSelectableByMouse)
            img = qrcode.make(qrl_address[0])
            img_saved = img.save("./assets/qr_code.png")
            mainWindow.pixmap = QPixmap('./assets/qr_code.png')
            mainWindow.qr_image_label.setPixmap(mainWindow.pixmap)
            mainWindow.qr_image_label.setScaledContents(True)

            #clean the history
            mainWindow.transaction_table.setRowCount(0)
            #mainWindow.send_button.setEnabled(True)
            mainWindow.inner_window.setEnabled(True)

            recoveryWindow.mnemonic_label_text.setText(mnemonic[0])
            recoveryWindow.hexseed_label_text.setText(hexseed[0])
            rowPosition = mainWindow.transaction_table.rowCount()

            # get Tx histrory
            QApplication.setOverrideCursor(Qt.WaitCursor)
            tx_histories = TableOutput.GetTxHistoryByAddress(qrl_address[0], qrl_network[0])
            print(f'-> Tx histories: {tx_histories}')

            # get OTS index
            signatures = [signature for _, _, _, _, signature in tx_histories]
            #ots_indx = int(Model.getAddressOtsKeyIndex(qrl_address[0], explorer_network[0]))
            ots_indx = Model.getOTSIndex(signatures) #
            #ots_indx = TableOutput.getOTSIndex(qrl_address[0], qrl_network[0]) 
            #print(f'-> OTS index from signature: {ots_indx} =? from node: {ots_indx_from_node}')
            #total_indx = Model.getOTSNumbers(hexseed[0])
            mainWindow.ots_key_index_input.setText(f'{ots_indx}')

            #balance = float(Model.getAddressBalance(qrl_address[0], explorer_network[0])) / 1000000000
            balance = TableOutput.getBalance(qrl_address[0], qrl_network[0]) / 1000000000
            # compute balance from Tx histories
            '''
            print(f'-> total balance: {balance}')
            amounts = [float(amount) for _, _, amount, _, _ in tx_histories]
            fees = [float(fee) for _, _, _, fee, _ in tx_histories]
            print(f'-> amounts: {amounts}, fees: {fees}')
            tx_balance = sum(amounts) - sum(fees)
            #assert balance == tx_balance, 'Balance not equal!'
            '''
            mainWindow.balance_label.setText(f"Balance: {balance} Q") 

            x, y, z = 0, 1, 2
            for _ in range(len(tx_histories)):
                mainWindow.transaction_table.insertRow(rowPosition)
            for addr_from, date, amount, fee, _ in tx_histories:
                date_box = datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d %I:%M:%S")
                mainWindow.transaction_table.setItem(x, 0, QTableWidgetItem(date_box))
                description_box = ''
                mainWindow.transaction_table.setItem(0, y, QTableWidgetItem(amount))
                mainWindow.transaction_table.setItem(0, z, QTableWidgetItem(str(description_box)))
                x += 1
                y += 3
                z += 3
            QApplication.restoreOverrideCursor()

class Worker(QObject):
    finished = pyqtSignal()
    update_text = pyqtSignal(str, str, str)

    def run(self):
        """Long-running task."""
        combo_height_options = {0: 8, 1: 10, 2: 12, 3: 14, 4: 16, 5: 18}
        combo_hash_options = {0: SHAKE_128, 1: SHAKE_256, 2: SHA2_256}
        qaddress, mnemonic, hexseed = Model.getAddress(combo_height_options[options[0]], combo_hash_options[options[1]])
        self.update_text.emit(qaddress, mnemonic, hexseed)
        self.finished.emit()

class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTitle("Welcome to QSC PyWallet v1.0!")

        self.combo = QComboBox(self)
        self.combo.setMaximumWidth(100)
        self.combo.addItem("Mainnet")
        self.combo.addItem("Testnet")

        self.label_description = QLabel("Select option:")
        self.radiobutton_1 = QRadioButton("Create new wallet")
        self.radiobutton_2 = QRadioButton("Open wallet file")
        self.radiobutton_3 = QRadioButton("Restore wallet from seed")
        self.radiobutton_4 = QRadioButton("Restore wallet from mnemonic phrase")
        self.Separador = QFrame()
        self.Separador.Shape(QFrame.HLine)
        self.Separador.setLineWidth(1)
        self.Separador.setFrameShape(QFrame.HLine)

        self.radiobutton_2.setChecked(True)

        #self.radiobutton_4 = QRadioButton("Create a Slaves.json")
        #self.radiobutton_5 = QRadioButton("Create wallet by random mouse movements [Experimental] [Not safe]")
        #self.radiobutton_2.setChecked(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.combo)
        layout.addWidget(self.label_description)
        layout.addWidget(self.radiobutton_1)
        layout.addWidget(self.radiobutton_2)
        layout.addWidget(self.radiobutton_3)
        layout.addWidget(self.radiobutton_4)
        #layout.addWidget(self.Separador)
        #layout.addWidget(self.radiobutton_4)
        #layout.addWidget(self.radiobutton_5)
        

    def nextId(self) -> int:
        if self.radiobutton_1.isChecked():
            return 1
        if self.radiobutton_2.isChecked():
            return 5
        if self.radiobutton_3.isChecked():
            return 6
        if self.radiobutton_4.isChecked():
            return 3

        return 0

class CreateWallet(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Create wallet")

        self.password_label = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit(self)
        self.passwordline_edit.setEchoMode(2)
        self.passwordline_edit.setPlaceholderText("Enter password")

        self.combo_height = QComboBox(self)
        #self.combo_height.addItem("Tree height: 8 | Signatures: 256")
        #self.combo_height.addItem("Tree height: 10 | Signatures: 1,024")
        #self.combo_height.addItem("Tree height: 12 | Signatures: 4,096")
        #self.combo_height.addItem("Tree height: 14 | Signatures: 16,384")
        #self.combo_height.addItem("Tree height: 16 | Signatures: 65,536")
        #self.combo_height.addItem("Tree height: 18 | Signatures: 262,144")
        self.combo_height.addItem("Tree height: 20 | Signatures: 1,048,756")
        self.combo_height.setEnabled(False)

        self.note = QLabel("\nButtons will be automatically disabled while generating wallet.\nThey will be enabled again once finished.")

        self.combo_hash = QComboBox(self)
        #self.combo_hash.addItem("Hash function: SHAKE_128")
        #self.combo_hash.addItem("Hash function: SHAKE_256")
        self.combo_hash.addItem("Hash function: SHA2_256") 
        self.combo_hash.setEnabled(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.combo_height)
        layout.addWidget(self.combo_hash)
        layout.addWidget(self.note)

    def nextId(self) -> int:
        return 2

class MnemonicPhrase(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTitle("Passphrase Input")
        self.WN = 34 # word number
        self.passphrase_label = QtWidgets.QLabel(f"Enter your {self.WN}-word passphrase:")
        self.passphrase_edit = QtWidgets.QLineEdit()
        self.passphrase_edit.textChanged.connect(self.checkCompleteness)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.passphrase_label)
        layout.addWidget(self.passphrase_edit)
        self.setLayout(layout)

    def isComplete(self):
        return len(self.passphrase_edit.text().split()) == self.WN

    def checkCompleteness(self):
        if len(self.passphrase_edit.text().split()) == self.WN:
            self.completeChanged.emit()

    def nextId(self) -> int:
        return 2

class WalletDetails(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Wallet details")

        self.qaddress_description = QLabel("QSC Public address:")
        self.qaddress = QTextEdit()
        self.qaddress.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.mnemonic_description = QLabel("Mnemonic phrase:")
        self.mnemonic = QLabel()
        self.hexseed_description = QLabel("Hexseed:")
        self.hexseed = QLabel()

        self.save_wallet_file = QPushButton('Save secure wallet file')


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.frame = QFrame(self)
        self.qaddress.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.qaddress.setFrameShadow(QFrame.Plain)
        self.qaddress.setLineWidth(1)

        self.mnemonic.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.mnemonic.setFrameShadow(QFrame.Plain)
        self.mnemonic.setLineWidth(1)
        self.mnemonic.setWordWrap(True)

        self.hexseed.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.hexseed.setFrameShadow(QFrame.Plain)
        self.hexseed.setLineWidth(1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.qaddress_description)
        layout.addWidget(self.qaddress)
        layout.addWidget(self.mnemonic_description)
        layout.addWidget(self.mnemonic)
        layout.addWidget(self.hexseed_description)
        layout.addWidget(self.hexseed)
        layout.addWidget(self.save_wallet_file)

    def nextId(self) -> int:
        return 11

class CreateSeedByMouse(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Generate entropy by mouse!")

        self.password_label = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit(self)
        self.passwordline_edit.setEchoMode(2)
        self.passwordline_edit.setPlaceholderText("Enter password")

        self.combo_height = QComboBox(self)
        self.combo_height.addItem("Tree height: 8 | Signatures: 256")
        self.combo_height.addItem("Tree height: 10 | Signatures: 1,024")
        self.combo_height.addItem("Tree height: 12 | Signatures: 4,096")
        self.combo_height.addItem("Tree height: 14 | Signatures: 16,384")
        self.combo_height.addItem("Tree height: 16 | Signatures: 65,536")
        self.combo_height.addItem("Tree height: 18 | Signatures: 262,144")

        self.combo_hash = QComboBox(self)
        self.combo_hash.addItem("Hash function: SHAKE_128")
        self.combo_hash.addItem("Hash function: SHAKE_256")
        self.combo_hash.addItem("Hash function: SHA2_256") 

        self.video_label = QtWidgets.QLabel()
        self.video_label.setStyleSheet("background-color: white; border: 1px solid black")
        self.video_label.setFixedWidth(510)
        self.video_label.setFixedHeight(175)

        tracker = MouseTracker(self.video_label)
        tracker.positionChanged.connect(self.on_positionChanged)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.combo_height)
        layout.addWidget(self.combo_hash)
        layout.addWidget(self.video_label)

        self.label_position = QtWidgets.QLabel(
            self.video_label, alignment=QtCore.Qt.AlignCenter
        )
        self.label_position.setStyleSheet('background-color: white; border: 1px solid black')

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_positionChanged(self, pos):
        delta = QtCore.QPoint(30, -15)
        self.label_position.show()
        self.label_position.move(pos + delta)
        self.label_position.setText("(%d, %d)" % (pos.x(), pos.y()))
        self.label_position.adjustSize()
        main.seed_data.append("%d" % (pos.x()))
        main.seed_data.append("%d" % (pos.y()))
        print(main.seed_data)


    def nextId(self) -> int:
        return 4

class MouseTracker(QtCore.QObject):
    positionChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, o, e):
        if o is self.widget and e.type() == QtCore.QEvent.MouseMove:
            self.positionChanged.emit(e.pos())
        return super().eventFilter(o, e)

class WalletDetailsExperimental(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Wallet details")

        self.qaddress_description = QLabel("QSC Public address:")
        self.qaddress = QTextEdit()
        self.qaddress.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.mnemonic_description = QLabel("Mnemonic phrase:")
        self.mnemonic = QLabel()
        self.hexseed_description = QLabel("Hexseed:")
        self.hexseed = QLabel()

        self.save_wallet_file = QPushButton('Save secure wallet file')


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.frame = QFrame(self)
        self.qaddress.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.qaddress.setFrameShadow(QFrame.Plain)
        self.qaddress.setLineWidth(1)

        self.mnemonic.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.mnemonic.setFrameShadow(QFrame.Plain)
        self.mnemonic.setLineWidth(1)
        self.mnemonic.setWordWrap(True)

        self.hexseed.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.hexseed.setFrameShadow(QFrame.Plain)
        self.hexseed.setLineWidth(1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.qaddress_description)
        layout.addWidget(self.qaddress)
        layout.addWidget(self.mnemonic_description)
        layout.addWidget(self.mnemonic)
        layout.addWidget(self.hexseed_description)
        layout.addWidget(self.hexseed)
        layout.addWidget(self.save_wallet_file)

    def nextId(self) -> int:
        return 11

class SlaveJsonOptions(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Slaves.json requires a wallet")


        self.label_description = QLabel("Select option:")
        self.radiobutton_1 = QRadioButton("Open wallet file")
        self.radiobutton_2 = QRadioButton("Restore wallet from seed")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_description)
        layout.addWidget(self.radiobutton_1)
        layout.addWidget(self.radiobutton_2)

    def nextId(self) -> int:
        if self.radiobutton_1.isChecked():
            return 9
        if self.radiobutton_2.isChecked():
            return 10
        return 0

class CreateSlavesJson(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setTitle("Slaves.json is finished!")

        self.generatedslave_label = QLabel("Move slaves.json file from current directory to the mining node inside ~/.qrl/\n\nYou can close the wallet now.")
        self.slave_number_label = QLabel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.generatedslave_label)
        layout.addWidget(self.slave_number_label)

    def nextId(self) -> int:
        return 11

class OpenWalletFile(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Open wallet file")

        self.password_qlabel = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit()
        self.passwordline_edit.setEchoMode(2)
        self.passwordline_edit.setPlaceholderText("Enter password")
        self.openFileBtn = QPushButton("Import secure wallet file")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.password_qlabel)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.openFileBtn)
        self.setLayout(layout)

    def nextId(self) -> int:
        return 11

class OpenWalletFileSlaves(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Open wallet file")

        self.password_qlabel = QLabel("Password (optional):")
        self.passwordline_edit = QLineEdit()
        self.passwordline_edit.setEchoMode(2)
        self.passwordline_edit.setPlaceholderText("Enter password")
        self.openFileBtn = QPushButton("Import secure wallet file")
        self.warning_label = QLabel("After clicking 'Next' button to begin, the slaves will be generated which will\ntake about 10 minutes. See the console for progress.\n\nPlease be patient.")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.password_qlabel)
        layout.addWidget(self.passwordline_edit)
        layout.addWidget(self.openFileBtn)
        layout.addWidget(self.warning_label)
        self.setLayout(layout)

    def nextId(self) -> int:
        return 8

class RegExpValidator(QtGui.QRegularExpressionValidator):
    validationChanged = QtCore.pyqtSignal(QtGui.QValidator.State)

    def validate(self, input, pos):
        state, input, pos = super().validate(input, pos)
        self.validationChanged.emit(state)
        return state, input, pos

class RestoreWallet(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Restore your wallet")

        self.seed_label = QLabel("Enter your seed:")
        self.seedline_edit = QLineEdit()
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.seed_label)
        layout.addWidget(self.seedline_edit)

        regexp_mnemonic = QtCore.QRegularExpression('[0-9a-fA-F]*') #(r'((\b|\s)+\w+(\b|\s)+){34}|.{102}') #QRL address regex
        
        validator = RegExpValidator(regexp_mnemonic, self)
        validator.validationChanged.connect(self.handleValidationChange)
        self.seedline_edit.setValidator(validator)

    def initializePage(self):
        # Perform actions when the page is displayed
        print(f'-> restoreWallet page displayed')
        self.setNextButtonEnable(False) # not working?

    def setNextButtonEnable(self, enabled):
        if self.wizard() is not None:
            next_button = self.wizard().button(QWizard.NextButton)
            if next_button is not None:
                next_button.setEnabled(enabled)  
            else:
                print(f'-> next button is not ready!')
        else:
            print(f'-> wizard is not ready!')

    def reset(self):
        self.seedline_edit.clear()


    def handleValidationChange(self, state):
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'gold'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'lime'
        self.seedline_edit.setStyleSheet('border: 1px solid %s' % colour)
        #print(f'> state: {state}')

        if len(self.seedline_edit.text()) == 102:
            self.setNextButtonEnable(True)
        else:
            self.setNextButtonEnable(False)

    def nextId(self) -> int:
        return 11

class RestoreWalletSlaves(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Restore your wallet")

        self.seed_label = QLabel("Enter your seed:")
        self.seedline_edit = QLineEdit()
        self.warning_label = QLabel("After clicking 'Next' button to begin, the slaves will be generated which will\ntake about 10 minutes. See the console for progress.\n\nPlease be patient.")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.seed_label)
        layout.addWidget(self.seedline_edit)
        layout.addWidget(self.warning_label)

        regexp_mnemonic = QtCore.QRegularExpression(r'((\b|\s)+\w+(\b|\s)+){34}|.{102}') #QRL address regex
        
        validator = RegExpValidator(regexp_mnemonic, self)
        validator.validationChanged.connect(self.handleValidationChange)
        self.seedline_edit.setValidator(validator)


    def handleValidationChange(self, state):
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'gold'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'lime'
        self.seedline_edit.setStyleSheet('border: 1px solid %s' % colour)

    def nextId(self) -> int:
        return 8

class LastPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Success!")
        
        
class QrlWallet(QtWidgets.QMainWindow, Ui_mainWindow, Ui_Form, Ui_Form2 , QtWidgets.QWizard, QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./assets/QSC_logo.png'))
        self.model = Model()

        regexp_ots_key = QRegExp(r'^[0-9]*$')
        self.ots_key_validator = QRegExpValidator(regexp_ots_key)
        self.ots_key_index_input.setEnabled(False)
        
        self.inner_window.setEnabled(False)

        header = self.transaction_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.save_history.clicked.connect(self.handleSavehistory)
        self.horizontalSlider.valueChanged.connect(self.sliderChanged)

        self.custom_fee.clicked.connect(self.setCustomFee)
        self.fee_edit.hide()

        self.send_button.clicked.connect(self.button_clicked)
        self.actionAbout.triggered.connect(self.about_popup)
        self.view_recovery_seed_btn.clicked.connect(self.recovery_seed_pop_up)
        self.actionCheck_for_updates.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/successor1/qrllight/releases")))
        self.actionOfficial_website.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://theqrl.org")))
        self.actionDocumentation.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://docs.theqrl.org/")))
        self.actionQRL_whitepaper.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://raw.githubusercontent.com/theQRL/Whitepaper/master/QRL_whitepaper.pdf")))
        self.actionReport_bug.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/successor1/qrllight/issues")))
        self.actionDonate_to_development.triggered.connect(self.donate_popup)

        self.actionCheck_for_updates.setVisible(False)
        self.actionOfficial_website.setVisible(False)
        self.actionDocumentation.setVisible(False)
        self.actionQRL_whitepaper.setVisible(False)
        self.actionReport_bug.setVisible(False)

        self.actionWizard.triggered.connect(self.showWizard)


    def showWizard(self):
        main.restart()
        main.restoreWallet.reset()
        main.show()
        

    def setCustomFee(self):
        if self.custom_fee.isChecked():
            self.horizontalSlider.hide()
            self.slider_label.hide()
            self.fee_edit.show()
        else:
            self.fee_edit.hide()
            self.horizontalSlider.show()
            self.slider_label.show()


    def sliderChanged(self, value):
        try:
            slider_values.pop(0)
        except:
            pass
        slider_values.append(value)

    def handleSavehistory(self):
        #with open('monschedule.csv', 'wb') as stream:
        with open('mytransactionhistory.csv', 'w') as stream:                  # 'w'
            writer = csv.writer(stream, lineterminator='\n')          # + , lineterminator='\n'
            for row in range(self.transaction_table.rowCount()):
                rowdata = []
                for column in range(self.transaction_table.columnCount()):
                    item = self.transaction_table.item(row, column)
                    if item is not None:
                        #rowdata.append(unicode(item.text()).encode('utf8'))
                        rowdata.append(item.text())                   # +
                    else:
                        rowdata.append('')

                writer.writerow(rowdata)

    def button_clicked(self):
        qrl_address = []
        mnemonic = []
        hexseed = []
        if QWizard.hasVisitedPage(main, 2):
            qrl_address.append(main.walletDetails.qaddress.toPlainText())
            mnemonic.append(main.walletDetails.mnemonic.text().rstrip())
            hexseed.append(main.walletDetails.hexseed.text())
        elif QWizard.hasVisitedPage(main, 5):
            qrl_address.append(main.data[0].split(" ")[0])
            mnemonic.append(" ".join(main.data[0].split(" ")[1:-1]))
            hexseed.append(main.data[0].split(" ")[35])
        elif QWizard.hasVisitedPage(main, 6):
            if main.restoreWallet.seedline_edit.text()[:6] ==  "absorb":
                qrl_address.append(Model.recoverAddressMnemonic(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(main.restoreWallet.seedline_edit.text())
                hexseed.append(Model.recoverHexseedMnemonic(main.restoreWallet.seedline_edit.text()))
            elif main.restoreWallet.seedline_edit.text()[:2] ==  "01":
                qrl_address.append(Model.recoverAddressHexseed(main.restoreWallet.seedline_edit.text()))
                mnemonic.append(Model.recoverMnemonicHexseed(main.restoreWallet.seedline_edit.text()))
                hexseed.append(main.restoreWallet.seedline_edit.text())
        elif QWizard.hasVisitedPage(main, 3):
            qrl_address.append(main.walletDetailsExperimental.qaddress.toPlainText())
            mnemonic.append(main.walletDetailsExperimental.mnemonic.text().rstrip())
            hexseed.append(main.walletDetailsExperimental.hexseed.text())
        ots_key_validator = self.ots_key_validator.validate(self.ots_key_index_input.text(), 0)

        if ots_key_validator[0] != 2:
            QMessageBox.warning(self, "Warning: Incorrect Input!", "Wrong or empty OTS key input")
        else:
            remove_first_char_addrs = [e[1:] for e in self.send_input.text().split()]
            amount_string = self.amount_input.text().split()
            amount_list = [float(i) for i in list(amount_string)]
            addrs_to = remove_first_char_addrs
            amounts = amount_list
            message_data = self.description_input.text().encode() if self.description_input.text() else ''.encode()
            if self.fee_edit.text() == None or self.fee_edit.text() == "":
                try:
                    if slider_values[0] < 33:
                        slider_values.pop(0)
                        slider_values.append(0.001)
                    elif slider_values[0] > 33 and slider_values[0] < 66:
                        slider_values.pop(0)
                        slider_values.append(0.01)
                    elif slider_values[0] > 50:
                        slider_values.pop(0)
                        slider_values.append(1)
                except:
                    slider_values.append(0.01)
            else:
                slider_values.clear()
                slider_values.append(self.fee_edit.text())
            print(slider_values[0])
            fee = str(float(slider_values[0]) * 1000000000)[:-2]

            ots_key = int(self.ots_key_index_input.text())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Do you want to proceed?")
            msg.setInformativeText("Send to: " + self.send_input.text()  +"\nAmount: " + self.amount_input.text() + "\nFee: " + str(slider_values[0]) + "\nOTS Key Index: " + self.ots_key_index_input.text())
            msg.setWindowTitle("QSC Confirmation")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = msg.exec()
            if returnValue == QMessageBox.Cancel:
                pass
            else:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                
                src_xmss = XMSS.from_extended_seed(hstr2bin(hexseed[0]))
                xmss_pk = src_xmss.pk
                txHash = models.TransferTransaction.tx_transfer(
                    addrs_to,
                    amounts,
                    message_data,
                    fee,
                    xmss_pk,
                    src_xmss,
                    ots_key,
                    qrl_network[0])
                
                if txHash is not None:
                    # wait for confirmation
                    import asyncio
                    async def waitTxConfirmationsTask():
                        confirms = 0
                        while confirms < 1:
                            _, confirms, _, _ = TableOutput.getTx(txHash, qrl_network[0])
                            await asyncio.sleep(1)
                            print(f'-> confirms: {confirms}')

                        # update the balance, OTS, 
                        balance = TableOutput.getBalance(qrl_address[0], qrl_network[0]) / 1000000000
                        self.balance_label.setText(f"Balance: {balance} Q") 
                        ots = int(self.ots_key_index_input.text())
                        self.ots_key_index_input.setText(f'{ots+1}')

                        # update histories in UI
                        rowPosition = 0 #self.transaction_table.rowCount()
                        self.transaction_table.insertRow(rowPosition)
                        date_box = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
                        self.transaction_table.setItem(rowPosition, 0, QTableWidgetItem(date_box))
                        amount = '-' + self.amount_input.text()
                        self.transaction_table.setItem(rowPosition, 1, QTableWidgetItem(amount))
                        self.transaction_table.setItem(rowPosition, 2, QTableWidgetItem(''))

                        QApplication.restoreOverrideCursor()
                        QMessageBox.about(self, "Succesful transaction", f"Sent with Tx Hash: {txHash}")

                    asyncio.run(waitTxConfirmationsTask())
                else:
                    QMessageBox.about(self, "Transaction failed", "Error!")
                    QApplication.restoreOverrideCursor()

                self.amount_input.clear()
                self.send_input.clear()
                self.description_input.clear()




    def update(self):
        self.balance_label.adjustSize()

    def about_popup(self):
        self.dialog=QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.dialog)
        self.dialog.show()
    
    def recovery_seed_pop_up(self):
        self.t = recoveryWindow
        self.t.show()

    def donate_popup(self):
        self.dialog=QtWidgets.QMainWindow()
        self.ui = Ui_Form2()
        self.ui.setupUi(self.dialog)
        self.dialog.show()

class RecoverySeedView(QWidget):
    def __init__(self):
        super(RecoverySeedView, self).__init__()
        self.setWindowTitle("Wallet details")
        self.warning_label = QLabel('Warning: If someone unauthorized gains access to these, your funds will be lost!', self )
        myFont=QtGui.QFont()
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setStyleSheet('color: red')
        myFont.setBold(True)
        self.warning_label.setFont(myFont)
        self.mnemonic_label = QLabel('Mnemonic phrase', self )
        self.mnemonic_label.setAlignment(Qt.AlignCenter)
        self.mnemonic_label_text = QLabel()
        self.mnemonic_label_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.hexseed_label = QLabel('Hexseed', self )
        self.hexseed_label.setAlignment(Qt.AlignCenter)
        self.hexseed_label_text = QLabel()
        self.hexseed_label_text.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.mnemonic_label_text.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.mnemonic_label_text.setFrameShadow(QFrame.Plain)
        self.mnemonic_label_text.setLineWidth(1)
        self.mnemonic_label_text.setWordWrap(True)

        self.hexseed_label_text.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.hexseed_label_text.setFrameShadow(QFrame.Plain)
        self.hexseed_label_text.setLineWidth(1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.mnemonic_label)
        layout.addWidget(self.mnemonic_label_text)
        layout.addWidget(self.hexseed_label)
        layout.addWidget(self.hexseed_label_text)


if __name__ == "__main__":
    update_node_list()
    

    app = QtWidgets.QApplication(sys.argv)
    main = MyWizard()
    mainWindow = QrlWallet()
    recoveryWindow = RecoverySeedView()
    app.setWindowIcon(QtGui.QIcon('./assets/QSC_logo.png'))
    main.setWindowModality(QtCore.Qt.ApplicationModal)
    mainWindow.show()
    main.hide()
    sys.exit(app.exec_())
