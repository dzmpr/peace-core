import sys

# Checking if file path was provided
if len(sys.argv) < 2:
    print("Too less arguments.")
    exit()
# Checking if file has correct extension
if sys.argv[1][-4:] != "pyss":
    print("Incorrect file.")
    exit()

print("Input file: {}".format(sys.argv[1]))

# Lexer