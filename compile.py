#!/usr/bin/env python
"""
author      Roy Barina
credits     Idan Haim Shalom
license     MIT
version     1.1.1
maintainer  Roy Barina
contact     https://github.com/Barina
"""

""" Compile script for Dark-Telegram.user.styl

A script to sync Dark-Telegram.user.styl and Dark-Telegram.user.css 
by modification date and compile one of them 
(usually Dark-Telegram.user.styl) to a plain CSS format 
to be compatible with services like Franz\Ferdi. """




import sys
import os.path
import shutil
import datetime
from subprocess import check_output
class Var:
    """
    Used to represent a line of a variable

    Parameters
    ----------
    type_name : str
        The name of the variable type. optional.
    var_name : str
        Variable name.
    comment : str
        This variable comment. optional
    value : str
        This variable value.
    """

    type_name = None
    var_name = None
    comment = None
    value = None

    def toString(self, is_meta=False, indent_level=0):
        """ Generate a string based on current variable. 
        Parameters
        ----------
        is_meta : bool
            Treat this variable as a meta variable and include an assignment operator if not meta. (default False)
        indent_level : int
            The level of indentation for this variable.
        """

        # built the resulting string
        s = ""
        if self.var_name is not None:
            s += self.var_name
            if self.value is not None:
                if not is_meta:
                    s += " ="
                s += " " + self.value
                if self.comment is not None:
                    s += " // " + self.comment
                    if self.type_name is not None:
                        s += " (" + self.type_name + ")"
            else:
                print("Empty value in " + self.var_name)

        # build indentation
        indent = ""
        if s != "":
            for i in range(indent_level):
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
    indent_level : int
        The level of indentation for this block. (default 0)

    """

    header = None
    meta = []
    body = []
    footer = None
    indent_level = 0

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
        self.indent_level = max(level, 0)

    def metaToString(self) -> str:
        """ Generate a string based on current block's meta elements. """
        result = ""
        for m in self.meta:
            if isinstance(m, Var) and m.var_name.find("preprocessor") < 0:
                result += m.toString(True, self.indent_level)
            else:
                result += "\n"
        return result

    def bodyToString(self) -> str:
        """ Generate a string based on current block's body elements. """
        result = ""
        for v in self.body:
            if isinstance(v, Var):
                result += v.toString(False, self.indent_level + 1)
            else:
                result += "\n"
        return result

    def toString(self) -> str:
        """ Generate a string based on current block's value. """
        indent_str = "    "
        ind = ""
        for i in range(self.indent_level):
            ind += indent_str

        result = ""
        if self.header is not None:
            result = ind + self.header + "\n"
            result += metaToString() + "\n"
            result += bodyToString() + "\n"
            if self.footer is not None:
                result += ind + self.footer + "\n"

        return result + "\n"


user_styl_file = "Dark-Telegram.user.styl"
user_css_file = "Dark-Telegram.user.css"

debug = False
user_style_block = Block()

help_msg = "\n\nCompiling Dark-Telegram.user.styl file to plain CSS\n" + \
    "===========================================\n\n" + \
    "Description:\n" + \
    "   Syncs and compiles Dark-Telegram.user.styl to a plain CSS file to use in services like Franz/Ferdi.\n\n" + \
    "Usage:\n" + \
    "   python compile.py [command(s)(optional)]\n\n" + \
    "Commands:\n" + \
    "   --debug, -d, /d             - Will display more output and won't clear files.\n" + \
    "   --compress, -c, /c          - Will compress the resulted CSS.\n" + \
    "   --noversionstring, -nv, /nv - Whether to ignore version string.\n" + \
    "   --sync, -s, /s              - Will only sync styl and CSS files.\n" + \
    "   --timestamp, -t, /t         - Will use file's timestamp rather than version when syncing files.\n" + \
    "   --help, -h, /h              - Will show this message.\n\n" + \
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
    v.var_name = args[0].strip()
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
    v.type_name = args[1].strip()
    v.var_name = args[2].strip()
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
        v.var_name = args[0].strip()
        v.value = args[1].strip()
        if v.var_name.startswith("--"):
            v.var_name = v.var_name[2:]
        if v.var_name is v.value:
            v.var_name = v.value = None

    return v


