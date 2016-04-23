__author__ = 'PaleNeutron'
from urllib.request import Request
from urllib.parse import unquote
import urllib.parse
import requests
import re
from pyquery import PyQuery as pq
import html2text

import messager


requests.utils.default_user_agent = lambda : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# class DeceptionOpener(FancyURLopener):
#     """decorate the FancyURLopener as an simple browser"""
#
#     def __init__(self):
#         super(DeceptionOpener, self).__init__()
#         self.version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
#         # #        self.proxies = {'http':'http://202.112.26.250:8080'} #使用SJTU的代理


class BookInfo(object):
    """grab all the book information from a specific website"""

    def __init__(self):
        super(BookInfo, self).__init__()
        self.title = None
        self.author = None
        self.description = None
        self.score = None
        self.cover_href = None
        self.cover = None
        self.host = None
        self.url = None
        self.protocol = "http://"

        self.session = requests.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                "Accept-Language": "en-US,zh-CN;q=0.7,en;q=0.3",
                                "Accept-Encoding": "gzip, deflate",
                                "Connection": "keep-alive"}
    def get_url(self, title_or_url):
        if title_or_url:
            url_regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)


            if url_regex.match(title_or_url):
                self.url = title_or_url
            elif url_regex.match(self.protocol + title_or_url):
                self.url = self.protocol + title_or_url
            else:
                self.url = 'http://www.yousuu.com/name/' + urllib.parse.quote(title_or_url)

            self.host = Request(self.url).host

    def open_page(self, title_or_url):
        self.get_url(title_or_url)

        self.response = self.session.get(self.url)
        status_code = self.response.status_code
        if status_code == 200:
            self.analyse_page()
        else:
            messager.statusbar_message.emit(str(status_code))


    # def scan_novel_site(self):

    def analyse_page(self):
        self.html = self.response.text
        self.pg = pq(self.html)
        # self.soup = bs4.BeautifulSoup(self.html, "lxml")
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
                bookpage = self.pg("a.hidden-xs").attr("href")
                newhost = Request(bookpage).host
                #防止跳到目录页而不是信息页
                # if newhost == 'www.qidian.com':
                #     self.url = bookpage.replace("BookReader", "Book")
                if newhost == 'book.zongheng.com':
                    bookpage = bookpage.replace("showchapter", "book")
                elif newhost == 'www.hbooker.com':
                    bookpage = bookpage.replace("chapter/get_chapter_list","book/book_detail")

                # else:
                #     messager.statusbar_message.emit("{host} is not developed".format(host=self.host))
                #     return
                self.open_page(bookpage)
                    # else:
                    # self.scan_lkong(self.url)
        elif self.host == "chuangshi.qq.com":
            self.scan_chuangshi()
        elif self.host == "www.qidian.com":
            self.scan_qidian()
        elif self.host == 'book.zongheng.com':
            self.scan_zongheng()
        elif self.host == 'www.hbooker.com':
            self.scan_hbooker()
        elif self.host == "www.8kana.com":
            self.scan_8kana()
        else:
            messager.statusbar_message.emit('Could not find book info, please set book page manually')

        if self.cover_href and not self.cover:
            # myopener = DeceptionOpener()
            response = self.session.get(self.cover_href)
            try:
                self.cover = response.content
            except:
                self.cover = self.session.get('http://image.cmfu.com/books/1.jpg').content

    def search_chuangshi(self, quoted_title):
        search_request = self.session.get("http://chuangshi.qq.com/search/searchindex?type=all&wd=" + quoted_title)
        search_pg = pq(search_request.text)
        if search_pg("searchResultList h1 a").text() == self.title:
            newurl = search_pg("searchResultList h1 a").attr("href")  # 似乎创世很没节操的搜索系统永远不会搜不出东西
            if "book.qq.com" in newurl:  # 创世和起点的某个坑爹活动，似乎可以互相访问书籍，但是事实上大部分是404
                return False
            self.url = newurl.split('?')[0]  # 权宜之计，暂时没找到把所有非ASCII字符自动quote的函数
            self.open_page(self.url)
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
                                       'method': ['Search'],
                                       'keyword': [self.title]
                                   }, doseq=True),
            ''])

        qidian_search_headers = {'Referer': 'http://sosu.qidian.com/searchresult.aspx?&keyword='}
        qidian_search_headers.update(self.session.headers)
        req = self.session.get(url, headers=qidian_search_headers)
        j = req.json()
        if j['Data']['search_response']["totalcount"]:
            bookinfo = j['Data']['search_response']['books'][0]
            if bookinfo['bookname'] == self.title:
                self.url = 'http://www.qidian.com/Book/%s.aspx' % bookinfo['bookid']
                self.open_page(self.url)
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
        self.title = self.pg('h1').text()
        self.author = self.pg('.list-unstyled > li:nth-child(1) > a:nth-child(1)').text()
        self.description = self.pg('div.indent bm_c').text().strip()
        self.score = self.pg('.ys-book-averrate > span:nth-child(1)').text()
        self.cover_href = self.pg('a.hidden-xs > img:nth-child(1)').attr('src')

    def scan_qidian(self):
        self.title = self.pg("div.title h1").text().strip()
        self.author = self.pg("span[itemprop='name']").text().strip()
        self.description = "\n".join(self.pg("span[itemprop='description']").text().split())
        self.cover_href = self.pg("img[itemprop='image']").attr("src")

    def scan_chuangshi(self):
        self.title = self.pg('div.title:nth-child(1) > a:nth-child(2) > b:nth-child(1)').text()
        self.author = self.pg('.bz > a:nth-child(1)').text()
        if not self.author:
            # 针对现在的页面有的在推广作者微信号，导致解析不到作者名
            self.author = self.pg('#authorWeixinContent').text().split("说：")[0]
        self.description = '\n'.join([self.pg(i).text() for i in self.pg('.info p')])
        self.cover_href = self.pg('.bookcover > img:nth-child(1)').attr('src')

    def scan_hbooker(self):
        self.title = self.pg('.book-title > h3:nth-child(1)').text()
        self.author = self.pg('.book-title > p:nth-child(2) > a:nth-child(2)').text()
        self.description = self.pg('.book-desc').text()
        self.cover_href = self.pg('.book-cover > img:nth-child(1)').attr('src')

    def scan_zongheng(self):
        # fl = self.soup.body.find('div', {'class': 'status fl'})
        # self.title = fl.h1.find("a", target=False).string.strip()
        # self.author = fl.p.em.a.string.strip()
        # self.description = fl.find('div', {'class': 'info_con'}).p.string
        # self.cover_href = self.soup.body.find('div', {'class': 'book_cover fl'}).a.img.get('src')
        if "访问页面出错" in self.pg('body').text():  # 说明书在原来的网址被删除了
            messager.statusbar_message.emit("book is deleted in zongheng")
            return
        self.title = self.pg('.status > h1:nth-child(1) > a:nth-child(1)').text()
        self.author = self.pg('.booksub > a:nth-child(2)').text()
        self.description = self.pg('.info_con > p:nth-child(1)').text()
        self.cover_href = self.pg('.book_cover > p:nth-child(2) > a:nth-child(1) > img:nth-child(1)').attr('src')

    def scan_8kana(self):
        self.title = self.pg('h2.left').text()
        self.author = self.pg('.authorName').text()
        self.description = html2text.html2text(self.pg('#li_booknote p').html())
        self.cover_href = self.pg('.bookContainImgBox > a:nth-child(1) > img:nth-child(1)').attr('src')

