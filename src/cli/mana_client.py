from request import Request
from file_manager import FileManager


class ManaClient:
    file_manager = FileManager()

    def __call__(self, *args):
        operation = next(iter(args), None)
        if operation in ["new", "set", "use", "drop", "push"]:
            response = Request(*args)()
            self.cout(response.json().get("detail", "unkown response"))
        elif operation == "pull":
            if len(args) > 1:
                response = Request(*args)()
                obj = args[1]
                self.file_manager(obj, response.json())
                self.cout(f"{obj} pulled.")
            else:
                raise Exception("Missing object")
        elif operation == "clear":
            self.file_manager.clear()
        else:
            raise Exception("Operation error")

    def cout(self, *args):
        # wrapper around print to easily allow an alternative method of logging.
        print(*args)
