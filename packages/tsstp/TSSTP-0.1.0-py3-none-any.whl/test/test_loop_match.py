from tsstp.datatemplate import DataTemplate

def test_loop_match():
    loop_data1 = """
     3
     8.3879995346000005    0.0000000000000000    0.0000000000000000
     0.0000000000000000    8.3879995346000005    0.0000000000000000
     0.0000000000000000    0.0000000000000000   23.0000000000000000
     0.0000000000000000    0.0000000000000000   23.0000000000000000
     0.0000000000000000    0.0000000000000000   23.0000000000000000
     0.0000000000000000    0.0000000000000000   23.0000000000000000
    """

    loop_data2 = """
    1 2 3
    string = 12
    4 5 6
    string = 123
    """

    loop_data3 = """
    number = 1
    1 2 3
    4 5 6
    7 8 9
    number = 2
    11 21 31
    11 21 31
    11 21 31
    """
    loop_data4 = """
    1 1 1 1 
    2 2 2 2
    3 3 3 3
    4 4 4 4
    5 5 5 5
    6 6 6 6
    """

    loop_template1 = """
    {{ loop_num }}
    {% loop 6 %}
        {{ Coordinates1 }} ~ 3
    {% endloop %}
    """

    loop_template2 = """
    {% loop 2 %}
        {{ Coordinates1 }} ~ 3
        string = {{ num }}
    {% endloop %}
    """

    loop_template3 = """
    {% loop 2 %}
        number = {{ num }}
        {% loop 3 %}
            {{ Coordinates }} ~ 3
        {% endloop %}
    {% endloop %}
    """

    loop_template4 = """
    {% loop 6 %}
        {{ row }} ~ 4
    {% endloop %}
    """
    parser = DataTemplate(loop_template3, loop_data3)
    parser.parse()
    result = parser.result()
    print(f'--result:{result}')