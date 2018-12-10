# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional, Any

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

from src.gui.ui_xor_dialog import Ui_XorDialog
from src.sx_item import xor

class XorDialog(Ui_XorDialog, QDialog): # type: ignore # Can not subclass QDialog, mypy does not deal well with PyQt
    
    def __init__(self,
                parent: Optional[Any] = None,
                name:str = "XorDialog", 
                modal:int = 0, 
                multiLines: bool = False, 
                maxLen:int = -1) -> None:
        QDialog.__init__(self, parent)
        self.setupUi(self)      # type: ignore # MyPy and PyQt problem
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

    def setData(self, text:str) -> None:
        self.dataLineEdit.setText(text)
        self.maskLineEdit.setMaxLength( len(text) )

    def slotTextChanged(self, pattern:str) -> None:
        data = str(self.dataLineEdit.text())
        res = xor(data, pattern)
        self.resultLineEdit.setText(res)
