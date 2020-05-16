# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information
import os
from typing import List, Optional, TextIO, Any, Tuple, Callable
from functools import wraps

from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, qApp, QFileDialog, QWidget, QGridLayout, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt

from src.gui.ui_main_form import Ui_MainForm
from src.data_table import DataTable
from src.insert_dialog import InsertDialog
from src.paste_dialog import PasteDialog
from src.form_insert_row_value import FormInsertRowValue
from src.form_set_row_size import FormSetRowSize
from src.form_split_item import FormSplitItem
from src.xor_dialog import XorDialog
from src.sx_file import SxFile
from src.utils import ItemHistoryMenu, ItemHistoryStringList

from src.const import VERSION, ABOUT_INFO

SX_FILES_PATTERNS = "SX files (*.s19 *.s28 *.s37 *.sx *.s3)"

def ensureAnyLinesAreSelected(f: Callable[['MainForm'], None]) -> Callable[['MainForm'], None]:
    @wraps(f)
    def wrapper(self: 'MainForm') -> None:
        if self.dataTable.numRowsSelected() == 0:
            QMessageBox.warning(self, "No selection", "You must select lines before applying this operation, aborting." )
            return
        return f(self)
    return wrapper

def ensureDataLinesAreSelected(f: Callable[['MainForm'], None]) -> Callable[['MainForm'], None]:
    @wraps(f)
    def wrapper(self: 'MainForm') -> None:
        selRows = [ v.row() for v in self.dataTable.selectionModel().selectedRows() ]
        if 0 in selRows or self.dataTable.rowCount()-1 in selRows:
            QMessageBox.warning(self, "First or last line selected", "This operation does not work on first or last lines, aborting." )
            return
        return f(self)
    return wrapper

