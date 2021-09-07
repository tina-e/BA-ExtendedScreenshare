from abc import ABC, abstractmethod


class BasePreCommitHook(ABC):

    @abstractmethod
    def do_work(self, data):
        """
        This is the base hook for pre-commit hooks. A pre-commit hook is called right before the clipboard request is persisted
        and may modify the request or deny further processing (this may allow for implementing auth-mechanisms)
        """
        pass
