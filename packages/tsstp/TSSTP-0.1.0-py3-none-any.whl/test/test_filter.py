from tsstp.datatemplate import DataTemplate


def test_filter():
    funtion_template1 = """
    {{ x }} ~ 3
    {{ y }} ~ sum(x)
    """

    funtion_template2 = """
    {{ x }} ~ 3
    {% loop sum(x) %}
        {{ y }}
    {% endloop %}
    """

    funtion_data1 = """
    1 2 3
    1 2 3 4 5 6
    """

    funtion_data2 = """
    1 2 3
    1
    2
    3
    4
    5
    666
    """
    template_int_data = """
    1 2 3 4 5
    """
    template_int = """
    {{ value | toInt }} ~ n
    """

    parser = DataTemplate(funtion_template2, funtion_data2)
    parser.parse()
    result = parser.result()
    print(f'--result:{result}')