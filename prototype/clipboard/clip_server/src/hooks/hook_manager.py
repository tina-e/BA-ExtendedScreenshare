from importlib import machinery
from os import listdir
from hooks.basehook import BaseHook
from hooks.pre_commit.baseprecommithook import BasePreCommitHook
from hooks.pre_access.basepreaccesshook import BasePreAccessHook
from hooks.post_commit.basepostcommithook import BasePostCommitHook
from hooks.pre_notify.baseprenotifyhook import BasePrenotifyHook
from hooks.post_notify.basepostnotifyhook import BasePostnotifyHook
from hooks.post_access.basepostaccesshook import BasePostAccessHook

class HookManager:

    def _load_hooks(self, root_dir, name_contains, BaseClass):
        hooks = []
        files = listdir(root_dir)
        hook_files = [f for f in files if f.endswith('_' + name_contains + '.py')]
        for file_name in hook_files:
            modname = file_name[:-3]
            module = machinery.SourceFileLoader(modname, root_dir + '/' + file_name).load_module()
            members = dir(module)
            for m in members:
                # Do not even check underscored stuff and Parent class
                if not m.startswith('_') and 'Base' not in m and 'Hook' in m:
                    try:
                        hook = getattr(module, m)()  # instanciate found class
                    except TypeError:
                        print("Could not instantiate hook", m, 'from module', modname)
                    if isinstance(hook, BaseClass):  # is child of BaseHook
                        hooks.append(hook)
        return hooks

    def call_hooks(self, request):
        for h in self.hooks:
            if not h.do_work(request):
                return False
        return True

    def trigger_precommit(self, data, hooks=None):
        if hooks is None:
            return self.trigger_precommit(data, self.pre_commit_hooks)
        elif len(hooks) > 0:
            curr_hook = hooks.pop()
            return self.trigger_precommit(curr_hook.do_work(data), hooks)
        else:
            return data

    def trigger_postcommit(self, data, hooks=None):
        if hooks is None:
            return self.trigger_postcommit(data, self.post_commit_hooks)
        elif len(hooks) > 0:
            curr_hook = hooks.pop()
            return self.trigger_postcommit(data, hooks)
        else:
            return data

    def trigger_preaccess(self, request):
        for h in self.pre_access_hooks:
            h.do_work(request)
        return

    def trigger_postaccess(self, response):
        for h in self.post_access_hooks:
            h.do_work(response)
        return

    def trigger_prenotify(self, item, recipients, from_hook, sender_id, hooks=None):
        if hooks is None:
            return self.trigger_prenotify(item, recipients, from_hook, sender_id, self.pre_notify_hooks)
        elif len(hooks) > 0:
            hook = hooks.pop()
            return self.trigger_prenotify(*hook.do_work(item, recipients, from_hook, sender_id), hooks)
        else:
            return item, recipients, from_hook, sender_id

    def trigger_postnotify(self, item, from_hook, sender_id, recipients):
        for h in self.post_notify_hooks:
            h.do_work(item, from_hook, sender_id, recipients)
        return item, from_hook, sender_id, recipients

    def __init__(self):
        self.hooks = []
        self.pre_access_hooks = self._load_hooks('./hooks/pre_access', 'preaccesshook', BasePreAccessHook)
        self.post_access_hooks = self._load_hooks('./hooks/post_access', 'postaccesshook', BasePostAccessHook)
        self.pre_commit_hooks = self._load_hooks('./hooks/pre_commit', 'precommithook', BasePreCommitHook)
        self.post_commit_hooks = self._load_hooks('./hooks/post_commit', 'postcommithook', BasePostCommitHook)
        self.pre_notify_hooks = self._load_hooks('./hooks/pre_notify', 'prenotifyhook', BasePrenotifyHook)
        self.post_notify_hooks = self._load_hooks('./hooks/post_notify', 'postnotifyhook', BasePostnotifyHook)
