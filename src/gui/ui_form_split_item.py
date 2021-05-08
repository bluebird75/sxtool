# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/ui_form_split_item.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormSplitItemBase(object):
    def setupUi(self, FormSplitItemBase):
        FormSplitItemBase.setObjectName("FormSplitItemBase")
        FormSplitItemBase.resize(522, 296)
        self.vboxlayout = QtWidgets.QVBoxLayout(FormSplitItemBase)
        self.vboxlayout.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.textLabel1 = QtWidgets.QLabel(FormSplitItemBase)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.hboxlayout.addWidget(self.textLabel1)
        self.spinRowOffset = QtWidgets.QSpinBox(FormSplitItemBase)
        self.spinRowOffset.setProperty("value", 1)
        self.spinRowOffset.setObjectName("spinRowOffset")
        self.hboxlayout.addWidget(self.spinRowOffset)
        spacerItem = QtWidgets.QSpacerItem(
            181, 21, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.groupData = QtWidgets.QGroupBox(FormSplitItemBase)
        self.groupData.setObjectName("groupData")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.groupData)
        self.vboxlayout1.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.lineEditDataFirstRow = QtWidgets.QLineEdit(self.groupData)
        self.lineEditDataFirstRow.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.lineEditDataFirstRow.setFont(font)
        self.lineEditDataFirstRow.setMaxLength(256)
        self.lineEditDataFirstRow.setAlignment(QtCore.Qt.AlignRight)
        self.lineEditDataFirstRow.setObjectName("lineEditDataFirstRow")
        self.vboxlayout1.addWidget(self.lineEditDataFirstRow)
        self.textLabelDataLengthFirstRow = QtWidgets.QLabel(self.groupData)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.textLabelDataLengthFirstRow.setFont(font)
        self.textLabelDataLengthFirstRow.setAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        )
        self.textLabelDataLengthFirstRow.setWordWrap(False)
        self.textLabelDataLengthFirstRow.setObjectName("textLabelDataLengthFirstRow")
        self.vboxlayout1.addWidget(self.textLabelDataLengthFirstRow)
        self.vboxlayout.addWidget(self.groupData)
        self.groupData_2 = QtWidgets.QGroupBox(FormSplitItemBase)
        self.groupData_2.setObjectName("groupData_2")
        self.vboxlayout2 = QtWidgets.QVBoxLayout(self.groupData_2)
        self.vboxlayout2.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.lineEditDataSecondRow = QtWidgets.QLineEdit(self.groupData_2)
        self.lineEditDataSecondRow.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.lineEditDataSecondRow.setFont(font)
        self.lineEditDataSecondRow.setMaxLength(256)
        self.lineEditDataSecondRow.setAlignment(QtCore.Qt.AlignRight)
        self.lineEditDataSecondRow.setObjectName("lineEditDataSecondRow")
        self.vboxlayout2.addWidget(self.lineEditDataSecondRow)
        self.textLabelDataLengthSecondRow = QtWidgets.QLabel(self.groupData_2)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.textLabelDataLengthSecondRow.setFont(font)
        self.textLabelDataLengthSecondRow.setAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        )
        self.textLabelDataLengthSecondRow.setWordWrap(False)
        self.textLabelDataLengthSecondRow.setObjectName("textLabelDataLengthSecondRow")
        self.vboxlayout2.addWidget(self.textLabelDataLengthSecondRow)
        self.vboxlayout.addWidget(self.groupData_2)
        spacerItem1 = QtWidgets.QSpacerItem(
            31, 41, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.vboxlayout.addItem(spacerItem1)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")
        spacerItem2 = QtWidgets.QSpacerItem(
            61, 21, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.hboxlayout1.addItem(spacerItem2)
        self.pushButtonOK = QtWidgets.QPushButton(FormSplitItemBase)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.hboxlayout1.addWidget(self.pushButtonOK)
        spacerItem3 = QtWidgets.QSpacerItem(
            61, 21, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.hboxlayout1.addItem(spacerItem3)
        self.pushButtonCancel = QtWidgets.QPushButton(FormSplitItemBase)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.hboxlayout1.addWidget(self.pushButtonCancel)
        spacerItem4 = QtWidgets.QSpacerItem(
            91, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.hboxlayout1.addItem(spacerItem4)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(FormSplitItemBase)
        self.spinRowOffset.valueChanged["int"].connect(
            FormSplitItemBase.slotNewRowOffset
        )
        self.pushButtonOK.clicked.connect(FormSplitItemBase.accept)
        self.pushButtonCancel.clicked.connect(FormSplitItemBase.reject)
        QtCore.QMetaObject.connectSlotsByName(FormSplitItemBase)

    def retranslateUi(self, FormSplitItemBase):
        _translate = QtCore.QCoreApplication.translate
        FormSplitItemBase.setWindowTitle(
            _translate("FormSplitItemBase", "Split Item Offset")
        )
        self.textLabel1.setText(_translate("FormSplitItemBase", "Split Offset :"))
        self.groupData.setTitle(_translate("FormSplitItemBase", "First Row"))
        self.lineEditDataFirstRow.setText(_translate("FormSplitItemBase", "00"))
        self.textLabelDataLengthFirstRow.setText(
            _translate("FormSplitItemBase", "Length: 2 (0x02)")
        )
        self.groupData_2.setTitle(_translate("FormSplitItemBase", "Second Row"))
        self.lineEditDataSecondRow.setText(_translate("FormSplitItemBase", "00"))
        self.textLabelDataLengthSecondRow.setText(
            _translate("FormSplitItemBase", "Length: 2 (0x02)")
        )
        self.pushButtonOK.setText(_translate("FormSplitItemBase", "Ok"))
        self.pushButtonCancel.setText(_translate("FormSplitItemBase", "Cancel"))
