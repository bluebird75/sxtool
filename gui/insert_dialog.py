# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from PyQt5.QtWidgets import QDialog

from gui.ui_insert_dialog import Ui_InsertDialog

class InsertDialog(Ui_InsertDialog, QDialog):
    def __init__(self,parent = None,name = "InsertDialog" ,modal = 0,fl = 0):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(modal)
        self.setObjectName(name)

