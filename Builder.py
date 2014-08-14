import re

import hxchange
import os
import txt2html
import arrange
import strucreat
import epubzip


def clean_txt(route, title=None):
    if not title:
        title = os.path.basename(route).split(".")[0]
        ##打开获得的txt文件
    with open(route, 'rb') as f:
        r1 = f.read()
        r2 = re.sub(rb'www.{0,20}(?:com|cn|org|net)', b'', r1)  #有些txt中有随意插入的网址，会导致文本乱码，在bytes模式下清除
    if len(r1) != len(r2):
        with open(route, 'wb') as f:
            f.write(r2)
    try:
        source = open(route, 'r', encoding='GB18030')
        rawread = source.read()
        print('code is utf8:\t' + route)
    except:
        source = open(route, 'r', encoding='utf8', errors='replace')
        rawread = source.read()##获取文本
    source.close()
    rawread = re.sub(r'^[ 　\t]+', '', rawread, flags = re.M)#去除行首的半角或全角空格以及制表符
    rawread = re.sub(r'<.{1,200}>.{1,50}<.{1,200}>', '', rawread)
    rawread = re.sub(r'<.{1,200}>', '', rawread)
    rawread = rawread.replace('本书纵横中文网首发，欢迎读者登录www.zongheng.com查看更多优秀作品。', '')
    rawread = rawread.replace('正文(520xs.com) ', '')
    rawread = rawread.replace('520小说', '书')
    rawread = rawread.replace('520xs', '')
    rawread = rawread.replace('\n正文', '\n')
    rawread = hxchange.change(rawread)
    rawread = rawread.replace('\n\n', '\n')

    rawread = rawread.split('\n')
    with open(r'D:\Documents\txt' + os.sep + title + '.txt', 'w', encoding='gb18030') as f:
        for i in rawread:
            f.write(i + '\n')
    return rawread


def start_build(route, title, author, description, chrpattern):
    ##制作开始
    rawread = clean_txt(route, title)
    txt2html.BuildEpub(title, author, rawread, description, chrpattern)
    strucreat.structure(description, chrpattern)
    epubzip.epubzip('epubobject', title)
    arrange.arrange(route, title)
