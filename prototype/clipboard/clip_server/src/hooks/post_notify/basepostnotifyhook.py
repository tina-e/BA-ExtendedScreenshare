from abc import ABC, abstractmethod


class BasePostnotifyHook(ABC):

    @abstractmethod
    def do_work(self, item, from_hook, sender_id, recipients):
        """
        The post-notify hook can be used to log, which recipient has received which clip.
        """
        return item, from_hook, sender_id, recipients,
