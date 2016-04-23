import re
import os

import messager


def format_txt(title, author, rawread, description, txt_folder, rule=r'(^.{0,20}第.{0,10}章.{0,20}$)'):
    # images = os.listdir('images')
    # if len(images) > 1:
    # os.remove('images\\cover.jpg')
    # if images[0] != 'cover.jpg':
    # os.rename('images\\' + images[0], 'images\\' + 'cover.jpg')
    if title == None:
        title = input('请输入书名')
    if author == None:
        author = input('请输入作者名')

    contents = []
    mark = -10
    read = []
    # 打开临时文档，用于存放格式化的数据
    temp_file = open(txt_folder + os.sep + "temp", 'w', encoding='utf8', errors="replace")
    ##读取文档
    for i in range(len(rawread) - 1):
        a = re.search(rule, rawread[i])
        if a != None:
            if i - mark > 6:
                old = a.group()
                new = '<title>' + old + '</title>' + '\n' + '<h1>' + old + '</h1>\n'
                read.append(new)
                temp_file.write(old + '\n')
                contents.append((old, str(round(i * 100 / len(rawread), 1))))  # 添加目录信息以及当前章节百分比
                mark = i
        elif len(rawread[i]) > 2:
            read.append('<p>' + rawread[i] + '</p>\n')
            temp_file.write('    ' + rawread[i] + '\n')

        messager.process_message.emit(messager.get_rate(3, i / (len(rawread) - 1)))
    read[-1] = '<p>' + read[-1] + '</p>\n'  # 添加html标签
    temp_file.write(read[-1] + '\n')
    description = description.replace("\n", "</p><p>")
    read = [title + '\n', author + '\n', '<title>封面</title>\n', '<img src="images/cover.jpg" />\n',
            '<p>' + title + '</p>\n', '<p>' + author + '</p>\n', '<p>' + description + "**********" + '</p>\n'] + read
    ##添加书名，作者，封面信息

    ##	if len(contents) < 30:
    ##		quit()

    output = open('index.html', 'w', encoding='UTF-8')
    output.writelines(read)
    output.close()
    ##输出

    charpter_number = len(contents)
    average_len = 100 / charpter_number
    result = ['<table style="font-size: 2em">']
    formal_percent = 0
    simple_tip = '<tr>'
    alert_tip = '<tr style="color:red">'
    for title, percent in contents:
        if float(percent) - formal_percent > 6*average_len:
            title = alert_tip + "<td>" +title + "</td>"
        else:
            title = simple_tip + "<td>" +title + "</td>"
        formal_percent = float(percent)
        result.append(title+ "<td>" + percent + "</td>" + "</tr>")
    result.append("</table>")
    with open('contents.html', 'w', encoding='UTF-8') as contents_out:
        contents_out.writelines(result)
        # #输出章节名用于检查
