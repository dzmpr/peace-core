import argparse
import os
import sys
from typing import TextIO
from lexer import lexer
from lexer.token import TokenClass
from syntaxer import syntaxer
from syntaxer.lang_dict import LangDict, SignatureType
from syntaxer.interpretation_error import InterpretationError, print_error_info
from codegenerator.code_generator import CodeGenerator
from parsetree.parse_tree import ParseTree
from semanticanalyzer.symbol_table import SymbolTable

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
    print("Incorrect file.", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(path):
    print("File doesn't exists.", file=sys.stderr)
    sys.exit(1)

if os.stat(path).st_size == 0:
    print("File is empty.", file=sys.stderr)
    sys.exit(1)

# Language dictionary
lang_dict = LangDict()
lang_dict.add_signature("q", SignatureType.operator, "QUEUE", 1, [
    TokenClass.word
])
lang_dict.add_signature("dq", SignatureType.operator, "DEPART", 1, [
    TokenClass.word
])
lang_dict.add_signature("gen", SignatureType.operator, "GENERATE", 1, [
    TokenClass.string
])
lang_dict.add_signature("init", SignatureType.operator, "START", 1, [
    TokenClass.num
])
lang_dict.add_signature("delay", SignatureType.operator, "ADVANCE", 1, [
    TokenClass.num,
    TokenClass.num
])
lang_dict.add_signature("delay", SignatureType.operator, "ADVANCE", 1, [
    TokenClass.string
])
lang_dict.add_signature("destroy", SignatureType.operator, "TERMINATE", 0, [
    TokenClass.num
])
lang_dict.add_signature("goto", SignatureType.operator, "TRANSFER", 1, [
    TokenClass.string
])
lang_dict.add_signature("compare", SignatureType.operator, "TEST", 2, [
    TokenClass.word,
    TokenClass.string
])
lang_dict.add_signature("changevar", SignatureType.operator, "SAVEVALUE", 1, [
    TokenClass.string
])
lang_dict.add_signature("var", SignatureType.operator, "INITIAL", 1, [
    TokenClass.string
])
lang_dict.add_signature("copy", SignatureType.operator, "SPLIT", 1, [
    TokenClass.string
])
lang_dict.add_signature("link", SignatureType.operator, "LINK", 1, [
    TokenClass.string
])
lang_dict.add_signature("unlink", SignatureType.operator, "UNLINK", 1, [
    TokenClass.string
])
lang_dict.add_signature("priority", SignatureType.operator, "PRIORITY", 1, [
    TokenClass.num
])
lang_dict.add_signature("priority", SignatureType.operator, "PRIORITY", 1, [
    TokenClass.string
])
lang_dict.add_signature("assign", SignatureType.operator, "ASSIGN", 1, [
    TokenClass.string
])
lang_dict.add_signature("func", SignatureType.operator, "FUNCTION", 3, [
    TokenClass.word,
    TokenClass.string,
    TokenClass.string
])
lang_dict.add_signature("preempt", SignatureType.operator, "PREEMPT", 1, [
    TokenClass.string
])
lang_dict.add_signature("ret", SignatureType.operator, "RETURN", 1, [
    TokenClass.string
])


token_list = []
pce_source: TextIO = open(path, "r", encoding="utf8")
for row in pce_source:
    if not row.endswith("\n"):
        row += "\n"
    token_list.extend(lexer.process_line(row))
pce_source.close()

# Print processed tokens to file
if arguments.lo:
    lexer_output: TextIO = open(path + ".lo", "w", encoding="utf8")
    for token in token_list:
        lexer_output.write(str(token) + "\n")
    lexer_output.close()

# Parse tree
parse_tree = ParseTree()
# Symbol table
symbol_table = SymbolTable()

# Process tokens with syntax analyzer
try:
    syntaxer.process_tokens(parse_tree, symbol_table, lang_dict, token_list)
    token_list.clear()
except InterpretationError as error:
    print_error_info(error, path)
    sys.exit(2)

# Print processed phrases to file FIXME: TreePrint
if arguments.so:
    syntaxer_output: TextIO = open(path + ".so", "w", encoding="utf8")
    syntaxer_output.close()

# Code generator
output_file: TextIO = open(path[:-3] + "gpss", "w", encoding="utf8")
cg = CodeGenerator(parse_tree, lang_dict, output_file)
cg.compile()
output_file.close()
