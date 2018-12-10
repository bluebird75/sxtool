# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information

w_dir = "./"

"""
    Used for generating forms in python with pyuic
"""

import os

filelist = os.listdir(w_dir)
for file in filelist:
    name = file[-3:len(file)]
    if name == ".ui":
        args = w_dir + "/" + file[:-3] + ".ui -o " + w_dir + "/" + file[:-3] + ".py"
        print( args )
        os.system("pyuic5.bat " + args)
        
print()
print( "--- Generation Complete ---" )
input("--- Press a key ---")