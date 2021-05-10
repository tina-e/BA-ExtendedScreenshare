import os

import pyperclip
import subprocess
#pyperclip.copy("abc")

clipboard_content = pyperclip.paste()

if clipboard_content.startswith("/"):
    #open file with standard program
    subprocess.call(('xdg-open', clipboard_content))


# bei files: path wird bei paste() ausgegeben