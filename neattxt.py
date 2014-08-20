import re
import os

import hxchange


def get_neat_txt(route, title, txt_folder):
    coding_list = ("utf8", "gb18030")
    with open(route, 'rb') as f:
        r1 = f.read()
        r2 = re.sub(rb'www.{0,20}(?:com|cn|org|net)', b'', r1)  # 有些txt中有随意插入的网址，会导致文本乱码，在bytes模式下清除
    if len(r1) != len(r2):
        with open(route, 'wb') as f:
            f.write(r2)
    for i in range(len(coding_list)):
        try:
            source = open(route, 'r', encoding=coding_list[i])
            text = source.read()
            source.close()
            break
        except UnicodeDecodeError:
            print("encoding is not", coding_list[i])
            pass
    text = re.sub(r'^[ 　\t]+', '', text, flags=re.M)  # 去除行首的半角或全角空格以及制表符
    text = re.sub(r'<.{1,200}>.{1,50}<.{1,200}>', '', text)
    text = re.sub(r'<.{1,200}>', '', text)
    text = text.replace('本书纵横中文网首发，欢迎读者登录www.zongheng.com查看更多优秀作品。', '')
    text = text.replace('正文(520xs.com) ', '')
    text = text.replace('520小说', '书')
    text = text.replace('520xs', '')
    text = re.sub('^正文[ 　\t]*', '', text, flags=re.M)
    text = hxchange.change(text)
    text = text.replace('\n\n', '\n')

    with open(txt_folder + os.sep + title + '.txt', 'w') as f:
        f.write(text)
    return text


# def start_build(route, title, author, description, chr_pattern, txt_folder):
# # 制作开始
#     text = get_neat_txt(route, title, txt_folder).split("\n")
#     txt2html.BuildEpub(title, author, text, description, chr_pattern)
#     strucreat.structure(description, chr_pattern)
#     epubzip.epubzip('epubobject', title)
#     arrange.arrange(route, title)
