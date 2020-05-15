import unittest

from sx_item import str2hex, hex2str, str2hexi, toHexLen, xor

s = 'S1130000285F245F2212226A000424290008237C2A'


class TestUtils( unittest.TestCase ) :
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

    def testXor(self):
        self.assertEqual( xor('0F', '1E'), '11')
        self.assertEqual( xor('1F',  'E'), 'FF')
        self.assertRaises( ValueError, xor, 'F', '1F')