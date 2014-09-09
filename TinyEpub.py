import zipfile

import bs4


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

    def epub2txt(self):
        tempread = ""
        for i in self.namelist():
            if i.startswith('OEBPS/') and i.endswith('.xhtml'):
                soup = bs4.BeautifulSoup(self.read(i).decode())
                chapter = soup.body.getText()[1:].splitlines()
                chapter = "\n\t".join(chapter) + "\n\n"
                tempread += chapter
        with open(self.title + '.txt', 'w', encoding='utf8') as f:
            f.write(tempread)
