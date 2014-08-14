__author__ = 'PaleNeutron'
from urllib.request import FancyURLopener, Request
import os

import bs4


class WebInfo(FancyURLopener):
    """grab all the book information from a specific website"""

    def __init__(self, url):
        super(WebInfo, self).__init__()
        self.version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
        protocol = "http://"
        # #        self.proxies = {'http':'http://202.112.26.250:8080'} #使用SJTU的代理
        if not url[0:len(protocol)] == protocol:
            url = protocol + url
        self.title = None
        self.author = None
        self.description = None
        self.score = None
        self.cover_href = None
        self.cover = None
        self.url = url
        self.response = self.open(self.url)
        self.info = self.response.info()
        try:
            self.soup = bs4.BeautifulSoup(self.response.read().decode(self.info.get_content_charset(), errors='ignore'))
            self.host = Request(self.url).host
        except OSError:
            print("site is busy")
        if self.host == 'www.lkong.net':
            try:
                self.title = self.soup.find('h1').string
                self.bookpage = self.soup.findAll('a', {'title': self.title})[1].get("href").split("/")
                if self.bookpage[2] == 'www.qidian.com':
                    # self.__init__("http://www.qidian.com/Book/" + self.bookpage[-1])
                    try:
                        w = WebInfo("http://www.qidian.com/Book/" + self.bookpage[-1])
                        self.duplicate(w)
                    except:
                        print("qidian page is discarded")
                        self.scan_lkong(self.url)
                elif self.bookpage[2] == 'book.zongheng.com':
                    try:
                        w = WebInfo("http://book.zongheng.com/book/" + self.bookpage[-1])
                        self.duplicate(w)
                    except:
                        print("zongheng page is discarded")
                        self.scan_lkong(self.url)
                else:
                    self.scan_lkong(self.url)

            except AttributeError:
                print("book not found")
        elif self.host == "chuangshi.qq.com":
            self.scan_chuangshi(self.url)
        elif self.host == "www.qidian.com":
            self.scan_qidian(self.url)

        elif self.host == 'book.zongheng.com':
            self.scan_zongheng(self.url)

        if 'images' not in os.listdir('.') and self.cover_href:
            os.mkdir('images')
        if self.cover_href:
            # with open(r'images/cover.jpg', 'wb') as f:
            myopener = FancyURLopener()
            myopener.version = self.version
            response = myopener.open(self.cover_href)
            self.cover = response.read()
            #f.write(self.cover)

    def scan_lkong(self, url):
        self.author = self.soup.find(attrs={'class': 'pl'}).nextSibling.nextSibling.string.strip()
        self.description = self.soup.find('div', {'class': 'indent bm_c'}).getText().strip()
        self.score = self.soup.find('strong', {'class': "ll rating_num"}).string
        self.cover_href = self.soup.find('img', attrs={'alt': self.title}).get('src')

    def scan_qidian(self, url):
        self.title = self.soup.find("div", {"class": "title"}).h1.getText().strip()
        self.author = self.soup.body.find("span", {"itemprop": "name"}).string.strip()
        self.description = "\n".join(self.soup.body.find("span", {"itemprop": "description"}).getText().split())
        self.cover_href = self.soup.body.find("img", {"itemprop": "image"}).get("src")

    def scan_chuangshi(self, url):
        title_line = self.soup.body.findAll("div", {"class": "title"})[1].getText().split(">\r\n            ")
        self.subject = title_line[1:3]
        self.title = title_line[3].strip()
        self.author = self.soup.find("div", {"class": "au_name"}).a.string.strip()
        self.description = "\n".join([a.string for a in self.soup.find("div", {"class": "info"}).contents])
        self.cover_href = self.soup.find("div", {"class": "cover"}).a.img.get("src")

    def scan_zongheng(self, url):
        fl = self.soup.body.find('div', {'class': 'status fl'})
        self.title = fl.h1.a.string.strip()
        self.author = fl.p.em.a.string.strip()
        self.description = fl.find('div', {'class': 'info_con'}).p.string
        self.cover_href = self.soup.body.find('div', {'class': 'book_cover fl'}).a.img.get('src')

    def duplicate(self, Webinfo):
        self.title = Webinfo.title
        self.author = Webinfo.author
        self.description = Webinfo.description
        self.score = Webinfo.score
        self.cover_href = Webinfo.cover_href
        self.cover = Webinfo.cover
        self.url = Webinfo.url
        self.response = Webinfo.response
        self.info = Webinfo.info

