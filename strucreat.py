import time
import os
import shutil
import uuid

import tmp
import messager


def structure(description, chrpattern):
    # Creat The Epub Structure Dir
    if 'epubobject' not in os.listdir('.'):
        os.makedirs(r'epubobject/OEBPS')
        os.makedirs(r'epubobject/META-INF')
    else:
        shutil.rmtree('epubobject')
        os.makedirs(r'epubobject/OEBPS')
        os.makedirs(r'epubobject/META-INF')

    # Create The MimeType File
    mimetype = open(r'epubobject/mimetype', 'w', encoding='UTF-8')
    mimetype.write(tmp.mimetype_tmp())
    mimetype.close()

    # Create the container.xml, it's in META-INF/
    container = open(r'epubobject/META-INF/container.xml', 'w', encoding='UTF-8')
    container.write(tmp.container_tmp())
    container.close()

    # Move the images & css files into the epubobject folder
    if os.path.exists('./images') and not os.path.exists(r'epubobject/OEBPS/images'):
        shutil.copytree(r'./images', r'epubobject/OEBPS/images')

    if os.path.exists('./style') and not os.path.exists(r'epubobject/OEBPS/style'):
        shutil.copytree(r'./style', r'epubobject/OEBPS/style')

    # Creatt the Book Files
    f = open('index.html', 'r', encoding='UTF-8')
    html_doc = f.readlines()
    f.close()

    book_title = html_doc[0]  # 后面构建opf文件时用
    book_title = book_title.replace('\n', '')
    book_author = html_doc[1]  # 后面构建opf文件时用
    book_author = book_author.replace('\n', '')
    chap_title_list = []  # 构建一个list，存放章节标题，后面构建toc.ncx时用
    title_line_nums = []
    style_con = ''

    for i in range(2, len(html_doc)):
        if '<title>' in html_doc[i]:
            title_line_nums.append(i)
        elif '<link rel=\"stylesheet\"' in html_doc[i]:
            style_con = html_doc[i]
        messager.process_message.emit(messager.get_rate(4, i / len(html_doc)))

    for j in range(0, len(title_line_nums)):
        messager.process_message.emit(messager.get_rate(5, j / len(title_line_nums)))
        chap_title = html_doc[title_line_nums[j]]  # 取得章节标题
        chap_title = chap_title.replace('\n', '')  # 去除换行符
        chap_title_list.append(chap_title)  # 存放每章标题，后面toc.ncx用
        chap_con_start_num = title_line_nums[j] + 1  # 取得每章正文开始的行号
        if j < len(title_line_nums) - 1:
            chap_con_end_num = title_line_nums[j + 1]  # 取得每章正文结束的行号，实际多了一行。因为后续要使用list输出
            chap_con_pre = html_doc[chap_con_start_num:chap_con_end_num]  # 通过行号把正文赋到一个变量。
        elif j == len(title_line_nums) - 1:
            chap_con_pre = html_doc[chap_con_start_num:]
        chap_con = '    '.join(chap_con_pre)  # 因为上面得到的是list，因此需要转为字符串，加四个空格做缩进，代码更整齐。
        chap_out_pre = tmp.html_tmp(chap_title, chap_con, style_con)
        if j >= 1000:
            num = str(j)
        elif j >= 100:
            num = '0' + str(j)
        elif j >= 10:
            num = '00' + str(j)
        else:
            num = '000' + str(j)
        chap_out = open('epubobject/OEBPS/c' + num + '.xhtml', 'w', encoding='UTF-8')
        chap_out.write(chap_out_pre)
        chap_out.close()

    # Creat The Book Files↑↑↑↑

    #Build the opf file

    ## Creat a UUID and creat date

    uuidnum = str(uuid.uuid1())
    creatdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    ##  Combine the manifest and spine
    ##  for the xhtml file looks like
    ##  <item href="c0.xhtml" id="c0.xhtml" media-type="application/xhtml+xml" />
    ##  for the image file looks like
    ##  <item href="images/jpg" id="img-suf-cap.jpg" media-type="image/jpeg" />
    ##  <item href="images/png" id="img-png.png" media-type="image/png" />
    ##  <item href="images/gif" id="img-gif-trans.gif" media-type="image/gif" />
    ##  for the spine look like
    ##  <itemref idref="c0.html" />

    fileslist = []
    manifest_out_pre = []
    spine_out_pre = []
    ncx_nav_list = []

    for k in os.walk(r'epubobject/OEBPS'):
        fileslist += k[2]

    fileslist.sort()

    for l in range(0, len(fileslist)):

        thefile = fileslist[l]

        if 'html' in thefile:
            manifest_out_pre.append(
                '<item href=\"' + thefile + '\" id=\"' + thefile + '\" media-type=\"application/xhtml+xml\" />\n')
            spine_out_pre.append('<itemref idref=\"' + thefile + '\" />\n')
            ncx_nav_list.append(thefile)

        elif 'css' in thefile:
            manifest_out_pre.append(
                '<item href=\"style/' + thefile + '\" id=\"' + thefile + '\" media-type=\"text/css\" />\n')

        elif 'jpg' in thefile:
            manifest_out_pre.append(
                '<item href=\"images/' + thefile + '\" id=\"x' + thefile + '\" media-type=\"image/jpeg\" />\n')

        elif 'png' in thefile:
            manifest_out_pre.append(
                '<item href=\"images/' + thefile + '\" id=\"x' + thefile + '\" media-type=\"image/png\" />\n')

        elif 'gif' in thefile:
            manifest_out_pre.append(
                '<item href=\"images/' + thefile + '\" id=\"x' + thefile + '\" media-type=\"image/gif\" />\n')

    manifest_out = '    '.join(manifest_out_pre)
    spine_out = '    '.join(spine_out_pre)

    opf_out_pre = tmp.opf_tmp(uuidnum, book_title, book_author, creatdate, manifest_out, spine_out, description,
                              chrpattern)

    opf_out = open('epubobject/OEBPS/content.opf', 'w', encoding='utf8')
    opf_out.write(opf_out_pre)
    opf_out.close()

    #Creat toc.ncx file

    navmap_out_pre = []

    for m in range(0, len(ncx_nav_list)):
        playorder = m + 1
        chap_title = chap_title_list[m]
        chap_title = chap_title.replace('<title>', '')
        chap_title = chap_title.replace('</title>', '')
        navmap = tmp.navmap_tmp(str(playorder), chap_title, ncx_nav_list[m])
        navmap_out_pre.append(navmap)

    navmap_out = '\n'.join(navmap_out_pre)

    ncx_out_pre = tmp.ncx_tmp(uuidnum, book_title, navmap_out)

    ncx_out = open('epubobject/OEBPS/toc.ncx', 'w', encoding='UTF-8')
    ncx_out.write(ncx_out_pre)
    ncx_out.close()


if __name__ == '__main__':
    structure("no description", "")
