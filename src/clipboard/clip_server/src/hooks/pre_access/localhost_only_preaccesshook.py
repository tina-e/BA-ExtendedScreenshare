from hooks.pre_access.basepreaccesshook import BasePreAccessHook


class LocalhostOnlyHook(BasePreAccessHook):
    """
    Hook for restricting access to the local machine
    """

    def do_work(self, request):
        remote = request.remote_addr
        #if remote.startswith('127.0.0'):
        return request
        #else:
        #    raise ValueError('User Not Authorized for Access on Resource!')
