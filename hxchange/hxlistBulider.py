import re
import pickle
import os
# ###用于生成替换列表的代码

# #hxdict = {}
##hxlist =list(hxdict.items())
def addword(hx, original):
    '''rplRule must be formated as a=b'''
    with open(package_dir + os.sep + 'hxlist.txt', 'a', encoding='utf8') as f:
        f.write(hx + '=' + original + '\n')
    rebuild()


def rebuild():
    with open(package_dir + os.sep + 'hxlist.txt', encoding='utf8') as f:
        source = f.read().splitlines()
    hxlist = []
    for i in source:
        p = i.index('=')
        hxlist.append((i[:p], i[p + 1:]))
    purechr = []
    chchr = []
    for i in hxlist:
        if re.match(r'^[a-z]+$', i[0]):
            purechr.append(i)
        else:
            chchr.append(i)
    purechr = list(set(purechr))
    purechr.sort(key=lambda x: len(x[0]), reverse=True)
    chchr = list(set(chchr))
    chchr.sort(key=lambda x: len(x[0]), reverse=True)
    with open(package_dir + os.sep + 'purechr.pkl', 'wb') as f:
        pickle.dump(purechr, f)
    with open(package_dir + os.sep + 'chchr.pkl', 'wb') as f:
        pickle.dump(chchr, f)


if __name__ == "__main__":
    package_dir = os.path.abspath(os.path.dirname(__file__))
    rebuild()
