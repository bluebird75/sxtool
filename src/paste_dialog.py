# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional

from PyQt5.QtWidgets import QDialog, QWidget

from src.gui.ui_paste_dialog import Ui_PasteDialog

class PasteDialog(Ui_PasteDialog, QDialog):  # type: ignore # PyQt and Mypy don't mix very well
    def __init__(self,
                parent: Optional[QWidget] = None,
                name:str = "PastDialog", 
                modal:int = 0,
                fl:int = 0):
        QDialog.__init__(self, parent)
        self.setupUi(self)  # type: ignore # PyQt and Mypy don't mix very well
        self.setObjectName(name)
        self.setModal(modal)
