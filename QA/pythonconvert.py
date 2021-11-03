import lxml.etree as etree
import unicodedata

with open('./joined1886allbooks.xml') as fobj:
    xml = fobj.read()

root = etree.fromstring(xml)
      
def nodes():
    nodes = []
    for element in root.xpath('//section'):
        node = [x for x in element.xpath('p/* | p')]
        nodes.extend(node)
    return nodes 

def verses(nodes):
    for item in nodes:

        # start of verse block, resets verse variable
        if item.tag == 'verseStart':
            verse = []
            annots = []
            ref = item.attrib['ID']

        skip_tags = set(['Misc','NoNote'])
        tag_path = 'notationCategories/category/text()'
        if item.tag == 'annotation' and not skip_tags.intersection(set(item.xpath(tag_path))):
            annot = item.xpath('notationQuote/para/span/text()')
            annots.append(unicodedata.normalize('NFC', annot[0]))
            tag = item.xpath('notationCategories/category/text()')

        if item.tag == 'trGroup':
            verse.extend(item.xpath('tr/text()'))

        # end of verse block
        if item.tag == 'verseEnd':
            # runs QA - checks if annotation term exists in verse
            verse = unicodedata.normalize('NFC', ' '.join(verse))
            match = [x for x in annots if x.lower() not in verse.lower()]
            if match: print(f"{ref},{match},{verse},{tag}")

node_items = nodes()
verses(node_items)