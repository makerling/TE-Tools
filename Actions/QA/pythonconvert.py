#import defusedxml.ElementTree as ET
import lxml.etree as etree

with open('./joined1886allbooks.xml') as fobj:
    xml = fobj.read()

root = etree.fromstring(xml)

def title_verse_num():
    elements = []
    for element in root.iter('book'):
        title_verse_num = "".join(element.xpath('titleGroup/title/annotation[1]/@status'))
        elements.append((title_verse_num,element))
    print(elements)
    return elements

def title_annots(elements):
    title_annots = {}
    for title_verse_num, element in elements: 
        # elements.xpath('titleGroup/title/annotation'):
        title_annot = element.xpath('titleGroup/title/annotation/notationQuote/para/span')
        title_annot_cat = element.xpath('titleGroup/title/annotation/notationCategories/category')
                
        if len(title_annot) > 0 and len(title_annot_cat) > 0: title_annots[title_annot[0].text] = title_annot_cat[0].text

    print(f"*{element.attrib['ID']}.0.{title_verse_num}*{'*'.join(title_annots)}")

elements = title_verse_num()
title_annots(elements)
# print(elements)