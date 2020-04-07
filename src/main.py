import argparse
import os
from lexer import lexer
from lexer.token import Token, TokenClass
from syntaxer import syntaxer
from syntaxer.syntaxer import SyntaxParseError
from codegenerator.code_generator import CodeGenerator
from parsetree.parse_tree import ParseTree
from semanticanalyzer.symbol_table import SymbolTable
from semanticanalyzer.semantic_analyzer import SemanticError
from typing import TextIO

parser = argparse.ArgumentParser(description="Interpreter for converting .pce files into .gpss.")
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
path = arguments.input
print(f"Input file: {path}")

if path[-4:] != ".pce":
    print("Incorrect file.")
    exit(1)

if not os.path.exists(path):
    print("File doesn't exists.")
    exit(1)

if os.stat(path).st_size == 0:
    print("File is empty.")
    exit(1)

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
    exit(2)
except SemanticError as error:
    print(error.msg)
    exit(2)

# Print processed phrases to file FIXME: TreePrint
if arguments.so:
    syntaxer_output: TextIO = open(path + ".so", "w")
    syntaxer_output.close()

# Code generator
output_file: TextIO = open(path[:-3] + "gpss", "w")
cg = CodeGenerator(parse_tree, output_file)
cg.generate()
