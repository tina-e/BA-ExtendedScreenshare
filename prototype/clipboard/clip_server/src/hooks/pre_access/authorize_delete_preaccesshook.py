from hooks.pre_access.basepreaccesshook import BasePreAccessHook

class LocalhostOnlyHook(BasePreAccessHook):
    """
    Hook for restricting access to the local machine
    """

    def do_work(self, request):
        # Ignore other methods than delete and requests from local machine
        if request.method is not 'DELETE' or request.remote_addr.startswith('127.0.0'):
            return request
        else:
            print("Unauthorized Delete from machine", request.remote_addr)
            raise ValueError('User Not Authorized for Delete!')
