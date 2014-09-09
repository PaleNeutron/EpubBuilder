import os
import shutil

import messager


message = messager.statusbar_message


def arrange(route, txt_folder, epub_folder, title):
    shutil.rmtree('epubobject')
    # 将epub移动到epub_folder中去
    if os.path.exists(epub_folder + os.sep + title + '.epub'):
        shutil.copy(title + '.epub', epub_folder)
        os.remove(title + '.epub')
    else:
        shutil.move(title + '.epub', epub_folder)
    # 如果文本文件位置不在设定的txt_folder里，则删除原文件
    if os.path.split(route)[0] != txt_folder:
        try:
            os.remove(route)
            message.emit('-origin txt removed')
        except FileNotFoundError:
            message.emit("-txt not found")
        
