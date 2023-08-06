from tsstp.template_parser import TemplateModel, StringModel, StringTemplateModel, LoopModel, \
    MultiTemplateModel
from tsstp.internal_ds import SymbolNode
from tsstp.utils import get_loop_number, calculate_lines, merge_symbol


def match(loop_model: LoopModel, token: list) -> list[SymbolNode]:
    """
    Compound statements nested basic statement.
    match and extract data from token list with loop model
    :param loop_model:  IfModel which represented by dataclass.
    :param token:  list of tokens.
    :return: list of nested SymbolsNodes.
    """
    loop_num = loop_model.loop_num
    stmt_list = loop_model.stmt
    # Number of token list lines per match
    # todo
    lines_number = calculate_lines(stmt_list)
    # print("loop model input models:", loop_model)
    # print(f"tokenlen:{len(token)},loop model tokens:{token}")
    # print("loop model lines_number:", lines_number)

    symbol_list = []
    row_number = 0
    # todo
    loop_num = get_loop_number(loop_num)

    def nest_match(stmts: list, token: list) -> list[SymbolNode]:
        # single loop match for loop model nest statements
        from tsstp.extract_symbol import base_unit_extract

        row_number = 0
        symbols = []
        for each_stmt in stmts:
            if isinstance(each_stmt, (TemplateModel, StringModel, StringTemplateModel, MultiTemplateModel)):
                token_list = token[row_number]
                symbol = base_unit_extract(each_stmt, token_list)
                row_number += 1
                symbols.extend(symbol)
            elif isinstance(each_stmt, LoopModel):
                # The nested loop statement restricts the use of a base unit representation and
                # merges the extracted data into a SymbolNode.
                tem_list = [each_stmt]
                lines_length = calculate_lines(tem_list)

                if len(each_stmt.stmt) != 1:
                    raise ValueError('The nested loop statement was set incorrectly, only 1 statement!')
                nest_stmt = each_stmt.stmt[0]

                token_list = token[row_number:row_number + lines_length]

                value_list = []
                temp_symbol = base_unit_extract(nest_stmt, token_list[0])
                symbol_name = temp_symbol[0].key
                for tok in token_list:
                    nest_symbol = base_unit_extract(nest_stmt, tok)
                    value_list.extend([sym.value for sym in nest_symbol if sym.type == 'template'])

                reshape_value = [value for row in value_list for value in row]
                symbol = SymbolNode('template', symbol_name, reshape_value)
                # print("nest loop match symbol:", symbol)
                row_number += lines_length
                symbols.append(symbol)
            else:
                raise ValueError()
        return symbols

    if loop_num == 'n':
        loop_count = 0
        while token[lines_number * loop_count:]:
            # print("n token:", token[lines_number * loop_count:lines_number * (loop_count + 1)])
            symbols = nest_match(stmt_list, token[lines_number * loop_count:lines_number * (loop_count + 1)])
            loop_count += 1
            symbol_list.extend(symbols)

    elif isinstance(loop_num, int):
        for i in range(loop_num):
            # print("int token:", token[lines_number * i:lines_number * (i + 1)])
            symbols = nest_match(stmt_list, token[lines_number * i:lines_number * (i + 1)])
            # print("symbols:", symbols)
            symbol_list.extend(symbols)
    else:
        symbols = None
    symbol_list = merge_symbol(symbol_list)
    # print("loop symbolist", symbol_list)
    # print("len(loop symbolist)", len(symbol_list))
    return symbol_list