import traceback

from tsstp.template_parser import StringModel
from tsstp.internal_ds import SymbolNode


def match(string: StringModel, token: list) -> list[SymbolNode]:
    """
    basic string statement .
    match and extract data from token list with string model
    :param string: string model which represented by dataclass.
    :param token:  list of tokens.
    :return: list of nested SymbolsNodes.
    """
    symbol_list = []

    first_element = string.strlist[0]
    # template string list
    match_list = string.strlist
    # data list
    token_value = [token.value for token in token]
    try:
        # 　whether the template string matches the data(sub list of token list)
        index = token_value.index(first_element)
        is_sub = match_list == token_value[index:index + len(match_list)]
    except Exception as e:
        is_sub = None
        traceback.print_exc()
    if is_sub:
        value = ' '.join(match_list)
    else:
        raise ValueError('String match error!')

    symbol = SymbolNode(type='string', key=value)
    symbol_list.append(symbol)

    return symbol_list