from request import Request


class ManaClient:
    def __call__(self, *args):
        response = Request(*args)()
        self.cout(response.json().get("detail", "unkown response"))

    def cout(self, *args):
        # wrapper around print to easily allow an alternative method of logging.
        print(*args)
