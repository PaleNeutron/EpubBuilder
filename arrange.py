import os
import shutil


def arrange(route, title):
    shutil.rmtree('epubobject')
    shutil.copy(title + '.epub', r'D:\Documents\epub')
    if os.path.split(route)[0] != 'D:\\Documents\\txt':
        try:
            os.remove(route)
        except:
            pass
    print('arrange is done')
        
