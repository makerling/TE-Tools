# coding=utf-8#
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
#from subprocess import check_output                             
#opens FLExTools if run from syswow
#C:\Windows\SysWOW64\cmd.exe
#set FWVersion=8
#check_output("C:\\Users\\workother\\code\\TE-Tools\\Python27.NET\\FW8\\python32.exe C:\\Users\\workother\\code\\TE-Tools\\FlexTools\\TETools.py")   
# ------------------------------------------------------------------
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
       optional_cols=2,
       default_size=(700,500))
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

    find_replace = subs.add_parser('Find/Replace')
    find_replace.add_argument('--opt5', action='store_true',
                        help='Option five')  

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

if __name__ == '__main__':
    main()