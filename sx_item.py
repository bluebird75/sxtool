# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

from typing import Optional, List, Dict, Union, TextIO

def str2hex( s:Optional[str] ) -> List[int]:
    '''Convert a string containing hexadecimal values, with possible space and newlines, into a list of corresponding bytes
    Ex: str2hex("1234 5678") -> [ 0x12, 0x34, 0x56, 0x78 ]'''
    if s == None: return []
    norm_s = s.replace(' ', '').replace('\n', '').replace('\t','')  # type: str
    if len(norm_s) % 2 != 0:
        raise ValueError('String contains an odd number of characters, can not convert to hex: "%s"' % norm_s)
    ret = []    # type: List[int]
    for i in range(len(norm_s)//2): # type: int
        sub_s =  norm_s[2*i:2*i+2]
        ret.append( int( sub_s, 16 ) )
    return ret

def hex2str( l:List[int] ) -> str:
    '''Convert a list of bytes into a string of hexadecimal values, without space'''
    errors = [ v for v in l if (v >= 0x100 or v < 0) ]  # type: List[int]
    if len(errors):
        raise ValueError('Somes values are not hex bytes: %s' % errors )
    return ''.join( [ '%02X' % v for v in l ])

def xor( v:str, mask:str ) -> str:
    '''Return v xor mask.

    v: string of hex values
    mask: string of hex values
    if v and mask are of different length, they are left aligned
    returns the xored hex string'''
    norm_v = v.replace(' ', '') # type: str
    norm_mask = mask.replace(' ', '')   # type: str
    norm_mask = (norm_mask + '0' * len(norm_v))[:len(norm_v)]   # type: str
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
    '''Return the int value of the hex string. Works also with empty strings'''
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
    """Return the number converted into hexadecimal, as a string of the length
    passed in argument.

    toHexLen(0x1234, 6 ) --> '001234'
    toHexLen('1234', 2 ) --> '34'
    """
    r=''    # type: str
    if type(number) == type(0.0):
        r = hex(int(number))
    elif type(number) == type(0):
        r = hex(number)
    elif type(number) == type(''):
        r = number
    else: # Bad format
        return ""
    # Delete the prefix "0x"
    if r[0:2] == "0x":
        r = r[2:]
    # and the suffix "L" if there is one (long int)
    if r[-1] == 'L':
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
    """ Design a single line in Sx files.
    All data (format, data_quantity, etc.) are stocked with a string
    format, in an hexadecimal form.
    """
    # Map format to length of address in bytes.
    format_corresp = {'19' : 2, '28' : 3, '37' : 4}     # type: Dict[str,int]
    
    def __init__(self, format:str, data_qty:str, address:str, data:str, checksum:str):
        self.format = format            # type: str
        self.data_quantity = data_qty   # type: str
        self.address = address          # type: str
        self.data = data                # type: str
        self.checksum = checksum        # type: str

    @staticmethod
    def formatAddress( address:int, format:str) -> str:
        '''Format an address integer according to the format S19, S28 or S37'''
        addrFormat = '%dX' % (SxItem.format_corresp[format[1:]]*2)
        return ('%0' + addrFormat) % address

    def setContent(self, content:str ) -> None:
        """Assign the item content with a line of sx file"""
        s2format = {
            'S1': '19',
            'S2': '28',
            'S3': '37',
        }
        self.format = s2format[ content[0:2] ]
        self.data_quantity = content[2:4]
        address_length = SxItem.format_corresp[self.format] * 2 # type: int
        self.address = content[4:4+address_length]
        self.data = content[4+address_length:-2]
        self.checksum = content[-2:]

    def dataLen(self) -> int:
        """Return the number of hexadecimal bytes in data:
        data='112233' --> dataLen(data) = 3
        """
        return len(self.data)//2

    def isValid(self) -> bool:
        """Return true of the content makes sense:
        - address length matches the format
        - data length matches quantity
        - checksum is correct
        """
        try:
            if str2hexi(  self.data_quantity ) != len(self.address+self.data+self.checksum)//2 : return False

            if self.calcChecksum() != self.checksum: return False
            
            if len(self.address) != 2*SxItem.format_corresp[self.format]: return False 

        except (ValueError, IndexError):
            return False
        return True

    def addressValue(self) -> int:
        '''Integer value of the data address'''
        return str2hexi( self.address )

    def addressEndValue(self) -> int:
        '''Integer value of the end data address'''
        return self.addressValue() + self.dataLen()

    def calcChecksum(self) -> str:
        checksum = str2hexi( self.data_quantity )       # type: int
        nb_digits = SxItem.format_corresp[self.format]  # type: int
        for i in range(0, nb_digits*2, 2):              # type: int
            checksum += str2hexi( self.address[i:i+2] ) # type: int
        for i in range(0, (str2hexi( self.data_quantity ) - 1 - nb_digits)*2, 2):   # type: int
            checksum += str2hexi( self.data[i:i+2] )
        checksum = (~checksum % 256)
        return toHexLen(checksum, 2)      
        
    def updateChecksum(self) -> None:
        """ Recalculate Checksum according to other values.
        Called when a value has been changed
        """
        self.checksum = self.calcChecksum()

    def updateDataQuantity(self) -> None:
        """Data quantity is len(data) + len(address) + len(checksum)"""
        new_data_quantity = SxItem.format_corresp[self.format] + len(self.data) // 2 + 1 # type: int
        self.data_quantity = toHexLen(new_data_quantity, 2)

    def updateData(self, new_data:str) -> None:
        self.data = new_data
        self.updateDataQuantity()
        self.updateChecksum()
        
    def updateAddress(self, new_address:str) -> None:
        """new_address must be a valid hexadecimal string"""
        if len(new_address) / 2 > SxItem.format_corresp[self.format]:
            raise SxItemBadNewAddress( "Invalid address. Too int for format." )
        self.address = toHexLen(new_address, SxItem.format_corresp[self.format]*2)
        self.updateChecksum()
        
    def convert(self, to_format:str) -> None:
        """Convert an SxItem to another format.
        to_format must be a string among: '19', '28' or '37'.
        If not, an SxItemBadOutFormat is raised.
        """
        if not (to_format in SxItem.format_corresp):
            raise SxItemBadOutFormat( 'Bad out format: %s' % to_format )
        if to_format == self.format:
            return
        # Updating new address.
        self.address = toHexLen(self.address, SxItem.format_corresp[to_format]*2)
        self.format = to_format
        self.updateDataQuantity()
        self.updateChecksum()

    def split( self, offset:int ) -> 'SxItem':
        """Split the current SxItem into two sxItems, separation happens 
        at offset. The current SxItem is modified and the new SxItem following
        the current Item is returned."""
        if offset >= self.dataLen() or offset <= 0:
            raise SxItemBadOffset( "Splitting is not possible at offset %d" % offset )
        sx2 = SxItem('','','','','')        
        sx2.format = self.format
        sx2.address = toHexLen( self.addressValue() + offset, 
            SxItem.format_corresp[self.format]*2 )
        sx2.updateData( self.data[offset*2:] )
        self.updateData( self.data[:offset*2] )
        return sx2

    def mergePossible( self, other:'SxItem' ) -> bool:
        """Return true if merging sx with other is possible. The merge 
        is possible of sx.address + len(sx.data) == other.address
        """
        return self.addressValue() + self.dataLen() == other.addressValue()

    def merge( self, other: 'SxItem' ) -> None:
        """Merge with another sxItem. If the merge is not possible, an
        exception SxItemBadNewAddress is raised.
        """
        if not self.mergePossible( other ):
            raise SxItemBadNewAddress( "Can not merge address %s, data len %d with new address %s" % (self.address, self.dataLen(), other.address ) )

        self.data += other.data
        self.updateDataQuantity()
        self.updateChecksum()
        
    def __repr__(self) -> str:
        return 'S' + self.format[0] + self.data_quantity + self.address + self.data + self.checksum

    def toOneString(self) -> str:
        s = "%s %s %s %s %s" % (
            str(self.format), str(self.data_quantity), str(self.address), str(self.data), str(self.checksum) )  # type: str
        return s

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
        
    def applyOffset(self, offset:str) -> None:
        offset = int(offset)    # type: int
        new_address = str2hexi( self.address )
        new_address += offset
        self.updateAddress(hex(new_address)[2:])
 
    
# First and last lines of a Sx file are special.
class SxItemLast(SxItem):
    def __repr__(self) -> str:
        return 'S9' + self.data_quantity + self.address + self.data + self.checksum

class SxItemFirst(SxItem):
    def __init__(self, data_quantity:str, data:str, checksum:str):
        self.data_quantity = data_quantity  # type: str
        self.data = data  # type: str
        self.checksum = checksum  # type: str
        
    def __repr__(self) -> str:
        return 'S0' + self.data_quantity + self.data + self.checksum


class SxFile:
    # noinspection PyMissingTypeHints
    def __init__(self):
        self.sxItemFirst = None     # type: Optional[SxItemFirst]
        self.sxItemLast = None      # type: Optional[SxItemLast]
        self.sxItems = []           # type: List[SxItem]
       
    def __repr__(self) -> str:
        s = ""  # type: str
        if self.sxItemFirst == None: s += 'None\n'
        else: s += self.sxItemFirst.toOneString() + "\n"
        for item in self.sxItems:   # type: SxItem
            s += item.toOneString() + "\n"
        if self.sxItemLast == None: s += 'None\n'
        else: s += self.sxItemLast.toOneString() + "\n"
        return s
 
    def fromFile(self, fname: str) -> None:
        self.sxItemFirst = None
        f = open(fname, 'r')    # type: TextIO
        self.fromFileStream(f, fname)
        f.close()

    def fromFileStream(self, fileStream: TextIO, fname:str) -> None:
        line = fileStream.readline()[:-1]   # type: str
        lineNb = 1
        if line[1] == '0':
            # optional S0 record
            data_qt = str2hexi( line[2:4] ) # type: int
            if len(line[4:]) != data_qt * 2:
                raise SxItemMissingData( "S0 line: data is announced as %d bytes but is actually %d bytes!" % (data_qt, len(line[4:]) // 2) )
            self.sxItemFirst = SxItemFirst(line[2:4], line[4:-2], line[-2:])

            line = fileStream.readline()[:-1]   # type: str
            lineNb += 1

        # Read every line starting with S{1,2,3}. Last line starts with S{9,8,7}
        while line[1] in ['1','2','3']:
            format = line[1] + str(10 - int(line[1]))   # type: str
            if not (format in SxItem.format_corresp):
                raise SxItemBadFileFormat( "%s: eroneous file or bad format !" % fname )
            data_qt = str2hexi( line[2:4] ) # type: int
            if len(line[4:]) != data_qt * 2:
                raise SxItemMissingData( "line %d: data is announced as %d bytes but is actually %d bytes!" % (lineNb, data_qt, len(line[4:]) // 2) )
            address = line[4:4+SxItem.format_corresp[format]*2] # type: str
            data = line[4+SxItem.format_corresp[format]*2:-2]   # type: str
            checksum = line[-2:] # type: str
            self.sxItems.append(SxItem(format, toHexLen(data_qt, 2), address, data, checksum))

            line = fileStream.readline()[:-1]
            lineNb += 1

        format = str(10 - int(line[1])) + line[1]   # type: str
        data_qt = line[2:4] # type: str
        address = line[4:4+SxItem.format_corresp[format]*2] # type: str
        data = line[4+SxItem.format_corresp[format]*2:-2]   # type: str
        checksum = line[-2:]    # type: str
        self.sxItemLast = SxItemLast(format, data_qt, address, data, checksum)

    def toFile(self, file_out:str) -> None:
        """ Pretty print every item into file_out"""
        f = open(file_out, "w") # type: TextIO
        if self.sxItemFirst:
            print(self.sxItemFirst, file=f)
        for item in self.sxItems:
            print(item, file=f)
        print(self.sxItemLast, file=f)
        f.close()

    def updateDataRange(self, new_data:str, range:List[int]) -> None:
        for item in self.sxItems[range[0]:range[1]]:
            item.updateData(new_data)

    def convertRange(self, new_format:str, range:List[int]) -> None:
        for item in self.sxItems[range[0]:range[1]]:
            item.convert(new_format)

    def splitItem( self, itemIdx:int, offset:int ) -> None:
        newItem = self.sxItems[itemIdx].split( offset ) # type: SxItem
        self.sxItems.insert( itemIdx+1, newItem )

    def mergeItem( self, itemStart:int, itemEnd:int ) -> None:
        idxOffset = 0   # type: int
        for idx in range(itemStart, itemEnd ):
            try:
                self.sxItems[idx+idxOffset].merge( self.sxItems[idx+idxOffset+1] )
                del self.sxItems[idx+idxOffset+1]
                idxOffset -= 1
            except SxItemBadNewAddress:
                continue

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

