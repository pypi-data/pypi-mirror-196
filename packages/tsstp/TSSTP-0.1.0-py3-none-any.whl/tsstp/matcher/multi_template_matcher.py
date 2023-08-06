from tsstp.template_parser import TemplateModel, MultiTemplateModel
from tsstp.internal_ds import SymbolNode
from tsstp.matcher import template_matcher
from tsstp.utils import get_loop_number

def match(muti_temp_model: MultiTemplateModel, token: list) -> list[SymbolNode]:
    """
    basic multi templates statement such as {{ x }} str {{ y }} ~ 3  {{ z }} ~ n
    match and extract data from token list with MultiTemplateModel model.
    :param template_string: MultiTemplateModel model which represented by dataclass.
    :param token:  list of tokens.
    :return: list of nested SymbolsNodes.
    """

    index = 0
    symbol_list = []
    for mod in muti_temp_model.models:
        if isinstance(mod, TemplateModel):
            # template match
            ele_num = get_loop_number(mod.elements_number)
            if ele_num == 'n':
                symbol = template_matcher.match(mod, token[index])
            else:
                symbol = template_matcher.match(mod, token[index:index + ele_num])
            index += ele_num
            symbol_list.extend(symbol)

        else:
            # string match
            for str in mod.strlist:
                mod_str_len = len(str.replace(' ',''))
                tok_str_len = 0

                # length match
                str_index = 0
                for ele in token[index:]:
                    if tok_str_len == mod_str_len:
                        break
                    elif tok_str_len > mod_str_len:
                        raise ValueError(f"{str} match {ele} error!")
                    else:
                        tok_str_len += len(ele.value)
                    str_index += 1

                if str == ''.join([ tok.value for tok in token[index:index +str_index]]):
                    index += str_index
                else:
                    raise ValueError(f"{str} matched error!")

    return symbol_list