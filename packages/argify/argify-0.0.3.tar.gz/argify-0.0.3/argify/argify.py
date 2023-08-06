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
        cargs = sys.argv[1:]  # Get all arguments except the script name

        i = 0
        while i < len(cargs):
            arg_name = cargs[i]

            # Check if the argument is decorated without considering the starting character
            decorated_args = set(arg for arg in self.arguments.keys())
            if arg_name in decorated_args:
                func = self.arguments[arg_name]
                arg_values = []

                i += 1  # Move to the next argument value

                while i < len(cargs) and cargs[i] not in decorated_args:
                    arg_values.append(cargs[i])
                    i += 1

                func(*arg_values)
            else:
                print("Unknown argument:", arg_name)
                i += 1

        if not cargs and self.no_args_function:
            self.no_args_function()