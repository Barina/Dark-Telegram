#!/usr/bin/env python

""" Old script to create a darkmode.css file out of a premade plain CSS file. 

Note: The new compile.py script will now handle this as well as creating a plain CSS file.
"""

import sys
import os.path
from subprocess import check_output

__author__ = "Roy Barina"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Roy Barina"
__email__ = "https://github.com/Barina"
__status__ = "Production"


def franzify(inFile):
    """ 
    Creates a new file without the outer 'moz-document' block.

    We will iterate over all lines and ignore the moz-document and the last closing curly brace
    by saving current lines in a temp variable until we found a closing curly brace
    if a closing curly brace has found, we will add the last line with closing brace we found to the
    temp lines variable and write it out. save the new line with curly brace and keep going
    until we found the next..
    after we reach the end of the file we can just write the remaining temp lines as is
    this way we ignoring the last line with curly brace
    """

    print("Processing..")

    # define needed variables
    target = "@-moz-document domain("
    processed = False
    outFile = 'darkmode.css'
    tempLines = ''
    lastBraceLine = ''

    # open in file to read and target file to write to
    with open(inFile, 'r') as readObj, open(outFile, 'w') as writeObj:
        # iterating over all lines in the file
        for line in readObj:
            # if the current line starts with the moz-document we'll skip it
            if line.startswith(target):
                # and mark that we modified the file
                processed = True
            else:
                # if the current line ends with a curly brace (meaning the end of a block)
                if line.lstrip().startswith('}'):
                    # means that there's a new 'end of a block' and we need to
                    # include the old one we found earlier (if not the first time we found)
                    # and add all of the lines we kept before
                    tempLines = lastBraceLine + tempLines

                    # then we need to write it all as usual
                    # at this point the output file is similar to the input file at this location
                    # except for the line we ignore at the start
                    writeObj.write(tempLines)

                    # now we will keep the new 'end block' line until we found another one
                    lastBraceLine = line

                    # reset variables
                    tempLines = ''
                else:
                    # here we simply save the current line in a temp variable
                    tempLines += line

        # writing all the remaining lines excluding last line with closing curly brace
        writeObj.write(tempLines)

    # we need to check if we processed a new file
    if processed:
        # then we don't need the original anymore
        os.remove(inFile)
    else:
        # or just remove the out file as it is identical to the original at this point
        os.remove(outFile)

    print("Done.")


# checking the amount of arguments given (name of this script is also an argument)
if len(sys.argv) > 1:
    argFile = sys.argv[1]
    if os.path.isfile(argFile):
        if argFile.endswith('.styl'):
            # call the shell command to compile to given object
            output = check_output("stylus " + argFile, shell=True).decode()
            print(output)
            # and check if the output contains a 'compiled' sub-string
            # this way we know the compilation was success
            if output.find("compiled") >= 0:
                # compilation was success
                processFile = argFile.replace('.styl', '.css')
                if os.path.isfile(processFile):
                    # and now we can franzify the compiled CSS
                    franzify(processFile)
                else:
                    print("Cannot find compiled file.")
            else:
                print("Couldn't compile styl file.")
        else:
            print("Not a styl file.")
    else:
        print("Not a valid file " + argFile)
else:
    print("No file given.")
