# -*- coding: utf-8 -*-

import sqlite3 as lite
from SIL.FieldWorks.FDO import ILangProjectRepository
from SIL.FieldWorks.Common.COMInterfaces import ITsString
import re

# conn = lite.connect("osmtest.db")
# cur = conn.cursor()
 
# cur.execute("""
# CREATE TABLE bibleTitles(
# id integer,
# title text)
# """)

# cur.execute("INSERT INTO bibleTitles VALUES(:id, :bibleTitles)", {'id':1, 'bibleTitles':"1665 Ali Bey'in el yazması - Yeni Ahit (İncil-i Şerif)"})
# cur.execute("INSERT INTO bibleTitles VALUES(:id, :bibleTitles)", {'id':2, 'bibleTitles':"1827 Kieffer"})

# cur.execute("""
# CREATE TABLE books(
# id integer,
# bibleTitleId integer,
# name text)
# """) 

# cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':1, 'bibleTitleId':1, 'name':"Genesis"})
# cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':2, 'bibleTitleId':2, 'name':"Exodus"})

# cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':1, 'bibleTitleId':1, 'name':"Genesis"})
# cur.execute("INSERT INTO books VALUES(:id, :bibleTitleId, :name)", {'id':2, 'bibleTitleId':2, 'name':"Exodus"})

# cur.execute("""
# CREATE TABLE verses(
# id integer,
# bibleTitleId integer,
# verseid text,
# verse text,)
# """) 

# cur.execute("INSERT INTO verses VALUES(:id, :bibleTitleId, :verseid, :verse)", 
    # {
    # 'id':1, 
    # 'bibleTitleId':1, 
    # 'verseid':"GEN.001.001", 
    # 'verse':'Oldu ki hâkimler hükm ėtdikleri günlerde yerde kaht oldu da Yahûdânıŋ Beyt-i Lehemden bir âdam o ve ʿavratı ve iki oğulları Moâb vilâyetinde sâkin olmağa vardılar '
    # })

# conn.commit()
# conn.close()
#----------------------------------------------------------------
def extracttoSQL(DB):
    
    conn = lite.connect("osmtestspeed.db")
    cur = conn.cursor()

    # cur.execute("DROP TABLE IF EXISTS bibleTitles")

    # cur.execute("""
    # CREATE TABLE bibleTitles(
    # id integer,
    # title text)
    # """)

    # cur.execute("DROP TABLE IF EXISTS books")

    # cur.execute("""
    # CREATE TABLE books(
    # id integer,
    # bookid text,
    # booknum integer,
    # title text)
    # """)

    # cur.execute("DROP TABLE IF EXISTS verses")

    # cur.execute("""
    # CREATE TABLE verses(
    # id integer,
    # bookid text,
    # booknum integer,
    # verse text,
    # origverse text)
    # """)
    # print('finished creating tables, populating them now')
   ################################## verses and refs ###################################
    books_in_proj = []
    verses_in_proj = []
    for obj in DB.ObjectsIn(ILangProjectRepository):            
        for i, book in enumerate(obj.TranslatedScriptureOA.ScriptureBooksOS):
            bookId = book.BookId
            bookNum = book.CanonicalNum
            books_in_proj.append((i,bookId,bookNum,str(book))) #without string just the object pointer gets transferred
            for section in book.SectionsOS: 
                for para in section.ContentOA.ParagraphsOS:
                    for j, paraSub in enumerate(para): 
                        if paraSub.ChapterNumberRun == False: #avoids the first blank entry of a chapter
                            chapter_num = int(paraSub.StartRef.Chapter)
                            verse_num = int(paraSub.StartRef.Verse)
                            ref = bookId + '.' + '%03d.%03d' % (chapter_num,verse_num) #padding to 3 place values
                            verse_text_w_num = ITsString(paraSub.Text).Text
                            verse_text = re.sub(r'^(\d+)',r'\1 ',verse_text_w_num) #separates versenum to make search catch all with space
                            verses_in_proj.append(('0',bookNum,ref,verse_text,None))

                            # tss = DB.db.TsStrFactory.MakeString('hello world', '999000008')
                            # scrTxtPara.Contents = tss

    cur.executemany("INSERT INTO books VALUES(?,?,?,?)", books_in_proj)
    cur.executemany("INSERT INTO verses VALUES(?,?,?,?,?)", verses_in_proj)

    conn.commit()

    #adding trigger to identify rows that have been changed in UPDATE statement
    # updateFlag = '1', might need to add this before origverses line
    # cur.execute("""
    # CREATE TRIGGER IF NOT EXISTS trig
    # AFTER UPDATE on verses 
    # FOR EACH ROW 
    #     WHEN old.origverse IS NULL
    # BEGIN 
    #     UPDATE verses SET             
    #         origverse = verse
    #     WHERE rowid = NEW.rowid;
    # END;
    # """)
    # conn.commit()

    conn.close()    

    print('finished populating tables')

#----------------------------------------------------------------
if __name__ == "__main__":    

    extracttoSQL(DB)
       
                            
    '''
    tried to do direct find/replace with string in FLEx database, but can't figure out replace
    but code below is a good start if you want to pick it up later

    # for obj in DB.ObjectsIn(IScrTxtParaRepository): 
    # for objsub in obj:  
        # text = ITsString(objsub.Text).Text
        # print(text)
        # tss = DB.db.TsStrFactory.MakeString('hello world', '999000008')
        # obj.Contents = tss # doesn't work, how do I set the string?

    # endFTtools = timer()
    # processtime = (endFTtools - startFTtools)
    # print('processtime FTtools is: %s' % processtime)
    '''                        

    # cur.executemany("""UPDATE books 
    #                 SET id = (?), 
    #                 bookid = (?), 
    #                 booknum = (?), 
    #                 title = (?) 
    #                 """, books_in_proj)
    # cur.executemany("""UPDATE verses 
    #                 SET id = (?),
    #                 bookid = (?),
    #                 booknum = (?),
    #                 title = (?)
    #                 """, verses_in_proj)