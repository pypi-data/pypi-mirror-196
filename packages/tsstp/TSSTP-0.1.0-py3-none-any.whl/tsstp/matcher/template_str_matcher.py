from tsstp.template_parser import StringTemplateModel
from tsstp.internal_ds import SymbolNode

from tsstp.matcher import string_matcher
from tsstp.matcher import template_matcher
from tsstp.utils import str_list_compare


def match(template_string: StringTemplateModel, token: list) -> list[SymbolNode]:
    """
    basic StringTemplate statement such as String = {{ variable }}
    match and extract data from token list with StringTemplateModel model.
    :param template_string: StringTemplate model which represented by dataclass.
    :param token:  list of tokens.
    :return: list of nested SymbolsNodes.
    """
    symbol_list = []
    string_model = template_string.string
    template_model = template_string.template
    src_str = string_model.strlist
    target_str = [tok.value for tok in token]

    str_compare = str_list_compare(src_str, target_str)
    # if string matched, split token list into string token list and template token list
    if str_compare:
        str_token = token[str_compare[0]:str_compare[1]]
        template_token = token[str_compare[1]:]
    else:
        raise ValueError('String does not matched!')

    string_symbol = string_matcher.match(string_model, str_token)
    template_symbol = template_matcher.match(template_model, template_token)
    symbol_list.extend(string_symbol)
    symbol_list.extend(template_symbol)

    return symbol_list