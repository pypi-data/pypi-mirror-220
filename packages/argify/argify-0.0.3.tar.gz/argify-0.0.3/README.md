# Args Parser Readme

## Overview

This is a simple Python script for parsing command-line arguments and executing corresponding functions. The `Args` class provides decorators to associate functions with argument names and allows the script to execute the corresponding function when the respective argument is provided in the command line.

## Usage

### Importing the Script

To use the `Args` class, you need to import the script into your Python code. Make sure the script file is in the same directory as your Python file or in a location where it can be imported.

```python
from args_parser import Args
```

### Creating an Instance

To get started, create an instance of the `Args` class:

```python
args_parser = Args()
```

### Associating Functions with Arguments

Use the `arg` decorator to associate functions with argument names. The `arg` decorator takes a list of argument names as its parameter.

```python
@args_parser.arg(["-hello", "--greet"])
def greet_user(name):
    print(f"Hello, {name}!")

@args_parser.arg(["-bye", "--farewell"])
def say_goodbye(name):
    print(f"Goodbye, {name}!")
```

In this example, the `greet_user` function is associated with arguments `-hello` and `--greet`, and the `say_goodbye` function is associated with arguments `-bye` and `--farewell`.

### Handling No Arguments

Use the `haveArgs` decorator to set a function that will be executed when no arguments are provided in the command line.

```python
@args_parser.haveArgs
def no_args_function():
    print("No arguments provided.")
```

### Parsing Arguments

After defining your functions and associating them with argument names, call the `parse_args()` method of the `Args` instance to process the command-line arguments and execute the corresponding function.

```python
if __name__ == "__main__":
    args_parser.parse_args()
```

### Running the Script

Run your Python script from the command line, passing the desired argument and its value (if required):

```bash
python your_script.py -hello Alice
```

Output:
```
Hello, Alice!
```

```bash
python your_script.py -bye Bob
```

Output:
```
Goodbye, Bob!
```

```bash
python your_script.py
```

Output:
```
No arguments provided.
```

## Conclusion

The `Args` class simplifies the process of parsing and handling command-line arguments in Python. By using decorators to associate functions with arguments, you can easily expand the functionality of your script and provide a better command-line interface for your users.

Please note that this is a basic example and may require additional error handling and input validation depending on the complexity of your use case. Enjoy using the `Args` parser and happy coding!