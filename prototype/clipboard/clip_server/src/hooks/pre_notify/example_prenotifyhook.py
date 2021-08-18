from hooks.pre_notify.baseprenotifyhook import BasePrenotifyHook

class ExamplePrenotifyHook(BasePrenotifyHook):

    def do_work(self, item, recipients, from_hook, sender_id):
        print("Hola de prenotify")
        print("Publishing", item, "to", recipients)
        """
        This is the base hook for the prenotify-hook, which is triggered right before other clipboards are updated and webhooks are notified.
        """
        return item, recipients, from_hook, sender_id
