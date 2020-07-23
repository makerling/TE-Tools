# -*- coding: utf-8 -*-
#   Project: FlexTools
#   Module:  FLExTools
#   Platform: .NET v2 Windows.Forms (Python.NET 2.5)
#
#   Main FLexTools UI: loads straight in to configured database and
#    Collection.
#    - Split panel with Collections list above and Report results below.
#
#
#   Craig Farrow
#   Oct 2010
# TODO: change "messagebox" in imports to tkinter boxes
from timeit import default_timer as timer
start = timer()

import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
import os
import traceback

import Version
try:
    import FTPaths
    #import UIGlobal
    #import UICollections, FTCollections
    #import UIModulesList, UIReport, UIModuleBrowser
    #import UIDbChooser
    import FTModules
    #import Help

except EnvironmentError, e:
    # # EnvironmentError is used to communicate a known situation that can be handled,
    # # typically with a restart.
    # MessageBox.Show(e.message,
                    # "FLExTools: Configuring",
                    # MessageBoxButtons.OK,
                    # MessageBoxIcon.Information)
    sys.exit(2)     # Signal a restart
                    
except Exception, e:
    # MessageBox.Show("Error interfacing with Fieldworks:\n%s\n(This version of FLExTools supports Fieldworks versions %s - %s.)\nSee error.log for more details."
                    # % (e.message, Version.MinFWVersion, Version.MaxFWVersion),
                    # "FLExTools: Fatal Error",
                    # MessageBoxButtons.OK,
                    # MessageBoxIcon.Exclamation)
    print "Fatal exception during imports:\n%s" % traceback.format_exc()
    print "FLExTools %s" % Version.number
    sys.exit(1)

import CDFDotNetUtils
from CDFConfigStore import CDFConfigStore

import FLExFDO 
from FLExDBAccess import FLExDBAccess 
                           
#opens FLExTools if run from syswow
#C:\Windows\SysWOW64\cmd.exe
#set FWVersion=8
#check_output("C:\\Users\\workother\\code\\TE-Tools\\Python27.NET\\FW8\\python32.exe C:\\Users\\workother\\code\\TE-Tools\\FlexTools\\FLExTools.py")   
# ------------------------------------------------------------------
import unicodedata
from FTModuleClass import *
import FLExFDO
from SIL.FieldWorks.FDO import (IScrBookRepository, IScrBook, IScriptureRepository, 
ILangProjectRepository, IScripture, IScriptureRepository, IStPara, 
IStParaRepository, IStText, IStTextRepository, IScrSection, IScrSectionRepository)

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

import OSM
from setuptables import foo

import sqlite3 as lite
from SIL.FieldWorks.FDO import (ILangProjectRepository, IStTxtParaFactory, 
        ITextFactory, IStTextFactory, IScrTxtParaRepository)
from SIL.FieldWorks.Common.COMInterfaces import ITsString

end = timer()
loadtime = (end - start)
print('loadtime is: %s' % loadtime)

#----------------------------------------------------------------
"""
Example program to show how to place multiple argument groups as tabs
"""

import argparse
from gooey import Gooey, GooeyParser


@Gooey(program_name='TE Tools',
       program_description='Translation Editor Toolbox',
       tabbed_groups=False,
       navigation='Sidebar',
       sidebar_title='Choose Action to run',
       show_sidebar=True,
       optional_cols=4,
       default_size=(800,550),
       advanced = True)
