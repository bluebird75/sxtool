# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/ui_xor_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_XorDialog(object):
    def setupUi(self, XorDialog):
        XorDialog.setObjectName("XorDialog")
        XorDialog.resize(400, 175)
        self.gridLayout = QtWidgets.QGridLayout(XorDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(XorDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.maskLineEdit = QtWidgets.QLineEdit(XorDialog)
        self.maskLineEdit.setObjectName("maskLineEdit")
        self.gridLayout.addWidget(self.maskLineEdit, 0, 1, 1, 2)
        self.dataLabel = QtWidgets.QLabel(XorDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dataLabel.setFont(font)
        self.dataLabel.setObjectName("dataLabel")
        self.gridLayout.addWidget(self.dataLabel, 1, 0, 1, 1)
        self.dataLineEdit = QtWidgets.QLineEdit(XorDialog)
        self.dataLineEdit.setReadOnly(True)
        self.dataLineEdit.setObjectName("dataLineEdit")
        self.gridLayout.addWidget(self.dataLineEdit, 1, 1, 1, 2)
        self.resultLabel = QtWidgets.QLabel(XorDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.resultLabel.setFont(font)
        self.resultLabel.setObjectName("resultLabel")
        self.gridLayout.addWidget(self.resultLabel, 2, 0, 1, 1)
        self.resultLineEdit = QtWidgets.QLineEdit(XorDialog)
        self.resultLineEdit.setReadOnly(True)
        self.resultLineEdit.setObjectName("resultLineEdit")
        self.gridLayout.addWidget(self.resultLineEdit, 2, 1, 1, 2)
        self.statusLabel = QtWidgets.QLabel(XorDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy)
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 3, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(XorDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)

        self.retranslateUi(XorDialog)
        self.buttonBox.accepted.connect(XorDialog.accept)
        self.buttonBox.rejected.connect(XorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(XorDialog)

    def retranslateUi(self, XorDialog):
        _translate = QtCore.QCoreApplication.translate
        XorDialog.setWindowTitle(_translate("XorDialog", "Dialog"))
        self.label_3.setText(_translate("XorDialog", "Mask:"))
        self.dataLabel.setText(_translate("XorDialog", "Data:"))
        self.resultLabel.setText(_translate("XorDialog", "Result:"))
