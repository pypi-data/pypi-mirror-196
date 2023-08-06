from tsstp.template_parser import IfModel, LoopModel


def calculate_lines(templates: list) -> int:
    """
    Calculate the number of rows of data needed for a corresponding model.
    :param templates: semantic models pared from template text.
    :return: lines of list of tokens.
    """
    row_number = 0
    for template in templates:
        if isinstance(template, LoopModel):
            loop_num = template.loop_num
            loop_num = get_loop_number(loop_num)
            stmt_num = calculate_lines(template.stmt)
            row_number += loop_num * stmt_num
        elif isinstance(template, IfModel):
            # Returned numbers of lines according to the judgment condition is stmt or else_stmt
            condition = template.condition
            stmt = template.stmt
            else_stmt = template.stmt

            from tsstp import datatemplate as dt
            con_exist = dt.DataTemplate.symbol_table.is_exist(condition)

            if condition and else_stmt:
                # 条件和else语句都存在
                if con_exist:
                    # condition existed, execute stmt
                    row_number += calculate_lines(stmt)
                else:
                    # condition does not existed, execute else_stmt
                    row_number += calculate_lines(else_stmt)
            elif condition and not else_stmt:
                # 条件存在,但是else语句不存在
                if con_exist:
                    row_number += calculate_lines(stmt)
                else:
                    row_number += 0
            else:
                raise ValueError('The conditional statement value is wrong!')
        else:
            # In addition to the above nested models, the lines of basic model like TemplateModel,StringModel,
            # StringTemplateModel is 1
            row_number += 1

    return row_number


def str_list_compare(src_str: list, target_str: list):
    """
    method to search string in template and string in inout data tokens.
    :param src_str: source string list.
    :param target_str: target string list.
    :return: the index of source string in target string.
    """
    first_element = src_str[0]
    start_index = target_str.index(first_element)
    is_sub = src_str == target_str[start_index:start_index + len(src_str)]
    # whether source string list is sub list of target string,return start index and final index in target string or None
    if is_sub:
        final_index = start_index + len(src_str)
        return (start_index, final_index)
    else:
        return None


def get_loop_number(loop_num: tuple or str) -> int or str:
    # get loop number used in Templatemodel or loopmodel
    if isinstance(loop_num, str):
        # element number quote previous variable name
        from tsstp import datatemplate as dt
        # print(f'symbol table{dt.DataTemplate.symbol_table}')

        if loop_num.isdigit():
            loop_num = int(loop_num)
        elif loop_num == 'n':
            loop_num = 'n'

        elif dt.DataTemplate.symbol_table.is_exist(loop_num):
            node = dt.DataTemplate.symbol_table.lookup_template(loop_num)
            # Number of elements to be matched
            loop_num = int(node.value)
        else:
            raise ValueError('Variable name does not exist')
    elif isinstance(loop_num, tuple):
        from tsstp import datatemplate as dt

        func_str = loop_num[0]
        func_arg = loop_num[1]
        func = extract_func(func_str)
        func_arg = dt.DataTemplate.symbol_table.lookup_template(func_arg)
        if func:
            if func_arg:
                func_arg_value = func_arg.value
                loop_num = func(func_arg_value)
            else:
                raise ValueError(f"invalid funtion argument:{func_arg}")

        else:
            raise ValueError(f"Invalid function name:{func_str}")
    else:
        raise ValueError(f'Invalid variable name {loop_num}references')

    return loop_num


def extract_func(func_name: str):
    # get function name
    from tsstp.filter import sum, toInt

    functions = {
        'sum': sum,
        'toInt': toInt,
    }

    return functions.get(func_name)


def merge_symbol(symbols: list):
    """
    merge same SymbolNodes which the variable name is equal.
    :param symbols: list of SymbolNodes.
    :return: list of SymbolNodes
    """

    # find Number of no duplicate nodes
    tem_node = symbols[0]
    step = 1
    for index in range(1, len(symbols)):
        if symbols[index] == tem_node:
            step = index
            break
        else:
            continue
    merge_symbol = symbols[:step]
    for symbol in merge_symbol:
        value = symbol.value
        symbol.value = [value]
    for i, symbol in enumerate(symbols[step:]):
        if symbol.type == 'template':
            merge_symbol[i % step].value.append(symbol.value)
        else:
            continue

    return merge_symbol
