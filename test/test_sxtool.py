#!/usr/bin/env python

# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

import unittest, io

from src.sx_item import *
from src.form_insert_row_value import FormInsertRowValue

s = 'S1130000285F245F2212226A000424290008237C2A'

class TestSxItem( unittest.TestCase ) :

    def testStr2hex(self):
        self.assertEqual( str2hex(''), [])
        self.assertEqual( str2hex(None), [])
        self.assertEqual( str2hex('1234'), [0x12, 0x34] )
        self.assertEqual( str2hex('\t12 34\n56'), [0x12, 0x34, 0x56])
        self.assertRaises( ValueError, str2hex, '1')

    def testHex2str(self):
        self.assertEqual( hex2str( [0x12, 0x34] ), '1234' )
        self.assertRaises( ValueError, hex2str, [0x100, 0x34] )
        self.assertEqual( hex2str([]), '' )

    def testStr2hexi( self ):
        self.assertEqual( str2hexi( 'FF'), 0xFF )
        self.assertEqual( str2hexi( ''), 0 )
        self.assertEqual( str2hexi( 'F'), 0xF )

    def testToHexLen(self):
        def testToHexLenSingle(expected, number, length):
            r = toHexLen(number, length)
            if r != expected:
                print( "FAIL toHexLen(%s, %d) \t= %s\t%s" % (str(number), length, r, s) )
            self.assertEqual( r, expected )

        testToHexLenSingle("1", 1, 1)
        testToHexLenSingle("01", 1, 2)
        testToHexLenSingle("012", 0x12, 3)
        testToHexLenSingle("112", 0x112, 3)
        testToHexLenSingle("002A", 0x2A, 4)
        testToHexLenSingle("000001", 1, 6)
        
        testToHexLenSingle("1", "0x01", 1)
        testToHexLenSingle("01", "0x01", 2)
        testToHexLenSingle("2A", "2A", 2)
        testToHexLenSingle("002A", "2A", 4)
        testToHexLenSingle("002A", "0x2A", 4)
        
        testToHexLenSingle("2A", 42, 2)
        testToHexLenSingle("02A", 42, 3)
        
        testToHexLenSingle("22", "22", 2)
        testToHexLenSingle("22", "0022", 2)
        testToHexLenSingle("22", "000022", 2)
        testToHexLenSingle("0022", "22", 4)
        testToHexLenSingle("0022", "0022", 4)
        testToHexLenSingle("0022", "000022", 4)
        testToHexLenSingle("000022", "22", 6)
        testToHexLenSingle("000022", "0022", 6)
        testToHexLenSingle("000022", "000022", 6)
        
        # Test reducing string with modulo 2^(length/2*8)
        testToHexLenSingle("11", "2211", 2)
        testToHexLenSingle("11", "222211", 2)


    def testChecksum( self ):
        sx = SxItem( '19', '13', '0000', '285F245F2212226A000424290008237C', 'FF' )
        sx.updateChecksum()
        self.assertEqual( sx.checksum, '2A' )

    def testDataQuantity( self ):
        sx = SxItem( '19', 'FF', '0000', '285F245F2212226A000424290008237C', '2A' )
        sx.updateDataQuantity()
        self.assertEqual( sx.data_quantity, '13' )

    def testData( self ):
        sx = SxItem( '19', 'FF', '0000', '285F245F2212226A00042429000823', '2A' )
        sx.updateData( '285F245F2212226A000424290008237C' )
        self.assertEqual( sx.data_quantity, '13' )
        self.assertEqual( sx.checksum, '2A' )

    def testAddress( self ):
        sx = SxItem( '19', '13', 'FFFF', '285F245F2212226A000424290008237C', 'FF' )
        sx.updateAddress( '0000' )
        self.assertEqual( sx.data_quantity, '13' )
        self.assertEqual( sx.checksum, '2A' )

    def testConvert( self ):
        ref_s19 = 'S1130000285F245F2212226A000424290008237C2A'
        ref_s28 = 'S214000000285F245F2212226A000424290008237C29'
        ref_s37 = 'S31500000000285F245F2212226A000424290008237C28'
        sx = SxItem( '19', '13', '0000', '285F245F2212226A000424290008237C', '2A' )

        self.assertEqual( str(sx) , ref_s19 )
        sx.convert('28')
        self.assertEqual( str(sx), ref_s28 )
        sx.convert('37')
        self.assertEqual( str(sx), ref_s37 )
        sx.convert('19')
        self.assertEqual( str(sx) , ref_s19 )

    def testSetContent(self):
        ref_s19 = 'S1130000285F245F2212226A000424290008237C2A'
        sx = SxItem('','','','','')
        sx.setContent( ref_s19 )
        # print sx.toOneString()
        sx.updateChecksum()
        self.assertEqual( sx.format, '19' )
        self.assertEqual( sx.data_quantity, '13' )
        self.assertEqual( sx.checksum, '2A' )

        ref_s28 = 'S214000000285F245F2212226A000424290008237C29'
        sx.setContent( ref_s28 )
        sx.updateChecksum()
        self.assertEqual( sx.format, '28' )
        self.assertEqual( sx.data_quantity, '14' )
        self.assertEqual( sx.checksum, '29' )

        ref_s37 = 'S31500000000285F245F2212226A000424290008237C28'
        sx.setContent( ref_s37 )
        sx.updateChecksum()
        self.assertEqual( sx.format, '37' )
        self.assertEqual( sx.data_quantity, '15' )
        self.assertEqual( sx.checksum, '28' )

    def testSplit( self ):
        sdata = 'S1090123112233445566FF'
        sx = SxItem( '', '', '', '', '' )
        sx.setContent( sdata )

        self.assertRaises( SxItemBadOffset, sx.split, 0 )
        self.assertRaises( SxItemBadOffset, sx.split, 6 )

        sx2 = sx.split(2)

        self.assertEqual( sx.address, '0123' )
        self.assertEqual( sx.data,    '1122' )
        self.assertEqual( sx.data_quantity, '05' )

        self.assertEqual( sx2.address, '0125' )
        self.assertEqual( sx2.data,    '33445566' )
        self.assertEqual( sx2.data_quantity, '07' )

        self.assertRaises( SxItemBadOffset, sx.split, 2 )

    def testMergePossible( self ):
        sdata = 'S1090123112233445566FF'
        sx = SxItem( '', '', '', '', '' )
        sx.setContent( sdata )
        sx2 = sx.split(2)

        sx2.address = '0124'
        self.assertEqual( sx.mergePossible( sx2 ), False )

        sx2.address = '0125'
        self.assertEqual( sx.mergePossible( sx2 ), True )
        sx.merge( sx2 )

    def testMerge( self ):
        sdata = 'S1090123112233445566FF'
        sx = SxItem( '', '', '', '', '' )
        sx.setContent( sdata )
        sx2 = sx.split(2)

        sx2.address = '0124'
        self.assertRaises( SxItemBadNewAddress, sx.merge, sx2 )

        sx2.address = '0125'
        sx.merge( sx2 )

        self.assertEqual( sx.address, '0123' )
        self.assertEqual( sx.data,    '112233445566' )
        self.assertEqual( sx.data_quantity, '09' )

    def testIsValid(self):
        sdata = 'S1090123112233445566FF'
        sx = SxItem( '19', '', '', '', '' )
        self.assertEqual( sx.isValid(), False )

        sx.setContent( sdata )
        self.assertEqual( sx.isValid(), False )

        sx.updateChecksum()
        self.assertEqual( sx.isValid(), True )

        sx.data_quantity = '08'
        self.assertEqual( sx.isValid(), False )
        sx.updateChecksum()
        self.assertEqual( sx.isValid(), False )
        sx.data_quantity = '09'
        self.assertEqual( sx.isValid(), False )
        sx.updateChecksum()
        self.assertEqual( sx.isValid(), True )

        sx.address = '001122'
        self.assertEqual( sx.isValid(), False )
        sx.updateChecksum()
        self.assertEqual( sx.isValid(), False )
        sx.format = '28'
        sx.updateDataQuantity()
        sx.updateChecksum()
        self.assertEqual( sx.isValid(), True )

        sx.address = '00112233'
        self.assertEqual( sx.isValid(), False )
        sx.updateChecksum()
        self.assertEqual( sx.isValid(), False )
        sx.format = '37'
        sx.updateDataQuantity()
        sx.updateChecksum()
        self.assertEqual( sx.isValid(), True )

    def testApplyNewRowSize( self ):
        sxfile = SxFile()
        sxfile.sxItems = [ 
            SxItem( '19', '03', '0123', '010203', 'FF' ),
            SxItem( '19', '03', '0123', '111213', 'FF' ),
            SxItem( '19', '03', '0126', '212223', 'FF' ),
            SxItem( '19', '03', '0129', '313233', 'FF' ),
            SxItem( '19', '03', '012C', '414243', 'FF' ),
        ]

        sxfile.applyNewRowSize( 2, 1 ,3 )

        self.assertEqual( sxfile.sxItems[0].data, '010203' )
        self.assertEqual( sxfile.sxItems[1].data, '1112' )
        self.assertEqual( sxfile.sxItems[2].data, '1321' )
        self.assertEqual( sxfile.sxItems[3].data, '2223' )
        self.assertEqual( sxfile.sxItems[4].data, '3132' )
        self.assertEqual( sxfile.sxItems[5].data, '33' )


    def testSxfileSplitItem(self):
        sxfile = SxFile()
        sxfile.sxItems = [ 
            SxItem( '19', '03', '0123', '010203', 'FF' ),
            SxItem( '19', '03', '0123', '111213', 'FF' ),
            SxItem( '19', '03', '012C', '212223', 'FF' ),
        ]

        sxfile.splitItem( 1, 2 )

        self.assertEqual( sxfile.sxItems[0].data, '010203' )
        self.assertEqual( sxfile.sxItems[1].data, '1112' )
        self.assertEqual( sxfile.sxItems[2].data, '13' )
        self.assertEqual( sxfile.sxItems[3].data, '212223' )

        
    def testSxfileMergeItem(self):
        sxfile = SxFile()
        sxfile.sxItems = [ 
            SxItem( '19', '03', '0123', '010203', 'FF' ),
            SxItem( '19', '03', '0126', '111213', 'FF' ),
            SxItem( '19', '03', '0129', '212223', 'FF' ),
            SxItem( '19', '03', '012C', '313233', 'FF' ),
            SxItem( '19', '03', '012F', '414243', 'FF' ),
        ]

        sxfile.mergeItem( 1, 3 )

        self.assertEqual( sxfile.sxItems[0].data, '010203' )
        self.assertEqual( sxfile.sxItems[1].data, '111213212223313233' )
        self.assertEqual( sxfile.sxItems[2].data, '414243' )

        sxfile.sxItems = [ 
            SxItem( '19', '03', '0123', '010203', 'FF' ),
            SxItem( '19', '03', '0126', '111213', 'FF' ),
            SxItem( '19', '03', '0123', '212223', 'FF' ),
            SxItem( '19', '03', '0126', '313233', 'FF' ),
            SxItem( '19', '03', '0129', '414243', 'FF' ),
        ]

        sxfile.mergeItem( 1, 3 )

        self.assertEqual( sxfile.sxItems[0].data, '010203' )
        self.assertEqual( sxfile.sxItems[1].data, '111213' )
        self.assertEqual( sxfile.sxItems[2].data, '212223313233' )
        self.assertEqual( sxfile.sxItems[3].data, '414243' )

    def testFlipBits(self):
        sxfile = SxFile()
        sxfile.sxItems = [ 
            SxItem( '19', '03', '0123', '010203', 'FF' ),
            SxItem( '19', '03', '0123', '111213', 'FF' ),
            SxItem( '19', '03', '0126', '212223', 'FF' ),
            SxItem( '19', '03', '0129', '313233', 'FF' ),
            SxItem( '19', '03', '012C', '414243', 'FF' ),
        ]
        for item in sxfile.sxItems :
            item.flipBits()
        self.assertEqual(sxfile.sxItems[0].data, 'FEFDFC')
        self.assertEqual(sxfile.sxItems[1].data, 'EEEDEC')
        self.assertEqual(sxfile.sxItems[2].data, 'DEDDDC')
        self.assertEqual(sxfile.sxItems[3].data, 'CECDCC')
        self.assertEqual(sxfile.sxItems[4].data, 'BEBDBC')
        
    def testApplyOffset(self):
        sxfile = SxFile()
        sxfile.sxItems = [ 
            SxItem( '19', '03', '0123', '010203', 'FF' ),
            SxItem( '19', '03', '0123', '111213', 'FF' ),
            SxItem( '19', '03', '0126', '212223', 'FF' ),
            SxItem( '19', '03', '0129', '313233', 'FF' ),
            SxItem( '19', '03', '012C', '414243', 'FF' ),
        ]
        i = 1
        for item in sxfile.sxItems :
            item.applyOffset(i)
            i += 5
        self.assertEqual(sxfile.sxItems[0].address, '0124')
        self.assertEqual(sxfile.sxItems[1].address, '0129')
        self.assertEqual(sxfile.sxItems[2].address, '0131')
        self.assertEqual(sxfile.sxItems[3].address, '0139')
        self.assertEqual(sxfile.sxItems[4].address, '0141')
    
    def testXorData(self):
        sxfile = SxFile()
        sxfile.sxItems = [ 
            SxItem( '19', '03', '0123', '010203', 'FF' ),
            SxItem( '19', '03', '0123', '111213', 'FF' ),
            SxItem( '19', '03', '0126', '212223', 'FF' ),
            SxItem( '19', '03', '0129', '313233', 'FF' ),
            SxItem( '19', '03', '012C', '414243', 'FF' ),
        ]
        for item in sxfile.sxItems :
            item.xorData('15AF')
        self.assertEqual(sxfile.sxItems[0].data, '14AD03')
        self.assertEqual(sxfile.sxItems[1].data, '04BD13')
        self.assertEqual(sxfile.sxItems[2].data, '348D23')
        self.assertEqual(sxfile.sxItems[3].data, '249D33')
        self.assertEqual(sxfile.sxItems[4].data, '54ED43')

class TestSxFile(unittest.TestCase):

    def test1(self):
        sxf = SxFile()
        del sxf

    def test2(self):
        mys = '''S00A11223344556677889900
S10B00000001020304050607FF
S10B000808090A0B0C0D0E0FFF
S90300000F
'''
        sxf = SxFile()
        fstream = io.StringIO(mys)  # type: TextIO
        sxf.fromFileStream( fstream, 'stream')
        del sxf

class TestAdjustAddressLength(unittest.TestCase):

    def testAdjustAddressLength(self):
        self.assertEqual( FormInsertRowValue.adjustAddressLength( FormInsertRowValue, '12', 'S19'), '0012' )
        self.assertEqual( FormInsertRowValue.adjustAddressLength( FormInsertRowValue, '1', 'S19'), '0001' )
        self.assertEqual( FormInsertRowValue.adjustAddressLength( FormInsertRowValue, '12345', 'S19'), '2345' )
        self.assertEqual( FormInsertRowValue.adjustAddressLength( FormInsertRowValue, '', 'S19'), '0000' )



if __name__ == "__main__":
    unittest.main()
    # main( testRunner = TextTestRunner( verbosity = 2 ) )

