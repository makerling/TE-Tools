import sqlite3 as lite
conn = lite.connect("osmtest.db")
cur = conn.cursor()
 
cur.execute("""
CREATE TABLE bibleTitles(
id integer,
title text)
""")

cur.execute("INSERT INTO bibleTitles VALUES(:id, :bibleTitles)", {'id':1, 'bibleTitles':"1665 Ali Bey'in el yazması - Yeni Ahit (İncil-i Şerif)"})
cur.execute("INSERT INTO bibleTitles VALUES(:id, :bibleTitles)", {'id':2, 'bibleTitles':"1827 Kieffer"})

cur.execute("""
CREATE TABLE books(
id integer,
bibleTitleId integer,
name text)
""") 

cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':1, 'bibleTitleId':1, 'name':"Genesis"})
cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':2, 'bibleTitleId':2, 'name':"Exodus"})

cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':1, 'bibleTitleId':1, 'name':"Genesis"})
cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':2, 'bibleTitleId':2, 'name':"Exodus"})

cur.execute("""
CREATE TABLE verses(
id integer,
bibleTitleId integer,
verseid text,
verse text)
""") 

cur.execute("INSERT INTO verses VALUES(:id, :bibleTitleId, :verseid, :verse)", 
    {
    'id':1, 
    'bibleTitleId':1, 
    'verseid':"GEN.001.001", 
    'verse':'Oldu ki hâkimler hükm ėtdikleri günlerde yerde kaht oldu da Yahûdânıŋ Beyt-i Lehemden bir âdam o ve ʿavratı ve iki oğulları Moâb vilâyetinde sâkin olmağa vardılar '
    })

conn.commit()
conn.close()