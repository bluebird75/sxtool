# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional, List, Dict, Union, TextIO

def str2hex( s:Optional[str] ) -> List[int]:
    '''Convert a string containing hexadecimal values, with possible space and newlines, into a list of corresponding bytes
    Ex: str2hex("1234 5678") -> [ 0x12, 0x34, 0x56, 0x78 ]'''
    if s is None: return []
    norm_s = s.replace(' ', '').replace('\n', '').replace('\t','')  # type: str
    if len(norm_s) % 2 != 0:
        raise ValueError('String contains an odd number of characters, can not convert to hex: "%s"' % norm_s)
    ret = []    # type: List[int]
    for i in range(len(norm_s)//2): # type: int
        sub_s =  norm_s[2*i:2*i+2]
        ret.append( int( sub_s, 16 ) )
    return ret

def hex2str( l:List[int] ) -> str:
    """Convert a list of bytes into a string of hexadecimal values, without space."""
    errors = [ v for v in l if (v >= 0x100 or v < 0) ]  # type: List[int]
    if len(errors):
        raise ValueError('Somes values are not hex bytes: %s' % errors )
    return ''.join( [ '%02X' % v for v in l ])

def xor( v:str, mask:str ) -> str:
    """
    Return v xor mask.

    v: string of hex values
    mask: string of hex values
    if v and mask are of different length, they are left aligned
    returns the xored hex string
    """
    norm_v = v.replace(' ', '') # type: str
    norm_mask = mask.replace(' ', '')   # type: str
    norm_mask = (norm_mask + '0' * len(norm_v))[:len(norm_v)]
    if len(norm_v) % 2:
        raise ValueError('Value has odd number of char: %s' % norm_v)

    assert len(norm_mask) == len(norm_v)

    ret_l = []  # type: List[str]
    for i in range( len(norm_v) // 2 ):
        vi = int( norm_v[i*2:i*2+2], 16)    # type: int
        mi = int( norm_mask[i*2:i*2+2], 16)# type: int
        resulti = ((vi ^ mi) & 0xFF )# type: int
        ret_l.append( "%02X" % resulti )

    return ''.join( ret_l )

def str2hexi( v: str ) -> int:
    """
    Return the int value of the hex string.

    Works also with empty strings
    """
    if v == '':
        return 0
    return int(v, 16)


class SxItemException(Exception): pass

class SxItemBadOutFormat(SxItemException): pass

class SxItemChecksumError(SxItemException): pass
class SxItemBadNewAddress(SxItemException): pass
class SxItemMissingData(SxItemException): pass
class SxItemBadFileFormat(SxItemException): pass
class SxItemBadOffset(SxItemException): pass

def toHexLen(number:Union[int,str], length:int) -> str:
    """
    Return the number converted into hexadecimal, as a string of the length passed in argument.

    toHexLen(0x1234, 6 ) --> '001234' toHexLen('1234', 2 ) --> '34'
    """
    r=''    # type: str
    if type(number) == type(0.0):
        r = hex(int(number))
    elif type(number) == type(0):
        r = hex(number) # type: ignore
    elif type(number) == type(''):
        r = number      # type: ignore
    else: # Bad format
        return ""
    # Delete the prefix "0x"
    if r[0:2] == "0x":
        r = r[2:]
    # and the suffix "L" if there is one (long int)
    if len(r) and r[-1] == 'L':
        r = r[:-1]
    # Delete the prefix '0'
    tmp = r # type: str
    for i in range(len(r) - 1):
        if r[i] != '0': break
        tmp = r[i+1:]
    r = tmp.upper()
    if len(r) > length:
        return r[len(r) - length:]
    prefix = '0'*(length - len(r))
    return prefix + r

class SxItem:
    """
    Design a single line in Sx files.

    All data (format, data_quantity, etc.) are stocked with a string
    format, in an hexadecimal form.
    """
    # Map format to length of address in bytes.
    format_corresp = {    '': 0, 
                        'S0' : 2, 
                        'S1' : 2, 
                        'S9' : 2, 
                        'S2' : 3, 
                        'S8' : 3, 
                        'S3' : 4, 
                        'S7' : 4, 
                        'S5' : 0, 
    }     # type: Dict[str,int]
    
    def __init__(self, format:str, data_qty:str, address:str, data:str, checksum:str):
        """Format is either: S0, S1, S2, S3, S5, S7, S8, S9."""
        if format not in self.format_corresp:
            raise ValueError('No such format: %s' % format)
        self.format = format            # type: str
        self.data_quantity = data_qty   # type: str
        self.address = address          # type: str
        self.data = data                # type: str
        self.checksum = checksum        # type: str
        self.addr_sz = self.format_corresp[self.format] # type: int
        # addr_sz is the length in bytes of the address

    @staticmethod
    def formatAddress( address:int, format:str) -> str:
        """
        Format an address integer according to the format S19, S28, S37.

        Format should be either: S0, S1, S2, S3, S5, S7, S8, S9
        """
        addrFormat = '%dX' % (SxItem.format_corresp[format]*2)
        return ('%0' + addrFormat) % address

    def setContent(self, content:str, lineNb:int = -1 ) -> None:
        """Assign the item content with a line of sx file."""
        self.format = content[0:2]
        if not (self.format in SxItem.format_corresp):
            raise SxItemBadFileFormat( "%s: eroneous file or bad format !" % self.format )
        self.addr_sz = self.format_corresp[self.format]
        self.data_quantity = content[2:4]
        address_length = self.addr_sz*2
        self.address = content[4:4+address_length]
        self.data = content[4+address_length:-2]
        self.checksum = content[-2:]
        if len(content[4:]) != str2hexi(self.data_quantity) * 2:
            raise SxItemMissingData( "%sAddress %s, data is announced as %d bytes but is actually %d bytes!" 
                % (('' if lineNb == -1 else "Line %d," % lineNb), self.address, str2hexi(self.data_quantity), len(content[4:]) // 2) )

    def dataLen(self) -> int:
        """Return the number of hexadecimal bytes in data:
        data='112233' --> dataLen(data) = 3
        """
        return len(self.data)//2

    def addressValue(self) -> int:
        """Integer value of the data address."""
        return str2hexi( self.address )

    def addressEndValue(self) -> int:
        """Integer value of the end data address."""
        return self.addressValue() + self.dataLen()

    def calcChecksum(self) -> str:
        checksum = str2hexi( self.data_quantity )       # type: int
        nb_digits = self.addr_sz                        # type: int
        for i in range(0, nb_digits*2, 2):              # type: int
            checksum += str2hexi( self.address[i:i+2] )
        for i in range(0, (str2hexi( self.data_quantity ) - 1 - nb_digits)*2, 2):
            checksum += str2hexi( self.data[i:i+2] )
        checksum = (~checksum % 256)
        return toHexLen(checksum, 2)      
        
    def updateChecksum(self) -> None:
        """
        Recalculate Checksum according to other values.

        Called when a value has been changed
        """
        self.checksum = self.calcChecksum()

    def updateDataQuantity(self) -> None:
        """Data quantity is len(data) + len(address) + len(checksum)"""
        new_data_quantity = self.addr_sz + len(self.data) // 2 + 1 # type: int
        self.data_quantity = toHexLen(new_data_quantity, 2)

    def updateData(self, new_data:str) -> None:
        self.data = new_data
        self.updateDataQuantity()
        self.updateChecksum()
        
    def updateAddress(self, new_address:str) -> None:
        """new_address must be a valid hexadecimal string."""
        if len(new_address) / 2 > self.addr_sz:
            raise SxItemBadNewAddress( "Invalid address. Too int for format." )
        self.address = toHexLen(new_address, self.addr_sz*2)
        self.updateChecksum()
       
    convertMap = { 
    'S19' : {
        '' :  '',
        'S0' :  'S0',
        'S1' :  'S1',
        'S2' :  'S1',
        'S3' :  'S1',
        'S5' :  'S5',
        'S7' :  'S9',
        'S8' :  'S9',
        'S9' :  'S9',
        },
    'S28' : {
        '' :  '',
        'S0' :  'S0',
        'S1' :  'S2',
        'S2' :  'S2',
        'S3' :  'S2',
        'S5' :  'S5',
        'S7' :  'S8',
        'S8' :  'S8',
        'S9' :  'S8',
        },
    'S37' : {
        '' :  '',
        'S0' :  'S0',
        'S1' :  'S3',
        'S2' :  'S3',
        'S3' :  'S3',
        'S5' :  'S5',
        'S7' :  'S7',
        'S8' :  'S7',
        'S9' :  'S7',
        },
    }

    def convert(self, sx_format:str) -> None:
        """
        Convert an SxItem to another format.

        sx_format must be a string among: 'S19', 'S28' or 'S37'. If not,
        an SxItemBadOutFormat is raised.
        """

        if not (sx_format in ['S19', 'S28', 'S37']):
            raise SxItemBadOutFormat( 'Bad out format: %s' % sx_format )

        to_format = self.convertMap[sx_format][self.format]
        if to_format == self.format:
            return
        # Updating new address.
        self.format = to_format
        self.addr_sz = self.format_corresp[self.format]
        self.address = toHexLen(self.address, self.addr_sz*2)
        self.updateDataQuantity()
        self.updateChecksum()

    def split( self, offset:int ) -> 'SxItem':
        """
        Split the current SxItem into two sxItems, separation happens at offset.

        The current SxItem is modified and the new SxItem following the
        current Item is returned.
        """
        if offset >= self.dataLen() or offset <= 0:
            raise SxItemBadOffset( "Splitting is not possible at offset %d" % offset )
        sx2 = SxItem(self.format,'','','','')        
        sx2.address = toHexLen( self.addressValue() + offset, self.addr_sz*2 )
        sx2.updateData( self.data[offset*2:] )
        self.updateData( self.data[:offset*2] )
        return sx2

    def mergePossible( self, other: 'SxItem' ) -> bool:
        """
        Return true if merging sx with other is possible.

        The merge is possible of sx.address + len(sx.data) ==
        other.address
        """
        return self.addressValue() + self.dataLen() == other.addressValue()

    def merge( self, other: 'SxItem' ) -> None:
        """
        Merge with another sxItem.

        If the merge is not possible, an exception SxItemBadNewAddress
        is raised.
        """
        if not self.mergePossible( other ):
            raise SxItemBadNewAddress( "Can not merge address %s, data len %d with new address %s" % (self.address, self.dataLen(), other.address ) )

        self.data += other.data
        self.updateDataQuantity()
        self.updateChecksum()
        
    def __repr__(self) -> str:
        return self.format + self.data_quantity + self.address + self.data + self.checksum

    def xorData(self, pattern:str) -> None:
        self.data = xor(self.data, pattern) # type: str
        self.updateChecksum()

    def flipBits(self) -> None:
        bytes = str2hex(self.data)  # List[int]
        newBytes = []   # List[int]
        for elem in bytes :
            newBytes.append(255 - elem)
        self.data = hex2str(newBytes)
        self.updateChecksum()
        
    def applyOffset(self, offset: Union[str,int]) -> None:
        ioffset = int(offset)
        new_address = str2hexi( self.address )
        new_address += ioffset
        self.updateAddress(hex(new_address)[2:])
 
    
class SxFile:
    # noinspection PyMissingTypeHints
    def __init__(self) -> None:
        self.clear()

    def getFormat(self) -> str:
        """Return s19, s28, s37 or empty string if no data."""
        if len(self.sxItemsEx) == 0:
            return ''
        lastFmtChar = int(self.sxItemsEx[-1].format[1])
        fmt = 's%d%d' % ((10-lastFmtChar),lastFmtChar)
        return fmt

    def clear(self) -> None:
        self.sxItemFirst = SxItem('','','','','')
        self.sxItemLast  = SxItem('','','','','')
        self.sxItems = []           # type: List[SxItem]
        self.sxItemsEx = []           # type: List[SxItem]

    def syncEx(self) -> None:
        self.sxItemsEx = [ self.sxItemFirst ]
        self.sxItemsEx.extend( self.sxItems )
        self.sxItemsEx.append( self.sxItemLast )
       
    def syncFromEx(self) -> None:
        self.sxItems = self.sxItemsEx[1:-1]
        self.sxItemFirst = self.sxItemsEx[0]
        self.sxItemLast  = self.sxItemsEx[-1]
       
    def __repr__(self) -> str:
        s = ""  # type: str
        if self.sxItemFirst == None: s += 'None\n'
        else: s += repr(self.sxItemFirst) + "\n"
        for item in self.sxItems:   # type: SxItem
            s += repr(item) + "\n"
        if self.sxItemLast == None: s += 'None\n'
        else: s += repr(self.sxItemLast)+ "\n"
        return s

    def __len__(self) -> int:
        return len(self.sxItemsEx)

    def __getitem__(self, idx):
        return self.sxItems[idx]
 
    def fromFile(self, fname: str) -> None:
        f = open(fname, 'r')    # type: TextIO
        self.fromFileStream(f, fname)
        f.close()

    def fromFileStream(self, fileStream: TextIO, fname:str) -> None:
        self.clear()
        lineNb = 1
        line = fileStream.readline().strip()
        while len(line):
            sxItem = SxItem('', '', '', '', '')
            sxItem.setContent( line, lineNb )
            self.sxItems.append(sxItem)
            line = fileStream.readline().strip()
            lineNb += 1

        self.sxItemsEx = self.sxItems[:]

        self.sxItemFirst = self.sxItems.pop(0)
        self.sxItemLast = self.sxItems.pop()

    def toFile(self, file_out:str) -> None:
        f = open(file_out, "w") # type: TextIO
        self.toFileStream(f)
        f.close()

    def toFileStream(self, fileStreamOut: TextIO) -> None:
        """Pretty print every item into file_out."""
        for item in self.sxItemsEx:
            print(item, file=fileStreamOut)

    def updateDataRange(self, new_data:str, range:List[int]) -> None:
        """
        Apply a data update on items at the index given in range.

        Index counts from S1 line (excludes S0) Last index is not
        included in the range
        """
        for item in self.sxItemsEx[range[0]+1:range[1]+1]:
            item.updateData(new_data)
        self.syncFromEx()

    def convertRange(self, new_format:str, range:List[int]) -> None:
        """
        Apply a convert on items at the index given in range.

        Index counts from S1 line (excludes S0) Last index is not
        included in the range
        """
        for item in self.sxItems[range[0]:range[1]]:
            item.convert(new_format)
        self.syncEx()

    def splitItem( self, itemIdx:int, offset:int ) -> None:
        newItem = self.sxItems[itemIdx].split( offset ) # type: SxItem
        self.sxItems.insert( itemIdx+1, newItem )
        self.syncEx()

    def mergeItem( self, itemStart:int, itemEnd:int ) -> None:
        idxOffset = 0   # type: int
        for idx in range(itemStart, itemEnd):
            try:
                self.sxItems[idx+idxOffset].merge( self.sxItems[idx+idxOffset+1] )
                del self.sxItems[idx+idxOffset+1]
                idxOffset -= 1
            except SxItemBadNewAddress:
                continue
        self.syncEx()

    def applyNewRowSize( self, newRowSize:int, itemStart:int, itemEnd:int ) -> None:
        idx = itemStart # type: int
        while idx <= itemEnd:
            if newRowSize > self.sxItems[idx].dataLen():
                # merge must occur first
                if idx+1 <= itemEnd \
                   and self.sxItems[idx].mergePossible( self.sxItems[idx+1] ):
                    self.sxItems[idx].merge( self.sxItems[idx+1] )
                    del self.sxItems[idx+1]
                    itemEnd -= 1

            if newRowSize < self.sxItems[idx].dataLen():
                # split it
                next_item = self.sxItems[idx].split( newRowSize )
                self.sxItems.insert( idx+1, next_item )
                itemEnd += 1

            idx += 1
        self.syncEx()

