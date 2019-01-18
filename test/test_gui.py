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

    @classmethod
    def tearDownClass(cls):
        sys.excepthook = cls.saveExceptHook
        # cls.app.exit()
        # cls.app = None

    def testLoadFile(self):
        w = MainForm(file=None)
        self.assertEqual( len(w.dataTable.sxfile), 0 )
        w.loadFile( 'example3.s28')
        self.assertEqual( len(w.dataTable.sxfile), 6 )

    def testLineEdit(self):
        le = QLineEdit()
        QTest.keyClicks(le, "coucou")
        self.assertEqual( le.text(), "coucou")


if __name__ == "__main__":
    unittest.main()
    # main( testRunner = TextTestRunner( verbosity = 2 ) )

