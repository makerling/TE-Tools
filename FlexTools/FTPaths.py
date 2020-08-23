#
#   Project: FlexTools
#   Module:  FTPaths
#
#   Global definitions of data paths for FLExTools
#
#   Craig Farrow
#   Mar 2012
#

import os

# Make sure FlexLibs is on the path (using .pth file in ..\)

import site
site.addsitedir(os.path.join(os.path.dirname(__file__), u"..\\"))