def extractVariables(in_file):
    """ Extracts variables from a given file. """

    log("Extracting variables...")

    global user_style_block
    global debug

    reading_user_style = False
    reading_select_block = False
    select_block = None
    reading_root = False

    with open(in_file, 'r') as rObj:
        for line in rObj:
            # finding UserStyle comment block
            if line.find("/*") >= 0 and line.find("UserStyle") >= 0:
                log("found UserStyle block start..")
                user_style_block = Block()
                user_style_block.setHeader(line)
                reading_user_style = True

            # finding UserStyle end block
            elif line.find("*/") >= 0 and line.find("/UserStyle") >= 0:
                log("found UserStyle block end..")
                user_style_block.setFooter(line)
                reading_user_style = False

            # within UserStyle block
            elif reading_user_style:
                # within a Select block
                if reading_select_block:
                    # finding the selected value
                    if line.find('*') >= 0:
                        select_block += " " + \
                            line.replace(' ', '').replace(
                                ',', '').split(':')[1]
                    # finding the end of the select block
                    elif line.find('}') >= 0:
                        reading_select_block = False
                        v = extractVar(select_block)
                        user_style_block.addVar(v)
                        select_block = None

                # finding a @var variable
                elif line.find("@var") >= 0:
                    vType = getVarType(line)
                    if vType != "UNKNOWN" and vType != "ROOT":
                        # finding range and number variables with values within square brackets
                        if vType == "range" or vType == "number":
                            v = extractVar(line)
                            v.value = extractRangeValue(v.value)
                            user_style_block.addVar(v)
                        # finding beggining of select blocks
                        elif vType == "select":
                            select_block = line.replace('{', '')
                            reading_select_block = True
                        # finding all other regular variables
                        else:
                            v = extractVar(line)
                            user_style_block.addVar(v)

                # finding a meta variable
                elif line.find("@") >= 0:
                    m = extractMeta(line)
                    user_style_block.addMeta(m)

                # if we want to include blank lines, not really needed but good for debugging
                elif debug:
                    user_style_block.addVar(None)

            # finding :root header
            elif line.find(":root") >= 0 and line.find("{") >= 0:
                log("found root start")
                # root block won't need a header or a footer nor meta variables
                reading_root = True

            # gathering root variables
            elif reading_root:
                # finding the end of the root block
                if line.find("}") >= 0:
                    log("found root block end")
                    reading_root = False
                    # this is the last block we need to save its children
                    # so we do not need to read the rest of the file
                    break
                else:
                    v = extractRootVar(line)
                    if v.var_name is not None and v.value is not None:
                        user_style_block.addVar(v)

            # else:
            #     log("error?")
            #     break

    log("Done extracting variables...")


def constructStylFile(in_file) -> str:
    """ Construct a new temp file based on the given file """

    log("Generating temporary style file...")

    global user_style_block

    out_file = "darkmode.styl"
    target = "@-moz-document domain("
    ignore = True
    within_root = False
    last_brace_line = ''
    temp_lines = ''

    # we will now write to a temp file the content of the given file replacing variables with our global variables
    with open(in_file, 'r') as read_obj, open(out_file, 'w') as write_obj:
        for line in read_obj:
            if line.startswith(target):
                # at this point we can insert the saved UserStyle from global variables
                write_obj.write(user_style_block.header + "\n")
                write_obj.write(user_style_block.metaToString())
                write_obj.write(user_style_block.footer + "\n")

                # we can ignore this here
                # write_obj.write(line)

                # and after that we can insert the variables from the UserStyle block
                write_obj.write(user_style_block.bodyToString())

                # making sure we stop ignoring from here
                ignore = False

            elif not ignore:
                if within_root:
                    if line.find("}") >= 0:
                        # end of root block here
                        within_root = False
                        # we can now insert all of the root css elements as stylus variables
                        # write_obj.write(rootBlock.bodyToString())

                elif line.find(":root") >= 0 and line.find("{") >= 0:
                    within_root = True

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
                        temp_lines = last_brace_line + temp_lines

                        # then we need to write it all as usual
                        # at this point the output file is similar to the input file at this location
                        # except for the line we ignore at the start
                        write_obj.write(temp_lines)

                        # now we will keep the new 'end block' line until we found another one
                        last_brace_line = l

                        # reset variables
                        temp_lines = ''

                    else:
                        # here we simply save the current line in a temp variable
                        temp_lines += l

                    # else:
                    #     write_obj.write(line)

    return out_file


