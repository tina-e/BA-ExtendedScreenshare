from flask import request

'''
ACCESS HOOKS

Access Hooks will be triggered, whenever an API Request is made. 

Access Hooks can be used for controlling access to resources based on the requests made or document access 
(e.g. for logging reasons).
'''


def access_hooks(func):
    def wrapper(*args, **kwargs):
        return _pre_access_hooks(
            _post_access_hooks(
                func
            )
        )(*args, **kwargs)
    return wrapper


def _pre_access_hooks(func):
    def wrapper(*args, **kwargs):
        try:
            args[0].hook_manager.trigger_preaccess(request)
            return func(*args, **kwargs)
        except ValueError:
            return 'Unauthorized Access', 403
    return wrapper


def _post_access_hooks(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        args[0].hook_manager.trigger_postaccess(response)
        return response
    return wrapper
#
#

'''
COMMIT HOOKS

Commit Hooks will be triggered right before saving a new clip or child clip.

Commit Hooks can be used to derive and save related formats or transform the clip to be saved.
'''


def commit_hooks(func):
    def wrapper(self, data):
        return _pre_commit_hooks(
            _post_commit_hooks(
                func
            )
        )(self, data)
    return wrapper


def _pre_commit_hooks(func):
    def wrapper(self, data):
        new_data = self.hook_manager.trigger_precommit(data)
        return func(self, new_data)
    return wrapper


def _post_commit_hooks(func):
    def wrapper(self, data):
        result = func(data)
        transformed_result = self.hook_manager.trigger_postcommit(result)
        return transformed_result
    return wrapper
#
#


def notify_hooks(func):
    def wrapper(self, clip, recipients, from_hook, sender_id):
        return _pre_notify_hooks(
            _post_notify_hooks(
                func
            )
        )(self, clip, recipients, from_hook, sender_id)
    return wrapper


def _pre_notify_hooks(func):
    def wrapper(self, item, recipients, from_hook, sender_id):
        args = self.hook_manager.trigger_prenotify(item, recipients, from_hook, sender_id)
        return func(self, *args)
    return wrapper


def _post_notify_hooks(func):
    def wrapper(self, item, recipients, from_hook, sender_id):
        result = func(item, recipients, from_hook, sender_id)
        self.hook_manager.trigger_postnotify(item, recipients, from_hook, sender_id)
        return result
    return wrapper
