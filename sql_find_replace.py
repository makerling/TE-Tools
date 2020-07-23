import sqlite3, re

db = sqlite3.connect('osmtestspeed.db')
c = db.cursor()

def preg_replace(string, pattern, replace):
    return re.sub(pattern, replace, string)

db.create_function('regexquery',3,preg_replace)
 
def regex_search(query_type, query, replace_text):
    c.execute("UPDATE verses SET title = " + query_type + "(title, ?, ?)", (query, replace_text))

query = '(lücceniŋ)' #regex or normal search term depending on the flag
replace_text = '\\1iiiii'

#'regexquery' for regex, 'replace' for normal replace
regex_search('regexquery', query, replace_text)

db.commit()

c.execute("SELECT title FROM verses WHERE title LIKE '%neşviii%' ")
print(c.fetchall())

db.close()

