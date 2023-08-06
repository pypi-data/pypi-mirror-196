from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout,QCheckBox
from PySide6.QtCore import Qt,Signal,Slot
#-------------------------------------------------------------------------------------------------------#
class encryptForm(QWidget):
    signal = Signal(bool)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("encrypting a file")
        self.setFixedHeight(130)
        self.setFixedWidth(300)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #email
        self.emailLabel = QLabel("email : ")
        self.emailLineEdit= QLineEdit()
        self.emailLineEdit.textEdited.connect(self.textEdited)

        #sign_CB
        self.signCB = QCheckBox("sign")
        self.signCB.stateChanged.connect(self.signCBChanged)

        #passphrase
        self.passphraseLabel = QLabel("passphrase : ")
        self.passphraseLabel.setHidden(True)
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setHidden(True)
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        #fingerprint
        self.fingerprintLabel = QLabel('fingerprint : ')
        self.fingerprintLabel.setHidden(True)
        self.fingerprintLineEdit = QLineEdit()
        self.fingerprintLineEdit.setHidden(True)
        self.fingerprintLineEdit.textEdited.connect(self.textEdited)

        #encrypt_button
        self.encryptButton = QPushButton("check and encrypt")
        self.encryptButton.setDisabled(True)
        self.encryptButton.clicked.connect(self.encryptClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.emailLabel,alignment= Qt.AlignTop)
        V_layout.addWidget(self.emailLineEdit)
        V_layout.addWidget(self.signCB)
        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)
        V_layout.addWidget(self.fingerprintLabel)
        V_layout.addWidget(self.fingerprintLineEdit)
        V_layout.addStretch()
        V_layout.addWidget(self.encryptButton,alignment= Qt.AlignCenter)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def signCBChanged(self):
        if self.signCB.isChecked():
            self.encryptButton.setDisabled(True)
            self.setFixedHeight(250)
            self.passphraseLabel.setHidden(False)
            self.passphraseLineEdit.setHidden(False)
            self.fingerprintLabel.setHidden(False)
            self.fingerprintLineEdit.setHidden(False)
        else:       
            if self.emailLineEdit.text() != "":
                self.encryptButton.setEnabled(True)
            else:
                self.encryptButton.setDisabled(True)
            self.passphraseLineEdit.clear()
            self.fingerprintLineEdit.clear()
            self.setFixedHeight(130)
            self.fingerprintLabel.setHidden(True)
            self.fingerprintLineEdit.setHidden(True)
            self.passphraseLabel.setHidden(True)
            self.passphraseLineEdit.setHidden(True)

    def textEdited(self):
        if not self.signCB.isChecked():
            if self.emailLineEdit.text() == "":                
                self.encryptButton.setDisabled(True)
                return
            else:
                self.encryptButton.setDisabled(False)
                return
        else:
            if self.emailLineEdit.text() == "": 
                self.encryptButton.setDisabled(True)
                return
            if self.passphraseLineEdit.text() == "": 
                self.encryptButton.setDisabled(True)
                return
            if self.fingerprintLineEdit.text() == "": 
                self.encryptButton.setDisabled(True)
                return
            else:
                self.encryptButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def encryptClicked(self):
        self.signal.emit(True)
        self.close()