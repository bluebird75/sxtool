# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

from gui.ui_xor_dialog import Ui_XorDialog
from src.sx_item import xor

class XorDialog(Ui_XorDialog, QDialog):
    
    def __init__(self,parent = None,name = "XorDialog" ,modal = 0, multiLines=False, maxLen=-1):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(modal)
        self.setObjectName(name)
        rx = QRegExp( "[A-Fa-f0-9]*" )
        validator = QRegExpValidator( rx, self.maskLineEdit )
        self.maskLineEdit.setValidator( validator )
        if multiLines :
            self.dataLineEdit.setEnabled(False)
            self.resultLineEdit.setEnabled(False)
            self.dataLabel.setEnabled(False)
            self.resultLabel.setEnabled(False)
        else:
            self.maskLineEdit.textChanged.connect(self.slotTextChanged)
        if maxLen >= 0:
            self.maskLineEdit.setMaxLength( maxLen )

    def setData(self, text):
        self.dataLineEdit.setText(text)
        self.maskLineEdit.setMaxLength( len(text) )

    def slotTextChanged(self, pattern):
        data = str(self.dataLineEdit.text())
        res = xor(data, pattern)
        self.resultLineEdit.setText(res)
