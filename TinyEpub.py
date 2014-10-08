import zipfile
from multiprocessing import Pool

import bs4


def char2text(i):
    soup = bs4.BeautifulSoup(i)
    chapter = soup.body.getText().splitlines()
    chapter = "\n".join(chapter).strip() + "\n\n"
    return chapter


class Epub(zipfile.ZipFile):
    def __init__(self, file, mode='r', compression=0, allowZip64=False):
        zipfile.ZipFile.__init__(self, file, mode, compression, allowZip64)
        if mode == 'r':
            self.opf = self.read('OEBPS/content.opf').decode()
            opf_soup = bs4.BeautifulSoup(self.opf)
            self.author = opf_soup.find(name='dc:creator').getText()
            self.title = opf_soup.find(name='dc:title').getText()
            try:
                self.description = opf_soup.find(name='dc:description').getText()
            except:
                self.description = ''
            try:
                self.chrpattern = opf_soup.find(name='dc:chrpattern').getText()
            except:
                self.chrpattern = ''
            self.cover = self.read('OEBPS/images/cover.jpg')
        elif mode == 'w':
            pass

    def get_text(self):
        self.tempread = ""
        charlist = self.readall(self.namelist())
        with Pool(4) as pool:
            txtlist = pool.map(char2text, charlist)
        self.tempread = "".join(txtlist)
        return self.tempread

    def readall(self, namelist):
        charlist = []
        for i in namelist:
            if i.startswith('OEBPS/') and i.endswith('.xhtml'):
                r = self.read(i).decode()
                charlist.append(r)
        return charlist

    def epub2txt(self):
        tempread = self.get_text()
        with open(self.title + '.txt', 'w', encoding='utf8') as f:
            f.write(tempread)


if __name__ == "__main__":
    e = Epub("assz.epub")
    e.epub2txt()