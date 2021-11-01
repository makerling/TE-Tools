import lxml.etree as etree
from collections import Counter

with open('./joined1886allbooks.xml') as fobj:
    xml = fobj.read()

root = etree.fromstring(xml)

def title_verse_num():
    elements = []
    for element in root.iter('book'):
        title_verse_num = "".join(element.xpath('titleGroup/title/annotation[1]/@status'))
        elements.append((title_verse_num,element))
    return elements

def title_annots(elements):

    titles_final = []
    for title_verse_num, element in elements: 
        
        title_annots = {}
        for annot in element.xpath('titleGroup/title'):
            title_annot = annot.xpath('annotation/notationQuote/para/span')
            # saving category of annotation (for future functionality)
            title_annot_cat = annot.xpath('annotation/notationCategories/category')

            # avoids null matches or matches that include secondary annotations (Misc, NoNote)
            if len(title_annot) > 0 and \
                    len(title_annot_cat) > 0 and \
                    title_annot_cat[0].text != 'Misc' and \
                    title_annot_cat[0].text != 'NoNote':
                
                # appends the title annotation to the dictionary one level higher to catch all under each book
                title_annots[title_annot[0].text] = title_annot_cat[0].text
            title_tr = annot.xpath('trGroup/tr')
            title_tr = title_tr[0].text if len(title_tr) > 0 else ''

        title_verse_num = title_verse_num if len(title_verse_num) > 0 else 0 

        title_final = f"*{element.attrib['ID']}.0.{title_verse_num}*{','.join(title_annots.keys())}####{title_tr}\p"
        titles_final.append(title_final)
    
    return titles_final
        
def nodes():
    nodes = []
    for element in root.xpath('//section'):
        node = [x for x in element.xpath('p/* | p')]
        nodes.extend(node)
    
    return nodes 

def verses(nodes):
    for i,item in enumerate(nodes):
        if item.tag == 'verseStart':
            verse = item.attrib['ID'] + ' '
        if item.tag == 'annotation':
            verse += ''.join(item.xpath('notationQuote/para/span/text()')) + '*'
        if item.tag == 'p' and i != 0:
            verse += '\p '
        if item.tag == 'trGroup':
            verse += ''.join(item.xpath('tr/text()'))
        if item.tag == 'verseEnd':
            print(verse)

node_items = nodes()
verses(node_items)