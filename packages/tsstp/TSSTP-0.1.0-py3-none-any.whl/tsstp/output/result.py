import json
import xmltodict


class Output:
    """
    Output module for converting the data in the symbol table into a standard output format.
    """

    def __init__(self, symbols: list):
        self.symbol = symbols

    def to_dict(self):
        template_key = []
        template_value = []
        for sym in self.symbol:
            template_key.append(sym.key)
            template_value.append(sym.value)

        return dict(zip(template_key, template_value))

    def to_json(self):

        return json.dumps(self.to_dict())

    def to_xml(self):
        xml_format = dict()
        xml_format['result'] = self.to_dict()
        result = xmltodict.unparse(xml_format)

        return result
