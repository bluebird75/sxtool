# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/ui_form_set_row_size.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormSetRowSizeBase(object):
    def setupUi(self, FormSetRowSizeBase):
        FormSetRowSizeBase.setObjectName("FormSetRowSizeBase")
        FormSetRowSizeBase.resize(522, 188)
        self.vboxlayout = QtWidgets.QVBoxLayout(FormSetRowSizeBase)
        self.vboxlayout.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.textLabel1 = QtWidgets.QLabel(FormSetRowSizeBase)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.hboxlayout.addWidget(self.textLabel1)
        self.spinRowSize = QtWidgets.QSpinBox(FormSetRowSizeBase)
        self.spinRowSize.setMinimum(1)
        self.spinRowSize.setObjectName("spinRowSize")
        self.hboxlayout.addWidget(self.spinRowSize)
        spacerItem = QtWidgets.QSpacerItem(181, 21, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.groupData = QtWidgets.QGroupBox(FormSetRowSizeBase)
        self.groupData.setObjectName("groupData")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.groupData)
        self.vboxlayout1.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.lineEditData = QtWidgets.QLineEdit(self.groupData)
        self.lineEditData.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.lineEditData.setFont(font)
        self.lineEditData.setMaxLength(256)
        self.lineEditData.setAlignment(QtCore.Qt.AlignRight)
        self.lineEditData.setObjectName("lineEditData")
        self.vboxlayout1.addWidget(self.lineEditData)
        self.textLabelDataLength = QtWidgets.QLabel(self.groupData)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.textLabelDataLength.setFont(font)
        self.textLabelDataLength.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing
                                              | QtCore.Qt.AlignVCenter)
        self.textLabelDataLength.setWordWrap(False)
        self.textLabelDataLength.setObjectName("textLabelDataLength")
        self.vboxlayout1.addWidget(self.textLabelDataLength)
        self.vboxlayout.addWidget(self.groupData)
        spacerItem1 = QtWidgets.QSpacerItem(31, 41, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")
        spacerItem2 = QtWidgets.QSpacerItem(61, 21, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem2)
        self.pushButtonOK = QtWidgets.QPushButton(FormSetRowSizeBase)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.hboxlayout1.addWidget(self.pushButtonOK)
        spacerItem3 = QtWidgets.QSpacerItem(61, 21, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem3)
        self.pushButtonCancel = QtWidgets.QPushButton(FormSetRowSizeBase)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.hboxlayout1.addWidget(self.pushButtonCancel)
        spacerItem4 = QtWidgets.QSpacerItem(91, 31, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem4)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(FormSetRowSizeBase)
        self.spinRowSize.valueChanged['int'].connect(FormSetRowSizeBase.slotNewRowSize)
        self.pushButtonOK.clicked.connect(FormSetRowSizeBase.accept)
        self.pushButtonCancel.clicked.connect(FormSetRowSizeBase.reject)
        QtCore.QMetaObject.connectSlotsByName(FormSetRowSizeBase)

    def retranslateUi(self, FormSetRowSizeBase):
        _translate = QtCore.QCoreApplication.translate
        FormSetRowSizeBase.setWindowTitle(_translate("FormSetRowSizeBase", "Adjust Row Size"))
        self.textLabel1.setText(_translate("FormSetRowSizeBase", "New Row Size :"))
        self.groupData.setTitle(_translate("FormSetRowSizeBase", "Data"))
        self.lineEditData.setText(_translate("FormSetRowSizeBase", "00"))
        self.textLabelDataLength.setText(_translate("FormSetRowSizeBase", "Length: 2 (0x02)"))
        self.pushButtonOK.setText(_translate("FormSetRowSizeBase", "Ok"))
        self.pushButtonCancel.setText(_translate("FormSetRowSizeBase", "Cancel"))
