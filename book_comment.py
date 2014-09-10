import os
import subprocess
import urllib.parse
from xml.dom.minidom import Document

import web_info


class ShelfComment(Document):
    def __init__(self):
        super(ShelfComment, self).__init__()
        self.shelf = self.createElement("shelf")
        self.appendChild(self.shelf)

    def addBook(self, title_text, author_text, description_text, strong_point_text, weak_point_text, score_int,
                lkong_score_int):
        def addSimpleElement(farther, element_name, source=""):
            ele = self.createElement(element_name)
            if not source == "":
                ele.appendChild(self.createTextNode(source))
            farther.appendChild(ele)
            return ele

        book = self.createElement("book")
        self.shelf.appendChild(book)
        addSimpleElement(book, "title", title_text)
        addSimpleElement(book, "author", author_text)
        addSimpleElement(book, "score", str(score_int))
        addSimpleElement(book, "lkong_score", str(lkong_score_int))
        addSimpleElement(book, "description", description_text)
        comment = addSimpleElement(book, "comment")
        addSimpleElement(comment, "strong_point", strong_point_text)
        addSimpleElement(comment, "weak_point", weak_point_text)


with open("书评.xml", "w", encoding="UTF-8") as f:
    s = ShelfComment()
    shelf_dir = "D:\\Documents\\txt\\网络小说\\test\\"
    for book in os.listdir(shelf_dir):
        title = os.path.splitext(book)[0]
        print(title)
        subprocess.Popen([r"C:\Program Files (x86)\Notepad++\notepad++.exe", shelf_dir + book])
        url = 'http://www.lkong.net/book.php?mod=view&bookname=' + urllib.parse.quote(title)
        info = web_info.BookInfo(url)
        if info.author:
            author = info.author
            lkong_score = info.score
            description = info.description
            print(author)
            print(lkong_score)
            print(description)
        else:
            author = input("type author: ")
            lkong_socre = "Null"
            lkong_score = "Null"
            description = "Null"
        strong_point = input("type strong_point: ")
        weak_point = input("type weak_point: ")
        score = input("type score: ")
        s.addBook(title, author, description, strong_point, weak_point, score, lkong_score)

    f.write(s.toprettyxml(indent='  '))