def cleanLeftoverComments(in_file):
    """ Clears all the leftover comments excluding UserStyle block comment """

    log("Cleaning leftover comments...")

    tmp_file = "styl.tmp"
    within_comment = False
    comment_count = 0

    # open in file to read and target file to write to
    with open(in_file, 'r') as read_obj, open(tmp_file, 'w') as write_obj:
        # iterating over all lines in the file
        for line in read_obj:
            if within_comment:
                # we are within a comment block and can ignore until we found closing block
                if line.find("*/") >= 0:
                    within_comment = False
                    comment_count += 1

            elif line.startswith("/*") and line.find("*/") > 0:
                # one line comment we can completely ignore
                comment_count += 1

            elif line.startswith("/*") and line.find("*/") < 0 and line.find("==UserStyle==") < 0:
                # start of a comment block
                within_comment = True
            else:
                # not a comment
                write_obj.write(line)

    log(str(comment_count) + " comments removed.")

    # renaming output file
    os.remove(in_file)
    os.rename(tmp_file, in_file)


def generateVersionString(in_file):
    """ Generates a version string for the given file. """

    log("Generating version string for '" + in_file + "'")

    tmp_file = "vstr.tmp"
    name = "Unknown"
    version = "-1"
    versionStringGenerated = False

    # building the date string of today
    date = datetime.datetime.now()
    day = date.day
    datestring = date.strftime("%B") + " " + str(day)
    if day < 2:
        datestring += "st"
    elif day < 3:
        datestring += "nd"
    elif day < 4:
        datestring += "rd"
    else:
        datestring += "th"

    datestring += ", " + date.strftime("%Y")

    # open in file to read and target file to write to
    with open(in_file, 'r') as read_obj, open(tmp_file, 'w') as write_obj:
        # iterating over all lines in the file
        for line in read_obj:
            if line.find("@name ") >= 0:
                name = line.replace("@name ", "").strip()
            elif line.find("@version ") >= 0:
                version = "v"+line.replace("@version ", "").strip()

            if not versionStringGenerated:
                i = line.find("--version ")
                if i >= 0:
                    line = ""
                    # building indentation
                    for c in range(i):
                        line += " "
                    line += "--version \"" + name + " " + version + \
                        " -- " + datestring + "\"\n"
                    versionStringGenerated = True

            write_obj.write(line)

    # renaming output file
    os.remove(in_file)
    os.rename(tmp_file, in_file)


def getVersionFromFile(in_file):
    """ Gets the version from the given Styl\CSS file.

    Parameters:
    -----------
    in_file : str
        The file to check against. cannot be empty.

    Returns:
    -----------
    Returns the version specified in the line containing '@version' or -1 if not found."""

    version = -1
    versionFound = False

    with open(in_file, "r") as read_obj:
        for line in read_obj:
            # searching for the line that contains the '@version' string
            if line.find("@version ") >= 0:
                temp = line.replace("@version", "").replace(" ", "")
                if len(temp) > 0:
                    version = temp
                    versionFound = True
                break

    # print any error
    if not versionFound or version == -1:
        print("Did not find version in file '" + in_file + "'")

    return version


def compareVersions(v1, v2) -> int:
    """ Compare two given version strings and return which is bigger.

    Returns 1 when version1 is bigger than version2, -1 when version2 is bigger and 0 when they are equals. """

    v1 = int(v1.replace(".", ""))
    v2 = int(v2.replace(".", ""))

    if v1 > v2:
        return 1
    if v2 > v1:
        return -1
    return 0


