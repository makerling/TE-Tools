# -*- coding: utf-8 -*-
#
#   OSM.py
#    - A FlexTools Module -
#
#   Working with OSM project.
#
#   stevan_vanderwerf@sil.org
#   April 2020
#
#   Platforms: Python .NET and IronPython
#

import unicodedata
from FTModuleClass import *
import FLExFDO
from SIL.FieldWorks.FDO import (IScrBookRepository, IScrBook, IScriptureRepository, 
ILangProjectRepository, IScripture, IScriptureRepository, IStPara, 
IStParaRepository, IStText, IStTextRepository, IScrSection, IScrSectionRepository, 
ITextRepository, IScrTxtParaRepository)
from SIL.FieldWorks.FDO import ITextFactory, IStTextFactory, IStTxtParaFactory, IScrTxtParaFactory


from SILUBS.SharedScrUtils import *

from SIL.FieldWorks.Common.COMInterfaces import ITsString
from SIL.FieldWorks.FDO.DomainServices import SegmentServices
import codecs
import re
import sys, os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os
import getpass

from itertools import tee, islice, chain, izip
from collections import OrderedDict 

from SIL.Utils import StringUtils
from SIL.FieldWorks.Common.COMInterfaces import ITsString, ITsStrBldr

#----------------------------------------------------------------
# Documentation that the user sees:        

docs = {FTM_Name        : "SetString",
        FTM_Version     : 1,
        FTM_ModifiesDB  : True,
        FTM_Synopsis    : "set replace string for verse",
        FTM_Description :
u"""
Sets string for verse
""" }
                 
#----------------------------------------------------------------
# The main processing function

def MainFunction(DB, report, modifyAllowed): 

    '''
    lexEntryValue = ITsString  (lexEntry.LexemeFormOA.Form.get_String(audioHandle)).Text  
                                lexEntry.LexemeFormOA.Form.set_String(audioHandle, mkstr)
    lexForm = lexEntry.LexemeFormOA  
    lexForm.Form.set_String(audioHandle, mkstr)
    '''

    # for obj in DB.ObjectsIn(IScrTxtParaRepository): 
    #     for objsub in obj:  
    #         text = ITsString(objsub.Text).Text
    #         # report.Info(text)
    #         if text == '1This is my verse.':
    #             report.Info(text)
    #             tss = DB.db.TsStrFactory.MakeString('hello world', '999000008')
    #             report.Info('tss is: %s' % tss)
    #             # objsub.Text.set_String('999000008', tss)
            
    # for obj in DB.ObjectsIn(IScrTxtParaRepository): 
        # for objsub in obj:  
            # text = ITsString(objsub.Text).Text
            # report.Info('new text is: %s' % text)                

    

    # # Create the text objects
    # # m_textFactory = DB.db.ServiceLocator.GetInstance(IScrSectionFactory)    
    # m_textFactory = DB.db.ServiceLocator.GetInstance(ITextFactory)
    # m_stTextFactory = DB.db.ServiceLocator.GetInstance(IStTextFactory)
    # m_stTxtParaFactory = DB.db.ServiceLocator.GetInstance(IScrTxtParaFactory)                
                
    # # Create a text and add it to the project      
    # text = m_textFactory.Create()           
    # stText = m_stTextFactory.Create()
    
    # # Set StText object as the Text contents
    # text.ContentsOA = stText  
    
    # # Add paragraphs from the synthesized file
    # f = ['one','two']
    # for line in f:
        # # Create paragraph object
        # stTxtPara = m_stTxtParaFactory.CreateWithStyle(stText, 'Paragraph')
        
        # # Add it to the stText object
        # stText.ParagraphsOS.Add(stTxtPara)       
        
        # # Create a TS String to hold the line of text. Use the default vern. writing system
        # tss = DB.db.TsStrFactory.MakeString('hello my world', '999000008')
        
        # # Set the paragraph contents to the TS String
        # stTxtPara.Contents = tss                             
#----------------------------------------------------------------
# The name 'FlexToolsModule' must be defined like this:

FlexToolsModule = FlexToolsModuleClass(runFunction = MainFunction,
                                       docs = docs)
            
#----------------------------------------------------------------
if __name__ == '__main__':
    FlexToolsModule.Help()                