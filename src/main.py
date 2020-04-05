import argparse
from src.lexer import lexer
from src.lexer.Token import Token, TokenClass
from src.syntaxer import syntaxer
from src.syntaxer.syntaxer import SyntaxParseError
from src.codegenerator.CodeGenerator import CodeGenerator
from src.parsetree.ParseTree import ParseTree
from src.SemanticAnalyzer.SymbolTable import SymbolTable
from src.SemanticAnalyzer.SemanticAnalyzer import SemanticError
from typing import TextIO

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
file: TextIO = open(path, "r")
for row in file:
    if not row.endswith("\n"):
        row += "\n"
    temp.append(lexer.process_line(row))

# Flatten lexer result
result = [item for sublist in temp for item in sublist]
result.append(Token(TokenClass.undefined, ""))
temp.clear()

# Print processed tokens to file
if arguments.lo:
    lexer_output: TextIO = open(path + ".lo", "w")
    for token in result:
        lexer_output.write(str(token) + "\n")
    lexer_output.close()

# Parse tree
parse_tree = ParseTree()
# Symbol table
symbol_table = SymbolTable()

# Process tokens with syntax analyzer
try:
    syntaxer.process_tokens(parse_tree, symbol_table, result)
except SyntaxParseError as error:
    print(error.msg)
    exit(1)
except SemanticError as error:
    print(error.msg)
    exit(1)

# Print processed phrases to file FIXME: TreePrint
if arguments.so:
    syntaxer_output: TextIO = open(path + ".so", "w")
    for phrase in temp:
        syntaxer_output.write(str(phrase) + '\n')
    syntaxer_output.close()

# Code generator
output_file: TextIO = open(path[:-4] + "gpss", "w")
cg = CodeGenerator(tree=parse_tree, file=output_file)
