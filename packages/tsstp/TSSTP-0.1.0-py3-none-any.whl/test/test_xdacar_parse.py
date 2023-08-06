from tsstp.datatemplate import DataTemplate

def test_xdatcar_parse():
    xdatacar_template = """
    {{ head }}
    {{ Scaling }}
    {% loop 3 %}
        {{ lattice_vector }} ~ 3
    {% endloop %}
    {{ elements }} ~ 3
    {{ element_num }} ~ 3
    {% loop n %}
        Direct configuration = {{ loop_index }}
        {% loop sum(element_num) %}
            {{ Coordinates }} ~ 3
        {% endloop %}
    {% endloop %}
    """

    basepath = 'D:\\workspace\\MDI\\datatemplate\\test\\testdata\\'
    xdatacar_file = basepath + 'XDATCAR'

    parser = DataTemplate(xdatacar_template, xdatacar_file)
    parser.parse()
    result = parser.result()
    print(f'--result:{result}')
test_xdatcar_parse()