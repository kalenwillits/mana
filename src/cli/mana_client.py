from request import Request
from file_manager import FileManager


class ManaClient:
    file_manager = FileManager()

    def __call__(self, *args):
        operation = next(iter(args), None)
        response = Request(*args)()
        if operation in ["new", "set", "use", "drop", "push"]:
            self.cout(response.json().get("detail", "unkown response"))
        elif operation == "pull":
            if len(args) > 1:
                obj = args[1]
                self.file_manager(obj, response.json())
                self.cout("Project pulled.")
            else:
                raise Exception("Missing object")
        else:
            raise Exception("Operation error")

    def cout(self, *args):
        # wrapper around print to easily allow an alternative method of logging.
        print(*args)