class MainForm(Ui_MainForm, QMainWindow): # type: ignore # PyQt and Mypy don't mix very well
    def __init__(self,parent: Optional[QWidget] = None, name:str = "SX Tool", fl: int = 0, file: Optional[str] = None) -> None:
        QMainWindow.__init__(self)
        Ui_MainForm.__init__(self)
        self.setupUi(self) # type: ignore # PyQt and Mypy don't mix very well
        self.setObjectName(name)
        self.setProgramTitle(None, False)
        self.dataTable = DataTable( self, "EmptyDataTable")  # type: DataTable
        self.layoutWidget = QWidget(self)
        self.layoutWidget.gridLayout = QGridLayout(self.layoutWidget)
        self.layoutWidget.gridLayout.addWidget(self.dataTable, 0, 0)
        self.setCentralWidget(self.layoutWidget)
        self.lastDir = []   # type: List[str]
        self.menuHistory = ItemHistoryMenu(fileName="open_recent_history.xml", maxSize=10, 
                                menu=self.menuOpenRecent, callbackMethod=self.loadFile)
        self.dirHistory = ItemHistoryStringList(fileName="last_dir.xml", maxSize=1, stringList=self.lastDir)
        if not self.lastDir :
            self.dirHistory.addItemToHistory('.')
            self.dirHistory.save()
        self.actionList = [
            self.insertAction,
            self.saveAction,
            self.saveasAction,
            self.copyAction,
            self.cutAction,
            self.deleteAction,
            self.convertToAction,
            self.convertToS19Action,
            self.convertToS28Action,
            self.convertToS37Action,
            self.selectallAction,
            self.insertRowAction,
            self.deleteRowAction,
            self.editDataAction,
            self.convertToS19Action,
            self.convertToS28Action,
            self.convertToS37Action,
            self.applyOffsetAction,
            self.mergeRowsAction,
            self.splitRowAction,
            self.setRowSizeAction,
            self.xorRowAction,
            self.flipBitsAction
        ]# type: List[Any]
        
        if file: 
            self.loadFile( file )

    def slotQuit(self) -> None:
        qApp.quit()
        
    def slotOpen(self) -> None:
        self.statusBar().showMessage("Opening file ...")
        # noinspection PyCallByClass,PyCallByClass
        fname, selectedFilter = QFileDialog.getOpenFileName(self, "Choose file", '', SX_FILES_PATTERNS)  # type: str, str
        if not fname :
            self.statusBar().showMessage("Loading aborted.")
        else:
            # TODO: refactor to use pathlib
            lastSlash = fname.rfind('/')    # type: int
            self.dirHistory.addItemToHistory(fname[0:lastSlash])
            self.dirHistory.save()
            if self.loadFile( fname ) :
                self.menuHistory.addItemToHistory( fname )
                self.menuHistory.save()

    def loadFile(self, fname : str) -> bool:
        self.setProgramTitle(None, False)
        self.dataTable = DataTable( self, "DataTable")
        self.layoutWidget.gridLayout.addWidget(self.dataTable, 0, 0)
        res = self.dataTable.loadFile( fname )
        if not res :
            self.statusBar().showMessage("File %s could not be opened" % fname)
            return False
        self.setProgramTitle(fname, False)
        for a in self.actionList:
            a.setEnabled( True )
        self.dataTable.itemDoubleClicked.connect( self.slotEditRowData )
        self.dataTable.sigDataModifiedChanged.connect( self.slotFileModifiedChanged )
        self.statusBar().showMessage("File %s opened" % fname)
        deskSize = qApp.desktop().availableGeometry(qApp.desktop().screen())
        # only take 80% of the screen in best case
        reasonableSize = int(deskSize.width()*0.8),int(deskSize.height()*0.8)
        szHint = self.sizeHint()
        # sizeHint needs a little margin to account for ... I don't know exactly what
        goodSize = int(szHint.width()*1.1),int(szHint.height()*1.1)
        self.resize(min(goodSize[0],reasonableSize[0]),min(goodSize[1],reasonableSize[1]))
        return True

    def slotInsert(self) -> None:
        self.statusBar().showMessage("Inserting file ...")
        fname, filterName = QFileDialog.getOpenFileName(self, "Insert file", self.lastDir[0], SX_FILES_PATTERNS ) # type: str, str
        if not fname or len(fname) == 0:
            self.statusBar().showMessage("Insertion aborted.")
            return
        self.dirHistory.addItemToHistory( os.path.split(fname)[0])
        self.dirHistory.save()
        self.insertFname(fname)

    def insertFname(self, fname:str, mockDialog: Optional[QDialog]=None) -> None:
        '''fname: file name to insert.
        mockDialog: not used by the application, used only for testing.'''
        sxtmp = SxFile()
        sxtmp.fromFile(fname)
        dialog = mockDialog or InsertDialog(self) # trick to allow mocking the dialog
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        pos = 0 # type: int
        if dialog.exec_() == QDialog.Accepted:
            if dialog.radioStart.isChecked():
                pos = DataTable.ISTART
            elif dialog.radioBeforeCurrent.isChecked():
                pos = DataTable.IBEFORESEL
            elif dialog.radioAfterCurrent.isChecked():
                pos = DataTable.IAFTERSEL
            else:
                pos = DataTable.IEND
            self.dataTable.insertItems(pos, sxtmp.sxItems)
            self.statusBar().showMessage("File %s successfully inserted !" % str(fname))
        else:
            self.statusBar().showMessage("Insertion aborted")
            

    def slotSave(self) -> bool:
        self.statusBar().showMessage("Saving...")
        if not self.dataTable:
            QMessageBox.critical(None, "Internal Error o_O", "An internal error occured.")
            return False
        try:
            self.dataTable.sxfile.toFile( self.dataTable.file )
        except Exception as e:
            QMessageBox.critical(None, "Error !", repr(e))
            return False
        self.statusBar().showMessage("File %s successfully saved !" % self.dataTable.file)
        self.setProgramTitle( self.dataTable.file, False )
        return True


    def slotSaveAs(self) -> None:
        self.statusBar().showMessage("Saving as ...")
        if not self.dataTable:
            QMessageBox.critical(None, "Internal Error o_O", "An internal error occured.")
            return
        fname, filterName = QFileDialog.getSaveFileName(self, "Save file as", self.lastDir[0], SX_FILES_PATTERNS ) # type: str, str
        if not fname : return
        prevName = self.dataTable.file
        self.dataTable.file = fname
        if self.slotSave():
            self.dirHistory.addItemToHistory(os.path.split(fname)[0])
            self.dirHistory.save()
        else:
            self.dataTable.file = prevName

    @ensureDataLinesAreSelected
    def slotCopy(self) -> None:
        i = self.dataTable.copyLines()  # type: int
        self.pasteAction.setEnabled( i > 0 )
        self.statusBar().showMessage("%d lines copied" % i)

    @ensureDataLinesAreSelected
    def slotCut(self) -> None:
        self.slotCopy()
        self.dataTable.deleteSelection()
        self.pasteAction.setEnabled(1)

    def slotPaste(self) -> None:
        dialog = PasteDialog(self)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        ok = dialog.exec_() # type: bool
        if not ok:
            self.statusBar().showMessage("Paste aborted")
            return
        pasting_mode, precise_mode = 0,0    # tpye: int,int
        if dialog.radioAddLines.isChecked():
            pasting_mode = DataTable.PADD
            if dialog.radioBeforeSelection.isChecked():
                precise_mode = DataTable.PADD_BEFORE
            else:
                precise_mode = DataTable.PADD_AFTER
        else:
            # replace pasting mode
            pasting_mode = DataTable.PREPLACE
            if dialog.radioSelectionOnly.isChecked():
                precise_mode = DataTable.PREPLACE_SELONLY
            elif dialog.radioSelectionAndAdd.isChecked():
                precise_mode = DataTable.PREPLACE_SELADD
            else:
                precise_mode = DataTable.PREPLACE_SELREPLACE

        res = self.dataTable.pasteLines(pasting_mode, precise_mode) # type: int
        self.statusBar().showMessage("Pasted %d lines" % res)

    @ensureDataLinesAreSelected
    def slotDelete(self) -> None:
        i = self.dataTable.numRowsSelected()    # type: int
        # noinspection PyTypeChecker
        answer = QMessageBox.question( self, "Are you sure ?", "Delete these %d lines ?" % i, QMessageBox.Yes , QMessageBox.No)
        if answer == QMessageBox.No:
            self.statusBar().showMessage("Deletion aborted")
            return
        j = self.dataTable.deleteSelection()
        self.statusBar().showMessage("%d lines deleted", j)

    def slotSelectAll(self) -> None:
        for x in range(self.dataTable.rowCount()): # type: int
            if not self.dataTable.isRowSelected(x):
                self.dataTable.selectRow(x)
        self.statusBar().showMessage("%d lines selected" % self.dataTable.rowCount())

    def slotConvertToS19(self) -> None:
        i = self.dataTable.convertTo('S19')
        self.statusBar().showMessage("Converted %d lines to format S19" % i)

    def slotConvertToS28(self) -> None:
        i = self.dataTable.convertTo('S28')
        self.statusBar().showMessage("Converted %d lines to format S28" % i)

    def slotConvertToS37(self) -> None:
        i = self.dataTable.convertTo('S37')
        self.statusBar().showMessage("Converted %d lines to format S37" % i)

    def slotInsertRow(self) -> None:
        default_format = str(self.dataTable.text(self.dataTable.rowCount() - 1, 0))
        default_format = default_format[0] + str(10 - int(default_format[1])) + default_format[1]
        dialog = FormInsertRowValue(default_format)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        if not dialog.exec_():
            self.statusBar().showMessage("Insert aborted")
            return
        self.dataTable.insertRowsWithData(dialog)        
        self.statusBar().showMessage("%d lines inserted" % dialog.spinNbLines.value() )

    @ensureDataLinesAreSelected
    def slotDeleteRow(self) -> None:
        self.slotDelete()

    @ensureDataLinesAreSelected
    def slotEditData(self) -> None:
        '''Called when selecting menu item Edit Data. Multiple lines or no lines may be selected'''
        text = "" # type: str
        if self.dataTable.numRowsSelected() == 1:
            text = self.dataTable.text(min(self.dataTable.rowSelectedList()), 3)
        val = QInputDialog.getText( self,
            "Enter new data for row(s)", "Enter new data:", QLineEdit.Normal,
            text) # type: Tuple[str,bool]
        text = val[0]
        ok   = val[1]   # type: bool
        if len(text) % 2 != 0:
            QMessageBox.critical(None, "Problem !", "Length of data must be even !")
            self.statusBar().showMessage("Do you know what you are really doing ?")
            return
        if ok:
            try:
                self.dataTable.editSelection(text)
            except ValueError as e:
                QMessageBox.critical(None, "Problem !", "Value must be HEXADECIMAL")
                self.statusBar().showMessage("Do you know what you are really doing ?")
            self.statusBar().showMessage("Data updated !")

    def slotEditRowData(self, item:Any) -> None:
        '''Called after double-click on a row. Always one row selected'''
        row = item.row()    # type: int
        item = self.dataTable.item(row, 3)
        val = QInputDialog.getText(
            self, "Enter new data for row(s)", "Enter new data:", QLineEdit.Normal,
            item.text(), flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint)    # type: Tuple[str,bool]
            # note: flags are ignored... dunno why but this triggers the help
            # title button to show up on Windows 10
        text = val[0]
        if not val[1]:
            return
        if len(text) % 2 != 0:
            QMessageBox.critical(None, "Problem !", "Length of data must be even !")
            self.statusBar().showMessage("Do you really know what you are doing ?")
            return
        try:
            self.dataTable.editRow(row, text) 
        except ValueError as e:
            QMessageBox.critical(None, "Problem !", "Value must be HEXADECIMAL")
            self.statusBar().showMessage("Do you really know what you are doing ?")
            return
        self.statusBar().showMessage("Data updated !")

    @ensureDataLinesAreSelected
    def slotApplyOffset(self) -> None:
        self.statusBar().showMessage("Applying offset...")
        val = QInputDialog.getInt(self, "Which Offset ?", "Which offset do you want to apply to addresses ?", 1,
                flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint)    # type: Tuple[int,bool]
        if not val[1] or not val[0]:
            self.statusBar().showMessage("Apply offset aborted")
            return
        self.dataTable.applyOffsetOnAddresses(val[0])
        self.statusBar().showMessage("Offset %s has been applied" % hex(val[0]))

    @ensureDataLinesAreSelected
    def slotSetRowSize(self) -> None:
        if not self.dataTable.isSelectionContinuus():
            QMessageBox.critical( self, "Non continuus selection", 
            "You must select one range of row for this action to work"
            )
            return
        rowList = self.dataTable.rowSelectedList()  # type: List[int]
        dialog = FormSetRowSize( self )
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setInitialData( self.dataTable.sxfile.sxItems[rowList[0]-1].data )
        if not dialog.exec_(): return
        newRowSize = dialog.spinRowSize.value()     # type: int
        self.dataTable.applyNewRowSize( newRowSize, rowList[0], rowList[-1] )

    @ensureDataLinesAreSelected
    def slotSplitRow(self) -> None:
        dialog = FormSplitItem( self )
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        allRowList = self.dataTable.rowSelectedList()  # type: List[int]
        rowList = [ r for r in allRowList if 0 < r < 1+len(self.dataTable.sxfile.sxItems) ]
        if len(allRowList) > len(rowList) and len(rowList) == 0:
            QMessageBox.warning( self, "Split not applicable",
                                  "You can not split first and last row",
                                  )
        if not rowList : return
        dialog.setInitialData( self.dataTable.sxfile.sxItems[rowList[0]-1].data )
        if not dialog.exec_(): return
        offset = dialog.spinRowOffset.value()   # type: int
        self.dataTable.splitRow( rowList, offset )

    def slotMergeRows(self) -> None:
        # no need for decorator ensureDataLinesAreSelected decorator, verification done inside the method
        if self.dataTable.numRowsSelected() < 2:
            QMessageBox.warning(self, "Not enough lines", "You must select at least two line to merge them!")
            return

        if not self.dataTable.isSelectionContinuus():
            # noinspection PyCallByClass
            QMessageBox.critical( self, "Non continuus selection",
            "You must select one range of row for this action to work"
            )
            return
        rowList = self.dataTable.rowSelectedList()  # type: List[int]
        self.dataTable.mergeRow( rowList[0], rowList[-1] )

    def slotAbout(self) -> None:
        QMessageBox.about(self, "SXFiles Manipulator",
            ABOUT_INFO )

    @ensureDataLinesAreSelected
    def slotXorRow(self) -> None:
        rows = self.dataTable.rowSelectedListWithoutFirstAndLast()  # type: List[int]
        maxLen = max( len(self.dataTable.sxfile.sxItems[x-1].data) for x in rows )
        if len(rows) == 1 :
            dialog = XorDialog(self, modal=True, multiLines=False, maxLen=maxLen)
            dialog.setData(self.dataTable.sxfile.sxItems[rows[0]-1].data)
        elif len(rows) > 1 :
            dialog = XorDialog(self, modal=True, multiLines=True, maxLen=maxLen )
        else : return
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        if not dialog.exec_(): return
        mask = dialog.maskLineEdit.text()  # type: str
        for x in rows:
            self.dataTable.sxfile.sxItems[x - 1].xorData(mask)
        self.dataTable.redisplayTable()

    @ensureDataLinesAreSelected
    def slotFlipBits(self) -> None:
        self.dataTable.flipRows()

    def setProgramTitle(self, fname:Optional[str], modified:bool) -> None:
        s = "SX Files Manipulator - v%s" % VERSION  # type: str
        if fname:
            s += ' - %s' % fname
        if modified:
            s += ' *'
        self.setWindowTitle(s)

    def slotFileModifiedChanged(self, modified: bool) -> None:
        self.setProgramTitle( self.dataTable.file, modified)

    @ensureAnyLinesAreSelected
    def slotVerifyChecksum(self) -> None:
        rows = self.dataTable.rowSelectedList()
        invalidChecksumRows = self.dataTable.verifyChecksum( rows )
        if len(invalidChecksumRows):
            msgList = []
            # show only the 10 first messages
            for rowNb, address, validChecksum, wrongChecksum in invalidChecksumRows:
                msgList.append( 'Invalid checksum for address %s (line %d): got %s instead of %s' % (address, rowNb+1, wrongChecksum, validChecksum) )
            if len(invalidChecksumRows) > 10:
                msgList.append('...')
            QMessageBox.warning(self, "Checksum verification failed", "Checksums verification failed!\n\n" + "\n".join(msgList) )
        else:
            if len(rows) > 1:
                msg = "Checksums of all %d lines are valid!" % len(rows)
            else:
                msg = "Checksums of the line is valid!"
            QMessageBox.information(self, "Checksum verification success", msg )

    @ensureAnyLinesAreSelected
    def slotRecalculateChecksum(self) -> None:
        nbInvalidChecksums = self.dataTable.updateSelectedChecksum()
        if nbInvalidChecksums > 0:
            QMessageBox.information(self, "Checksum recalculation", "%d checksums adjusted." % nbInvalidChecksums )
        else:
            QMessageBox.information(self, "Checksum recalculation", "All checksums were already valid")

