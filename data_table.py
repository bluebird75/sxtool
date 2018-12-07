# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional, List, Any, Tuple, Union

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QAbstractItemView, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from sx_item import SxFile, SxItem, str2hexi
from gui.form_insert_row_value import FormInsertRowValue

class DataItem(QTableWidgetItem):
    def __init__(self, table, text:str, data:bool):
        QTableWidgetItem.__init__(self, text)
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.data = data    # type:bool
        if self.data:
            self.setTextAlignment(Qt.AlignLeft)
        else:
            self.setTextAlignment(Qt.AlignHCenter)

class DataTable(QTableWidget):
    ISTART = 0                  # type: int
    IBEFORESEL = 1              # type: int
    IAFTERSEL = 2               # type: int
    IEND = 3                    # type: int
    PADD = 0                    # type: int
    PADD_BEFORE = 1             # type: int
    PADD_AFTER = 2              # type: int
    PREPLACE = 3                # type: int
    PREPLACE_SELONLY = 4        # type: int
    PREPLACE_SELADD = 5         # type: int
    PREPLACE_SELREPLACE = 6     # type: int

    sigDataModifiedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, name : Optional[str]=None ):
        QTableWidget.__init__(self, 0, 0, parent)
        self.setObjectName(name)
        self.sxfile = SxFile()  # type: SxFile
        self.setFont(QFont("Courier new", 10))
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.initTable()
        self.file = ''  # type: str
        self.copy_list = [] # type: List[SxItem]

    def initTable(self) -> None:
        self.setHorizontalHeaderLabels(["Format", "Size", "Address", "Data", "Checksum"])
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setColumnWidth(3, 300)
        self.horizontalHeader().setStretchLastSection(1)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

    def loadFile(self, fname : str) -> bool:
        self.file = fname
        self.copy_list = []
        try:
            self.sxfile.fromFile(self.file)
        except Exception as e:
            QMessageBox.critical(None, "Error", "Could not open file %s\n%s" % (self.file, str(e)))
            return False
        self.redisplayTable()
        self.sigDataModifiedChanged.emit(False)
        return True

    def clear(self) -> None:
        for i in range(0, self.columnCount()): # type: int
            self.removeColumn(i)

    def redisplayTable(self) -> None:
        self.clear()
        self.clearSelection()
        self.setRowCount(2 + len(self.sxfile.sxItems))
        self.setColumnCount(5)

        if self.sxfile.sxItemFirst:
            self.setText(0, 0, "S0")
            self.setText(0, 1, self.sxfile.sxItemFirst.data_quantity)
            self.setText(0, 3, self.sxfile.sxItemFirst.data)
            self.setText(0, 4, self.sxfile.sxItemFirst.checksum)
        x = 1   # type: int
        for l in self.sxfile.sxItems:
            self.setText(x, 0, "S" + l.format[0])
            self.setText(x, 1, l.data_quantity)
            self.setText(x, 2, l.address)
            self.setText(x, 3, l.data)
            self.setText(x, 4, l.checksum)
            x += 1
        self.setText(x, 0, "S" + self.sxfile.sxItemLast.format[1])
        self.setText(x, 1, self.sxfile.sxItemLast.data_quantity)
        self.setText(x, 2, self.sxfile.sxItemLast.address)
        self.setText(x, 3, self.sxfile.sxItemLast.data)
        self.setText(x, 4, self.sxfile.sxItemLast.checksum)

        self.initTable()
        self.show()

    def setText(self, row:int, col:int, text:str) -> None:
        self.takeItem(row, col)
        item = DataItem(self, text, (col == 3))
        self.setItem(row, col, item)
        self.sigDataModifiedChanged.emit(True)

    def rowSelectedList(self) -> List[int]:
        """Return a list of all the row that are selected"""
        rows = []   # type: List[int]
        indexes = self.selectionModel().selectedRows()
        for index in indexes:
            rows.append(index.row())
        rows.sort()
        return rows

    def rowSelectedListWithoutFirstAndLast(self) -> List[int]:
        """Return a list of all the row that are selected"""
        rows = self.rowSelectedList()   # type: List[int]
        rows = [ x for x in rows if x not in [0, self.rowCount() - 1] ]
        return rows

    def isSelectionContinuus(self) -> bool:
        """Return true if the selection is continuus, false
        if there is no selection or if there are holes in the
        selection"""
        nbSwitch = 0    # type: int
        currentState = self.isRowSelected(0)    # type: bool
        for row in range(1, self.rowCount()):   # type: int
            if self.isRowSelected(row) != currentState:
                currentState = self.isRowSelected(row)
                nbSwitch += 1
        return (nbSwitch == 2)

    def numRowsSelected(self) -> int:
        """Return the number of selected rows"""
        return len(self.selectionModel().selectedRows())

    def updateRow(self, row:int) -> None:
        '''Refresh the display for the given row, reading the data again from sxfile'''
        if row < 0 or row > self.rowCount():
            return
        if row == 0 and self.sxfile.sxItemFirst:
            self.setText(0, 0, "S0")
            self.setText(0, 1, self.sxfile.sxItemFirst.data_quantity)
            self.setText(0, 2, "")
            self.setText(0, 3, self.sxfile.sxItemFirst.data)
            self.setText(0, 4, self.sxfile.sxItemFirst.checksum)
        elif row == self.rowCount() - 1:
            self.setText(row, 0, "S" + self.sxfile.sxItemLast.format[1])
            self.setText(row, 1, self.sxfile.sxItemLast.data_quantity)
            self.setText(row, 2, self.sxfile.sxItemLast.address)
            self.setText(row, 3, self.sxfile.sxItemLast.data)
            self.setText(row, 4, self.sxfile.sxItemLast.checksum)
        else:
            self.setText(row, 0, "S" + self.sxfile.sxItems[row - 1].format[0])
            self.setText(row, 1, self.sxfile.sxItems[row - 1].data_quantity)
            self.setText(row, 2, self.sxfile.sxItems[row - 1].address)
            self.setText(row, 3, self.sxfile.sxItems[row - 1].data)
            self.setText(row, 4, self.sxfile.sxItems[row - 1].checksum)
        self.sigDataModifiedChanged.emit(True)

    def insertItems(self, pos: int, items : Any) -> None:
        """ Insert a list of /items/ in the table"""
        insert_start = 0    # type: int
        if pos == DataTable.ISTART:
            insert_start = 0
        elif pos == DataTable.IBEFORESEL:
            insert_start = min(self.rowSelectedList()) - 1
            if insert_start < 0:
                insert_start = 0
        elif pos == DataTable.IAFTERSEL:
            insert_start = max(self.rowSelectedList())
            if insert_start == self.rowCount() - 1:
                insert_start -= 1
        elif pos == DataTable.IEND:
            insert_start = self.rowCount() - 2
        else:
            QMessageBox.critical(None, "Error !", "Bad argument ! Operation aborted.")
            self.statusBar().showMessage("Insertion aborted")
            return
        old_len = len(self.sxfile.sxItems) # type: int
        items.reverse()
        for i in items:
            self.sxfile.sxItems.insert(insert_start, i)
        self.insertRows(insert_start + 1, len(items))
        for i in range(insert_start + 1,
                       insert_start + len(items) + 1, 1):
            self.updateRow(i)

    def copyLines(self) -> int:
        """Copy the items corresponding to selection in a copy_list"""
        res = 0 # type: int
        self.copy_list = []
        hasFirstItem = int(bool(self.sxfile.sxItemFirst))   # type: int
        if self.isRowSelected(0):
            res += 1
            self.copy_list.append(self.sxfile.sxItemFirst)
        for i in range(0, self.rowCount() - 1, 1):
            if self.isRowSelected(i):
                res += 1
                if i == 0 and hasFirstItem:
                    self.copy_list.append(self.sxfile.sxItemFirst)
                else:
                    self.copy_list.append(self.sxfile.sxItems[i - hasFirstItem])
        if self.isRowSelected(self.rowCount() - 1):
            res += 1
            self.copy_list.append(self.sxfile.sxItemLast)
        return res

    def convertTo(self, format: str) -> int:
        """Convert selected rows to a given format"""
        res = 0 # type: int
        for x in range(1, self.rowCount() - 1): # type: int
            if self.isRowSelected(x):
                res += 1
                self.sxfile.sxItems[x - 1].convert(format)
                self.updateRow(x)
        if self.isRowSelected(self.rowCount() - 1):
            res += 1
            self.sxfile.sxItemLast.convert(format)
            self.updateRow(self.rowCount() - 1)
        return res

    def editRow(self, row:int, data:str) -> None:
        """ Update the contain of an item corresponding to 'row' with given data"""
        if (row == self.rowCount() - 1):
            self.sxfile.sxItemLast.updateData(data.upper())
        else:
            self.sxfile.sxItems[row - 1].updateData(data.upper())
        self.updateRow(row)

    def editSelection(self, data:str) -> None:
        """Edit every row selected with data"""
        for x in range(1, self.rowCount() - 1): # type:int
            if self.isRowSelected(x):
                self.sxfile.sxItems[x - 1].updateData(data.upper())
                self.updateRow(x)
        if self.isRowSelected(self.rowCount() - 1):
            self.sxfile.sxItemLast.updateData(data.upper())
            self.updateRow(self.rowCount() - 1)

    def deleteSelection(self) -> int:
        """Deleted the selected rows excluding first and last rows"""
        l = self.rowSelectedListWithoutFirstAndLast() # Type l: List[int]
        if not l: return 0
        l.sort()
        self.clearSelection()
        self.removeRows(l)
        #   if 0 in l :
        #       l = l[1:]
        #       del self.sxfile.sxItemFirst
        #   last = len(self.sxfile.sxItems) + 1
        #   if last in l :
        #       l = l[:-1]
        #       del self.sxfile.sxItemLast
        for x in l: # type: int
            del self.sxfile.sxItems[x - 1]
        return len(l)

    def pasteLines(self, pasting_mode:int, precise_mode:int) -> int:
        """Paste lines according to some options"""
        pos = 0 # type: int
        if pasting_mode == DataTable.PADD:
            if precise_mode == DataTable.PADD_BEFORE:
                pos = DataTable.IBEFORESEL
            else:
                pos = DataTable.IAFTERSEL
            self.insertItems(pos, self.copy_list)
            return len(self.copy_list)
        else:
            x = 0   # type: int
            last = 1    # type: int
            for i in range(1, self.rowCount() - 1, 1):
                if x >= len(self.copy_list):
                    return x
                if self.isRowSelected(i):
                    self.sxfile.sxItems[i - 1] = self.copy_list[x]
                    x += 1
                    self.updateRow(i)
                    last = i
            if x < len(self.copy_list):
                if not self.isRowSelected(0):
                    last += 1
                if precise_mode == DataTable.PREPLACE_SELONLY:
                    return x + 1
                elif precise_mode == DataTable.PREPLACE_SELREPLACE:
                    for i in range(last, self.rowCount() - 1, 1):
                        if x >= len(self.copy_list):
                            return x
                        self.sxfile.sxItems[i - 1] = self.copy_list[x]
                        self.updateRow(i)
                        x += 1
                    return (x + 1)
                else:
                    self.clearSelection()
                    self.selectRow(last)
                    self.insertItems(DataTable.IAFTERSEL, self.copy_list[x:])
                    return len(self.copy_list)
            return x

    def insertRowsWithData(self, dialog:FormInsertRowValue) -> None:
        """Called after showing the "Insert Rows" dialog. Insert the actual
        data in the view and in the sxfile."""
        start = min(self.rowSelectedList()) # int
        if start == 0:
            start = 1
        self.insertRows(start, dialog.spinNbLines.value())
        format = str(dialog.comboBoxFormat.currentText())   # type: str
        dataLen = dialog.spinRowSize.value()
        data = ('00' * dataLen + dialog.lineEditData.text().upper())[-dataLen*2:]      # type: str
        if dialog.radioPrevContinuity.isChecked():
            if start < 2:
                # no previous address, start at 0
                addr_start = 0
            else:
                addr_start = self.sxfile.sxItems[start-2].addressEndValue()
        elif dialog.radioNextContinuity.isChecked():
            if start == self.rowCount()-dialog.spinNbLines.value()-1:
                # no next line, just use 0
                addr_start = 0
            else:
                addr_start = self.sxfile.sxItems[start-1].addressValue() - dialog.spinNbLines.value()*dataLen
        elif dialog.radioExplicitAddr.isChecked():
            addr_start = str2hexi(dialog.lineAddrStart.text())
        else:
            raise ValueError('No address strategy selected')

        for i in range(start, start + dialog.spinNbLines.value(), 1):
            sx = SxItem(format[1:], "00", SxItem.formatAddress(addr_start, format), "00", "00")   # type: SxItem
            sx.updateData(data)
            self.sxfile.sxItems.insert(i - 1, sx)
            self.updateRow(i)
            addr_start += dataLen

    def applyOffsetOnAddresses(self, offset:Union[str,int]) -> None:
        """Apply an offset on address of every selected row"""
        rows = self.rowSelectedListWithoutFirstAndLast()    # type: List[int]
        for i in rows:
            self.sxfile.sxItems[i - 1].applyOffset(offset)
            self.updateRow(i)

    def applyNewRowSize(self, newRowSize:int, selectedRowStart:int, selectedRowEnd:int) -> None:
        """Adjust the size of the rows is the range (selectedRowStart,
        selectedRowEnd) with selectedRowEnd included"""
        self.sxfile.applyNewRowSize(newRowSize, selectedRowStart - 1, selectedRowEnd - 1)
        self.redisplayTable()
        self.sigDataModifiedChanged.emit(True)

    def splitRow(self, rowList:List[int], offset:int) -> None:
        """Split all the rows in rowList. The row must be given in ascending order"""
        rowOffset = 0   # type: int
        for row in rowList:
            # possible case:
            # - item is smaller or equal to offset asis
            #       => nothing to do
            # - item is splitted
            #       => a new item is inserted after the current one
            #       => skip this new item, it should not be splitted
            if self.sxfile.sxItems[row+rowOffset-1].dataLen() > offset:
                self.sxfile.splitItem(row + rowOffset - 1, offset)
                rowOffset += 1
        self.redisplayTable()
        self.sigDataModifiedChanged.emit(True)

    def mergeRow(self, rowStart:int, rowEnd:int) -> None:
        """Merge the rows of the range (rowStart, rowEnd) (end included)
        together."""
        self.sxfile.mergeItem(rowStart - 1, rowEnd - 1)
        self.redisplayTable()
        self.sigDataModifiedChanged.emit(True)

    def isRowSelected(self, row:int) -> bool:
        indexes = self.selectionModel().selectedRows()
        for index in indexes:
            if row == index.row(): return True
        return False

    def text(self, row:int, col:int) -> str:
        item = self.item(row, col)
        s = str(item.text()) if item else ''
        return s

    def insertRows(self, pos:int, length:int) -> None:
        for i in range(pos, pos + length):
            self.insertRow(i)
        self.sigDataModifiedChanged.emit(True)


    def removeRows(self, rows:List[int]) -> None:
        i = 0
        for row in rows:
            self.removeRow(row - i)
            i += 1
        self.sigDataModifiedChanged.emit(True)

    def flipRows(self) -> None:
        rows = self.rowSelectedListWithoutFirstAndLast()    # type: List[int]
        for x in rows:
            self.sxfile.sxItems[x - 1].flipBits()
        self.redisplayTable()
        self.sigDataModifiedChanged.emit(True)


    def verifyChecksum(self, rows: List[int] ) -> List[ Tuple[int,str,str,str] ]:
        '''Verify the checksum of the rows number given in argument.

        Returns a list of tuple of: row number with a wrong checksum, address, correct checksum, invalid checksum.

        If all checksum are valid, returns an empty list.'''
        ret = [] # type: List[Tuple[int,str,str,str]]
        for r in rows:
            item = self.sxfile.sxItems[r-1]
            if item.calcChecksum() != item.checksum:
                ret.append( (r, item.address, item.calcChecksum(), item.checksum) )
        return ret

    def updateSelectedChecksum(self) -> int:
        invalidChecksumRows = self.verifyChecksum( self.rowSelectedList() )
        for rowNb, address, validChecksum, wrongChecksum in invalidChecksumRows:
            self.sxfile.sxItems[rowNb-1].updateChecksum()
            self.updateRow(rowNb-1)
        return len(invalidChecksumRows)



