test_string = b'<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body><pre style="background-color:#2b2b2b;color:#a9b7c6;font-family:\'JetBrains Mono\',monospace;font-size:9.8pt;"><span style="color:#cc7832;">def&#32;</span><span style="color:#ffc66d;">main</span>():<br>&#32;&#32;&#32;&#32;app&#32;=&#32;QApplication(sys.argv)<br>&#32;&#32;&#32;&#32;app.setQuitOnLastWindowClosed(<span style="color:#cc7832;">False</span>)<br>&#32;&#32;&#32;&#32;w&#32;=&#32;QWidget()<br>&#32;&#32;&#32;&#32;tray_icon&#32;=&#32;Menu(QIcon(<span style="color:#6a8759;">"icon.png"</span>)<span style="color:#cc7832;">,&#32;</span>w)<br>&#32;&#32;&#32;&#32;tray_icon.show()<br>&#32;&#32;&#32;&#32;sys.exit(app.exec_())</pre></body></html>'.decode('iso-8859-1')
test_string_gtk = b'GTKTEXTBUFFERCONTENTS-0001\x00\x00\x00_ <text_view_markup>\n <tags>\n </tags>\n<text>hallo mein name ist tina</text>\n</text_view_markup>\n'
test_string_html = b'<meta http-equiv="content-type" content="text/html; charset=utf-8">Its easier than it is thought:'
test_string_non_ascii = b'GTKTEXTBUFFERCONTENTS-0001\x00\x00\x00\x85 \n \n \nhallo mein name ist tina\nund ich sitze hier an dieser schei\xc3\x9fe\n\n'

import html2text
text = html2text.html2text(test_string).rstrip('\n')
print(text)
text = html2text.html2text(test_string_gtk.decode('iso-8859-1')).rstrip('\n')
print(text)
text = html2text.html2text(test_string_html.decode('iso-8859-1')).rstrip('\n')
print(text)
text = html2text.html2text(test_string_non_ascii.decode('iso-8859-1')).rstrip('\n')
print(text)
print("___")

from bs4 import BeautifulSoup
soup = BeautifulSoup(test_string_gtk.decode(), features="lxml")
text = soup.get_text()
#print(text)
#print("___")

import re
cleanr = re.compile('<.*?>')
cleantext = re.sub(cleanr, '', test_string_gtk.decode('iso-8859-1'))
#print(cleantext)
'''cleanr = re.compile('<.*?>')
cleantext = re.sub(cleanr, '', test_string_html.decode('utf-8'))
print(cleantext)
cleanr = re.compile('<.*?>')
cleantext = re.sub(cleanr, '', test_string)
print(cleantext)'''

print("______")
print(b'GTKTEXTBUFFERCONTENTS-0001\x00\x00\x00X \n \n \nitze hier an dies\n\n'.decode())
print("______")
print(b'GTKTEXTBUFFERCONTENTS-0001\x00\x00\x00\x85 \n \n \nhallo mein name ist tina\nund ich sitze hier an dieser scheisse\n\n'.decode('iso-8859-1'))

