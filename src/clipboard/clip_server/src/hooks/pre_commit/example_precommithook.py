from hooks.pre_commit.baseprecommithook import BasePreCommitHook


class ExamplePreCommitHook(BasePreCommitHook):

    def do_work(self, data):
        if data['mimetype'] == 'text/plain':
            # data['data'] = "save another text instead of the original text, or convert it somehow"
            print("Hi from commit hook!")
            print(data['data'])
        return data