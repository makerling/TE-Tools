import sqlite3, re
from colored import stylize, attr, fg

def main(args, query, replace_text):

    db = sqlite3.connect('osmtestspeed.db')
    c = db.cursor()

    ################################ BULK REPLACE FUNCTIONS - REGEX AND STANDARD REPLACE#############
    def preg_replace(string, pattern, replace):
        return re.sub(pattern, replace, string)
    db.create_function('regexquery',3,preg_replace) #3 represents number of arguments
    def regex_search(query_type, query, replace_text):
        # query type determins whether the replace is standard replace() or custom regex()
        c.execute("UPDATE verses SET verse = " + query_type + "(verse, ?, ?)", (query, replace_text))    
    #################################################################################################
    def preg_regexsearch(pattern,string):
        return re.findall(pattern, string)
    db.create_function('regexquerysearch',2,preg_regexsearch) 
    def find_only(query):
        # command = "SELECT verse FROM verses WHERE verse REGEXQUERYSEARCH(verse,'" + query + "')"
        c.execute("SELECT verse FROM verses WHERE verse REGEXQUERYSEARCH(verse,'" + query + "')"
        # print(command)
        # c.execute(command)   
    #################################################################################################
    # def find_only(query):
    #     command = "SELECT verse FROM verses WHERE verse like '%" + query + "%'"
    #     c.execute(command) # having percent signs makes it do fuzzy match
    #     query_result_raw = c.fetchall()

    #     for i in query_result_raw:
    #         argument = stylize(query, attr('bold'))
    #         query_result_formatted = re.sub(query, argument,i[0]) # result (i) is list of tuples, second item is always empty
    #         print(query_result_formatted)

    # if replace_text == None:
    # print('replace text is: %s' % replace_text)
    # find_only(query)

    #'regexquery' for regex, 'replace' for normal replace
    # regex_search('replace', query, replace_text)    
    db.commit()
    db.close()

    print('-' * 30)  # separating

if __name__ == "__main__":
    main()