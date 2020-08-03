import sqlite3, re

db = sqlite3.connect('osmtesting.db')
c = db.cursor()

# def preg_replace(string, pattern, replace):
    # return re.sub(pattern, replace, string)

# db.create_function('regexquery',3,preg_replace) #3 represents number of arguments
 
# def regex_search(query_type, query, replace_text):
    # c.execute("UPDATE verses SET title = " + query_type + "(title, ?, ?)", (query, replace_text))

# query = 'iidiler' #regex or normal search term depending on the flag
# replace_text = 'midiler'

#'regexquery' for regex, 'replace' for normal replace
# regex_search('regexquery', query, replace_text)

# db.commit()

# c.execute("SELECT title FROM verses WHERE title LIKE '%midiler%' ")

c.execute("""
CREATE TRIGGER IF NOT EXISTS trig
AFTER UPDATE on verses 
FOR EACH ROW 
    WHEN old.updateFlag IS NULL
BEGIN 
    UPDATE verses SET updateFlag = '1'
    WHERE rowid = NEW.rowid;
END;
""")
db.commit()

#clearing out previous query's flags
# c.execute("""
# UPDATE verses SET updateFlag = Null WHERE updateFlag IS NOT NULL
# """)

# db.commit()    
query = 'ise'
command = "SELECT verse FROM verses WHERE verse like '%" + query + "%'"

# good for find part, returns before and after# c.execute("SELECT verse, replace( verse, 'midiler', 'didiler' ) FROM verses WHERE verse like '%midiler%'")
c.execute(command)

# c.execute("DROP TRIGGER IF EXISTS trig;")

#need spaces to match only string, not substrings - in normal search that is expected behavior
# c.execute("UPDATE verses SET verse = replace( verse, 'Dâvûd', 'david' ) WHERE verse like '% Dâvûd %'") 

db.commit()

print(c.fetchall())

db.close()