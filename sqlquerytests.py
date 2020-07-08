import sqlite3, re

db = sqlite3.connect('osmtest.db')
c = db.cursor()

def preg_replace(string, pattern, replace):
    return re.sub(pattern, replace, string)

db.create_function('regexquery',3,preg_replace)
 
def regex_search(query_type, query, replace_text):
    c.execute("UPDATE verses SET verse = " + query_type + "(verse, ?, ?)", (query, replace_text))

query = '..rse' #regex or normal search term depending on the flag
replace_text = 'nurse'

#'regexquery' for regex, 'replace' for normal replace
regex_search('replace', query, replace_text)

db.commit()

c.execute("SELECT verse FROM verses")
print(c.fetchall())

db.close()