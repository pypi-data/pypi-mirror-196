import re

from tsstp.template_parser import IfModel
from tsstp.internal_ds import SymbolNode
from tsstp.extract_symbol import muti_unit_extract


def match(if_model: IfModel, token: list) -> list[SymbolNode]:
    """
    Compound statements nested basic statement.
    match and extract data from token list with IfModel model.
    :param if_model:  IfModel which represented by dataclass.
    :param token:  list of tokens.
    :return: list of nested SymbolsNodes.
    """

    stmts = get_if_stmt(if_model)
    # print("if exec stmts:", stmts)
    symbol = muti_unit_extract(stmts, token)

    return symbol


def get_if_stmt(model: IfModel) -> list:
    # Get the statements to be executed in if model which contain condition,stmt and else_stmt
    condition_str = model.condition
    stmt = model.stmt
    else_stmt = model.else_stmt
    # print("if model:", model)
    from tsstp import datatemplate as dt

    def is_conditon(condition: str) -> bool:
        # whether the condition statement is true or false
        global con_flag
        con_list = condition.split(' ')
        # print("con list:", con_list)
        if len(con_list) == 1:
            con_flag = dt.DataTemplate.symbol_table.value_exist(condition)
        else:
            # get variable name and value in condition string
            variable_name = re.search(r'[a-zA-Z]\w{1,}', condition).group()
            # print("variable_name:", variable_name)
            variable_node = dt.DataTemplate.symbol_table.lookup_template(variable_name)
            variable_value = variable_node.value
            # execute condition string and decide whether the condition is true or false
            exec(f'{variable_name}={variable_value}')
            con_flag = eval(condition)

        return con_flag

    con_exist = is_conditon(condition_str)
    if con_exist:
        # condition is true, return stmt
        return stmt
    else:
        # condition is false, return else_stmt
        # list of else_stmts can be empty
        return else_stmt