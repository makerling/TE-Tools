import lxml.etree as etree
import unicodedata
from colored import stylize

      
def nodes(root):
    nodes = []
    for element in root.xpath('//section'):
        node = [x for x in element.xpath('p/* | p')]
        nodes.extend(node)
    return nodes 

def verses(nodes):
    n = 0
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
            # the annotation type(s)
            tag = item.xpath('notationCategories/category/text()')

        # there can be multiple trGroup tags within one verse
        # there can also be \p tags in between a single verse also
        if item.tag == 'trGroup':
            verse.extend(item.xpath('tr/text()'))

        # end of verse block
        if item.tag == 'verseEnd':
            # runs QA - checks if annotation term exists in verse
            verse = unicodedata.normalize('NFC', ' '.join(verse))
            match = [x for x in annots if x.lower() not in verse.lower()]
            match_bold = stylize(', '.join(match), attr('bold'))
            if match: 
                n += 1
                print(f"{n} | {ref} - {match_bold} --> {verse}")
    
    print(f"\n{n} verses have annotations that don't match the verse text")
            

def main(args):
    with open(args.QA) as fobj:
        xml = fobj.read()

        root = etree.fromstring(xml)

    print('-' * 50)
    node_items = nodes(root)
    verses(node_items)
    print('-' * 50)