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
        self.open_page()

    def open_page(self):
        try:
            self.response = self.open(self.url)
        except OSError as err:
            if err.errno == 'socket error':
                print("please check url or website is busy")
        if self.response.getcode() == 200:
            self.analyse_page()
        elif self.response.getcode() == 404:
            print("ERROR 404, page not found")
        else:
            print(self.response.getcode())

    def analyse_page(self):
        self.info = self.response.info()
        self.soup = bs4.BeautifulSoup(self.response.read().decode(self.info.get_content_charset(), errors='ignore'))
        self.host = Request(self.url).host
        if self.host == 'www.lkong.net':
            if self.soup.find("div", {"class": "alert_info"}):
                print("book not in lkong")
            else:
                bookpage = self.soup.findAll('a', {'title': self.title})[1].get("href")
                newhost = bookpage.split("/")
                if newhost == 'www.qidian.com':
                    # self.__init__("http://www.qidian.com/Book/" + self.bookpage[-1])
                    self.url = bookpage.replace("BookReader", "Book")
                    self.open_page()
                elif newhost == 'book.zongheng.com':
                    self.url = bookpage.replace("showchapter", "book")
                    self.open_page()
                else:
                    self.scan_lkong(self.url)


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
            # f.write(self.cover)

    def scan_lkong(self, url):
        self.title = self.soup.find('h1').string
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

    def duplicate(self, webinfo_obj):
        self.title = webinfo_obj.title
        self.author = webinfo_obj.author
        self.description = webinfo_obj.description
        self.score = webinfo_obj.score
        self.cover_href = webinfo_obj.cover_href
        self.cover = webinfo_obj.cover
        self.url = webinfo_obj.url
        self.response = webinfo_obj.response
        self.info = webinfo_obj.info

