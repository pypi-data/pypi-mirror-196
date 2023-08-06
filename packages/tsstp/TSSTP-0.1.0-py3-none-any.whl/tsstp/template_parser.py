# -*- coding: utf-8 -*-
import traceback

from lark import Lark, Transformer, v_args, Token
from tsstp.semantic_model import SemanticModel, TemplateModel, StringModel, StringTemplateModel, \
    MultiTemplateModel, LoopModel, IfModel


class TemplateParser:
    '''
    Classes for parsing template string.

    Parsing the template string, storing it as a dictionary in an intermediate form,
    and then transforming it into semantic model classes.

    :param template_text: Template as text.

    Examples:
        template_obj = TemplateParser(template_string)
        template_AST = template_obj.get_AST()
        template_dict = template_obj.get_dict_AST()
        semantic_model = template_obj.get_semantic_model()
    '''

    def __init__(self, template_text):
        self.template_text = template_text

    def get_AST(self):
        template_parser = Lark.open('template_grammar.lark', rel_to=__file__)
        try:
            template_AST = template_parser.parse(self.template_text)
        except Exception as e:
            template_AST = None
            traceback.print_exc()

        return template_AST

    def get_dict_AST(self):
        template_dict = TemplateTransformer().transform(self.get_AST())

        return template_dict

    def get_semantic_model(self):
        ''' convert parsed template dict to semantic models '''
        semantic_model = SemanticModel()
        templates = self.get_dict_AST()

        def choose_model(model_dict: dict):
            if 'loop_template' in model_dict:
                return template_init(model_dict)
            elif 'template_string' in model_dict:
                return template_string_init(model_dict)
            elif 'string' in model_dict:
                return string_init(model_dict)
            elif 'if' in model_dict:
                return if_init(model_dict)
            elif 'loop' in model_dict:
                return loop_init(model_dict)
            elif 'multi_template' in model_dict:
                return muti_template_init(model_dict)
            else:
                raise ValueError("parsed dict error!")

        def template_init(temp_dict: dict):
            '''
            Instantiating template model
            :param temp_dict: example such as:{'loop_template': {'template': {'name': 'var', 'indicator': 'string', 'function': 'func'}, 'loop_num': '3'}}
            '''
            value = temp_dict['loop_template'].get('template')
            model = TemplateModel(variable=value.get('name'),
                                  elements_number=temp_dict['loop_template'].get('loop_num'),
                                  indicator=value.get('indicator'),
                                  filter=value.get('filter'))
            return model

        def string_init(str_dict: dict):
            '''
            Instantiating string model
            :param str_dict: example such as:{'string': ['POSCAR', '\\', '(', '4', ')']}
            '''
            value = str_dict.get('string')
            model = StringModel(value)

            return model

        def muti_template_init(temp_dict: dict):
            '''
            Instantiating MultiTemplateModel model
            :param temp_list: example such as:{{ x }} {{ y }} ~ 3 string {{ z }}
            '''
            models = temp_dict.get('multi_template')
            model_list = [choose_model(m) for m in models]
            model = MultiTemplateModel(models=model_list)

            return model

        def if_init(if_dict: dict):
            '''
            Instantiating if model
            :param if_dict: example such as: {'if': {'condition': 'you', 'stmt': {'loop_template': {'template': {'name': 'var', 'indicator': 'string'}, 'loop_num': '4'}},
            'else_stmt': {'template_string': {'string': ['definition', '='], 'template': {'name': 'var'}}}}},
            '''
            value = if_dict.get('if')
            condition = value.get('condition')
            stmt = value.get('stmt')
            else_stmt = value.get('else_stmt')

            stmt_model = [choose_model(model) for model in stmt]
            model = IfModel(condition=condition, stmt=stmt_model)
            if else_stmt:
                model.else_stmt = [choose_model(model) for model in else_stmt]

            return model

        def loop_init(loop_dict: dict):
            '''
            Instantiating loop model
            :param loop_dict: example such as:{'loop': {'iter_num': 'name', 'stmt': {'loop_template': {'template': {'name': 'aaa'}, 'loop_num': '1'}}}}
            '''
            value = loop_dict.get('loop')
            iter_num = value.get('iter_num')
            stmt = value.get('stmt')
            model = LoopModel(iter_num)
            model.stmt = [choose_model(model) for model in stmt]

            return model

        def template_string_init(temstr_dict: dict):
            '''
            Instantiating template string model
            :param template_string_init: example such as:{'template_string': {'string': ['sasa', '='], 'loop_template': {'template': {'name': 'sasa'}, 'loop_num': '1'}}}
            '''
            value = temstr_dict.get('template_string')
            string_dict = dict()
            string_dict['string'] = value.get('string')
            str_model = string_init(string_dict)

            stmt_dict = dict()
            stmt_dict['loop_template'] = value.get('loop_template')
            stmt_model = template_init(stmt_dict)

            model = StringTemplateModel(string=str_model, template=stmt_model)

            return model

        for model_dict in templates:
            # 遍历字典转换并将其转化为语义模型
            model = choose_model(model_dict)
            semantic_model.add_model(model)

        return semantic_model


