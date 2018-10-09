# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from PyQt5.QtWidgets import QDialog

from gui.ui_form_split_item import Ui_FormSplitItemBase

class FormSplitItem( Ui_FormSplitItemBase, QDialog ):
    def __init__(self,parent = None,name = "FormSplitItem",modal = 0,fl = 0):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(modal)
        self.setObjectName(name)
        
    def setInitialData( self, data ):   # type: (str) -> None
        self.data = data
        maxVal = max(1,len(data)//2-1)      # type: int
        self.spinRowOffset.setValue( maxVal )
        self.slotNewRowOffset( maxVal )
        self.spinRowOffset.setMinimum( 1 )
        self.spinRowOffset.setMaximum( maxVal )

    def slotNewRowOffset( self, newOffset ):    # type: (int) -> None
        self.lineEditDataFirstRow.setText( self.data[0:newOffset*2] )
        self.textLabelDataLengthFirstRow.setText("Length: %d (0x%s)" % (newOffset, hex(newOffset)[2:].upper()))
        secondLength = len(self.data)//2-newOffset
        self.lineEditDataSecondRow.setText( self.data[newOffset*2:] )
        self.textLabelDataLengthSecondRow.setText("Length: %d (0x%s)" % (secondLength, hex(secondLength)[2:].upper()))
        
