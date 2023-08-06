from tsstp.datatemplate import DataTemplate

def test_poscar_parse():
    poscar_template = """
    {{ head }}
    {{ Scaling }}
    {% loop 3 %}
        {{ lattice_vector }} ~ 3
    {% endloop %}
    {{ elements }} ~ 3
    {{ element_num }} ~ 3
    {{ model }}
    {% if direct %}
        {% loop sum(element_num) %}
          {{ Coordinates }} ~ 3
        {% endloop %}
    {% else %}
        {{ Direct }}
        {% loop sum(element_num) %}
          {{ Coordinates }} ~ 6
        {% endloop %}
    {% endif %}
    {% loop n %}
        {{ other }}
    {% endloop %}
    """
    basepath = 'D:\\workspace\\MDI\\datatemplate\\semi_structure_parser\\testdata\\'
    poscar_file = basepath + 'POSCAR'
    parser = DataTemplate(poscar_template, poscar_file)
    parser.parse()
    result = parser.get_result()
    print(f'--result:{result}')