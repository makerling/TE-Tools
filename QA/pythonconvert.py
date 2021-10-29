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
    for title_verse_num, element in elements: 
        
        title_annots = {}
        for annot in element.xpath('titleGroup/title/annotation'):
            title_annot = annot.xpath('notationQuote/para/span')
            title_annot_cat = annot.xpath('notationCategories/category')

            if len(title_annot) > 0 and \
                    len(title_annot_cat) and \
                    title_annot_cat[0].text != 'Misc' and \
                    title_annot_cat[0].text != 'NoNote':
                
                title_annots[title_annot[0].text] = title_annot_cat[0].text

        title_verse_num = title_verse_num if len(title_verse_num) > 0 else 0
        print(f"*{element.attrib['ID']}.0.{title_verse_num}*{','.join(title_annots.keys())}####")

elements = title_verse_num()
title_annots(elements)