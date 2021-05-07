from typing import TextIO, List

from src.sx_item import SxItem, SxItemBadNewAddress


class SxFile:
    # noinspection PyMissingTypeHints
    def __init__(self) -> None:
        self.clear()

    def getFormat(self) -> str:
        """Return s19, s28, s37 or empty string if no data"""
        if len(self.sxItemsEx) == 0:
            return ''
        lastFmtChar = int(self.sxItemsEx[-1].format[1])
        fmt = 's%d%d' % ((10 - lastFmtChar), lastFmtChar)
        return fmt

    def clear(self) -> None:
        self.sxItemFirst = SxItem('', '', '', '', '')
        self.sxItemLast = SxItem('', '', '', '', '')
        self.sxItems = []           # type: List[SxItem]
        self.sxItemsEx = []           # type: List[SxItem]

    def syncEx(self) -> None:
        self.sxItemsEx = [self.sxItemFirst]
        self.sxItemsEx.extend(self.sxItems)
        self.sxItemsEx.append(self.sxItemLast)

    def syncFromEx(self) -> None:
        self.sxItems = self.sxItemsEx[1:-1]
        self.sxItemFirst = self.sxItemsEx[0]
        self.sxItemLast = self.sxItemsEx[-1]

    def __repr__(self) -> str:
        s = ''  # type: str
        if self.sxItemFirst == None:
            s += 'None\n'
        else:
            s += repr(self.sxItemFirst) + '\n'
        for item in self.sxItems:   # type: SxItem
            s += repr(item) + '\n'
        if self.sxItemLast == None:
            s += 'None\n'
        else:
            s += repr(self.sxItemLast) + '\n'
        return s

    def __len__(self) -> int:
        return len(self.sxItemsEx)

    def __getitem__(self, idx):
        return self.sxItems[idx]

    def fromFile(self, fname: str) -> None:
        f = open(fname, 'r')    # type: TextIO
        self.fromFileStream(f, fname)
        f.close()

    def fromFileStream(self, fileStream: TextIO, fname: str) -> None:
        self.clear()
        lineNb = 1
        line = fileStream.readline().strip()
        while len(line):
            sxItem = SxItem('', '', '', '', '')
            sxItem.setContent(line, lineNb)
            self.sxItems.append(sxItem)
            line = fileStream.readline().strip()
            lineNb += 1

        self.sxItemsEx = self.sxItems[:]

        self.sxItemFirst = self.sxItems.pop(0)
        self.sxItemLast = self.sxItems.pop()

    def toFile(self, file_out: str) -> None:
        f = open(file_out, 'w')   # type: TextIO
        self.toFileStream(f)
        f.close()

    def toFileStream(self, fileStreamOut: TextIO) -> None:
        """ Pretty print every item into file_out"""
        for item in self.sxItemsEx:
            print(item, file=fileStreamOut)

    def updateDataRange(self, new_data: str, range: List[int]) -> None:
        """Apply a data update on items at the index given in range.
        Index counts from S1 line (excludes S0)
        Last index is not included in the range"""
        for item in self.sxItemsEx[range[0] + 1 : range[1] + 1]:
            item.updateData(new_data)
        self.syncFromEx()

    def convertRange(self, new_format: str, range: List[int]) -> None:
        """Apply a convert on items at the index given in range.
        Index counts from S1 line (excludes S0)
        Last index is not included in the range"""
        for item in self.sxItems[range[0] : range[1]]:
            item.convert(new_format)
        self.syncEx()

    def splitItem(self, itemIdx: int, offset: int) -> None:
        newItem = self.sxItems[itemIdx].split(offset)   # type: SxItem
        self.sxItems.insert(itemIdx + 1, newItem)
        self.syncEx()

    def mergeItem(self, itemStart: int, itemEnd: int) -> None:
        idxOffset = 0   # type: int
        for idx in range(itemStart, itemEnd):
            try:
                self.sxItems[idx + idxOffset].merge(self.sxItems[idx + idxOffset + 1])
                del self.sxItems[idx + idxOffset + 1]
                idxOffset -= 1
            except SxItemBadNewAddress:
                continue
        self.syncEx()

    def applyNewRowSize(self, newRowSize: int, itemStart: int, itemEnd: int) -> None:
        idx = itemStart   # type: int
        while idx <= itemEnd:
            if newRowSize > self.sxItems[idx].dataLen():
                # merge must occur first
                if idx + 1 <= itemEnd and self.sxItems[idx].mergePossible(self.sxItems[idx + 1]):
                    self.sxItems[idx].merge(self.sxItems[idx + 1])
                    del self.sxItems[idx + 1]
                    itemEnd -= 1

            if newRowSize < self.sxItems[idx].dataLen():
                # split it
                next_item = self.sxItems[idx].split(newRowSize)
                self.sxItems.insert(idx + 1, next_item)
                itemEnd += 1

            idx += 1
        self.syncEx()
