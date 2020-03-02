import sys
from src.lexer import lexer
from src.syntaxer import syntaxer
from src.lexer.lexer import Token

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
    if not row.endswith("\n"):
        row = row + "\n"
    temp.append(lexer.processLine(lexer.machines, row))

# Flatten lexer result
result = [item for sublist in temp for item in sublist]
result.append([lexer.Token.undefined, ""])
del temp

print(result)

try:
    syntaxer.processTokens(syntaxer.machines, result)
except syntaxer.SyntaxerError as error:
    print("Syntax error. Expected {}, but found {}.".format(error.expectedToken, error.foundToken))

