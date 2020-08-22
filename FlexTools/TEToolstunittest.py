# -*- coding: utf-8 -*-
import sqlite3, re
from colored import stylize, attr, fg

class FindReplace:

    def __init__(self, query_type, query, replace_text):
        
        self.query_type = query_type
        self.query = query
        self.query_type = query_type
        
        ####################### BULK REPLACE FUNCTIONS - REGEX AND STANDARD FIND/REPLACE #######################
        # this order of arguments in functions preserves ability to swap replace() and regexp() interchangably
        def reSub(self, string, query, replace_text):
            return re.sub(query, replace_text, string)
        db.create_function('regexp', 3, reSub) #3 represents number of arguments
        
        # query_type determines whether the replace is built-in (non-regex) replace() or custom function regexp()
        def replaceQuery(self, query_type, query, replace_text): 
            # without WHERE statement entire database is updated, affects trigger        
            c.execute("""
                UPDATE verses 
                SET verse = 
                    """ + query_type + """(verse, '""" + query + """','""" + replace_text + """') 
                WHERE verse 
                    MATCH '""" + query + """' 
                """)
            return c.fetchall()
        ############################## FIND FUNCTIONS - REGEX AND STANDARD FIND ################################
        db.create_function('match', 2, lambda x, y: 1 if re.findall(x, y) else 0)
        
        #returns verse string pre and post replace, doesn't actually make any replacements (because of SELECT)
        def findQuery(self, query_type, query, replace_text): 
            c.execute("""
                SELECT verse, 
                    """ + query_type + """(verse, '""" + query + """', '""" + replace_text + """') 
                FROM verses 
                WHERE verse 
                    MATCH '""" + query + """'
                """)    
            return c.fetchall()   
        #########################################################################################################
        
        
def main(args):    
    
    db = sqlite3.connect('osmtestspeed.db')
    c = db.cursor()    
    
    # # determines if query should be using built-in replace() or custom regexp()
    # query_type = 'replace' if args.Regex == False else 'regexp'  
    # query = args.find 
    # # determines if only findQuery() should be run or findQuery() and replaceQuery()
    # # replace() & regexp() function errors when replace_text is None, workaround to still get pre/post replace strings
    # replace_text = query if args.replace == None else args.replace    

    fr = FindReplace(query_type, query, replace_text)
    findQueryResults = fr.findQuery()     
    sql_find_replace.main(args, query_type, query, replace_text)


    
    # loops through results of query and highlights search term/replace term
    for i in findQueryResults:
        oldstring = stylize(re.findall(query,i[0])[0], attr('bold')) # need to select first result of re.findall
        newstring = stylize(replace_text, attr('bold')) # TODO implement regex backreferences 
        old_string_formatted = re.sub(query, oldstring,i[0]) 
        new_string_formatted = re.sub(replace_text, newstring,i[1])

        # adding replace strings to output only if text is put into 'Replace' field
        if replace_text == query:
            print(' found:     ', old_string_formatted)
        else:
            # actual database find/replace
            replaceQuery(query_type,query, replace_text) 
            print(' found:     ', old_string_formatted, '\\\n', 'replaced: ', new_string_formatted, '\\\n') 

    print('match(es) found in', len(findQueryResults), 'verse(s)')
    print('-' * 50) 

    db.commit()
    db.close()    

if __name__ == "__main__":
    main(args)