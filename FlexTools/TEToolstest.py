# -*- coding: utf-8 -*-
import sqlite3, re
from colored import stylize, attr, fg

def main(query_type, query, replace_text):

    db = sqlite3.connect('osmtestspeed.db')
    c = db.cursor()

    ####################### BULK REPLACE FUNCTIONS - REGEX AND STANDARD FIND/REPLACE #######################
    # this order of arguments in functions preserves ability to swap replace() and regexp() interchangably
    def reSub(string, query, replace_text):
        return re.sub(query, replace_text, string)
    db.create_function('regexp', 3, reSub) #3 represents number of arguments
    
    # query_type determines whether the replace is built-in (non-regex) replace() or custom function regexp()
    def replaceQuery(query_type, query, replace_text): 
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
    def findQuery(query_type, query, replace_text): 
        c.execute("""
            SELECT verse, 
                """ + query_type + """(verse, '""" + query + """', '""" + replace_text + """') 
            FROM verses 
            WHERE verse 
                MATCH '""" + query + """'
            """)    
        return c.fetchall()   
    #########################################################################################################

    # replace() & regexp() function errors when replace_text is None, workaround to still get pre/post replace strings
    # replace_text = query if replace_text is None 
    
    print('query_type is: ',query_type,' || query is: ',query,' || replace_text is: ',replace_text)
    
    findQueryResults = findQuery(query_type,query, replace_text) 
    print(findQueryResults)
    # loops through results of query and highlights search term/replace term
    for i in findQueryResults:
        oldstring = stylize(re.findall(query,i[0])[0], attr('bold')) # need to select first result of re.findall
        newstring = stylize(replace_text, attr('bold')) # TODO implement regex backreferences 
        old_string_formatted = re.sub(query, oldstring,i[0]) 
        new_string_formatted = re.sub(replace_text, newstring,i[1])
        print('new_string_formatted is: ', new_string_formatted)

        # adding replace strings to output only if text is put into 'Replace' field
        if replace_text == query:
            print(' found:     ', old_string_formatted)
        else:
            # actual database find/replace
            replaceQuery(query_type, query, replace_text) 
            print('replace_text is: ', replace_text)
            print(' found:     ', old_string_formatted, '\\\n', 'replaced: ', new_string_formatted, '\\\n') 

    print('match(es) found in', len(findQueryResults), 'verse(s)')
    print('-' * 50) 

    db.commit()
    db.close()     

if __name__ == "__main__":
    query = 'Mah.*?\sve'
    replace_text = 'Magoo'
    query_type = 'regexp'
    
    main(query_type, query, replace_text)