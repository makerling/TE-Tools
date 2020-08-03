# TE-Tools
A utility based on [Flex Tools v1](https://github.com/cdfarrow/flextools/wiki/FLExTools-v1) to extend the functionality of SIL's Translation Editor software. The Translation Editor project databases (.fwdata files) are loaded into a Sqlite database each time the program loads. Any changes made to the Sqlite database are synced back to the .fwdata xml file. This project is based on Python 3, but uses a specially compiled version of Python 2.7 to include an external manifest. This Python 2.7 binary is only used at startup as a subprocess to extract data from the .fwdata file (FDO Model database).  

INSTALL:
- install pre-requisites: 
  - [FLEx 8.3 BTE version](https://software.sil.org/fieldworks/download/fw-8312/)
  - [python 3](https://www.python.org/downloads/release/python-385/) (x86 or x86-64 depending on your computer's architecture)
- download this code and unzip: https://codeload.github.com/makerling/TE-Tools/zip/master  
- open Translation Editor and create or import a project
- click the FlexTools.vbs or FlexTools_Debug.bat file to load the program