@v_args(inline=True)
class TemplateTransformer(Transformer):
    """
    The template transformer class, Inheritance of T class.

    Iterate through the AST(abstract syntax tree) and convert
    the internal structure of the AST into dict.

    """

    def start(self, *args):
        element_list = []
        for ele in args:
            if isinstance(ele, Token):
                continue
            else:
                element_list.extend(list(ele))

        return element_list

    def unit(self, *args):

        return args

    def multi_template(self, *args):
        tem_dict = dict()
        tem_dict['multi_template'] = [arg for arg in args]
        return tem_dict

    # loop transform
    def loop(self, *args):
        tem_dict = dict()
        tem_dict['loop'] = {}
        for d in args:
            if isinstance(d, dict):
                tem_dict['loop'].update(d)

        return tem_dict

    def iter_num(self, arg):
        tem_dict = dict()
        if len(arg) == 1:
            tem_dict['iter_num'] = arg.value
        else:
            tem_dict['iter_num'] = (arg[0].value, arg[1].value)

        return tem_dict

    # if transform
    def if_stmt(self, *args):
        tem_dict = dict()
        tem_dict['if'] = {}
        for d in args:
            if isinstance(d, dict):
                tem_dict['if'].update(d)

        return tem_dict

    def condition(self, *args):
        tem_dict = dict()
        tem_dict['condition'] = ' '.join([arg.value for arg in args])

        return tem_dict

    def statement(self, *args):
        tem_dict = dict()
        tem_dict['stmt'] = {}
        element_list = list()
        for ele in args:
            if isinstance(ele, Token):
                continue
            else:
                element_list.extend(list(ele))
        tem_dict['stmt'] = element_list

        return tem_dict

    def else_statement(self, *args):
        tem_dict = dict()
        tem_dict['else_stmt'] = {}
        element_list = list()
        for ele in args:
            if isinstance(ele, Token):
                continue
            else:
                element_list.extend(list(ele))
        tem_dict['else_stmt'] = element_list

        return tem_dict

    # template_string transform
    def template_string(self, *args):
        tem_dict = dict()
        tem_dict['template_string'] = {}
        for t in args:
            tem_dict['template_string'].update(t)

        return tem_dict

    def string(self, *args):
        tem_dict = dict()
        tem_dict['string'] = args[0]

        return tem_dict

    def const_string(self, *args):
        res = [t.value for t in args]

        return res

    def symbol_string(self, *args):
        res = [t.value for t in args]

        return res

    # loop_template transform
    def loop_template(self, *args):
        tem_dict = dict()
        tem_dict['loop_template'] = {}
        for i in args:
            if isinstance(i, dict):
                tem_dict['loop_template'].update(i)

        if tem_dict['loop_template'].get('template'):
            tem_dict['loop_template'].setdefault('loop_num', '1')

        return tem_dict

    def loop_num(self, *args):
        tem_dict = dict()
        if args:
            if isinstance(args[0], tuple):
                tem_dict['loop_num'] = (args[0][0].value, args[0][1].value)
            else:
                tem_dict['loop_num'] = args[0].value
        else:
            tem_dict['loop_num'] = 'n'

        return tem_dict

    def template(self, *args):
        tem_dict = dict()
        tem_dict['template'] = {}
        for i in args:
            tem_dict['template'].update(i)

        return tem_dict

    # var transform
    def var(self, *args):
        tem_dict = dict()
        for i in args:
            tem_dict.update(i)

        return tem_dict

    def var_name(self, *args):
        tem_dict = dict()
        tem_dict['name'] = [i.value for i in args][0]

        return tem_dict

    def indicator(self, *args):
        tem_dict = dict()
        tem_dict['indicator'] = [i.value for i in args][0]

        return tem_dict

    def filter(self, *args):
        tem_dict = dict()
        tem_dict['filter'] = [i.value for i in args][0]

        return tem_dict

    def function(self, *args):
        return args

