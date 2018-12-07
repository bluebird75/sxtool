#!/usr/bin/env python

# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

import sys, traceback
from optparse import OptionParser
from typing import List, Any, Callable, Optional, Union

from PyQt5.QtWidgets import QApplication

from gui.main_form import MainForm
from sx_item import SxFile
from const import ABOUT_INFO

def main() -> None:
    if len(sys.argv) == 1 : 
        startWinMode([])
        return
    parser = OptionParser("sxtool.py [options] [filename1, ..., filenameN]") # type: 'OptionParser'
    parser.add_option("-w", "--window", action="store_true", 
                  dest="window", default=False, 
                  help="Start the application in window mode")
    parser.add_option("-v", "--verbose", action="store_true", 
                  dest="verbose", default=False, 
                  help="Verbose mode")
    parser.add_option("-f", "--flip", action="store_true", 
                  dest="flipBits", default=False, 
                  help="Flip the bits of all data fields in the records. Will be performed before mask command")
    parser.add_option("-o", "--offset", 
                  dest="offset", 
                  help="Apply an integer offset on all adresses of the records")
    parser.add_option("--version", action="store_true",
                  dest="version", 
                  help="Show tool version")
    parser.add_option("-m", "--mask", 
                  dest="xorData", 
                  help="Apply a XOR hexadecimal mask on all data fields of the records")
    (options, args) = parser.parse_args() # type: Any, List[str]
    if options.version:
        print( ABOUT_INFO )
        sys.exit(0)
    if options.flipBits :
        apply(args, 'flipBits', verbose=options.verbose)
    if options.offset :
        apply(args, 'applyOffset', options.offset, verbose=options.verbose)
    if options.xorData :
        apply(args, 'xorData', options.xorData, verbose=options.verbose)

    if options.window or (not options.flipBits and not options.offset and not options.xorData):
        startWinMode(args)
        return

def apply(files : List[str], operation : str, args=None, verbose : bool=False) -> None:
    '''Apply the given operation on all files.'''
    if not operation : return
    for file in files : # type: str
        try:
            if verbose : print( "Opening file " + file )
            sxfile = SxFile()   # type: SxFile
            sxfile.fromFile(file)
        except IOError as e:
            print( "Error: couldn't open file: " + file )
            continue
        if verbose : print( "Applying operation \"" + operation + "\" on file:")
        for item in sxfile.sxItems :
            method = getattr(item, operation, None) # type: Optional[Callable[..., None ]]
            if method :
                if verbose : print( str(item) )
                if args :
                    method(args)
                else :
                    method()
                if verbose : print( " => " + str(item) )
        # noinspection PyBroadException
        try:
            if verbose : print( "Closing file " + file )
            sxfile.toFile(file)
        except Exception as e:
            print( "Error: couldn't save file: " + file )

# mandatory to avoid Python crashing on exceptions raised inside slots
app = None # type: Optional[ QApplication ]

# by default Qt abort on Python exceptions so we need to provide
# our own hook that does the job
def myExceptHook(exc_type, exc_value, exc_tb):
    traceback.print_exception(exc_type, exc_value, exc_tb)
    sys.exit(0)

def startWinMode(files: List[str] ) -> None:
    global app
    file = None # type: Optional[str]
    if files :
        file = files[0]
    app = QApplication([])
    w = MainForm(file=file)
    w.show()

    # to avoid crashes when Python exceptions are raised inside Qt slots
    sys.excepthook = myExceptHook

    app.exec_()

if __name__ == '__main__': 
    main()
