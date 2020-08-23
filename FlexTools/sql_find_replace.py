# -*- coding: utf-8 -*-
import sqlite3, re
from colored import stylize, attr, fg 

def main(args):

    db = sqlite3.connect('FlexTools\\osmtestspeed.db')
    c = db.cursor()
    # this order of arguments in functions preserves ability to swap replace() and regexp() interchangably
    def reSub(string, query, replace_text):
        return re.sub(query, replace_text, string)    
    # for replace function
    db.create_function('regexp', 3, reSub) #3 represents number of arguments
    # for match function
    db.create_function('match', 2, lambda x, y: 1 if re.findall(x, y) else 0)

    ####################### BULK REPLACE FUNCTIONS - REGEX AND STANDARD FIND/REPLACE #######################
    
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
    ################################ Stylizing Results ######################################################

    def stylizeResult(findQueryResults, query, replace_text):
        # loops through results of query and highlights search term/replace term
        results = []
        for i in findQueryResults:
            oldstring = stylize(re.findall(query,i[0])[0], attr('bold')) # need to select first result of re.findall
            newstring = stylize(replace_text, attr('bold')) # TODO implement regex backreferences 
            old_string_formatted = re.sub(query, oldstring,i[0]) 
            new_string_formatted = re.sub(replace_text, newstring,i[1])
            results.append((old_string_formatted,new_string_formatted))

        return results
    #########################################################################################################
    
    # replace() & regexp() function errors when replace_text is None, workaround to still get pre/post replace strings
    # replace_text = query if replace_text is None     

    query = args.find    
    # determines if query should be using built-in replace() or custom regexp()
    query_type = 'replace' if args.Regex == False else 'regexp'
    # determines if only find should be run or find and replace
    replace_text = query if args.replace == None else args.replace
    # print(query_type)

    findQueryResults = findQuery(query_type, query, replace_text) 
    # print(findQueryResults)

    result = stylizeResult(findQueryResults, query, replace_text) #result is list of tuples 

    # adding replace strings to output only if text is put into 'Replace' field
    if replace_text == query:
        for i in result:
            print(' found:     ', i[0])
    else:
        # actual database find/replace
        replaceQuery(query_type,query, replace_text) 
        for i in result:
            print(' found:     ', i[0], '\\\n', 'replaced: ', i[1], '\\\n')         


    print('match(es) found in', len(findQueryResults), 'verse(s)')
    print('-' * 50) 

    db.commit()
    db.close()    

if __name__ == "__main__":
    main()