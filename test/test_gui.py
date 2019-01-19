#!/usr/bin/env python

# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

import unittest, io, sys, os, tempfile
from unittest.mock import Mock, patch

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtTest import QTest

from src.form_insert_row_value import FormInsertRowValue
from src import main_form
from sxtool import myExceptHook

class TestWithGui(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # to avoid crashes when Python exceptions are raised inside Qt slots
        cls.saveExceptHook = sys.excepthook
        sys.excepthook = myExceptHook
        cls.app = QApplication([])
        cls.maxDiff = None

    @classmethod
    def tearDownClass(cls):
        sys.excepthook = cls.saveExceptHook
        # cls.app.exit()
        # cls.app = None

    def testLoadFile(self):
        w = main_form.MainForm(file=None)
        self.assertEqual( len(w.dataTable.sxfile), 0 )
        w.loadFile( 'example3.s28')
        sxf = w.dataTable.sxfile
        self.assertEqual( len(sxf), 6 )
        self.assertEqual( str(sxf.sxItemFirst), 'S0030000FF' )
        self.assertEqual( str(sxf.sxItemLast),  'S8040000000F' )
        self.assertEqual( str(sxf[-1]), 'S21000B0306F207265616420746869733FCD' )
        self.assertEqual( str(sxf[0]), 'S21400B000576F77212044696420796F7520726561D7' )


    def testInsertFile(self):
        w = main_form.MainForm(file='example3.s28')
        sxf = w.dataTable.sxfile
        self.assertEqual( len(sxf), 6 )

        # Refuse insertion
        mockDialog = Mock(
            exec_=lambda:QDialog.Rejected,
            windowFlags=lambda:0,
            radioStart=Mock(isChecked=lambda:True)
        )
        w.insertFname('example1.s19', mockDialog)
        self.assertEqual( len(sxf), 6 )

        # Insert file is too interactive, it may only be tested
        mockDialog = Mock(
            exec_=lambda:QDialog.Accepted,
            windowFlags=lambda:0,
            radioStart=Mock(isChecked=lambda:True)
        )
        w.insertFname('example1.s19', mockDialog)
        self.assertEqual( len(sxf), 8 )

    def testSave(self):
        w = main_form.MainForm(file='example3.s28')
        sxf = w.dataTable.sxfile
        self.assertEqual( str(sxf), '''S0030000FF
S21400B000576F77212044696420796F7520726561D7
S21400B0106C6C7920676F207468726F756768206142
S21400B0206C20746861742074726F75626C6520742D
S21000B0306F207265616420746869733FCD
S8040000000F
''' )
        w.dataTable.sxfile[0].updateData('')
        with tempfile.NamedTemporaryFile(delete=False) as f:
            w.dataTable.file = f.name
            w.slotSave()
            f.close()
            with open(f.name) as f2:
                self.assertEqual( f2.read(), '''S0030000FF
S20400B0004B
S21400B0106C6C7920676F207468726F756768206142
S21400B0206C20746861742074726F75626C6520742D
S21000B0306F207265616420746869733FCD
S8040000000F
''' )

    # copy & cut is tested as part of datatables

    def testPaste(self):
        pass

    @patch.object(main_form.QMessageBox, 'question')
    def testDelete(self, mockQuestion):
        w = main_form.MainForm(file='example3.s28')
        sxf = w.dataTable.sxfile
        self.assertEqual( len(sxf), 6 )

        mockQuestion.configure_mock( return_value=main_form.QMessageBox.No )
        w.slotDelete() # aborted
        self.assertEqual( len(sxf), 6 )

        mockQuestion.configure_mock( return_value=main_form.QMessageBox.Yes )
        w.dataTable.setCurrentItem( w.dataTable.item(2,0) )
        QTest.keyEvent( QTest.Click, w.dataTable, Qt.Key_Down, Qt.ShiftModifier )
        w.slotDelete() # success
        self.assertEqual( len(sxf), 4 )

    # conversion to s19 s28 s37 is tested as part of datatable



if __name__ == "__main__":
    unittest.main()
    # main( testRunner = TextTestRunner( verbosity = 2 ) )

