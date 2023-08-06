from tsstp.semantic_model import StringModel, StringTemplateModel
from tsstp.template_parser import TemplateParser

def test_template_parser():
    template = r'''
    sasa = {{ sasa }}
    {{ var | _string_ | func}} ~ 3
    string saws a
    POSCAR\(4)
    str = str
    {{ name | func }} ~ n
    this is string
    sasa = {{ sasa }}
    {{ num }} ~ 3
    {% if you  %}
        {{ var | _string_ }} ~ 4
       {% else %}
         definition = {{ var }}
    {% endif %}
    {% if con  %}
        {{ var | _string_ }} ~ 4
    {% endif %}
    {% loop name %}
        {{ aaa }}
    {% endloop %}
    '''
    template1 = '''
    {{ head_h }}
    poscar
    {{ Scaling }}
    {{ Coordinates1 }} ~ head_h
    {{ Coordinates2 }} ~ 3
    {{ Coordinates3 }} ~ 3
    {{ elements }} ~ n
    {{ elements_num }} ~ n
    Direct configuration= {{ number }}
    '''
    nest_template = '''
    {% if con  %}
        {{ var | _string_ }} ~ 4
        {{ name | _string_ }} ~ 4
    {% else %}
        {{ else_name}} ~ 4
    {% endif %}
    '''

    multi_templates = '''
    {{ x }} ~ 2 {{ y }} ~ 3  {{ z }}  ~ n
    '''

    funtion_template = """
    {{ x }} ~ 3
    {{ y }} ~ sum(x)
    """

    filter_template = """
    {{ value | toInt }} ~ n
    """

    ts_template = """
    energy without entropy = {{ sada }} ~ n
    """
    ts_template1 = """
    {{ line1 }} ~ n
    entropy = {{ sada }} ~ n
    """

    final_energy = """
    Free energy of the ion-electron system (eV)
    {{ line1}} ~ n
    {{ line2}} ~ n
    {{ line3}} ~ n
    {{ line4}} ~ n
    {{ line5}} ~ n
    {{ line6}} ~ n
    {{ line7}} ~ n
    {{ line8}} ~ n
    {{ line9}} ~ n
    {{ line10}} ~ n
    {{ line11}} ~ n
    {{ line12}} ~ n
    {{ line13}} ~ n
    energy without entropy = {{ sada }} ~ n
    """

    template_obj = TemplateParser(final_energy)
    template_AST = template_obj.get_AST()
    template_dict = template_obj.get_dict_AST()
    semantic_model = template_obj.get_semantic_model()
    start_model = semantic_model.models[0]
    end_model = semantic_model.models[-1]
    print(f"start:{start_model},end:{end_model}")
    print(f"type end model{type(end_model)}")
    print(f"{isinstance(start_model, (StringModel, StringTemplateModel))},{isinstance(end_model, (StringModel, StringTemplateModel))}")

    for model in semantic_model.models:
        print(f"model:{model}")

    print("template_AST", template_AST)
    print("template_dict", template_dict)
    print('semantic_model:', semantic_model)
    print('models:', semantic_model.models)

test_template_parser()