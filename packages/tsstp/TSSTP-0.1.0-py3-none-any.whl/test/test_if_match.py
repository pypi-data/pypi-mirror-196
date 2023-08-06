from tsstp.datatemplate import DataTemplate


def test_if_match():


    if_data1 = """
    poscar
    direct
    1 2 3
    4 5 6
    7 8 9
    """
    if_data2 = """
    poscar
    selective
    1 2 3 t t t
    4 5 6 t t t
    7 8 9 t t t
    7 8 9 t t t
    7 8 9 t t t
    """
    if_data3 = """
    4
    1 2 3
    2 3 4
    3 4 3
    3 4 3
    """
    if_data4 = """
    3
    1 2 3
    2 3 4
    """

    if_template12 = """
    {{ head }}
    {{ model }}
    {% if direct %}
        {% loop n %}
          {{Coordinates}} ~ 3
        {% endloop %}
    {% else %}
        {% loop n %}
          {{Coordinates}} ~ 6
        {% endloop %}
    {% endif %}
    """

    if_template_loop = """
    {{ head }}
    {{ model }}
    {% if direct %}
        {% loop n %}
          {{Coordinates}} ~ 3
        {% endloop %}
    {% else %}
        {% loop n %}
          {{Coordinates}} ~ 6
        {% endloop %}
    {% endif %}
    """
    if_template_comp = """
    {{ num }}
    {% if num > 3 %}
        {% loop 4 %}
            {{ row }} ~ 3
        {% endloop %}
    {% else %}
        {% loop 2 %}
            {{ row }} ~ 3
        {% endloop %}
    {% endif %}
    """
    parser = DataTemplate(if_template12, if_data2)
    parser.parse()
    result = parser.result()
    print(f'--result:{result}')