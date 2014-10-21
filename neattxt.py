import re

import hxchange
import messager


def get_neat_txt(route, title, txt_folder):
    coding_list = ("gb18030", "utf8")
    with open(route, 'rb') as f:
        r1 = f.read()
        r2 = re.sub(rb'www.{0,20}(?:com|cn|org|net)', b'', r1)  # 有些txt中有随意插入的网址，会导致文本乱码，在bytes模式下清除
    if len(r1) != len(r2):
        with open(route, 'wb') as f:
            f.write(r2)
    for i in range(len(coding_list)):
        try:
            with open(route, 'r', encoding=coding_list[i]) as source:
                text = source.read()
            break
        except UnicodeDecodeError:
            messager.statusbar_message.emit("encoding is not " + coding_list[i])
            if i == len(coding_list) - 1:
                messager.statusbar_message.emit("can't read text file")
                raise IOError("can't read text file")
    if len(text) < 10:
        messager.statusbar_message.emit("txt is wrong!")
        raise IOError("can't read correct text file")

    # messager.process_message.emit(messager.process_rate_list[1])  # 进度1
    text = re.sub(r'^[ 　\t]+', '', text, flags=re.M)  # 去除行首的半角或全角空格以及制表符
    text = re.sub(r'<.{1,200}>.{1,50}<.{1,200}>', '', text)
    text = re.sub(r'<.{1,200}>', '', text)
    text = text.replace('本书纵横中文网首发，欢迎读者登录www.zongheng.com查看更多优秀作品。', '')
    text = text.replace('正文(520xs.com) ', '')
    text = text.replace('520小说', '书')
    text = text.replace('520xs', '')
    text = re.sub('^正文[ 　\t]*', '', text, flags=re.M)
    text = hxchange.smart_change(text)
    text = text.replace('\n\n', '\n')

    # with open(txt_folder + os.sep + title + '.txt', 'w', encoding='utf8') as f:
    # f.write(text)

    # messager.process_message.emit(messager.process_rate_list[2])  #进度2
    return text


# def start_build(route, title, author, description, chr_pattern, txt_folder):
# # 制作开始
# text = get_neat_txt(route, title, txt_folder).split("\n")
# txt2html.BuildEpub(title, author, text, description, chr_pattern)
# strucreat.structure(description, chr_pattern)
# epubzip.epubzip('epubobject', title)
# arrange.arrange(route, title)
if __name__ == '__main__':
    import cProfile

    cProfile.run("""get_neat_txt("琥珀之剑.txt","琥珀之剑","")""")