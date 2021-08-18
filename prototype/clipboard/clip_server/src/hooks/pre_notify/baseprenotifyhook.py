from abc import ABC, abstractmethod


class BasePrenotifyHook(ABC):

    @abstractmethod
    def do_work(self, item, recipients, from_hook, sender_id):
        """
        The pre-notify hook manages the list of recipients to be notified
        """
        pass
