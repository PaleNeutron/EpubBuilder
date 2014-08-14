import re

import cn2dig


p = re.compile(r'^第(.{1,10})章')
with open('contents.txt', encoding='utf8') as f:
    con = f.read()
cnlist = re.findall(r'第(.{1,10})章', con)
diglist = []
n = 1
for i in cnlist:
    try:
        dig = cn2dig.cn2dig(i)
        if dig != n:
            print(n)
            n = dig + 1
        else:
            n += 1
    except:
        print('wrong with', i)
