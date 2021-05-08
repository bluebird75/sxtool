import io
import unittest

from src.sx_file import SxFile
from src.sx_item import SxItem
from test.test_const import *


class TestSxFile(unittest.TestCase):
    def testDeleteEmptySxFile(self):
        sxf = SxFile()
        del sxf

    def testDeleteFullSxFile(self):
        mys = """S00A11223344556677889900
S10B00000001020304050607FF
S10B000808090A0B0C0D0E0FFF
S90300000F
"""
        sxf = SxFile()
        fstream = io.StringIO(mys)  # type: TextIO
        sxf.fromFileStream(fstream, "stream")
        del sxf

    def testSxFileSplitItem(self):
        sxfile = SxFile()
        sxfile.sxItems = [
            SxItem("S1", "03", "0123", "010203", "FF"),
            SxItem("S1", "03", "0123", "111213", "FF"),
            SxItem("S1", "03", "012C", "212223", "FF"),
        ]

        sxfile.splitItem(1, 2)

        self.assertEqual(sxfile.sxItems[0].data, "010203")
        self.assertEqual(sxfile.sxItems[1].data, "1112")
        self.assertEqual(sxfile.sxItems[2].data, "13")
        self.assertEqual(sxfile.sxItems[3].data, "212223")

    def testSxFileMergeItem(self):
        sxfile = SxFile()
        sxfile.sxItems = [
            SxItem("S1", "03", "0123", "010203", "FF"),
            SxItem("S1", "03", "0126", "111213", "FF"),
            SxItem("S1", "03", "0129", "212223", "FF"),
            SxItem("S1", "03", "012C", "313233", "FF"),
            SxItem("S1", "03", "012F", "414243", "FF"),
        ]

        sxfile.mergeItem(1, 3)

        self.assertEqual(sxfile.sxItems[0].data, "010203")
        self.assertEqual(sxfile.sxItems[1].data, "111213212223313233")
        self.assertEqual(sxfile.sxItems[2].data, "414243")

        sxfile.sxItems = [
            SxItem("S1", "03", "0123", "010203", "FF"),
            SxItem("S1", "03", "0126", "111213", "FF"),
            SxItem("S1", "03", "0123", "212223", "FF"),
            SxItem("S1", "03", "0126", "313233", "FF"),
            SxItem("S1", "03", "0129", "414243", "FF"),
        ]

        sxfile.mergeItem(1, 3)

        self.assertEqual(sxfile.sxItems[0].data, "010203")
        self.assertEqual(sxfile.sxItems[1].data, "111213")
        self.assertEqual(sxfile.sxItems[2].data, "212223313233")
        self.assertEqual(sxfile.sxItems[3].data, "414243")

    def testSxFileLoadSave(self):
        sxFile = SxFile()
        fnames = ALL_EXAMPLES
        for fname in fnames:
            sxFile.fromFile(str(fname))
            with open(fname) as f:
                refOut = f.read().strip()
            strOut = io.StringIO()
            sxFile.toFileStream(strOut)
            self.assertEqual(strOut.getvalue().strip(), refOut)
            strOut.close()

    def testGetFormat(self):
        sxFile = SxFile()
        self.assertEqual(sxFile.getFormat(), "")
        fnamesAndFmt = [
            (SX_EXAMPLE1, "s19"),
            (SX_EXAMPLE2, "s19"),
            (SX_EXAMPLE3, "s28"),
            (SX_EXAMPLE4, "s37"),
            (SX_EXAMPLE5, "s19"),
        ]
        for fname, fmt in fnamesAndFmt:
            with self.subTest(fname):
                sxFile.fromFile(fname)
                self.assertEqual(sxFile.getFormat(), fmt)

    def testSxFileRepr(self):
        sxfile = SxFile()
        sxfile.sxItems = [
            SxItem("S1", "03", "0123", "010203", "FF"),
            SxItem("S1", "03", "0126", "111213", "FF"),
        ]
        self.assertEqual(
            str(sxfile),
            """
S1030123010203FF
S1030126111213FF

""",
        )

    def testUpdateDataRange(self):
        sxfile = SxFile()
        sin = "\n".join(
            [
                "S004000088FF",
                "S1" "06" "0123" "010203" "FF",
                "S1" "06" "0126" "111213" "FF",
                "S1" "06" "0129" "212223" "FF",
                "S1" "06" "012C" "313233" "FF",
                "S1" "06" "012F" "414243" "FF",
            ]
        )
        sxfile.fromFileStream(io.StringIO(sin), "stream")

        self.assertEqual(
            str(sxfile),
            """S004000088FF
S1060123010203FF
S1060126111213FF
S1060129212223FF
S106012C313233FF
S106012F414243FF
""",
        )

        sxfile.updateDataRange("AABB", (1, 4))
        self.assertEqual(
            str(sxfile),
            """S004000088FF
S1060123010203FF
S1050126AABB6E
S1050129AABB6B
S105012CAABB68
S106012F414243FF
""",
        )

    def testConvertRange(self):
        sxfile = SxFile()
        sin = "\n".join(
            [
                "S004000088FF",
                "S1" "06" "0123" "010203" "FF",
                "S1" "06" "0126" "111213" "FF",
                "S1" "06" "0129" "212223" "FF",
                "S1" "06" "012C" "313233" "FF",
                "S1" "06" "012F" "414243" "FF",
            ]
        )
        sxfile.fromFileStream(io.StringIO(sin), "stream")
        self.assertEqual(
            str(sxfile),
            """S004000088FF
S1060123010203FF
S1060126111213FF
S1060129212223FF
S106012C313233FF
S106012F414243FF
""",
        )

        sxfile.convertRange("S28", (1, 4))
        self.assertEqual(
            str(sxfile),
            """S004000088FF
S1060123010203FF
S2070001261112139B
S20700012921222368
S20700012C31323335
S106012F414243FF
""",
        )
