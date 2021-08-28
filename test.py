import re

if re.match("^add\d+", "add"):
    print("matched")
else:
    print("no match")