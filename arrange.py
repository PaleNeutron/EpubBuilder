import os
import shutil

import messager


message = messager.statusbar_message


def arrange(file_path, txt_folder, epub_folder, title):
    shutil.rmtree('epubobject')
    # 将epub移动到epub_folder中去,如果已经存在则覆盖之
    if os.path.exists(epub_folder + os.sep + title + '.epub'):
        shutil.copy(title + '.epub', epub_folder)
        os.remove(title + '.epub')
    else:
        shutil.move(title + '.epub', epub_folder)
    # 如果文本文件位置不在设定的txt_folder里，则删除原文件
    try:
        # ebook = TinyEpub.Epub(epub_folder + os.sep + title + '.epub')
        # with open(txt_folder+os.sep+ title + '.txt','w',encoding='utf8',errors="replace") as f:
        # r = ebook.get_text()
        #     f.write(r)
        if os.path.exists(txt_folder + os.sep + title + '.txt'):
            shutil.copy(txt_folder + os.sep + "temp", txt_folder + os.sep + title + '.txt')
            os.remove(txt_folder + os.sep + "temp")
        else:
            os.rename(txt_folder + os.sep + "temp", txt_folder + os.sep + title + '.txt')
        if file_path != txt_folder + os.sep + title + '.txt':
            os.remove(file_path)
        message.emit('-origin txt removed')
    except FileNotFoundError:
        message.emit("-txt not found")
        
