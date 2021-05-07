# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/ui_paste_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PasteDialog(object):
    def setupUi(self, PasteDialog):
        PasteDialog.setObjectName('PasteDialog')
        PasteDialog.resize(403, 205)
        self.gridLayout = QtWidgets.QGridLayout(PasteDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName('gridLayout')
        self.buttonGroupMain = QtWidgets.QGroupBox(PasteDialog)
        self.buttonGroupMain.setObjectName('buttonGroupMain')
        self.radioReplaceSelection = QtWidgets.QRadioButton(self.buttonGroupMain)
        self.radioReplaceSelection.setGeometry(QtCore.QRect(10, 40, 120, 20))
        self.radioReplaceSelection.setObjectName('radioReplaceSelection')
        self.radioAddLines = QtWidgets.QRadioButton(self.buttonGroupMain)
        self.radioAddLines.setGeometry(QtCore.QRect(10, 20, 100, 20))
        self.radioAddLines.setChecked(True)
        self.radioAddLines.setObjectName('radioAddLines')
        self.gridLayout.addWidget(self.buttonGroupMain, 0, 0, 1, 1)
        self.buttonGroupReplace = QtWidgets.QGroupBox(PasteDialog)
        self.buttonGroupReplace.setEnabled(False)
        self.buttonGroupReplace.setObjectName('buttonGroupReplace')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.buttonGroupReplace)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName('verticalLayout')
        self.radioSelectionOnly = QtWidgets.QRadioButton(self.buttonGroupReplace)
        self.radioSelectionOnly.setObjectName('radioSelectionOnly')
        self.verticalLayout.addWidget(self.radioSelectionOnly)
        self.radioSelectionAndReplace = QtWidgets.QRadioButton(self.buttonGroupReplace)
        self.radioSelectionAndReplace.setObjectName('radioSelectionAndReplace')
        self.verticalLayout.addWidget(self.radioSelectionAndReplace)
        self.radioSelectionAndAdd = QtWidgets.QRadioButton(self.buttonGroupReplace)
        self.radioSelectionAndAdd.setChecked(True)
        self.radioSelectionAndAdd.setObjectName('radioSelectionAndAdd')
        self.verticalLayout.addWidget(self.radioSelectionAndAdd)
        self.gridLayout.addWidget(self.buttonGroupReplace, 0, 1, 2, 1)
        self.buttonGroupAdd = QtWidgets.QGroupBox(PasteDialog)
        self.buttonGroupAdd.setEnabled(True)
        self.buttonGroupAdd.setObjectName('buttonGroupAdd')
        self.radioAfterSelection = QtWidgets.QRadioButton(self.buttonGroupAdd)
        self.radioAfterSelection.setGeometry(QtCore.QRect(10, 40, 130, 20))
        self.radioAfterSelection.setObjectName('radioAfterSelection')
        self.radioBeforeSelection = QtWidgets.QRadioButton(self.buttonGroupAdd)
        self.radioBeforeSelection.setGeometry(QtCore.QRect(10, 20, 140, 20))
        self.radioBeforeSelection.setChecked(True)
        self.radioBeforeSelection.setObjectName('radioBeforeSelection')
        self.gridLayout.addWidget(self.buttonGroupAdd, 1, 0, 1, 1)
        self.pushOk = QtWidgets.QPushButton(PasteDialog)
        self.pushOk.setObjectName('pushOk')
        self.gridLayout.addWidget(self.pushOk, 2, 0, 1, 1)
        self.pushCancel = QtWidgets.QPushButton(PasteDialog)
        self.pushCancel.setObjectName('pushCancel')
        self.gridLayout.addWidget(self.pushCancel, 2, 1, 1, 1)

        self.retranslateUi(PasteDialog)
        self.pushOk.clicked.connect(PasteDialog.accept)
        self.pushCancel.clicked.connect(PasteDialog.reject)
        self.radioAddLines.toggled['bool'].connect(self.buttonGroupAdd.setEnabled)
        self.radioReplaceSelection.toggled['bool'].connect(self.buttonGroupReplace.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(PasteDialog)

    def retranslateUi(self, PasteDialog):
        _translate = QtCore.QCoreApplication.translate
        PasteDialog.setWindowTitle(_translate('PasteDialog', 'Paste mode'))
        self.buttonGroupMain.setTitle(_translate('PasteDialog', 'Pasting mode'))
        self.radioReplaceSelection.setText(_translate('PasteDialog', 'Replace selection'))
        self.radioAddLines.setText(_translate('PasteDialog', 'Add lines'))
        self.buttonGroupReplace.setTitle(_translate('PasteDialog', 'How do you want to replace lines ?'))
        self.radioSelectionOnly.setText(_translate('PasteDialog', 'Selection only'))
        self.radioSelectionAndReplace.setText(
            _translate('PasteDialog', 'If selection is too small, replace\n' 'the lines after')
        )
        self.radioSelectionAndAdd.setText(_translate('PasteDialog', 'If selection is too small, \n' 'add new lines'))
        self.buttonGroupAdd.setTitle(_translate('PasteDialog', 'Where do you want to add lines ?'))
        self.radioAfterSelection.setText(_translate('PasteDialog', 'After selection'))
        self.radioBeforeSelection.setText(_translate('PasteDialog', 'Before selection'))
        self.pushOk.setText(_translate('PasteDialog', 'OK'))
        self.pushCancel.setText(_translate('PasteDialog', 'Cancel'))
