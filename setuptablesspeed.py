'''
testing for speed to import flextools data into sqlite3
1) do a first run grab of all flextools data into python dict or maybe csv
2) then either do a 10000 line chunck + BEGIN XXX COMMIT loop or a 

how to set database to all-in-memory db?


'''
import sqlite3 as lite
from SIL.FieldWorks.FDO import ILangProjectRepository
conn = lite.connect("osmtestspeed.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS bibleTitles")

cur.execute("""
CREATE TABLE bibleTitles(
id integer,
title text)
""")

cur.execute("INSERT INTO bibleTitles VALUES(NULL, :bibleTitles)", 
            {'bibleTitles':"1665 Ali Bey'in el yazması - Yeni Ahit (İncil-i Şerif)"})

cur.execute("SELECT * FROM bibleTitles")
print(cur.fetchall())

for obj in DB.ObjectsIn(ILangProjectRepository):            
    for i, book in enumerate(obj.TranslatedScriptureOA.ScriptureBooksOS):
        ExportBook(book, i)   

conn.commit()
conn.close()