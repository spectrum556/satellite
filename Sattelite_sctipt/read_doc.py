from pprint import pprint
import json

FILENAME = 'SDATA_discription.doc'
FILENAME_2 = 'desc.txt'
OUT_FILENAME_DESC = 'data/description.json'
OUT_FILENAME_NAMES = 'data/names.txt'


with open(FILENAME_2, encoding='utf-8') as f:
    content = f.readlines()

content = [line.replace('\n', '') for line in content]
content = [line.split('–') for line in content]
content = content[:-1]
content = [[line[0].replace(' ', ''), line[1].strip(' ')] for line in content]

names = [line[0] for line in content]
description = dict(content)

with open(OUT_FILENAME_DESC, 'w') as f:
    json.dump(description, f)

with open(OUT_FILENAME_NAMES, 'w') as f:
    for name in names:
        f.write(name + ' ')
print(names)
