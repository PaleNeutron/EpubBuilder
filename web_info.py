__author__ = 'PaleNeutron'
from urllib.request import FancyURLopener, Request, urlopen
from urllib.parse import quote, unquote
import urllib.request
import urllib.parse
import json
import os
from pyquery import PyQuery as pq
import bs4

import messager


class DeceptionOpener(FancyURLopener):
    """decorate the FancyURLopener as an simple browser"""

    def __init__(self):
        super(DeceptionOpener, self).__init__()
        self.version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
        self.protocol = "http://"
        # #        self.proxies = {'http':'http://202.112.26.250:8080'} #使用SJTU的代理


class BookInfo(DeceptionOpener):
    """grab all the book information from a specific website"""

    def __init__(self, url=None):
        super(BookInfo, self).__init__()
        self.title = None
        self.author = None
        self.description = None
        self.score = None
        self.cover_href = None
        self.cover = None
        self.host = None
        self.url = url

    def open_page(self):
        # 确定访问的协议为http
        if self.url:
            if not self.url.startswith(self.protocol):
                self.url = 'http://www.yousuu.com/name/' + urllib.parse.quote(self.url)
            self.host = Request(self.url).host


            try:
                self.response = self.open(self.url)
            except OSError as err:
                if err.errno == 'socket error':
                    messager.statusbar_message.emit("please check url or website is busy")
            if self.response.getcode() == 200:
                self.analyse_page()
            elif self.response.getcode() == 404:
                messager.statusbar_message.emit("ERROR 404, page not found")
            else:
                messager.statusbar_message.emit(self.response.getcode())
            messager.page_opened.emit()

    def analyse_page(self):
        self.info = self.response.info()
        self.html = self.response.read().decode(self.info.get_content_charset(), errors='ignore')
        self.pg = pq(self.html)
        self.soup = bs4.BeautifulSoup(self.html, "lxml")
        if self.host == 'www.yousuu.com':
            if "对不起，本页没有找到匹配的书" in self.pg('body').text():
                quoted_title = self.url.replace('http://www.yousuu.com/name/', '')
                self.title = unquote(quoted_title)
                messager.statusbar_message.emit("book not in lkong")
                if self.search_chuangshi(quoted_title):
                    pass
                elif self.search_qidian(quoted_title):
                    pass
            else:
                self.scan_yousuu()
                bookpage = self.soup.find("a", {"class":"hidden-xs"}).get("href")
                newhost = Request(bookpage).host
                if newhost == 'www.qidian.com':
                    self.url = bookpage.replace("BookReader", "Book")
                    self.open_page()
                elif newhost == 'book.zongheng.com':
                    self.url = bookpage.replace("showchapter", "book")
                    self.open_page()
                    # else:
                    # self.scan_lkong(self.url)
        elif self.host == "chuangshi.qq.com":
            self.scan_chuangshi()
        elif self.host == "www.qidian.com":
            self.scan_qidian()
        elif self.host == 'book.zongheng.com':
            self.scan_zongheng()
        else:
            messager.statusbar_message.emit('Could not find book info, please set book page manually')

        if self.cover_href:
            myopener = DeceptionOpener()
            response = myopener.open(self.cover_href)
            try:
                self.cover = response.read()
            except:
                self.cover = myopener.open('http://image.cmfu.com/books/1.jpg').read()

    def search_chuangshi(self, quoted_title):
        search_opener = DeceptionOpener()
        search_result = search_opener.open(
            "http://chuangshi.qq.com/search/searchindex?type=all&wd=" + quoted_title)
        search_soup = bs4.BeautifulSoup(
            search_result.read().decode(search_result.info().get_content_charset(), errors='ignore'))
        if search_soup.find(id="searchResultList").h1.a.getText() == self.title:
            newurl = search_soup.find(id="searchResultList").h1.a.get("href")  # 似乎创世很没节操的搜索系统永远不会搜不出东西
            if "book.qq.com" in newurl:  # 创世和起点的某个坑爹活动，似乎可以互相访问书籍，但是事实上大部分是404
                return False
            self.url = newurl.split('?')[0]  # 权宜之计，暂时没找到把所有非ASCII字符自动quote的函数
            self.open_page()
            return True
        else:
            messager.statusbar_message.emit("book not in chuangshi")

    def search_qidian(self, quoted_title):  # TODO 其实获取的bookinfo已经包含了所需的全部信息，只是修改的话需要大改结构，暂时放下
        import json

        url = urllib.parse.urlunparse([
            'http',
            'sosu.qidian.com', '/ajax/search.ashx',
            '',
            urllib.parse.urlencode({
                                       'method': ['suggestion'],
                                       'keyword': [self.title]
                                   }, doseq=True),
            ''])

        qidian_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',  # 非必要
            'Referer': 'http://sosu.qidian.com/searchresult.aspx?&keyword=',
        }
        req = urllib.request.Request(url, headers=qidian_search_headers, method='GET')
        j = json.loads(urllib.request.urlopen(req).read().decode('utf8'))
        if j['Data']['search_response']["totalcount"]:
            bookinfo = j['Data']['search_response']['books'][0]
            if bookinfo['bookname'] == self.title:
                self.url = 'http://www.qidian.com/Book/%s.aspx' % bookinfo['bookid']
                self.open_page()
                return True
        else:
            messager.statusbar_message.emit("book not in qidian")

    def scan_yousuu(self):
        self.title = self.pg("div.col-sm-7:nth-child(1) > div:nth-child(1) > span:nth-child(1)").text()
        self.author = self.pg('.list-unstyled > li:nth-child(1)').text().replace("作者: ","")
        self.description = self.pg(".text-indent").text()
        self.cover_href = self.pg('.hidden-xs > img:nth-child(1)').attr('src')
        self.score = self.pg('.ys-book-averrate > span:nth-child(1)').text()

    def scan_lkong(self):
        self.title = self.soup.find('h1').string
        self.author = self.soup.find(attrs={'class': 'pl'}).nextSibling.nextSibling.string.strip()
        self.description = self.soup.find('div', {'class': 'indent bm_c'}).getText().strip()
        self.score = self.soup.find('strong', {'class': "ll rating_num"}).string
        self.cover_href = self.soup.find('img', attrs={'alt': self.title}).get('src')

    def scan_qidian(self):
        self.title = self.soup.find("div", {"class": "title"}).h1.getText().strip()
        self.author = self.soup.body.find("span", {"itemprop": "name"}).string.strip()
        self.description = "\n".join(self.soup.body.find("span", {"itemprop": "description"}).getText().split())
        self.cover_href = self.soup.body.find("img", {"itemprop": "image"}).get("src")

    def scan_chuangshi(self):
        self.title = self.pg('div.title:nth-child(1) > a:nth-child(2) > b:nth-child(1)').text()
        self.author = self.pg('.au_name > p:nth-child(2) > a:nth-child(1)').text()
        self.description = '\n'.join([self.pg(i).text() for i in self.pg('.info p')])
        self.cover_href = self.pg('.bookcover > img:nth-child(1)').attr('src')

    def scan_zongheng(self):
        # fl = self.soup.body.find('div', {'class': 'status fl'})
        # self.title = fl.h1.find("a", target=False).string.strip()
        # self.author = fl.p.em.a.string.strip()
        # self.description = fl.find('div', {'class': 'info_con'}).p.string
        # self.cover_href = self.soup.body.find('div', {'class': 'book_cover fl'}).a.img.get('src')
        if "访问页面出错" in self.pg('body').text():  # 说明书在原来的网址被删除了
            messager.statusbar_message.emit("book is deleted in zongheng")
            return
        self.title = self.pg('.status a')[1].text
        self.author = self.pg('.author > em:nth-child(1) > a:nth-child(1)').text()
        self.description = self.pg('.info_con').text()
        self.cover_href = self.pg('.book_cover > p:nth-child(2) > a:nth-child(1) > img:nth-child(1)').attr('src')
