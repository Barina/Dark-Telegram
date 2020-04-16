#!/usr/bin/env python

""" Compile script for Dark-Telegram.user.styl

A script to sync Dark-Telegram.user.styl and Dark-Telegram.user.css 
by modification date and compile one of them 
(usually Dark-Telegram.user.styl) to a plain CSS format 
to be compatible with services like Franz\Ferdi. """

import sys
import os.path
import shutil
from subprocess import check_output

__author__ = "Roy Barina"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Roy Barina"
__email__ = "https://github.com/Barina"
__status__ = "Production"


class Var:
    """
    Used to represent a line of a variable

    Parameters
    ----------
    typeName : str
        The name of the variable type. optional.
    varName : str
        Variable name.
    comment : str
        This variable comment. optional
    value : str
        This variable value.
    """

    typeName = None
    varName = None
    comment = None
    value = None

    def toString(self, isMeta=False, indentLevel=0):
        """ Generate a string based on current variable. 
        Parameters
        ----------
        isMeta : bool
            Treat this variable as a meta variable and include an assignment operator if not meta. (default False)
        indentLevel : int
            The level of indentation for this variable.
        """

        # built the resulting string
        s = ""
        if self.varName != None:
            s += self.varName
            if self.value != None:
                if not isMeta:
                    s += " ="
                s += " " + self.value
                if self.comment != None:
                    s += " // " + self.comment
                    if self.typeName != None:
                        s += " (" + self.typeName + ")"
            else:
                print("Empty value in " + self.varName)

        # build indentation
        indent = ""
        if s != "":
            for i in range(indentLevel):
                indent += "    "

        return indent + s + "\n"


class Block:
    """
    Used to represent a stylus\css code block.

    Parameters:
    -----------
    header : str
        The header of the block including opening curly brace.
    meta : array of Var
        An array of Var items to include within this block. Not indented.
    body : array
        An array of items to include within this block. Indented. Can hold Vars and Blocks as well.
    footer : str
        The closing string of this block. Usually just a closing curly brace.
    indentLevel : int
        The level of indentation for this block. (default 0)

    """

    header = None
    meta = []
    body = []
    footer = None
    indentLevel = 0

    def setHeader(self, header: str):
        """ Sets a given str as the current block header. """
        self.header = header.strip()

    def addMeta(self, meta: Var):
        """ Adds a given Var to the meta array. """
        self.meta.append(meta)
        log("Added meta variable " + meta.toString(True))

    def addVar(self, v):
        """ Adds a given object to the body array. """
        self.body.append(v)
        if isinstance(v, Var):
            log("Added variable " + v.toString())

    def setFooter(self, footer: str):
        """ Sets a given str as the current block footer. """
        self.footer = footer.strip()

    def setIndentationLevel(self, level=0):
        """ Sets a given level as indentation level of this block. maxed to 0. """
        self.indentLevel = max(level, 0)

    def metaToString(self) -> str:
        """ Generate a string based on current block's meta elements. """
        result = ""
        for m in self.meta:
            if isinstance(m, Var) and m.varName.find("preprocessor") < 0:
                result += m.toString(True, self.indentLevel)
            else:
                result += "\n"
        return result

    def bodyToString(self) -> str:
        """ Generate a string based on current block's body elements. """
        result = ""
        for v in self.body:
            if isinstance(v, Var):
                result += v.toString(False, self.indentLevel + 1)
            else:
                result += "\n"
        return result

    def toString(self) -> str:
        """ Generate a string based on current block's value. """
        indentStr = "    "
        ind = ""
        for i in range(self.indentLevel):
            ind += indentStr

        result = ""
        if self.header != None:
            result = ind + self.header + "\n"
            result += metaToString() + "\n"
            result += bodyToString() + "\n"
            if self.footer != None:
                result += ind + self.footer + "\n"

        return result + "\n"


userStylFile = "Dark-Telegram.user.styl"
userCSSFile = "Dark-Telegram.user.css"

debug = False
userStyleBlock = Block()

