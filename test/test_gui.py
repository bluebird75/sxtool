#!/usr/bin/env python

# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

import unittest, io, sys, os

from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtTest import QTest

from src.form_insert_row_value import FormInsertRowValue
from src.main_form import MainForm
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
        w = MainForm(file=None)
        self.assertEqual( len(w.dataTable.sxfile), 0 )
        w.loadFile( 'example3.s28')
        sxf = w.dataTable.sxfile
        self.assertEqual( len(sxf), 6 )
        self.assertEqual( str(sxf.sxItemFirst), 'S0030000FF' )
        self.assertEqual( str(sxf.sxItemLast),  'S90300000F' )
        self.assertEqual( str(sxf[-1]), 'S21000B0306F207265616420746869733FCD' )
        self.assertEqual( str(sxf[0]), 'S21400B000576F77212044696420796F7520726561D7' )


    def XtestInsertFile(self):
        w = MainForm(file='example3.s28')
        sxf = w.dataTable.sxfile
        self.assertEqual( str(sxf), '''S0 03 0000 FF
S2 14 00B000 576F77212044696420796F7520726561 D7
S2 14 00B010 6C6C7920676F207468726F7567682061 42
S2 14 00B020 6C20746861742074726F75626C652074 2D
S2 10 00B030 6F207265616420746869733F CD
S9 03 0000 0F''' )





    def testLineEdit(self):
        le = QLineEdit()
        QTest.keyClicks(le, "coucou")
        self.assertEqual( le.text(), "coucou")


if __name__ == "__main__":
    unittest.main()
    # main( testRunner = TextTestRunner( verbosity = 2 ) )

