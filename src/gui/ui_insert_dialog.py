# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/ui_insert_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InsertDialog(object):
    def setupUi(self, InsertDialog):
        InsertDialog.setObjectName("InsertDialog")
        InsertDialog.resize(250, 180)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InsertDialog.sizePolicy().hasHeightForWidth())
        InsertDialog.setSizePolicy(sizePolicy)
        InsertDialog.setMinimumSize(QtCore.QSize(250, 180))
        InsertDialog.setMaximumSize(QtCore.QSize(250, 180))
        InsertDialog.setBaseSize(QtCore.QSize(250, 150))
        InsertDialog.setModal(True)
        self.OkButton = QtWidgets.QPushButton(InsertDialog)
        self.OkButton.setGeometry(QtCore.QRect(25, 145, 90, 30))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OkButton.sizePolicy().hasHeightForWidth())
        self.OkButton.setSizePolicy(sizePolicy)
        self.OkButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.OkButton.setFlat(False)
        self.OkButton.setObjectName("OkButton")
        self.CancelButton = QtWidgets.QPushButton(InsertDialog)
        self.CancelButton.setGeometry(QtCore.QRect(125, 145, 90, 30))
        self.CancelButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.CancelButton.setFlat(False)
        self.CancelButton.setObjectName("CancelButton")
        self.InsertGroup = QtWidgets.QGroupBox(InsertDialog)
        self.InsertGroup.setGeometry(QtCore.QRect(5, 5, 240, 135))
        self.InsertGroup.setFlat(False)
        self.InsertGroup.setProperty("exclusive", True)
        self.InsertGroup.setObjectName("InsertGroup")
        self.radioBeforeCurrent = QtWidgets.QRadioButton(self.InsertGroup)
        self.radioBeforeCurrent.setGeometry(QtCore.QRect(20, 50, 170, 20))
        self.radioBeforeCurrent.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.radioBeforeCurrent.setObjectName("radioBeforeCurrent")
        self.radioStart = QtWidgets.QRadioButton(self.InsertGroup)
        self.radioStart.setGeometry(QtCore.QRect(20, 20, 170, 20))
        self.radioStart.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.radioStart.setObjectName("radioStart")
        self.radioAfterCurrent = QtWidgets.QRadioButton(self.InsertGroup)
        self.radioAfterCurrent.setGeometry(QtCore.QRect(20, 80, 151, 19))
        self.radioAfterCurrent.setObjectName("radioAfterCurrent")
        self.radioEnd = QtWidgets.QRadioButton(self.InsertGroup)
        self.radioEnd.setGeometry(QtCore.QRect(20, 110, 170, 20))
        self.radioEnd.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.radioEnd.setChecked(True)
        self.radioEnd.setObjectName("radioEnd")

        self.retranslateUi(InsertDialog)
        self.OkButton.clicked.connect(InsertDialog.accept)
        self.CancelButton.clicked.connect(InsertDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InsertDialog)

    def retranslateUi(self, InsertDialog):
        _translate = QtCore.QCoreApplication.translate
        InsertDialog.setWindowTitle(
            _translate("InsertDialog", "Emplacement of insertion ?")
        )
        self.OkButton.setText(_translate("InsertDialog", "OK"))
        self.CancelButton.setText(_translate("InsertDialog", "Cancel"))
        self.InsertGroup.setTitle(
            _translate("InsertDialog", "Where do you want to insert the file ?")
        )
        self.radioBeforeCurrent.setText(
            _translate("InsertDialog", "Before current selection")
        )
        self.radioStart.setText(_translate("InsertDialog", "At the start of the file"))
        self.radioAfterCurrent.setText(
            _translate("InsertDialog", "After current selection")
        )
        self.radioEnd.setText(_translate("InsertDialog", "At the end of the file"))
