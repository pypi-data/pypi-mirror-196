import json
import os
import traceback
import importlib

import xmltodict

from tsstp.template_parser import TemplateParser
from tsstp.semantic_model import TemplateModel, StringModel, StringTemplateModel, \
    MultiTemplateModel, LoopModel, IfModel
from tsstp.internal_ds import SymbolTable
from tsstp.output.result import Output
from tsstp.input.file_input import Input, search_lines, search_muti_lines
from tsstp.matcher import  loop_matcher as lm, if_matcher as im
from tsstp.utils import calculate_lines, get_loop_number
from tsstp.extract_symbol import base_unit_extract

class DataTemplate:
    '''
    The parser system main class to load data, templates, then output final results.

    :param data: (obj) file object or OS path to text file
    :param template: (obj) file object or OS path to text file with template or template text string

    Example::

        from tsstp import DataTemplate
        parser = DataTemplate(template, template_data)
        parser.parse()
        result = parser.result(format='json')
        print(result)
    '''
    # save the extracted data
    symbol_table = SymbolTable()

    def __init__(self, template_text, data):
        self.template = template_text
        self.data = data

    def result(self,format=''):
        '''
        Method to get parsing results,results can be formatted.
        :param format:Specify the format to be returned, currently it is  xml or json.
        :return: formatted output result.

        Example::

            from tsstp import DataTemplate
            parser = DataTemplate(template, template_data)
            parser.parse()
            json_result = parser.result(format='json')
            xml_result = parser.result(format='xml')
            print(json_result)
            print(xml_result)
        '''
        dt = importlib.import_module('tsstp.datatemplate')

        template_result = dt.DataTemplate.symbol_table.template_table
        result = Output(template_result).to_json()
        if format.lower() == 'xml':
            result = Output(template_result).to_xml()
        dt.DataTemplate.symbol_table.template_table.clear()
        return result

    def parse(self, data_token='', semantic_model=''):
        '''
        main method to parse input data with semantic model which transform from template text.
        '''
        global token_list
        if not data_token and not semantic_model:
            data_token = self.data_parse()
            semantic_model = self.template_parse()
        models = semantic_model.models
        # print(f"tokens:{data_token},length:{len(data_token)},model:{models}")

        dt = importlib.import_module('tsstp.datatemplate')

        row_number = 0
        for index, model in enumerate(models):
            # print("main parser model:", model)
            if isinstance(model, (TemplateModel, StringModel, StringTemplateModel, MultiTemplateModel)):
                token_list = data_token[row_number]
                # symbol_list = self._base_tem_parse(model, token_list)
                try:
                    symbol_list = base_unit_extract(model, token_list)
                    dt.DataTemplate.symbol_table.add_list(symbol_list)
                except Exception as e:
                    print(f"{e} at line:{' '.join([t.value for t in data_token[0]])}")
                row_number += 1

            elif isinstance(model, IfModel):
                # stmts = self._get_if_stmt(model)
                from tsstp.matcher.if_matcher import get_if_stmt
                stmts = get_if_stmt(model)
                if stmts:
                    print(f'ifmodel stmt:{stmts}')
                    # lines_num = self.calculate_lines(stmts)
                else:
                    continue
                # print(f"looplength:{lines_num},loopstmts:{stmts}")

                # where ifmodel contain s loop model, which get length of token list
                has_loop = [model for model in stmts if isinstance(model, LoopModel)]
                if has_loop:
                    for loop in has_loop:
                        if loop.loop_num == 'n' or loop.loop_num == 'N':
                            token_list = data_token[row_number:]
                        else:
                            lines_num = calculate_lines(stmts)
                            token_list = data_token[row_number:row_number + lines_num]
                            row_number += lines_num
                else:
                    lines_num = calculate_lines(stmts)
                    token_list = data_token[row_number:row_number + lines_num]
                    row_number += lines_num

                # print("if token list:", token_list)
                # symbol_list = self._if_match(model, token_list)
                try:
                    symbol_list = im.match(model, token_list)
                    dt.DataTemplate.symbol_table.add_list(symbol_list)
                except Exception as e:
                    print(f"{e} at line:{' '.join([t.value for t in data_token[0]])}")

            elif isinstance(model, LoopModel):
                tem_list = [model]
                symbol_list = []
                loop_num = model.loop_num
                # loop_num = self._get_loop_number(loop_num)
                loop_num = get_loop_number(loop_num)
                if loop_num == 'n':
                    # the n loop statement should be the last statement
                    if models[-1] != model:
                        raise ValueError(
                            "Incorrect template grammar: n loop and there should be no subsequent statements!")
                    # if loop number is n，get statement number and change token lists per loop.
                    tokens = data_token[row_number:]
                    # print("n tokens:", tokens)
                    try:
                        symbol_list = lm.match(model, tokens)
                        dt.DataTemplate.symbol_table.add_list(symbol_list)
                    except Exception as e:
                        print(f"{e} at line:{' '.join([t.value for t in data_token[0]])}")
                    break

                elif isinstance(loop_num, int):
                    lines_num = calculate_lines(tem_list)

                    token_list = data_token[row_number:row_number + lines_num]
                    symbol_list = lm.match(model, token_list)
                else:
                    raise ValueError('Wrong loop number!')

                row_number += lines_num
                try:
                    dt.DataTemplate.symbol_table.add_list(symbol_list)
                except Exception as e:
                    traceback.print_exc()
            else:
                raise ValueError

    def match(self):
        '''
        method to match the data blocks that meet the template description, then parse them to get the parsed results.
        Unlike parse(), which gets all the data of a file, it gets some data blocks in the whole data by the features of the template.
        :return: result in json.

        Example::

            match_parser = DataTemplate(match_template1, text_file)
            result = match_parser.match()
            print(result)
        '''

        semantic_model = self.template_parse()
        models = semantic_model.models

        start_model = models[0]
        end_model = models[-1]
        print(f"match_models:{models}")
        print(f"start:{start_model},end:{end_model}")
        # Determine if the template meets the requirements of match method
        if isinstance(start_model, (StringModel, StringTemplateModel, MultiTemplateModel)) and \
                isinstance(end_model, (StringModel, StringTemplateModel, MultiTemplateModel)):
            start_string = start_model.get_no_space_string()
            end_string = end_model.get_no_space_string()
            print(f"start_string:{start_string},end_string:{end_string}")
        else:
            raise ValueError("invalid template text: the start and end of template line need contains string!")

        # get data ready to parse
        source_data = self.read_input_data()
        results = []

        parsing_data = search_muti_lines(source_data, start_string, end_string)
        print(f"lengh parsing_data:{len(parsing_data)}")
        for each_data in parsing_data:
            # data blank,then continue next loop
            if not each_data:
                continue
            token_list = self.data_parse(data=each_data)
            # print(f"len of line:{len(token_list)}")
            self.parse(data_token=token_list, semantic_model=semantic_model)
            template_result = DataTemplate.symbol_table.template_table
            single_result = Output(template_result).to_dict()
            results.append(single_result)
            # clear symbol_table for next parse
            DataTemplate.symbol_table.clear()

        return json.dumps(results)

    def search(self):
        '''
        method to Search for rows of data that match the template description and then parse them to get the parsed data.
        Unlike parse(), which gets all the data in the file,and match(), which gets a block of data,
        it gets some data rows in the whole data by the characteristics of the template.
        :return: result in json

        Example::

            parser = DataTemplate(search_template1, text_file)
            result = parser.search()
            print(result)
        '''
        semantic_model = self.template_parse()
        model_list = semantic_model.models[0]
        if isinstance(model_list, MultiTemplateModel):
            models = model_list.models
        else:
            models = model_list
        print(f"models:{models}")

        # Positioning strings to get data from input
        p_string = ''

        # list contain template info for get input data
        parsing_info = []
        for ele in models:
            if isinstance(ele, StringModel):
                p_string = ele.strlist[0]
                parsing_info.extend(ele.strlist)
            elif isinstance(ele, TemplateModel):
                if ele.elements_number.isdigit():
                    parsing_info.append(int(ele.elements_number))
                else:
                    parsing_info.append(ele.elements_number)
        has_str = False
        for ele in parsing_info:
            if isinstance(ele,str):
                if ele == 'N' or ele =='n':
                    continue
                else:
                    has_str = True
            else:
                continue
        if not has_str:
            raise ValueError(f'template must contain string identifier!')
        print(f"parsing_info:{parsing_info}")

        source_data = self.read_input_data()
        if p_string:
            input_data = search_lines(source_data, parsing_info)
        else:
            raise ValueError("")
        print(f"input_data:{input_data}")

        def get_data_with_tem(parsing_info: list, input_data: str):
            result = []
            index = 0
            # input_data = [x for x in input_data.split(' ') if x != '']
            input_data += '\n'
            input = Input(string=input_data)
            input_token = input.parse()
            print(f"data:{input_data},token:{input_token[0]}")

            for ele in parsing_info:
                if isinstance(ele, str):
                    if ele == 'n' or ele == 'N':
                        result.extend(input_data[index:])
                        break
                    else:
                        print(f"index:{input_data[index]};{index}")
                        result.append(input_data[index])
                        index += 1
                else:
                    result.extend(input_data[index:index + ele])
                    index += ele

            # print(f"result:{result}")
            result_str = ' '.join(result)

            return result_str + '\n'

        # splitting each row of data according to the template information
        # parsing_data = []
        # for line in input_data:
        #     parsing_data.append(get_data_with_tem(parsing_info, line))

        # print(f"parsing_data:{parsing_data}")
        results = []

        for each_data in input_data:
            each_data += '\n'
            token_list = self.data_parse(data=each_data)
            self.parse(data_token=token_list, semantic_model=semantic_model)
            template_result = DataTemplate.symbol_table.template_table
            single_result = Output(template_result).to_dict()
            results.append(single_result)
            # clear symbol_table for next parse
            DataTemplate.symbol_table.clear()

        return results

    def read_template_text(self):
        # get temaplte text from string or OS path

        if os.path.isfile(self.template):
            with open('data.txt', 'r', encoding='utf-8') as f:
                template_text = f.read()
        else:
            template_text = self.template
        return template_text

    def template_parse(self):
        '''
        parse template text and convert to semantic model.
        :return: list of semantic model.
        '''
        template = self.read_template_text()
        template_obj = TemplateParser(template)
        semantic_model = template_obj.get_semantic_model()

        return semantic_model

    def read_input_data(self):
        '''
        read data from input string or filepath.
        :return: content in file or str.
        '''
        # print(f'read data:{self.data} isfile:{os.path.isfile(self.data)}')
        if os.path.isfile(self.data):
            file_obj = Input(path=self.data)
            content = file_obj.get_content()
        else:
            input_obj = Input(string=self.data)
            content = input_obj.get_content()

        return content

    def data_parse(self, data=''):
        '''
        parse input data and convert it to list of tokens.
        :return: list of tokens.
        '''
        if data:
            file_obj = Input()
            token_list = file_obj.parse(data)
        else:
            content = self.read_input_data()
            input_obj = Input()
            token_list = input_obj.parse(content)

        return token_list

    def _indicator_match(self, indicator: str or None, token: list):
        # Check if a token list match an indicator from template

        # todo string类型和symbol类型的token应该与string类型的标识符匹配
        if indicator:
            flag = True
            for tok in token:
                if tok.type == flag:
                    continue
                else:
                    flag = False

            return flag
        else:
            return True
