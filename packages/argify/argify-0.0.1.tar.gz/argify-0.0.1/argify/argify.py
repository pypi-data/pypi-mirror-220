import sys

class Args:
    def __init__(self):
        self.arguments = {}
        self.no_args_function = None

    def arg(self, names):
        def decorator(func):
            for name in names:
                self.arguments[name] = func
            return func
        return decorator

    def haveArgs(self, func):
        self.no_args_function = func
        return func

    def parse_args(self):
        if len(sys.argv) > 1:
            arg_name = sys.argv[1]
            if arg_name in self.arguments:
                func = self.arguments[arg_name]
                arg_values = sys.argv[2:]
                func(*arg_values)
            else:
                print("Unknown argument:", arg_name)
        else:
            if self.no_args_function:
                self.no_args_function()
            else:
                print("No arguments provided.")
