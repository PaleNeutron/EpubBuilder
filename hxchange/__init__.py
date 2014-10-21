import re

from . import hxlist


# package_dir = os.path.abspath(os.path.dirname(__file__))
# with open(package_dir + os.sep + 'purechr.pkl', 'rb') as f:
# purechr = pickle.load(f)
# with open(package_dir + os.sep + 'chchr.pkl', 'rb') as f:
#     chchr = pickle.load(f)


purechr = hxlist.purechr
chchr = hxlist.chchr


def change(string, chchr=chchr, purechr=purechr):
    for i in purechr:
        string = re.sub(r'(?<![a-zA-Z])' + i[0] + r'(?![a-zA-Z])', i[1], string)
    for i in chchr:
        string = string.replace(i[0], i[1])
    return string


def smart_change(string):
    if string.count("yan") + string.count("jiān") + string.count("yàn") + string.count("chao") > 3:
        return change(string)
    else:
        return string

# def changefile(route):
    # with open(route, encoding="gb18030") as f:
    #         new_string = change(f.read())
    #     with open(package_dir + os.sep + "bak.txt", "w", encoding="gb18030") as f:
    #         f.write(new_string)
    #     with open(route, "w", encoding="gb18030") as f:
    #         f.write(new_string)
    #     print("done")
    #
    #
    # if __name__ == "__main__":
    #     changefile(input("route is: "))
