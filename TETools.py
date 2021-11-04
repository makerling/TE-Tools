# -*- coding: utf-8 -*-

from timeit import default_timer as timer
import argparse
from gooey import Gooey, GooeyParser
import Actions.sql_find_replace_class as find_replace


@Gooey(program_name='TE Tools',
       program_description='Translation Editor Toolbox',
       tabbed_groups=False,
       navigation='Sidebar',
       sidebar_title='Choose Action to run',
       show_sidebar=True,
       optional_cols=4,
       default_size=(1100,600),
       advanced = True,
       richtext_controls=True,
       menu=[{
            'name': 'File',
            'items': [{
                'type': 'AboutDialog',
                'menuTitle': 'About',
                'name': 'Gooey Layout Demo',
                'description': 'An example of Gooey\'s layout flexibility',
                'version': '0.12',
                'copyright': '2021',
                'website': 'https://github.com/makerling/TE-Tools',
                'developer': 'Stevan Vanderwerf',
                'license': 'GPL'
                }]
       }])
def main():
    settings_msg = 'Example program to show how to place multiple argument groups as tabs'
    parser = GooeyParser(description=settings_msg)
    subs = parser.add_subparsers(help='commands', dest='command')

    home = subs.add_parser('Home')
    # home.add_argument(help='Option one')
    # can't use add_argument_group to change "required arguments" text, 
    # that only works with ArgumentParser()
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

    qa = subs.add_parser('QA for .oxes files')
    qa_group = qa.add_argument_group("QA for .oxes")
    qa_group.add_argument(
        '-QA', #what is seen by user in GUI, can't have spaces or will cause error
        # '-find', #this is what is called by args to store user input e.g. args.find_what
        help='Find what:',
        widget="FileChooser",
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


    args=parser.parse_args()
    run(args) 

def run(args):
    
    if args.command == "Find/Bulk-Replace":
        find_replace.main(args)
    
#----------------------------------------------------------------
if __name__ == "__main__":
    main()