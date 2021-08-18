from abc import ABC, abstractmethod


class BasePreAccessHook(ABC):

    @abstractmethod
    def do_work(self, request):
        """
        This is the base hook for pre-access hooks. A pre-access is triggered right before calling any route
        and may modify the request or deny further processing (this may allow for implementing auth-mechanisms)
        """
        return request