def main():
    settings_msg = 'Example program to show how to place multiple argument groups as tabs'
    parser = GooeyParser(description=settings_msg)
    subs = parser.add_subparsers(help='commands', dest='command')

    home = subs.add_parser('Home')
    # home.add_argument(help='Option one')
    #can't use add_argument_group to change "required arguments" text, 
    #that only works with ArgumentParser()
    home.add_argument(
        'Welcome to the Translation Editor Toolbox', 
        default='This is a collection of scripts written for use with the Ottoman Transcription Project\n\n\
        Instructions:\n\
        \t- Choose one of the Action scripts on the left\n\
        \t- Select the options for the script in the interface\n\
        \t- Cick the START button to run the script\n\
        \t- The output and results will be shown in the program\n\
        \t- Afterwards, click the EDIT button to run another script\n\n\
        ',
        widget='Textarea',
        gooey_options={
            'height': 200,
            'show_label': True,
            'show_help': True,
            'show_border': True
        }
                
    )
    #home_group.add_argument('-OSM', widget='Textarea')

    export = subs.add_parser('Export')
    export.add_mutually_exclusive_group(
        #choices=['one','two'],
        # gooey_options={
        #     'initial_selection': 5
        # }
        required=True,
        # gooey_options={
        #     #title="Choose the file naming scheme", 
        #     full_width=True
        # }        
    )   
    export.add_argument(
        "--original_filename", metavar="Keep original filename", action="store_true"
    )
    export.add_argument(
         "--file_prefix",
        metavar="Create a sequence",
        help="Choose the file prefix",
        widget="TextField",
        default="video",
    )                        

    anotations = subs.add_parser('Annotations')
    anotations.add_argument('--opt3', action='store_true',
                        help='Option three')    

    qa = subs.add_parser('QA')
    qa.add_argument('--opt4', action='store_true',
                        help='Option four')                          

    #using add_argument_group lets you eliminates/customize the 'option/required' headings
    find_replace = subs.add_parser('Find/Replace')
    find_replace_group = find_replace.add_argument_group("Find-Replace")
    find_replace_group.add_argument(
        '--Find what:', 
        help='Defaults: case insensitive/non-regex/text normalization = NFC\n\
        Check boxes below for other options.',
        gooey_options={
            'show_border': True,            
            # 'help_bg_color': '#d4193c',
            # 'help_color': '#f2eded',
            # 'columns': 4,
            'full_width': True,
            'show_help': False
        }
    )     

    find_replace_group.add_argument(
        '--Replace with:', 
        #help='Defaults: ',
        gooey_options={
            'show_border': True,            
            # 'help_bg_color': '#d4193c',
            # 'help_color': '#f2eded',
            # 'columns': 4,
            'full_width': True,
            'show_help': False
        }
    )                          

    #Search box options for Find/Replace screen
    find_replace_group_2 = find_replace.add_argument_group(
        "Search Options",
        # description='Search Options',
        gooey_options={
        'show_border': True,
        'margin_top': 1               
        }
    )

    #using for loop to avoid having to have 5 of these!
    options = ['Regular Expression',
        'Match case',
        'NFC Search mode',
        'Search Text + Notes',
        'Search Notes only']
    for i in options:
        print(i)        
        find_replace_group_2.add_argument(
            '--' + i,
            help=i,
            action='store_true',
            gooey_options={
                'show_label': False,
                'show_help': True,
                'show_border': True
            }
        )  

    backup_sync = subs.add_parser('Backup/Sync')
    backup_sync.add_argument(
        #'--load',
        metavar='Select a Project to Export',
        dest='filename',
        widget='Dropdown',
        choices=projects_list(),
        gooey_options={
            'validator': {
                'test': 'user_input != "Select Project"',
                'message': 'Choose a save file from the list'
            }
        }
    )                        


    args=parser.parse_args()

    #display_message()
    
def projects_list():
    
    #TODO - fill out this function to get all available projects from FDO
    projects = ['Ali Bey 1665','Kieffer 1827']
    return projects


#----------------------------------------------------------------
if __name__ == "__main__":


    
    # databases = ['1665Eski-A','RuthTestFLExTools','1827-12_31_2019','1665 to QA']
    databases = ['RuthTestFLExTools']
    for database in databases:
        start = timer()
        DB = FLExDBAccess()
        DB.OpenDatabase(database)
        print("DB is: %s" % DB)

        

        #running OSM module (export to xml)
        # OSM.MainFunction(DB)
        
        #setup database tables and populate them
        foo(DB)
    
    main()

