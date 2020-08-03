# -*- coding: utf-8 -*-

import re
newfile = r"C:\Users\workother\code\TE-Tools\1665HB-Aallbooks-nonotesforreal.oxes"
with open ('1665HB-Aallbooks-nonotes.oxes', 'r+', encoding='utf-8') as f:
    content = f.read()
    new_content = re.sub('<annotation.*?<\/annotation>', '', content, flags = re.DOTALL)
    newfileopen = open(newfile, 'w', encoding='utf-8')
    newfileopen.write(new_content)
    newfileopen.close()