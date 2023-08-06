from tsstp.template_parser import TemplateModel
from tsstp.internal_ds import SymbolNode
from tsstp.utils import get_loop_number,extract_func


def match(template: TemplateModel, token: list) -> list[SymbolNode]:
    """
    basic template statement such as {{ variable }} ~ number.
    match and extract data from token list with template model.
    :param template: template model which represented by dataclass.
    :param token:  list of tokens.
    :return: list of nested SymbolsNodes.
    """
    symbol_list = []

    # elements number store in string
    # print(f'matcher loop:{template.elements_number}')
    element_number = get_loop_number(template.elements_number)
    # print(f'matcher loop number:{element_number}')

    # template variable name
    variable_name = template.variable
    # symbol node in Symbol table
    symbol = SymbolNode(type='template', key=variable_name)

    #todo 　Whether an indicator is used
    indicator = template.indicator
    if indicator:
        indicator_flag = indicator
    else:
        indicator_flag = None

    # get filter
    filter = extract_func(template.filter)

    # whether symbol table contain variable
    from tsstp import datatemplate as dt

    variable_exist = dt.DataTemplate.symbol_table.is_exist(variable_name)
    if variable_exist:
        raise ValueError(f"The variable name:{variable_name} is existed")

    # Lex of input data adn return token list, token.type is type of value,token.value is the value
    token_value = [token.value for token in token]

    if element_number == 1:
        # 如果匹配元素数目为1的话 直接拼接整个token list中的值(带符号和数字的字符串,解析的时候分割成一个字符串列表,这里需要进行拼接)
        value = ''.join(token_value)
        symbol.value = value
    elif isinstance(element_number, int) and element_number > 1:
        # elements number > 1

        if len(token_value) == element_number:
            symbol.value = token_value[0:element_number]
        else:
            raise ValueError("Error in the number of elements to match!")

    elif element_number == 'n':
        # elements number is n,math all token value
        symbol.value = token_value
    elif isinstance(element_number, str):
        # element number quote previous variable name
        if dt.DataTemplate.symbol_table.is_exist(element_number):
            node = dt.DataTemplate.symbol_table.lookup_template(element_number)
            # Number of elements to be matched
            number = int(node.value)
            symbol.value = token_value[0:number]
        else:
            raise ValueError('Variable name does not exist')
    else:
        raise ValueError('Number of elements error')

    symbol_list.append(symbol)
    if filter:
        filter(symbol_list)
    # print("symbol_list:", symbol_list)
    return symbol_list
