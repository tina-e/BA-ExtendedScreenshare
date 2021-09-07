from abc import ABC, abstractmethod


class BasePostCommitHook(ABC):

    @abstractmethod
    def do_work(self, data):
        """
        This is the base hook for post-commit hooks. It is called right after the clipboard request is persisted
        and may return transformed request data.
        """
        return data
