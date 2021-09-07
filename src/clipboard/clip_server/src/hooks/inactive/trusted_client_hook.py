from util.context import Context
import server
from importlib import machinery
import json


from server.hooks.basehook import BaseHook

class TrustedClientHook(BaseHook):
    """
    Hook for restricting or allowing access to the clipboard server.

    trusted-clients-config.json contains an array with the addresses of allowed devices, all requests from other
    sources will effect an "access forbidden" warning.
    """

    def do_work(self, request):
        file = open(Context.ctx.get_resource("config/trusted-clients-config.json"))
        trusted_addresses = json.load(file)
        file.close()
        remote = request.remote_addr
        if (remote in trusted_addresses) or remote.startswith('192.') or remote.startswith('127.'):
            return True
        else:
            return False
