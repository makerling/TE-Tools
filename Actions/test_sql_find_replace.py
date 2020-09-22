# -*- coding: utf-8 -*-
import unittest
import sqlite3, re
from sql_find_replace_class import Term

class testsqlfindreplace(unittest.TestCase):
    
    def setUp(self):
        
        self.db = sqlite3.connect(':memory:')
        self.c = self.db.cursor()        
        self.c.execute("""
            CREATE TABLE verses(
            id integer,
            bookid text,
            booknum integer,
            verse text,
            origverse text)
        """)      

        self.verses = [(0,8,"RUT.001.005","5 ȯndan Mahlon ikisi de öldüler",None), 
            (0,8,"RUT.001.005","5 ȯndan Kilyona ikisi de öldüler",None), 
            (0,8,"RUT.001.003",'3 ondan Naominin kocasi Elimelek oldu',None), 
            (0,8,"RUT.001.003",'3 ȯndan Naʿominiŋ kocası Elimelek ȯndan öldü',None)] # testing repeat words


        self.c.executemany("INSERT INTO verses VALUES(?,?,?,?,?)", self.verses)

    # def test_findTermfunction(self):
    #     self.query_type = 'replace'
    #     self.query = 'Mahlon'  
    #     self.replace_text = 'Kilyona'    
    #     print(Term.findTerm(self)[0][0])
    #     print(self.verses[0][3])
    #     self.assertEqual(Term.findTerm(self)[0][0],self.verses[0][3]) 

    def test_replaceTermfunction(self):
        query = 'Mahlon'        
        query_type = 'replace'
        replace_text = 'Kilyona'        
        self.assertEqual(Term.replaceTerm(self),self.verses[0][3])         

    # def test_replaceTermfunction(self):        
    #     query = 'Mahlon'        
    #     query_type = 'replace'
    #     replace_text = 'Kilyona'        
    #     term1 = Term(query, query_type, replace_text)
    #     self.assertEqual(term1.replaceTerm(),self.verses[1][3]) 

if __name__ == '__main__':
    unittest.main()