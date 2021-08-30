test_string = b'<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body><pre style="background-color:#2b2b2b;color:#a9b7c6;font-family:\'JetBrains Mono\',monospace;font-size:9.8pt;"><span style="color:#cc7832;">def&#32;</span><span style="color:#ffc66d;">main</span>():<br>&#32;&#32;&#32;&#32;app&#32;=&#32;QApplication(sys.argv)<br>&#32;&#32;&#32;&#32;app.setQuitOnLastWindowClosed(<span style="color:#cc7832;">False</span>)<br>&#32;&#32;&#32;&#32;w&#32;=&#32;QWidget()<br>&#32;&#32;&#32;&#32;tray_icon&#32;=&#32;Menu(QIcon(<span style="color:#6a8759;">"icon.png"</span>)<span style="color:#cc7832;">,&#32;</span>w)<br>&#32;&#32;&#32;&#32;tray_icon.show()<br>&#32;&#32;&#32;&#32;sys.exit(app.exec_())</pre></body></html>'.decode('utf-8')

import html2text
text = html2text.html2text(test_string)
print(text)

from bs4 import BeautifulSoup
soup = BeautifulSoup(test_string, features="lxml")
text = soup.get_text()
print(text)
