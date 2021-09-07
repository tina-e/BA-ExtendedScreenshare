from abc import ABC, abstractmethod


class BaseHook(ABC):

    @abstractmethod
    def do_work(self, request):
        """
        This method gets called when a hook should do his work.
        It will get passed the object sent to the server by the client
        and may modify it.
        Since you will get every object regardless of the type,
        it is the hook's responsibility to check,
        if it's operation is applicable.
        Use obj['mimetype'] to determine the content of obj['content'].
        Content of files will be binary even if the are text files.
        """
        pass
