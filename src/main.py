import argparse
from src.lexer import lexer
from src.lexer.Token import Token, TokenGroup
from src.syntaxer import syntaxer
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
result.append(Token(TokenGroup.undefined, ""))
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
    for phrase in temp:
        syntaxer_output.write(str(phrase) + '\n')
    syntaxer_output.close()

# Code generator part FIXME: will be moved out of there
output = open(path[:-4] + "gpss", "w")
generator = CodeGenerator()
for phrase in temp:
    if phrase[0] == syntaxer.PhraseGroup.comment:
        continue
    elif phrase[0] == syntaxer.PhraseGroup.label:
        generator.add_label(phrase)
        continue
    elif phrase[0] == syntaxer.PhraseGroup.body or phrase[0] == syntaxer.PhraseGroup.device:
        generator.block_open(phrase)
    elif phrase[0] == syntaxer.PhraseGroup.blockClose:
        generator.close_block(phrase)
    else:
        generator.generate_line(phrase)
    output.write(generator.get_line())
    generator.reset_content()
