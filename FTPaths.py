import os

# Make sure FlexLibs is on the path (using .pth file in ..\)

import site
site.addsitedir(os.path.dirname(__file__))