helpMsg = "\n\nCompiling Dark-Telegram.user.styl file to plain CSS\n" + \
    "===========================================\n\n" + \
    "Description:\n" + \
    "   Syncs and compiles Dark-Telegram.user.styl to a plain CSS file to use in services like Franz/Ferdi.\n\n" + \
    "Usage:\n" + \
    "   python compile.py [command(s)(optional)]\n\n" + \
    "Commands:\n" + \
    "   --debug, -d, /d     - Will display more output and won't clear files.\n" + \
    "   --compress, -c, /c  - Will compress the resulted CSS.\n" + \
    "   --sync, -s, /s      - Will only sync styl and CSS files.\n" + \
    "   --help, -h, /h      - Will show this message.\n\n" + \
    "Example:\n" + \
    "   python compile.py -c -d\n\n" + \
    "   -> Will compile and compress 'Dark-Telegram.user.styl' file showing a bunch of info as output.\n" + \
    "\n"


def log(msg):
    """ Prints a message if debug is True. """

    global debug

    if debug:
        print(msg)


def stripLine(line):
    """ Gets rid of the trailing line break. """

    l = line
    if line.endswith(os.linesep):
        l = line.replace(os.linesep, '')
    elif line.endswith("\r\n"):
        l = line[:-2]
    elif line.endswith("\n"):
        l = line[:-1]
    return l


def getVarType(line) -> str:
    """ Gets the type from a given string and returns it as str """

    l = line.strip().split(' ')
    if l[0].startswith("@"):
        if l[0].startswith("@var"):
            return l[1].strip()
        else:
            return "META"
    elif l[0].startswith("--"):
        return "ROOT"
    return "UNKNOWN"


def extractMeta(line):
    """ Extracts a new meta Var based on the given string """

    line = stripLine(line)

    args = line.strip().split(' ', 1)
    v = Var()
    v.varName = args[0].strip()
    v.value = args[1].strip()

    return v


def extractRangeValue(range):
    """ Extracts a value from the given range/number string """

    r = stripLine(range)
    r = r.replace('[', '').replace(']', '')
    val = r.split(',')[0]
    if r.find("\"") >= 0:
        val += r.split("\"")[1]
    elif r.find("'") >= 0:
        val += r.split("'")[1]
    return val


def extractVar(line):
    """ Extracts a new Var based on the given string """

    global debug

    line = stripLine(line)

    args = line.strip().split(' ', 3)
    props = line.split('\'', 1)[1].split('\'', 1)

    v = Var()
    v.typeName = args[1].strip()
    v.varName = args[2].strip()
    v.value = props[1].strip()
    if debug:
        v.comment = props[0].strip()

    return v


def extractRootVar(line):
    """ Extracts a new root Var based on the given string """

    line = stripLine(line)

    args = line.strip().split(' ', 1)

    v = Var()
    if len(args) > 1:
        v.varName = args[0].strip()
        v.value = args[1].strip()
        if v.varName.startswith("--"):
            v.varName = v.varName[2:]
        if v.varName == v.value:
            v.varName = v.value = None

    return v


def extractVariables(inFile):
    """ Extracts variables from a given file. """

    print("Extracting variables...")

    global userStyleBlock
    global debug

    readingUserStyle = False
    readingSelectBlock = False
    selectBlock = None
    readingRoot = False
    readingRoot = False

    with open(inFile, 'r') as rObj:
        for line in rObj:
            # finding UserStyle comment block
            if line.find("/*") >= 0 and line.find("UserStyle") >= 0:
                log("found UserStyle block start..")
                userStyleBlock = Block()
                userStyleBlock.setHeader(line)
                readingUserStyle = True

            # finding UserStyle end block
            elif line.find("*/") >= 0 and line.find("/UserStyle") >= 0:
                log("found UserStyle block end..")
                userStyleBlock.setFooter(line)
                readingUserStyle = False

            # within UserStyle block
            elif readingUserStyle:
                # within a Select block
                if readingSelectBlock:
                    # finding the selected value
                    if line.find('*') >= 0:
                        selectBlock += " " + \
                            line.replace(' ', '').replace(
                                ',', '').split(':')[1]
                    # finding the end of the select block
                    elif line.find('}') >= 0:
                        readingSelectBlock = False
                        v = extractVar(selectBlock)
                        userStyleBlock.addVar(v)
                        selectBlock = None

                # finding a @var variable
                elif line.find("@var") >= 0:
                    vType = getVarType(line)
                    if vType != "UNKNOWN" and vType != "ROOT":
                        # finding range and number variables with values within square brackets
                        if vType == "range" or vType == "number":
                            v = extractVar(line)
                            v.value = extractRangeValue(v.value)
                            userStyleBlock.addVar(v)
                        # finding beggining of select blocks
                        elif vType == "select":
                            selectBlock = line.replace('{', '')
                            readingSelectBlock = True
                        # finding all other regular variables
                        else:
                            v = extractVar(line)
                            userStyleBlock.addVar(v)

                # finding a meta variable
                elif line.find("@") >= 0:
                    m = extractMeta(line)
                    userStyleBlock.addMeta(m)

                # if we want to include blank lines, not really needed but good for debugging
                elif debug:
                    userStyleBlock.addVar(None)

            # finding :root header
            elif line.find(":root") >= 0 and line.find("{") >= 0:
                log("found root start")
                # root block won't need a header or a footer nor meta variables
                readingRoot = True

            # gathering root variables
            elif readingRoot:
                # finding the end of the root block
                if line.find("}") >= 0:
                    log("found root block end")
                    readingRoot = False
                    # this is the last block we need to save its children
                    # so we do not need to read the rest of the file
                    break
                else:
                    v = extractRootVar(line)
                    if v.varName != None and v.value != None:
                        userStyleBlock.addVar(v)

            # else:
            #     log("error?")
            #     break

    print("Done extracting variables...")


