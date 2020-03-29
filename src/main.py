import argparse
from src.lexer import lexer
from src.lexer.Token import Token, TokenClass
from src.syntaxer import syntaxer
from src.syntaxer.Construction import ConstructionClass
from src.syntaxer.SemanticProcessor import SyntaxParseError
from src.codegenerator.CodeGenerator import CodeGenerator

parser = argparse.ArgumentParser(description="Interpreter for converting .pyss files into .gpss.")
parser.add_argument(
    'input',
    type=str,
    help="File with source code to process."
)
parser.add_argument(
    '-lo',
    action='store_true',
    help="Verbose lexer output."
)
parser.add_argument(
    '-so',
    action='store_true',
    help="Verbose syntaxer output."
)
arguments = parser.parse_args()

# Checking if file has correct extension
if arguments.input[-4:] != "pyss":
    print("Incorrect file.")
    exit(2)

path = arguments.input
print("Input file: {}".format(path))

temp = []
file = open(path, "r")
for row in file:
    if not row.endswith("\n"):
        row = row + "\n"
    temp.append(lexer.process_line(lexer.machines, row))

# Flatten lexer result
result = [item for sublist in temp for item in sublist]
result.append(Token(TokenClass.undefined, ""))
temp.clear()

# Print processed tokens to file
if arguments.lo:
    lexer_output = open(path + ".lo", "w")
    for token in result:
        lexer_output.write(str(token) + "\n")
    lexer_output.close()

# Process tokens with syntax analyzer
try:
    temp = syntaxer.process_tokens(syntaxer.machines, result)
except SyntaxParseError as error:
    print(error.msg)

# Print processed phrases to file
if arguments.so:
    syntaxer_output = open(path + ".so", "w")
    for construction in temp:
        syntaxer_output.write(str(construction) + '\n')
    syntaxer_output.close()

# Code generator part FIXME: will be moved out of there
output = open(path[:-4] + "gpss", "w")
generator = CodeGenerator()
for construction in temp:
    if construction[0] == ConstructionClass.comment:
        continue
    elif construction[0] == ConstructionClass.label:
        generator.add_label(construction)
        continue
    elif construction[0] == ConstructionClass.body or construction[0] == ConstructionClass.device:
        generator.block_open(construction)
    elif construction[0] == ConstructionClass.blockClose:
        generator.close_block(construction)
    else:
        generator.generate_line(construction)
    output.write(generator.get_line())
    generator.reset_content()
