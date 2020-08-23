# -*- coding: utf-8 -*-

from timeit import default_timer as timer
import argparse
from gooey import Gooey, GooeyParser
import sql_find_replace_class


@Gooey(program_name='TE Tools',
       program_description='Translation Editor Toolbox',
       tabbed_groups=False,
       navigation='Sidebar',
       sidebar_title='Choose Action to run',
       show_sidebar=True,
       optional_cols=4,
       default_size=(1100,600),
       advanced = True,
       richtext_controls=True)
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
    # export = subs.add_parser('Export')
    # export.add_mutually_exclusive_group(
    #     #choices=['one','two'],
    #     # gooey_options={
    #     #     'initial_selection': 5
    #     # }
    #     required=True,
    #     # gooey_options={
    #     #     #title="Choose the file naming scheme", 
    #     #     full_width=True
    #     # }        
    # )   
    # export.add_argument(
    #     "--original_filename", metavar="Keep original filename", action="store_true"
    # )
    # export.add_argument(
    #      "--file_prefix",
    #     metavar="Create a sequence",
    #     help="Choose the file prefix",
    #     widget="TextField",
    #     default="video",
    # )                        

    # anotations = subs.add_parser('Annotations')
    # anotations.add_argument('--opt3', action='store_true',
    #                     help='Option three')    

    # qa = subs.add_parser('QA')
    # qa.add_argument('--opt4', action='store_true',
    #                     help='Option four')                          

    #using add_argument_group lets you eliminates/customize the 'option/required' headings
    find_replace = subs.add_parser('Find/Bulk-Replace')
    find_replace_group = find_replace.add_argument_group("Find/Bulk Replace")
    find_replace_group.add_argument(
        '-find', #what is seen by user in GUI, can't have spaces or will cause error
        # '-find', #this is what is called by args to store user input e.g. args.find_what
        type=str,
        help='Find what:',
        gooey_options={
            # 'show_border': True,            
            # 'help_bg_color': '#d4193c',
            # 'help_color': '#f2eded',
            # 'columns': 4,
            'full_width': True,
            'show_help': True,
            'show_label': False
        }
    )     

    find_replace_group.add_argument(
        '-replace', 
        # '--replace',
        help='Replace with (optional): ',
        gooey_options={
            # 'show_border': True,            
            # 'help_bg_color': '#d4193c',
            # 'help_color': '#f2eded',
            # 'columns': 4,
            'full_width': True,
            'show_help': True,
            'show_label': False
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
    """TODO implement: 'Match case',
        'NFC Search mode',
        'Search Text + Notes',
        'Search Notes only',
        'Match whole word only',
        'Begins with',
        'Ends with'"""

    options = ['Regex']
    for i in options:
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

    # backup_sync = subs.add_parser('Backup/Sync')
    # backup_sync.add_argument(
    #     #'--load',
    #     metavar='Select a Project to Export',
    #     dest='filename',
    #     widget='Dropdown',
    #     choices=projects_list(),
    #     gooey_options={
    #         'validator': {
    #             'test': 'user_input != "Select Project"',
    #             'message': 'Choose a save file from the list'
    #         }
    #     }
    # )                        


    args=parser.parse_args()
    run(args) 

def run(args):
    
    if args.command == "Find/Bulk-Replace":
        sql_find_replace_class.main(args)
    
#----------------------------------------------------------------
if __name__ == "__main__":

    from subprocess import check_output 

    start = timer()

    dbloading = check_output(".\\TELibs\\Python27.NET\\FW8\\python32.exe FDO2sqlite.py")             
    # print(dbloading)

    end = timer()
    loadtime = (end - start)
    # print('loadtime of is:%s' % loadtime)
    main()
    # sql()