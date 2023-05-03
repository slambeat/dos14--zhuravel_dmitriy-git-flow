import os

shell = os.environ["SHELL"]
if shell == ("/bin/bash"):
    print("Greetings bash")
else:
    print("Hello " + shell)
