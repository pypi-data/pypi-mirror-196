from tsstp.template_parser import TemplateModel, StringModel, StringTemplateModel, LoopModel, MultiTemplateModel
from tsstp.internal_ds import SymbolNode
from tsstp.matcher import template_matcher as tm, string_matcher as sm, template_str_matcher as tsm, \
    multi_template_matcher as mtm
from tsstp.utils import calculate_lines, get_loop_number
from tsstp.matcher import loop_matcher


def base_unit_extract(template, token: list) -> list[SymbolNode]:
    """
    basic unit model which parse with one line data
    :param template: basic template.
    :param token:  list of tokens.
    :return: list of symbols which is  the instance of SymbolNode.
    """
    symbol_list = []

    if isinstance(template, TemplateModel):
        symbol = tm.match(template, token)
        symbol_list.extend(symbol)

    elif isinstance(template, StringModel):
        symbol = sm.match(template, token)
        symbol_list.extend(symbol)

    elif isinstance(template, StringTemplateModel):

        symbol = tsm.match(template, token)
        symbol_list.extend(symbol)

    elif isinstance(template, MultiTemplateModel):
        symbol = mtm.match(template, token)
        symbol_list.extend(symbol)

    return symbol_list


def muti_unit_extract(templates: list, token: list) -> list[SymbolNode]:
    """
    list of nested basic units model which parse with multi-line data.
    for loop and if statements nest statement.
    :param templates: list
    :param token: list of tokens.
    :return: list of SymbolNodes.
    """
    from tsstp.datatemplate import DataTemplate

    symbol_list = []
    # print("muti_tems:", templates)
    # print("muti_tokens:", token)
    row_number = 0

    for template in templates:
        # print("muti_template:", template)
        if isinstance(template, (TemplateModel, StringModel, StringTemplateModel)):
            token_list = token[row_number]
            symbol = base_unit_extract(template, token_list)
            row_number += 1
            symbol_list.extend(symbol)
            DataTemplate.symbol_table.add_list(symbol)

        elif isinstance(template, LoopModel):
            tem_list = [template]
            loop_num = template.loop_num
            loop_num = get_loop_number(loop_num)

            if loop_num == 'n':
                # the n loop statement should be the last statement
                if templates[-1] != template:
                    raise ValueError(
                        "Incorrect template grammar: n loop and there should be no subsequent statements!")
                # if loop number is n，get statement number and change token lists per loop.
                tokens = token[row_number:]
                # print("n tokens:", tokens)
                symbol = loop_matcher.match(template, tokens)
                DataTemplate.symbol_table.add_list(symbol)
                symbol_list.extend(symbol)

                break

            elif isinstance(loop_num, int):
                lines_length = calculate_lines(tem_list)
                token_list = token[row_number:row_number + lines_length]
                # print("number tokens:", token_list)
                symbol = loop_matcher.match(template, token_list)
                DataTemplate.symbol_table.add_list(symbol)
                symbol_list.extend(symbol)

            else:
                raise ValueError('Wrong loop number!')

            row_number += lines_length

        else:
            raise ValueError("Wrong templates")

    return symbol_list
