# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from PyQt5.QtWidgets import QDialog

from src.gui.ui_form_set_row_size import Ui_FormSetRowSizeBase

class FormSetRowSize( Ui_FormSetRowSizeBase, QDialog ):
    def __init__(self,parent = None,name = "FormSetRowSize", modal = 0,fl = 0):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(modal)
        self.setObjectName(name)
        
    def setInitialData( self, data ):
        self.initial_data = data
        self.spinRowSize.setValue( len(data)//2 )
        self.slotNewRowSize(len(data)//2 )

    def slotNewRowSize(self,a0):
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
