import sqlite3, re
from colored import stylize, attr
from pathlib import Path

class Term:

    def __init__(self, query, query_type, replace_text):
         
        # platform independent file path solution
        db_path = Path("Actions/")
                
        self.query = query
        # determines if query should be using built-in replace() or custom regexp()
        self.query_type = query_type
        # determines if only find should be run or find and replace
        self.replace_text = replace_text
        self.db = sqlite3.connect(db_path / 'project.db')
        self.c = self.db.cursor()
        # can't use this construction because unit test won't work
        # order of re.sub is weird because replaceTerm() is written to default to replace() order of arguments
        # self.regexp = self.db.create_function('regexp', 3, lambda x, y, z: re.sub(y, z, x))
        # self.match = self.db.create_function('match', 2, lambda x, y: 1 if re.findall(x, y) else 0)  

    ####################### BULK REPLACE FUNCTIONS - REGEX AND STANDARD FIND/REPLACE #######################        

    # query_type determines whether the replace is built-in (non-regex) replace() or user-defined function regexp()
    def replaceTerm(self):     
        self.db.create_function('regexp', 3, lambda x, y, z: re.sub(y, z, x))
        self.db.create_function('match', 2, lambda x, y: 1 if re.findall(x, y) else 0)               
        # without WHERE statement entire database is updated, affects trigger
        self.c.execute("""
            UPDATE verses 
            SET verse = 
                """ + self.query_type + """(verse, '""" + self.query + """','""" + self.replace_text + """') 
            WHERE verse 
                MATCH '""" + self.query + """' 
            """)
        return self.c.fetchall()
    ############################## FIND FUNCTIONS - REGEX AND STANDARD FIND ################################ 
    
    #returns verse string pre and post replace, doesn't actually make any replacements (because of SELECT)
    def findTerm(self):      
        self.db.create_function('regexp', 3, lambda x, y, z: re.sub(y, z, x))
        self.db.create_function('match', 2, lambda x, y: 1 if re.findall(x, y) else 0)                               
        self.c.execute("""
            SELECT verse, 
                """ + self.query_type + """(verse, '""" + self.query + """', '""" + self.replace_text + """') 
            FROM verses 
            WHERE verse 
                MATCH '""" + self.query + """'
            """)    
        return self.c.fetchall()   
    ################################ Stylizing Results ######################################################

    def stylizeResult(self,findTermResults):
        # loops through results of query and highlights search term/replace term for output
        results = []
        for i in findTermResults:
            oldstring = stylize(re.findall(self.query,i[0])[0], attr('bold')) # need to select first result of re.findall
            newstring = stylize(self.replace_text, attr('bold')) # TODO implement regex backreferences 
            old_string_formatted = re.sub(self.query, oldstring,i[0]) 
            new_string_formatted = re.sub(self.replace_text, newstring,i[1])
            results.append((old_string_formatted,new_string_formatted))
        return results

def main(args):

    ############# populating constructor arguments #############
    query = args.find    
    # determines if query should be using built-in replace() or custom regexp()
    query_type = 'replace' if args.Regex == False else 'regexp'
    # determines if only find should be run or find and replace
    replace_text = query if args.replace == None else args.replace

    ######## running query/replace/stylize functions ###########
    term1 = Term(query, query_type, replace_text)
    findTermResults = term1.findTerm()
    result = term1.stylizeResult(findTermResults) # result is list of tuples 
    # adding replace strings to output only if 'Replace' field contains text
    if replace_text == query:
        for i in result:
            print(' found:      ', i[0])
    else:
        term1.replaceTerm() # actual database find/replace 
        for i in result:
            print(' found:         ', i[0], '\\\n', 'replaced:  ', i[1], '\\\n')         

    print('match(es) found in', len(findTermResults), 'verse(s)')
    print('-' * 50) 

    term1.db.commit()
    term1.db.close()