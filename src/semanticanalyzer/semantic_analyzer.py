from parsetree.parse_tree import ParseTree
from parsetree.tree_composer import TreeComposer
from semanticanalyzer.symbol_table import SymbolTable
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from syntaxer.lang_dict import LangDict, SignatureType, Signature
from lexer.token import TokenClass
from syntaxer.interpretation_error import InterpretationError, ErrorType, PeaceError
from typing import Union


class SemanticAnalyzer:
    def __init__(self, tree: ParseTree, symbol_table: SymbolTable, lang_dict: LangDict):
        self.tree: ParseTree = tree
        self.composer: TreeComposer = TreeComposer(tree)
        self.table: SymbolTable = symbol_table
        self.lang_dict: LangDict = lang_dict
        self._line_count: int = 1
        self._expr_params: Union[dict, None] = None
        self._expr_name: Union[str, None] = None
        self._expr_id: Union[int, None] = None

    def add_line(self):
        self._line_count += 1

    def remove_line(self):
        self._line_count -= 1

    def get_line(self) -> int:
        return self._line_count

    def __repr__(self):
        return f"Semantic an. ({self.tree}, {self.table}, {self.lang_dict})"

    def process_phrase(self, phrase: Phrase, line_number: int):
        self._signature_recorder(phrase)
        self._signature_inference(phrase, line_number)
        self._name_processing(phrase, line_number)
        self.composer.add_phrase(phrase, line_number)

    # TODO: First version (without scope-dependent check), to be refactored
    def _name_processing(self, phrase: Phrase, line_number: int):
        if phrase.phrase_class == PhraseClass.block:
            identifier: str = phrase.keyword.value
            if not self.table.is_symbol_presence(identifier):
                self.table.add_symbol(identifier, phrase.phrase_subclass)
            else:
                raise InterpretationError(
                    PeaceError(f"\nName \"{identifier}\" already used by "
                               f"{self.table.get_symbol(identifier).phrase_class.name}.",
                               ErrorType.naming_error, line_number, identifier))

        elif phrase.phrase_class == PhraseClass.label:
            identifier: str = phrase.keyword.value
            if not self.table.is_symbol_presence(identifier):
                self.table.add_symbol(identifier, phrase.phrase_class)
            else:
                raise InterpretationError(
                    PeaceError(f"\nName \"{identifier}\" already used by "
                               f"{self.table.get_symbol(identifier).phrase_class.name}.",
                               ErrorType.naming_error, line_number, identifier))

        elif phrase.phrase_class == PhraseClass.operator:
            operator: str = phrase.keyword.value
            if self.lang_dict.check_definition(operator):
                sig_type = self.lang_dict.get_signature(operator).signature_type
                if sig_type == SignatureType.operator:
                    if len(phrase.params):
                        identifier: str = phrase.params[0].value
                        if operator == "q":
                            if not self.table.is_symbol_presence(identifier):
                                self.table.add_symbol(identifier, phrase.phrase_class)
                            else:
                                raise InterpretationError(
                                    PeaceError(f"Name \"{identifier}\" already used by "
                                               f"{self.table.get_symbol(identifier).phrase_class.name}.",
                                               ErrorType.naming_error, line_number, identifier))
                        elif operator == "dq":
                            if not self.table.is_symbol_presence(identifier):
                                raise InterpretationError(
                                    PeaceError(f"\nName \"{identifier}\" was never defined.",
                                               ErrorType.naming_error, line_number, identifier))
            else:
                raise InterpretationError(
                    PeaceError(f"Unknown operator \"{operator}\".",
                               ErrorType.naming_error, line_number, operator))

    def _signature_inference(self, phrase: Phrase, line_number: int):
        if phrase.phrase_class == PhraseClass.operator:
            keyword = phrase.keyword.value
            candidates = self.lang_dict.get_candidates(keyword)
            unsuitable_candidates = InterpretationError()
            for signature_id in candidates:
                signature = self.lang_dict.get_signature(signature_id)
                try:
                    temp_params = self._expr_params.copy()
                    temp_param_usage = signature.contains_param
                    self._signature_check(signature, phrase, temp_params, temp_param_usage, line_number)
                except PeaceError as error:
                    unsuitable_candidates.add_error(error)
                else:
                    self._expr_params.update(temp_params)
                    signature.contains_param = temp_param_usage
                    phrase.signature_id = signature_id
                    break

            if phrase.signature_id is None:
                raise unsuitable_candidates

    def _signature_check(self, candidate: Signature, phrase: Phrase, expr_params: dict, param_usage: bool, line_number: int):
        keyword = phrase.keyword.value
        context = self.tree.get_context()
        params_num = len(phrase.params)
        if candidate.required_params <= params_num <= candidate.max_params:
            for i in range(params_num):
                # Using parameters in body forbidden
                if context.phrase_subclass == PhraseSubclass.body:
                    if phrase.params[i].token_class == TokenClass.parameter:
                        raise InterpretationError(
                            PeaceError(f"Parameter \"{phrase.params[i].value}\" can't be used inside main.",
                                       ErrorType.parameter_error, line_number, phrase.params[i].value))

                # Check parameter define in expression
                elif context.phrase_subclass == PhraseSubclass.expression:
                    if phrase.params[i].token_class == TokenClass.parameter:
                        if phrase.params[i].value in expr_params:
                            if expr_params[phrase.params[i].value] != candidate.params[i]:
                                raise InterpretationError(
                                    PeaceError(f"Wrong parameter for \"{keyword}\", expected "
                                               f"{candidate.params[i].name} but "
                                               f"\"{phrase.params[i].value}\" has "
                                               f"{expr_params[phrase.params[i].value].name} type.",
                                               ErrorType.parameter_error, line_number, phrase.params[i].value))

                        else:
                            expr_params[phrase.params[i].value] = candidate.params[i]

                        param_usage = True
                        continue

                # Check coincidence of parameter with operator signature
                if phrase.params[i].token_class != candidate.params[i]:
                    raise InterpretationError(
                        PeaceError(f"Wrong parameter for \"{keyword}\", expected "
                                   f"{candidate.params[i].name} but "
                                   f"\"{phrase.params[i].value}\" has "
                                   f"{expr_params[phrase.params[i].value].name} type.",
                                   ErrorType.parameter_error, line_number, phrase.params[i].value))
        else:
            raise InterpretationError(
                PeaceError(f"Found \"{keyword}\" operator with {params_num} "
                           f"parameters, but expected {candidate.required_params}-{candidate.max_params}.",
                           ErrorType.parameter_error, line_number, keyword))

    def _signature_recorder(self, phrase: Phrase):
        # Check if parameter names are consistent
        def is_params_consistent(params: dict):
            for i in range(1, len(params)):
                key = "@" + str(i)
                if key not in params:
                    return False
            return True

        # Build ordered parameter list
        def build_params(params_dict: dict):
            params = list()
            for i in range(1, len(params_dict)):
                key = "@" + str(i)
                params.append(params_dict[key])
            return params

        # When enter expression block
        if phrase.phrase_subclass == PhraseSubclass.expression:
            # Add signature for expression
            self._expr_id = self.lang_dict.add_signature(phrase.keyword.value, SignatureType.expression, "", 0)
            # If this is first expression - create template
            if self._expr_params is None:
                self._expr_params = dict()
                self._expr_params.update({"@": TokenClass.num})
                self._expr_name = phrase.keyword.value
            else:
                # Parameter numbers should be consistent
                if not is_params_consistent(self._expr_params):
                    raise InterpretationError(
                        PeaceError(f"Parameters in {self._expr_name} not consistent.",
                                   ErrorType.parameter_error))
                # Update expression signature
                else:
                    self.lang_dict.get_signature(self._expr_id).update_params(build_params(self._expr_params))
                self._expr_params.clear()
                self._expr_params.update({"@": TokenClass.num})
                self._expr_name = phrase.keyword.value

        # When enter body
        elif phrase.phrase_subclass == PhraseSubclass.body:
            # If above body was expression declaration
            if self._expr_params is not None:
                # Parameter numbers should be consistent
                if not is_params_consistent(self._expr_params):
                    raise InterpretationError(
                        PeaceError(f"Parameters in {self._expr_name} not consistent.",
                                   ErrorType.parameter_error))
                # Update expression signature
                else:
                    self.lang_dict.get_signature(self._expr_id).update_params(build_params(self._expr_params))
                # TODO: is this should be here?
                self._expr_params.clear()
                self._expr_name = phrase.keyword.value
