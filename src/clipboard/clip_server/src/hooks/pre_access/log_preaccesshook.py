from hooks.pre_access.basepreaccesshook import BasePreAccessHook
import os
import json
from pathlib import Path

class LogPreaccessHook(BasePreAccessHook):
    """
    Hook for restricting access to the local machine
    """
    filename=str(Path.home()) +'/acclog.txt'

    def do_work(self, request):
        print("Howdy from preaccess")
        mode = None
        if os.path.exists(self.filename):
            mode = 'a'
        else:
            mode = 'w'
        f = open(self.filename, mode)
        f.write(str(request.__dict__) + '\n')
        f.close()
        return request