import argparse
from src.lexer import lexer
from src.lexer.Token import Token, TokenClass
from src.syntaxer import syntaxer
from src.syntaxer.Phrase import PhraseClass
from src.syntaxer.SemanticAnalyzer import SyntaxParseError
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
if arguments.input[-5:] != ".pyss":
    print("Incorrect file.")
    exit(2)

path = arguments.input
print(f"Input file: {path}")

temp = []
file = open(path, "r")
for row in file:
    if not row.endswith("\n"):
        row = row + "\n"
    temp.append(lexer.process_line(row))

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
    temp = syntaxer.process_tokens(result)
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
    if phrase.phrase_class == PhraseClass.comment:
        continue
    elif phrase.phrase_class == PhraseClass.label:
        generator.add_label(phrase)
        continue
    elif phrase.phrase_class == PhraseClass.body or phrase.phrase_class == PhraseClass.device:
        generator.block_open(phrase)
    elif phrase.phrase_class == PhraseClass.blockClose:
        generator.close_block(phrase)
    else:
        generator.generate_line(phrase)
    output.write(generator.get_line())
    generator.reset_content()
