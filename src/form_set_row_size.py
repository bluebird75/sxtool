# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional

from PyQt5.QtWidgets import QDialog, QWidget

from src.gui.ui_form_set_row_size import Ui_FormSetRowSizeBase


class FormSetRowSize(Ui_FormSetRowSizeBase, QDialog ): # type: ignore # PyQt and Mypy don't mix very well
    def __init__(self,
                parent: Optional[QWidget] = None,
                name:str = "FormSetRowSize", 
                modal:int = 0,
                fl:int = 0):
        QDialog.__init__(self, parent)
        self.setupUi(self)      # type: ignore # PyQt and Mypy don't mix very well
        self.setModal(modal)
        self.setObjectName(name)
        
    def setInitialData(self, data:str) -> None:
        self.initial_data = data
        self.spinRowSize.setValue( len(data)//2 )
        self.slotNewRowSize(len(data)//2 )

    def slotNewRowSize(self, a0:int) -> None:
        if (a0 <= 0): return
        data = self.initial_data
        merging = False
        if (a0 > len(self.initial_data)//2):
            merging = True
            data = data + '00'*( a0-len(data)//2 )
        self.lineEditData.setText( data[0:a0*2] )
        mergeText = ""
        if merging: mergeText = "[Merging with next selected line if possible]"
        self.textLabelDataLength.setText("%s Length: %d (0x%s)" % (mergeText, a0, hex(a0)[2:].upper()))
