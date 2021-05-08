# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QWidget

from src.gui.ui_form_insert_row_value import Ui_FormInsertRowValue


def formatToAddressLength(format:str) -> int:
    """Return the length -in characters- that an address must have,
    according to a format"""
    if format == 'S19':
        return 4
    elif format == 'S28':
        return 6
    elif format == 'S37':
        return 8
    else:
        raise ValueError("Invalid parameter in method formatToAddressLength: %s" % format)

class FormInsertRowValue(Ui_FormInsertRowValue, QDialog):  # type: ignore # PyQt and Mypy don't mix very well
    def __init__(self,
                default_format:str,
                parent: Optional[QWidget] = None,
                name:str = "FormInsertRowValue", 
                modal:int = 0,
                fl:int = 0):
        QDialog.__init__(self, parent)
        self.setupUi(self)      # type: ignore # PyQt and Mypy don't mix very well
        self.setModal(modal)
        self.setObjectName(name)
        self.nlines = 1
        self.default_format = default_format

        # Set validators
        rx = QRegExp("[A-Fa-f0-9]*")
        validator = QRegExpValidator(rx, self.lineAddrStart)
        self.lineAddrStart.setValidator(validator)
        validator = QRegExpValidator(rx, self.lineEditData)
        self.lineEditData.setValidator(validator)

        self.slotAutoFormatToggled( True )

        self.spinRowSize.valueChanged.connect( self.slotUpdateDataLength )
        self.spinRowSize.setValue(8)
        self.slotUpdateDataLength( 8 )

    def adjustAddressLength(self, address:str, format:str) -> str:
        """Adjust a -valid- address length according to a format"""
        length = formatToAddressLength(format)     # type: int
        ret = ('0'*length + address)[-length:]
        return ret

    def slotUpdateAddressesLength(self, format:str) -> None:
        newText = self.adjustAddressLength(self.lineAddrStart.text(), format)
        self.lineAddrStart.setText(newText)
        l = formatToAddressLength(format)
        self.lineAddrStart.setMaxLength( l )

    def slotUpdateLabelDataLength(self, value:str) -> None:
        length = len(value)
        self.textLabelDataLength.setText("Length: %d (0x%s)" % (length, hex(length)[2:].upper()))

    def slotAutoFormatToggled(self, val:bool) -> None:
        if val:
            index = self.comboBoxFormat.findText(self.default_format)
            if index == -1: return
            self.comboBoxFormat.setCurrentIndex(index)
            self.slotUpdateAddressesLength(self.comboBoxFormat.currentText())

    def slotUpdateDataLength(self, newLength:int) -> None:
        '''Update the datacontent field according to the new length specified'''
        if newLength <= 0:
            self.lineEditData.setText(00)
            self.lineEditData.setMaxLength(2)
            return

        data = self.lineEditData.text()
        self.lineEditData.setMaxLength( newLength * 2)



