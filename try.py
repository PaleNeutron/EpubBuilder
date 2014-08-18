import os
import chardet

dit = r'D:\Documents\txt'
for root, dirs, files in os.walk(dit):
    os.chdir(root)
    for dst in os.listdir(root):
        if dst.endswith('.txt'):
            testf = open(dst, 'br')
            test = testf.readline()
            testf.close()
            code = chardet.detect(test)['encoding']
            if code == 'EUC-TW':
                continue
            f = open(dst, 'r', encoding=code, errors='ignore')
            con = f.readlines()
            for line in range(len(con)):
                con[line] = con[line].replace('漏*点', '激情')
            new = open(dst, 'w', encoding='utf8', errors='replace')
            new.writelines(con)
            new.close()
            print(dst)