def checkStylCss(useTimestamp=False) -> bool:
    """ Checks the presence of Dark-Telegram.user.styl 
    and Dark-Telegram.user.css and make sure they're synced.

    Parameters:
    -----------
    useTimestamp : bool
        Whether to use file's timestamp rather than version. default is False.

    Returns:
    -----------
    Returns True if the check has passed False otherwise."""

    ok_result = True
    if os.path.isfile(user_styl_file) and not os.path.isfile(user_css_file):
        # style file exists but css file does not
        shutil.copyfile(user_styl_file, user_css_file)
        log("Dark-Telegram.user.styl -> Dark-Telegram.user.css")

    elif not os.path.isfile(user_styl_file) and os.path.isfile(user_css_file):
        # style file does not exists but css file does
        shutil.copyfile(user_css_file, user_styl_file)
        log("Dark-Telegram.user.css -> Dark-Telegram.user.styl")

    elif not os.path.isfile(user_styl_file) and not os.path.isfile(user_css_file):
        # both files does not exists at all
        ok_result = False
        print("Cannot find '" + user_styl_file +
              "' or '" + user_css_file + "'.")

    else:
        # both files exists, need to sync them up

        vCompare = 0

        if useTimestamp:
            # checking which file was edited later
            styl_time = os.path.getmtime(user_styl_file)
            css_time = os.path.getmtime(user_css_file)
            log("Dark-Telegram.user.styl timestamp: " + str(styl_time))
            log("Dark-Telegram.user.css timestamp: " + str(css_time))
            vCompare = compareVersions(styl_time, css_time)
        else:
            # checking which file have a grater version
            stylv = getVersionFromFile(user_styl_file)
            cssv = getVersionFromFile(user_css_file)
            log("Dark-Telegram.user.styl version: " + str(stylv))
            log("Dark-Telegram.user.css version: " + str(cssv))
            vCompare = compareVersions(stylv, cssv)

        if vCompare > 0:
            # styl was modified after or is newer than css
            shutil.copyfile(user_styl_file, user_css_file)
            log("Dark-Telegram.user.styl -> Dark-Telegram.user.css")

        elif vCompare < 0:
            # css was modified after or is newer than styl
            shutil.copyfile(user_css_file, user_styl_file)
            log("Dark-Telegram.user.css -> Dark-Telegram.user.styl")

        else:
            # both files version\timestamp are the same (in other words, unreachable code :P )
            log("Dark-Telegram.user.styl = Dark-Telegram.user.css")

    log("File sync check done.")
    return ok_result


# check if the debug argument was given
debug = "--debug" in sys.argv or "-d" in sys.argv or "/d" in sys.argv

# check if the compress argument was given
c = "--compress" in sys.argv or "-c" in sys.argv or "/c" in sys.argv

# check if the ignoreversionstring argument was given
nv = "--noversionstring" in sys.argv or "-nv" in sys.argv or "/nv" in sys.argv

# check if the sync argument was given
s = "--sync" in sys.argv or "-s" in sys.argv or "/s" in sys.argv

# check if the timestamp argument was given
t = "--timestamp" in sys.argv or "-t" in sys.argv or "/t" in sys.argv

# check if the help argument was given
h = "--help" in sys.argv or "-h" in sys.argv or "/h" in sys.argv

if not nv:
    generateVersionString(user_styl_file)
    generateVersionString(user_css_file)

if s:
    checkStylCss(t)

elif h:
    print(help_msg)

# check if Dark-Telegram.user.styl and Dark-Telegram.user.css are synced and sync them if they don't
elif checkStylCss(t):

    arg_file = user_styl_file
    if os.path.isfile(arg_file):
        if arg_file.endswith('.styl'):
            # extracting variables from the file to global variables
            extractVariables(arg_file)

            # construct a stylus file with the saved variables
            styl_file = constructStylFile(arg_file)
            css_file = styl_file.replace(".styl", ".css")

            # call the shell command to compile to given object
            styl_cmd = "stylus "
            if c:
                styl_cmd += "--compress "
            if debug:
                styl_cmd += "--line-numbers "

            output = check_output(styl_cmd + styl_file, shell=True).decode()
            print(output)

            # removing temp styl file as we do not need it anymore
            if not debug:
                log("Removing temp styl file...")
                os.remove(styl_file)

            # and check if the output contains a 'compiled' sub-string
            # this way we know the compilation was success
            if output.find("compiled") >= 0:
                if os.path.isfile(css_file):
                    # compilation was success

                    if not debug:
                        # clean all leftover comments
                        cleanLeftoverComments(css_file)

                    print("Compilation done. Please check '" + css_file + "'.")

                else:
                    print("Couldn't find compiled CSS file!")
            else:
                print("Couldn't compile styl file.")
        else:
            print("Not a styl file.")
            print(help_msg)
    else:
        print("Not a valid file " + arg_file)
        print(help_msg)
else:
    print("Sync error. Make sure you have at least 'Dark-Telegram.user.styl' or 'Dark-Telegram.user.css' file.")
    print(help_msg)
