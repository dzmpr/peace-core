import sys
from src.lexer import lexer

# Checking if file path was provided
if len(sys.argv) < 2:
    print("Too less arguments.")
    exit()
# Checking if file has correct extension
if sys.argv[1][-4:] != "pyss":
    print("Incorrect file.")
    exit()

path = sys.argv[1]
print("Input file: {}".format(path))


temp = []
file = open(path, "r")
for row in file:
    temp.append(lexer.processLine(lexer.machines, row))

# Flatten lexer result
result = [item for sublist in temp for item in sublist]
print(result)

