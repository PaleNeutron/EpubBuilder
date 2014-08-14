import os
import zipfile


def epubzip(book_dir, book_title):
    """This Zip Script is used to build the .epub file"""

    list = []

    # #book_title = book_title.decode('utf8')

    ##book_title = book_title.encode('gbk')

    for i in os.walk(book_dir):
        for l in i[2]:
            list.append(os.path.join(i[0], l))

    z = zipfile.ZipFile(book_title + '.epub', 'w', zipfile.ZIP_DEFLATED)

    for i in list:
        zipdir = i.replace(book_dir + '\\', '')
        z.write(i, zipdir)