def constructStylFile(inFile) -> str:
    """ Construct a new temp file based on the given file """

    print("Generating temporary style file...")

    global userStyleBlock

    outFile = "darkmode.styl"
    target = "@-moz-document domain("
    ignore = True
    withinRoot = False
    lastBraceLine = ''
    tempLines = ''

    # we will now write to a temp file the content of the given file replacing variables with our global variables
    with open(inFile, 'r') as readObj, open(outFile, 'w') as writeObj:
        for line in readObj:
            if line.startswith(target):
                # at this point we can insert the saved UserStyle from global variables
                writeObj.write(userStyleBlock.header + "\n")
                writeObj.write(userStyleBlock.metaToString())
                writeObj.write(userStyleBlock.footer + "\n")

                # we can ignore this here
                # writeObj.write(line)

                # and after that we can insert the variables from the UserStyle block
                writeObj.write(userStyleBlock.bodyToString())

                # making sure we stop ignoring from here
                ignore = False

            elif not ignore:
                if withinRoot:
                    if line.find("}") >= 0:
                        # end of root block here
                        withinRoot = False
                        # we can now insert all of the root css elements as stylus variables
                        # writeObj.write(rootBlock.bodyToString())

                elif line.find(":root") >= 0 and line.find("{") >= 0:
                    withinRoot = True

                else:
                    l = line

                    # change var(--x) if exists
                    if line.find("var(--") >= 0:
                        parts = line.split("var(--")
                        l = parts[0]
                        for i, p in enumerate(parts):
                            if i > 0:
                                l += p.replace(')', '', 1)

                    # if the current line ends with a curly brace (meaning the end of a block)
                    if l.lstrip().startswith('}'):
                        # means that there's a new 'end of a block' and we need to
                        # include the old one we found earlier (if not the first time we found)
                        # and add all of the lines we kept before
                        tempLines = lastBraceLine + tempLines

                        # then we need to write it all as usual
                        # at this point the output file is similar to the input file at this location
                        # except for the line we ignore at the start
                        writeObj.write(tempLines)

                        # now we will keep the new 'end block' line until we found another one
                        lastBraceLine = l

                        # reset variables
                        tempLines = ''

                    else:
                        # here we simply save the current line in a temp variable
                        tempLines += l

                    # else:
                    #     writeObj.write(line)

    return outFile


def cleanLeftoverComments(inFile):
    """ Clears all the leftover comments excluding UserStyle block comment """

    print("Cleaning leftover comments...")

    tmpFile = "styl.tmp"
    withinComment = False
    commentCount = 0

    # open in file to read and target file to write to
    with open(inFile, 'r') as readObj, open(tmpFile, 'w') as writeObj:
        # iterating over all lines in the file
        for line in readObj:
            if withinComment:
                # we are within a comment block and can ignore until we found closing block
                if line.find("*/") >= 0:
                    withinComment = False
                    commentCount += 1

            elif line.startswith("/*") and line.find("*/") > 0:
                # one line comment we can completely ignore
                commentCount += 1

            elif line.startswith("/*") and line.find("*/") < 0 and line.find("==UserStyle==") < 0:
                # start of a comment block
                withinComment = True
            else:
                # not a comment
                writeObj.write(line)

    print(str(commentCount) + " comments removed.")

    # renaming output file
    os.remove(inFile)
    os.rename(tmpFile, inFile)


