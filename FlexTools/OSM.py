# -*- coding: utf-8 -*-

import unicodedata
from FTModuleClass import *
import FLExFDO
from SIL.FieldWorks.FDO import (IScrBookRepository, IScrBook, IScriptureRepository, 
ILangProjectRepository, IScripture, IScriptureRepository, IStPara, 
IStParaRepository, IStText, IStTextRepository, IScrSection, IScrSectionRepository)

from SILUBS.SharedScrUtils import *

from SIL.FieldWorks.Common.COMInterfaces import ITsString
from SIL.FieldWorks.FDO.DomainServices import SegmentServices
import codecs
import re
import sys, os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os
import getpass

from itertools import tee, islice, chain, izip
from collections import OrderedDict 

#----------------------------------------------------------------

# Scripture Repository > ScriptureBookOS (IScrBook) > TitleOA (StText) > ParagraphOS (IStPara) > Text (ITsString) = "Rût"
# TODO - add options for AllBooks, FilteredBooks, SingleBook - line 458 471

# #TODO work on encapsulation/inheritance with python
                 
#----------------------------------------------------------------

def MainFunction(DB):    
    
    print("DB is: %s" % DB)
                
    #--------UTIL-FUNCTIONS/METHODS--------------------------------    
        
    #https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
    #proper way to check is string is null in python    
    def isBlank (string):
        # return not (string and string.strip())
        return not string      

    #https://stackoverflow.com/questions/1011938/python-loop-that-also-accesses-previous-and-next-values/54995234#54995234
    #Python loop that also accesses previous and next values
    def previous_and_next(value):
        prevs, items, nexts = tee(value, 3)
        prevs = chain([None], prevs)
        nexts = chain(islice(nexts, 1, None), [None])
        return izip(prevs, items, nexts)        
                
    #----------------------------------------------------------------

    #https://github.com/sillsdev/FieldWorks/blob/hotfix/8.3.14/Src/TE/TeImportExport/ExportXml.cs
    ####<oxes>####  line 280 - 295
    oxes = ET.Element("oxes")
    oxes.set('xmnls', 'http://www.wycliffe.net/scripture/namespace/version_1.1.4')      

    def ExportTE():         
        
        #<oxesText>
        oxesText = ET.SubElement(oxes, 'oxesText')        
        oxesText.set('canonical', 'true')
        oxesText.set('xml:lang', 'tr')        
        oxesText.set('oxesIDWork', 'WBT.tr')        
        oxesText.set('type', 'Wycliffe-1.1.4')
        
    ####<header>#### #line 333 - 375        
        header = ET.SubElement(oxesText, 'header')
        #<revisionDesc resp="wor">
        revisionDesc = ET.SubElement(header, 'revisionDesc', resp='wor')

        #<date>
        dateForm = str(datetime.now().strftime("%Y.%m.%d"))
        datetoday = ET.SubElement(revisionDesc, 'date')
        datetoday.text = dateForm

        def projectName(): #is there another easier way? dbName?
            projectsPath = FLExFDO.FwDirectoryFinder.ProjectsDirectory
            objs = os.listdir(unicode(projectsPath))
            dbList = []
            for f in objs:
                # if os.path.isdir(os.path.join(projectsPath, f)):
                    # dbList.append(f)
                g = os.path.join(projectsPath, f)
                dbList.append(g)
            projectDir = max(dbList, key=os.path.getatime)
            for h in os.listdir(unicode(projectDir)):
                if h.endswith(".fwdata"):
                    filenameNoext = os.path.splitext(h)[0]
                    print("current project is: %s" % filenameNoext)
                    return filenameNoext 
        
        #<para xml:lang="en">
        domain = os.environ['userdomain'] + '\\' + getpass.getuser()                 
        longDate = str(datetime.now().strftime("%B %d, %Y at %I:%M %p"))
        string = projectName() + " exported by " + domain + " on " + longDate
        para = ET.SubElement(revisionDesc, 'para')
        para.set('xml:lang','en')
        para.text = string
        
        #<work oxesWork="WBT.tr">
        work = ET.SubElement(header, 'work', oxesWork='WBT.tr')
        #<titleGroup>
        titleGroup = ET.SubElement(work, 'titleGroup')        
        #<title type="main">
        title = ET.SubElement(titleGroup, 'title', type='main')
        #<trGroup>
        trGroup = ET.SubElement(title, 'trGroup')
        #<tr>
        tr = ET.SubElement(trGroup, 'tr')
        tr.text = "TODO: title of New Testament or Bible goes here"
        
        #<contributor role="Translator" ID="wor">DESKTOP-HLVGD70\workother</contributor>
        contributor = ET.SubElement(work, 'contributor')
        contributor.set('ID', 'wor')        
        contributor.set('role', 'Translator')
        contributor.text = domain  
    
    ####<titlePage>####    #line 403 - 423
        titlePage = ET.SubElement(oxesText, 'titlePage')
        #<titleGroup>
        titleGroup = ET.SubElement(titlePage, 'titleGroup')        
        #<title type="main">
        title = ET.SubElement(titleGroup, 'title', type='main')
        #<trGroup>
        trGroup = ET.SubElement(title, 'trGroup')
        #<tr>
        tr = ET.SubElement(trGroup, 'tr')
        tr.text = "TODO: title of New Testament or Bible goes here"        

    #----------------------------------------------------------------                     
    
    def ExportScripture():
        
        sCanon = None
        #iterate through ScriptureBooksOS object for AllBooks
        #TODO - give options for single books or filtered books - will have to build this myself since FLEx can't be open while this is run
        for obj in DB.ObjectsIn(ILangProjectRepository):            
            # bookCount = obj.TranslatedScriptureOA.ScriptureBooksOS.Count
            for i, book in enumerate(obj.TranslatedScriptureOA.ScriptureBooksOS):
                ExportBook(book, i)                                 

    #----------------------------------------------------------------   

    def ExportBook(book, i):            
        
        def canonExists(oxes, sCanon):  #check for existence of canon tag
            for i in oxes.findall('.//oxesText'): 
                for j in i.findall('./canon[@ID="%s"]' % sCanon):
                    return j

        def createCanon(oxes, sCanon):  #create canon tag 
            if canonExists(oxes, sCanon) == None:
                oxesText = oxes.find('.//oxesText')
                canon = ET.SubElement(oxesText, 'canon', ID=sCanon)                            
        
        m_iCurrentBook = book.CanonicalNum
        m_sCurrentBookId = book.BookId 
        m_iCurrentChapter = 0
        m_sCurrentChapterNumber = None
        m_iCurrentVerse = 0
        m_sCurrentVerseNumber = None
               
        #conditional ternary operator - set the canon value
        sCanon = 'ot' if book.CanonicalNum < 40 else 'nt'
        
        createCanon(oxes, sCanon)
        #creates book tag
        bookElement = ET.SubElement(canonExists(oxes, sCanon), 'book', ID=m_sCurrentBookId)   

        ExportBookTitle(book, bookElement)
        
        # iLim = book.SectionsOS.Count
        
        # for i,section in enumerate(book.SectionsOS): 
            # nextSection = book.SectionsOS[i + 1] if (i + 1) < iLim else None
        # for previousSection, section, nextSection in previous_and_next(book.SectionsOS):             
            # ExportBookSection(section, nextSection, m_iCurrentChapter, bookElement)

              
    #----------------------------------------------------------------         
     
    def ExportBookTitle(book, bookElement):  #FINISHED
        
        titleGroupShort = ITsString(book.Name.BestVernacularAlternative).Text  
        # print("titleGroupShort is: %s" % titleGroupShort)     #Sifr-İ Raʿos 

        def titleGroupNameFunction():
            for titlePara in book.TitleOA.ParagraphsOS:  
                titleGroupName = ITsString(titlePara.Contents).Text       
                # print("titleGroupName is: %s" % titleGroupName)  #Rût 
                return titleGroupName
        
        titleGroup = ET.SubElement(bookElement, 'titleGroup', short=titleGroupShort)   #Sifr-İ Raʿos     
        # print("titleGroup is: %s" % titleGroupNameFunction())  
        title = ET.SubElement(titleGroup, 'title', type="main")
        trGroup = ET.SubElement(title, 'trGroup')
        tr = ET.SubElement(trGroup, 'tr')   
        tr.text = titleGroupNameFunction() #Rût 
        
        ExportSection(book, bookElement)
        
    def ExportSection(book, bookElement):

        for section in book.SectionsOS:       
                        
            sectionElement = ET.SubElement(bookElement, 'section')
            # print("Section.ContentOA.ParagraphOS Count is: %s" % section.ContentOA.ParagraphsOS.Count)
            
            ExportParaHeading(book, section, bookElement, sectionElement)
            
    def ExportParaHeading(book, section, bookElement, sectionElement):
    
        for paraHeading in section.HeadingOA.ParagraphsOS:
            sectionHeadTitle = ITsString(paraHeading.Contents).Text
            # print("sectionHeadTitle is: %s" % sectionHeadTitle)
            sectionHead = ET.SubElement(sectionElement, 'sectionHead')        
            trGroup = ET.SubElement(sectionHead, 'trGroup')        
            tr = ET.SubElement(trGroup, 'tr') 
            tr.text = sectionHeadTitle
            
            ExportPara(book, section, bookElement, sectionElement)
            
    def ExportPara(book, section, bookElement, sectionElement):
            
        sectionCount = section.ContentOA.ParagraphsOS.Count #not necessary?                
        totalVerseRefs = []

        for para in section.ContentOA.ParagraphsOS:
            for paraSub in para: 
                z = paraSub.StartRef.Verse, paraSub
                if paraSub.FirstInStText == False:
                    totalVerseRefs.append(z)
            
        enumeration = list(enumerate(totalVerseRefs))        
        n = 0 #for iterator

        for previousSection, section, nextSection in previous_and_next(enumeration): 
                                      
            paraSub = section[1][1]
            
            n += 1
            # print("n is: %s, current verse is: %s" % (n, paraSub.StartRef.Verse))

            bookID = book.BookId
            chapter = int(paraSub.StartRef.Chapter)
            verse = int(paraSub.StartRef.Verse)
            
            chapterStartString = bookID + '.' + str(chapter)
            verseStartString = bookID + '.' + str(chapter) + '.' + str(verse)                            

            paraElement = ET.SubElement(sectionElement, 'p')             
            
            # if paraSub.FirstInStText == True: 
                # OpenChapter(paraSub, paraElement, bookID, chapter, verse, sectionCount, chapterStartString)
                
            if paraSub.VerseNumberRun == True:
                if n == 1:
                    OpenChapter(paraSub, paraElement, bookID, chapter, verse, sectionCount, chapterStartString)
                
                OpenVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString)                                        
                ExportVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString)             
                if nextSection != None: #catches everything but the last element
                    # print("current verse is: %s, next verse is: %s" % (section[0],nextSection[0]))                
                    if section[1][0] < nextSection[1][0]: #only processes elements with one <p>
                        EndVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString)
                elif n == len(totalVerseRefs): #processes the very last element
                    EndVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString)
                    CloseChapter(paraSub, paraElement, bookID, chapter, verse, sectionCount, chapterStartString)
                    
            elif paraSub.VerseNumberRun == False: #catches multi-<p> paragraphs                       
                ExportVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString)
                if n == len(totalVerseRefs): ##processes the very last element if it is part of a multi-<p> paragraphs
                    EndVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString)
                    CloseChapter(paraSub, paraElement, bookID, chapter, verse, sectionCount, chapterStartString)
    
        # print("verse1 are: %s, count is: %s" % (totalVerseRefs,len(totalVerseRefs)))
        # print("i-s------- are: %s, count is: %s" % (enumeration, len(enumeration)))  
            
        # paraElement.insert(1,chapterStartElement)
        # paraElement.insert(2,verseStartElement)
        # paraElement.insert(3,trGroupElement)
        # paraElement.insert(4,verseEndElement)
        # paraElement.insert(5,chapterEndElement)
    
    def OpenChapter(paraSub, paraElement, bookID, chapter, verse, sectionCount, chapterStartString):        
                       
        # print("FirstInStText is True")
        chapterStartElement = ET.SubElement(paraElement, "chapterStart")             
        chapterStartElement.set('ID',chapterStartString)
        chapterStartElement.set('n',str(chapter))                       

    def OpenVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString):
            
        verseStartElement = ET.SubElement(paraElement, "verseStart")                 
        verseStartElement.set('ID',verseStartString)
        verseStartElement.set('n',str(verse))
        # paraElement.insert(2,verseStartElement)
        
    def ExportVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString):                          
            
        trGroupElement = ET.SubElement(paraElement, "trGroup")
        trElement = ET.SubElement(trGroupElement, "tr")                            
        if paraSub.ChapterNumberRun == False:
            trElement.text = ITsString(paraSub.Text).Text    
            # print("verse is: %s" % ITsString(paraSub.Text).Text)
    
    def EndVerse(paraSub, paraElement, bookID, chapter, verse, sectionCount, verseStartString):
        
        verseEndElement = ET.SubElement(paraElement, "verseEnd")                 
        verseEndElement.set('ID',verseStartString)             

    def CloseChapter(paraSub, paraElement, bookID, chapter, verse, sectionCount, chapterStartString):
    
        chapterEndElement = ET.SubElement(paraElement, "chapterEnd") 
        chapterEndElement.set('ID',chapterStartString) 

#----------------------------------------------------------------
        
    ExportTE()
    ExportScripture()   
    
    xmlfile = 'testosm.oxes'
    tree = ET.ElementTree(oxes)
    writing = tree.write(xmlfile, encoding="utf-8", xml_declaration=True)                                     