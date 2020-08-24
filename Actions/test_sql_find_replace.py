# -*- coding: utf-8 -*-
import unittest
import sqlite3, re
import sql_find_replace

class testsqlfindreplace(unittest.TestCase):
    
    def setUP(self):
        
        db = sqlite3.connect(':memory:')
        c = db.cursor()        
        cur.execute("""
            CREATE TABLE verses(
            id integer,
            bookid text,
            booknum integer,
            verse text,
            origverse text)
        """)      

        verses = [(0,8,"RUT.001.005","5 ȯndan Mahlon ve Kilyon ikisi de öldüler",None), # testing ASCII regex search
            (0,8,"RUT.001.003",'3 ȯndan Naʿominiŋ kocası Elimelek öldü',None), # testing non-ASCII regex search
            (0,8,"RUT.001.003",'3 ȯndan Naʿominiŋ kocası Elimelek ȯndan öldü',None)] # testing repeat words


        cur.executemany("INSERT INTO verses VALUES(?,?,?,?,?)", verses)

    def test_replacefunction(self):
        query_type = 'replace'
        query = 'Mahlon'
        replace_text = 'Magoo'

        #simple find only
        result = sql_find_replace.main()
        #.findQuery(query_type, query, replace_text)
        assertEqual(result,verses[0][3])
        


print('hello world')

if __name__ == '__main__':
    unittest.main()