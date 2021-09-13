import re
import unicodedata

################################
### cleaning result.sfm file ###
################################
srcfile = './result.sfm'
with open(srcfile, 'r') as file:
	filedata = file.read()
# move \p line to previous line
filedataPara = re.sub(r'(\n)(\s+)(\\p)',r'\3',filedata)
# removes initial white spaces
filedataNewline = re.sub(r'^\s+','',filedataPara, flags=re.MULTILINE)
with open(srcfile, 'w') as file:
	file.write(filedataNewline)

#######################################
### finding annotations not in text ###
#######################################
with open(srcfile, 'r') as file:
	filedata = file.readlines()

outputfile = './output.csv'
with open(outputfile, 'w') as file:
    header = 'reference,annotation,verse text\n'
    file.write(header)
    for line in filedata:
        verse = unicodedata.normalize('NFC', line.split('*')[-1])
        ref = line.split('*')[1]
        annots = line.split('*')[2:-1]
        if len(annots) > 0:
            for annot in annots:
                annot = unicodedata.normalize('NFC', annot)
                if annot.lower() not in verse.lower():
                    output = ref + ',' + annot + ',' + verse
                    file.write(output)