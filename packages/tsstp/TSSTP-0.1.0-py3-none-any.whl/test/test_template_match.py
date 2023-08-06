from pprint import pprint

from tsstp.datatemplate import DataTemplate

def test_template_match():
    template_data = """
     POSCAR\(4)
     3                              
    1.00000000000000     
      8.3879995346000005    0.0000000000000000    0.0000000000000000
      0.0000000000000000    8.3879995346000005    0.0000000000000000
      0.0000000000000000    0.0000000000000000   23.0000000000000000
    O    Fe   Ni
     50    33     1
     Direct configuration= 1
     """

    template1 = """
     {{ head }}
     {{ loop_num }}
     {{ Scaling }} 
     {{ Coordinates1 }} ~ loop_num
     {{ Coordinates2 }} 
     {{ Coordinates3 }} 
     {{ elements }}
     {{ elements_num }} 
     Direct configuration= {{ number }}
     """

    multi_template1 = """
    {{ x }} ~ 2 {{ y }} ~ 2 {{ z }} ~ 2
    """

    multi_template2 = """
    {{ x1 }} ~ 1 st-r {{ y1 }} ~ 1 st/r {{ z1 }} ~ 1
    """

    multi_template3 = """
    free energy  TOTEN  =  {{ TOTEN }} eV
    """

    multi_temp_data1 = """
    1 11 2 22 3 33
    """

    multi_temp_data2 = """
    1 st-r  2 st/r 3
    """

    multi_temp_data3 = """
    free energy    TOTEN  =      -565.56798583 eV
    """

    parser1 = DataTemplate(multi_template3, multi_temp_data3)
    parser1.parse()
    result1 = parser1.result(format='json')
    print(result1)

    parser2 = DataTemplate(multi_template1, multi_temp_data1)
    parser2.parse()
    result2 = parser2.result(format='xml')
    print(result2)

test_template_match()