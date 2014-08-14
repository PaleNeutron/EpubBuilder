# # This is a template file

def mimetype_tmp():
    """the mimetpye file. return string"""
    tmp = 'application/epub+zip'
    return tmp


def container_tmp():
    """the container.xml file. return string"""

    tmp = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>"""

    return tmp


def html_tmp(chap_title, chap_con, style_con):
    """the html tmp. return string."""

    tmp = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn">
<head>
    {%title%}
    {%style%}
</head>
<body>
    {%content%}
</body>
</html>"""

    tmp = tmp.replace('{%title%}', chap_title)

    tmp = tmp.replace('{%content%}', chap_con)

    tmp = tmp.replace('{%style%}', style_con)

    return tmp


def opf_tmp(uuidnum, book_title, book_author, creatdate, manifest, spine, description, chrpattern):
    """the content.opf file. return string"""
    tmp = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:{%UUID%}</dc:identifier>
    <dc:title>{%title%}</dc:title>
    <dc:creator opf:file-as="PaleNeutron" opf:role="aut">{%author%}</dc:creator>
    <dc:language>zh_CN</dc:language>
    <dc:date opf:event="publication">{%date%}</dc:date>
	<dc:type>网络小说</dc:type>
	<dc:subject>网络小说</dc:subject>
	<dc:description>{%description%}</dc:description>
	<dc:publisher>PaleNeutron</dc:publisher>
	<dc:chrpattern>{%chrpattern%}</dc:chrpattern>
    <meta name="cover" content="xcover.jpg" />
    <meta content="1.0" name="python Epub Buliding Script" />
    <meta content="zecy" name="Script Creator" />
  </metadata>
  <manifest>
    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml" />
    {%items%}
  </manifest>
  <spine toc="ncx">
    {%itemref%}
  </spine>
  <guide>
    <reference href="c00.xhtml" title="cover" type="cover" />
  </guide>
</package>"""

    tmp = tmp.replace('{%UUID%}', uuidnum)
    tmp = tmp.replace('{%title%}', book_title)
    tmp = tmp.replace('{%author%}', book_author)
    tmp = tmp.replace('{%date%}', creatdate)
    tmp = tmp.replace('{%items%}', manifest)
    tmp = tmp.replace('{%itemref%}', spine)
    tmp = tmp.replace('{%description%}', description)
    tmp = tmp.replace('{%chrpattern%}', chrpattern)

    return tmp


def navmap_tmp(playorder, chap_title, ncx_nav_list):
    """it's in toc.ncx"""

    tmp = """<navPoint id="chapter{%playorder%}" playOrder="{%playorder%}">
    <navLabel>
        <text>{%chaptitle%}</text>
    </navLabel>
    <content src="{%chap_src%}" />
</navPoint>
"""
    tmp = tmp.replace('{%playorder%}', playorder)
    tmp = tmp.replace('{%chaptitle%}', chap_title)
    tmp = tmp.replace('{%chap_src%}', ncx_nav_list)

    return tmp


def ncx_tmp(uuidnum, book_title, navmap_out):
    """the toc.ncx file. return string"""

    tmp = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
   <meta name="dtb:uid" content="urn:uuid:{%UUID%}" />
   <meta name="dtb:depth" content="0" />
   <meta name="dtb:totalPageCount" content="0" />
   <meta name="dtb:maxPageNumber" content="0" />
</head>
<docTitle>
    <text>{%title%}</text>
</docTitle>
<navMap>
    {%navmap%}
</navMap>
</ncx>"""

    tmp = tmp.replace('{%UUID%}', uuidnum)
    tmp = tmp.replace('{%title%}', book_title)
    tmp = tmp.replace('{%navmap%}', navmap_out)

    return tmp
