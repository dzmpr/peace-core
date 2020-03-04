import argparse
from src.lexer import lexer
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
    temp.append(lexer.processLine(lexer.machines, row))

# Flatten lexer result
result = [item for sublist in temp for item in sublist]
result.append([lexer.Token.undefined, ""])
temp.clear()

if arguments.lo:
    lexeroutput = open(path + ".lo", "w")
    for token in result:
        lexeroutput.writelines(str(token) + '\n')

try:
    temp = syntaxer.processTokens(syntaxer.machines, result)
except SyntaxParseError as error:
    print(error.msg)

if arguments.so:
    syntaxeroutput = open(path + ".so", "w")
    for phrase in temp:
        syntaxeroutput.write(str(phrase) + '\n')

output = open(path[:-4] + "gpss", "w")
generator = CodeGenerator()
for phrase in temp:
    if phrase[0] == syntaxer.Phrase.comment:
        continue
    elif phrase[0] == syntaxer.Phrase.label:
        generator.addLabel(phrase)
        continue
    elif phrase[0] == syntaxer.Phrase.body or phrase[0] == syntaxer.Phrase.device:
        generator.blockOpen(phrase)
    elif phrase[0] == syntaxer.Phrase.blockClose:
        generator.closeBlock(phrase)
    else:
        generator.generateLine(phrase)
    output.write(generator.getLine())
    generator.resetContent()
