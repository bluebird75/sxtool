# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from PyQt5.QtWidgets import QDialog

from gui.ui_paste_dialog import Ui_PasteDialog

class PasteDialog(Ui_PasteDialog, QDialog):
    def __init__(self,parent = None,name = 'PasteDialog',modal = 0,fl = 0):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setObjectName(name)
        self.setModal(modal)
