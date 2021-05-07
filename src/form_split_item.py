# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional

from PyQt5.QtWidgets import QDialog, QWidget

from src.gui.ui_form_split_item import Ui_FormSplitItemBase


class FormSplitItem(Ui_FormSplitItemBase, QDialog):  # type: ignore # PyQt and Mypy don't mix very well
    def __init__(
        self, parent: Optional[QWidget] = None, name: str = "FormSplitItem", modal: int = 0, fl: int = 0
    ) -> None:
        QDialog.__init__(self, parent)
        self.setupUi(self)  # type: ignore # PyQt and Mypy don't mix very well
        self.setModal(modal)
        self.setObjectName(name)

    def setInitialData(self, data: str) -> None:
        self.data = data
        maxVal = max(1, len(data) // 2 - 1)  # type: int
        self.spinRowOffset.setValue(maxVal)
        self.slotNewRowOffset(maxVal)
        self.spinRowOffset.setMinimum(1)
        self.spinRowOffset.setMaximum(maxVal)

    def slotNewRowOffset(self, newOffset: int) -> None:
        self.lineEditDataFirstRow.setText(self.data[0 : newOffset * 2])
        self.textLabelDataLengthFirstRow.setText("Length: %d (0x%s)" % (newOffset, hex(newOffset)[2:].upper()))
        secondLength = len(self.data) // 2 - newOffset
        self.lineEditDataSecondRow.setText(self.data[newOffset * 2 :])
        self.textLabelDataLengthSecondRow.setText("Length: %d (0x%s)" % (secondLength, hex(secondLength)[2:].upper()))
