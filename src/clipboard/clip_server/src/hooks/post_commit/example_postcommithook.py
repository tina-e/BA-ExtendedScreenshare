from hooks.post_commit.basepostcommithook import BasePostCommitHook


class ExamplePostCommitHook(BasePostCommitHook):

    def do_work(self, data):
        print("Auf Wiedersehen von postcommit")
        return data
