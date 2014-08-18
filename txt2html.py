import re


def BuildEpub(title, author, rawread, description, rule=r'(^.{0,20}第.{0,10}章.{0,20}$)'):
    # images = os.listdir('images')
    # if len(images) > 1:
    # os.remove('images\\cover.jpg')
    #if images[0] != 'cover.jpg':
    #    os.rename('images\\' + images[0], 'images\\' + 'cover.jpg')
    if title == None:
        title = input('请输入书名')
    if author == None:
        author = input('请输入作者名')

    contents = []
    mark = -10
    read = []
    ##读取文档
    for i in range(len(rawread) - 1):
        a = re.search(rule, rawread[i])
        if a != None and i - mark > 6:
            old = a.group()
            new = '<title>' + old + '</title>' + '\n' + '<h1>' + old + '</h1>\n'
            read.append(new)
            contents.append(old + '\t\t' + str(round(i * 100 / len(rawread), 1)) + '\n')  # #添加目录信息以及当前章节百分比
            mark = i
        elif len(rawread[i]) > 2:
            read.append('<p>' + rawread[i] + '</p>\n')
    read[-1] = '<p>' + read[-1] + '</p>\n'  ##添加html标签
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

    contents_out = open('contents.txt', 'w', encoding='UTF-8')
    contents_out.writelines(contents)
    contents_out.close()
    ##输出章节名用于检查

    print('format is done')
