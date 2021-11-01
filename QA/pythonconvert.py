import lxml.etree as etree
from collections import Counter

with open('./joined1886allbooks.xml') as fobj:
    xml = fobj.read()

root = etree.fromstring(xml)
      
def nodes():
    nodes = []
    for element in root.xpath('//section'):
        node = [x for x in element.xpath('p/* | p | ../titleGroup/title/trGroup | ../titleGroup/title/annotation')]
        nodes.extend(node)
    return nodes 

def verses(nodes):
    for i,item in enumerate(nodes):
        # catches title annotations
        if item.tag == 'annotation' and '.0.0' in item.attrib['oxesRef']:
            verse = item.attrib['oxesRef'] + '*'
            verse += ''.join(item.xpath('notationQuote/para/span/text()')) + '*'
        if item.tag == 'verseStart':
            verse = item.attrib['ID'] + '*'
        if item.tag == 'annotation':
            verse += ''.join(item.xpath('notationQuote/para/span/text()')) + '*'
        if item.tag == 'p' and i != 0:
            verse += '\p '
        if item.tag == 'trGroup':
            verse += ''.join(item.xpath('tr/text()'))
            # catches and prints title
            if '.0.0' in verse:
                print(verse)
        if item.tag == 'verseEnd':
            print(verse)

node_items = nodes()
verses(node_items)