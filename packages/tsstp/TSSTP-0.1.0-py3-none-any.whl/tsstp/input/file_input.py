# -*- coding:utf-8 -*-
import os
import traceback

from lark import Lark, Transformer, v_args, Token, Tree

class Input:
    """
    Input module, which reads the input parsed data and does lexical analysis to convert it into token list.

    :param path:Data passed in as file path.
    :param string:Data passed in as a string.

    Example:
        filepath = 'D:\\data\\file\\text.txt'
        data = Input(path=filepath)
        token_list = data.parse()

        file_string = 'str1 str2 str3 x y z 1 2 3'
        data = Input(data=file_string)
        token_list = data.parse()
    """

    def __init__(self, path='', string=''):
        self.filepath = path
        # normal String to raw String
        self.data = r'{}'.format(string)

    def get_content(self):
        content = ''
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r',encoding='utf-8') as file_obj:
                    content = file_obj.read()
            except Exception as e:
                traceback.print_exc()
        elif self.data:
            content = self.data
        else:
            raise ValueError("Input error!")

        return content

    def parse(self, input_data=''):
        token_list = []
        parser = Lark.open('token_grammar.lark', rel_to=__file__)

        if input_data:

            data_token = parser.parse(input_data)
        else:
            data_token = parser.parse(self.get_content())

        for ele in data_token.children:
            if isinstance(ele, Tree):
                token_list.append(ele.children)

        return token_list


def search_muti_lines(source: str, start_string: str, end_string: str):
    """Search for the given string in file and return lines between start and end"""
    list_of_results = []
    result = []

    append_flag = False
    for index,line in enumerate(source.splitlines()):
        # Starting line data
        line_string = line.replace(' ','')
        if start_string in line_string or start_string == line_string:
            # if line start with start_string, add the data to result
            append_flag = True
        if append_flag:
            # if append_flag is true, keep adding data
            result.append(line.strip())
        if append_flag and (end_string in line_string or end_string == line_string):
            # if line start with end_string,
            append_flag = False
            list_of_results.append('\n'.join(result)+'\n')
            result = []
    # print(f"list_of_results:{list_of_results}")
    return list_of_results


def search_lines(source: str, parsing_info:list):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    list_of_results = []

    def is_target(token_list:list, parsing_info:list):
        # print(f"token:{token_list}")
        value_list = [t.value for t in token_list]
        flag = True
        try:
            for ele in parsing_info:
                if isinstance(ele,str):
                    if ele == 'N' or ele =='n':
                        continue
                    else:
                        if ele not in value_list:
                            flag = False
                else:
                    continue
            element_number = 0
            first_str_index = 0
            for ele in parsing_info:
                if isinstance(ele,str):
                    if ele == 'N' or ele =='n':
                        break
                        # raise ValueError(f"template number:n can not be used this way!")
                    else:
                        if ele in value_list:
                            first_str_index = value_list.index(ele)
                            break
                else:
                    element_number += ele
            print(f"index:{first_str_index},ele_number:{element_number}")
            if first_str_index != element_number:
                flag = False
        except Exception as e:
            flag = False
            pass
        print(f"flag:{flag}")
        return flag

    for line in source.splitlines():
        line += '\n'
        line_obj = Input(string=line)
        line_token = line_obj.parse()
        if is_target(line_token[0],parsing_info):
            # If yes, then add the line number & line as a tuple in the list
            print(f"line:{line}")
            list_of_results.append(line)

    return list_of_results


if __name__ == '__main__':
    basepath = 'D:\\workspace\\MDI\\datatemplate\\semi_structure_parser\\testdata\\'
    file_path_list = [basepath + x for x in os.listdir(basepath)]

    poscar_file = basepath + 'POSCAR'
    test_data = basepath + 'text_file.txt'

    # file_obj = Input(test_data)
    # content = file_obj.get_content()
    # search_content = search_muti_lines(content,'loop','end')
    # token_list = file_obj.parse()
    # line_content = search_lines(content,"=")
    # print("line content :", line_content)

    poscar_data = '''
    POSCAR\(4)                              
       1.00000000000000     
         8.3879995346000005    0.0000000000000000    0.0000000000000000
         0.0000000000000000    8.3879995346000005    0.0000000000000000
         0.0000000000000000    0.0000000000000000   23.0000000000000000
       O    Fe   Ni
        50    33     1
    Selective dynamics
    Direct
      0.5915683032071809  0.4076348462601602  0.3236733991222093   T   T   T
      0.6870646622156227  0.3019365196287453  0.3103828207546814   T   T   T
      0.3630810210536513  0.3675710238882842  0.4462171285301444   T   T   T
      0.6312774165690974  0.6359020719110883  0.4460652700582469   T   T   T
      0.1034239149821314  0.6182630749662752  0.4443934592078488   T   T   T
      0.8884112102198707  0.3842516059121611  0.4453508619041938   T   T   T
      0.3798693812881971  0.8943751866295495  0.4442736794178238   T   T   T
      0.6138185431204929  0.1094628714447662  0.4453949264532074   T   T   T
      0.1460929563952582  0.1511753838855331  0.4495652323750344   T   T   T
      0.8481353013092298  0.8527124318740430  0.4499216601262892   T   T   T
      0.3622735022466660  0.6366474075220162  0.5337409646875285   T   T   T
      0.6304779841965802  0.3684030218642275  0.5368171582936877   T   T   T
      0.1128001793327870  0.8852245477662335  0.5437372635670031   T   T   T
      0.8854582153913581  0.1118876070999771  0.5389489857602635   T   T   T
      0.1089344200672412  0.3674780231491631  0.5405416957824908   T   T   T
      0.8828364160941208  0.6354067641796362  0.5395969860907350   T   T   T
    '''
    test_data = """
     POSCAR\(4)                              
    1.00000000000000     
      8.3879995346000005    0.0000000000000000    0.0000000000000000
      0.0000000000000000    8.3879995346000005    0.0000000000000000
      0.0000000000000000    0.0000000000000000   23.0000000000000000
    O    Fe   Ni
     50    33     1
    Direct configuration=     1
     """
    # {'string': ['CeO', '2', '-', '111', '-', 'ovac', '-', '11', 'Au']}
    # print(r'{}'.format(poscar_data))
    ne_number = """
    -0.00050255  0.99951883  0.43019119
    """
    input_obj = Input(path=poscar_file)
    token_list = input_obj.parse()
    print('token_list:',token_list[:10])
    print('len of token_list:',len(token_list))