def checkStylCss() -> bool:
    """ Checks the presence of Dark-Telegram.user.styl 
    and Dark-Telegram.user.css and makes sure they're synced.
    Returns True if the check has passed False otherwise."""

    okResult = True
    if os.path.isfile(userStylFile) and not os.path.isfile(userCSSFile):
        # style file exists but css file does not
        shutil.copyfile(userStylFile, userCSSFile)
        log("Dark-Telegram.user.styl -> Dark-Telegram.user.css")

    elif not os.path.isfile(userStylFile) and os.path.isfile(userCSSFile):
        # style file does not exists but css file does
        shutil.copyfile(userCSSFile, userStylFile)
        log("Dark-Telegram.user.css -> Dark-Telegram.user.styl")

    elif not os.path.isfile(userStylFile) and not os.path.isfile(userCSSFile):
        # both files does not exists at all
        okResult = False
        print("Cannot find '" + userStylFile + "' or '" + userCSSFile + "'.")

    else:
        # both files exists, need to sync them up
        stylTime = os.path.getmtime(userStylFile)
        cssTime = os.path.getmtime(userCSSFile)
        log("Dark-Telegram.user.styl timestamp: " + str(stylTime))
        log("Dark-Telegram.user.css timestamp: " + str(cssTime))

        if stylTime > cssTime:
            # styl was modified after css
            shutil.copyfile(userStylFile, userCSSFile)
            log("Dark-Telegram.user.styl -> Dark-Telegram.user.css")

        elif stylTime < cssTime:
            # css was modified after styl
            shutil.copyfile(userCSSFile, userStylFile)
            log("Dark-Telegram.user.css -> Dark-Telegram.user.styl")

        else:
            # both files modified at the exact same time (in other words, unreachable code :P )
            log("Dark-Telegram.user.styl = Dark-Telegram.user.css")

    print("File sync check done.")
    return okResult


# check if the debug argument was given
debug = "--debug" in sys.argv or "-d" in sys.argv or "/d" in sys.argv

# check if the compress argument was given
c = "--compress" in sys.argv or "-c" in sys.argv or "/c" in sys.argv

# check if the sync argument was given
s = "--sync" in sys.argv or "-s" in sys.argv or "/s" in sys.argv

# check if the help argument was given
h = "--help" in sys.argv or "-h" in sys.argv or "/h" in sys.argv


if s:
    checkStylCss()

elif h:
    print(helpMsg)

# check if Dark-Telegram.user.styl and Dark-Telegram.user.css are synced and sync them if they don't
elif checkStylCss():

    argFile = userStylFile
    if os.path.isfile(argFile):
        if argFile.endswith('.styl'):
            # extracting variables from the file to global variables
            extractVariables(argFile)

            # construct a stylus file with the saved variables
            stylFile = constructStylFile(argFile)
            cssFile = stylFile.replace(".styl", ".css")

            # call the shell command to compile to given object
            stylCmd = "stylus "
            if c:
                stylCmd += "--compress "
            if debug:
                stylCmd += "--line-numbers "

            output = check_output(stylCmd + stylFile, shell=True).decode()
            print(output)

            # removing temp styl file as we do not need it anymore
            if not debug:
                print("Removing temp styl file...")
                os.remove(stylFile)

            # and check if the output contains a 'compiled' sub-string
            # this way we know the compilation was success
            if output.find("compiled") >= 0:
                if os.path.isfile(cssFile):
                    # compilation was success

                    if not debug:
                        # clean all leftover comments
                        cleanLeftoverComments(cssFile)

                    print("Compilation done. Please check '" + cssFile + "'.")

                else:
                    print("Couldn't find compiled CSS file!")
            else:
                print("Couldn't compile styl file.")
        else:
            print("Not a styl file.")
            print(helpMsg)
    else:
        print("Not a valid file " + argFile)
        print(helpMsg)
else:
    print("Sync error. Make sure you have at least 'Dark-Telegram.user.styl' or 'Dark-Telegram.user.css' file.")
    print(helpMsg)
