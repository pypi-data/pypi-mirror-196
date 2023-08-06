# -*- coding: utf-8 -*-
"""Semantic model class to hold the results of template parser.

Data classes that hold the parsing results of various syntax rules such as
loop statements, if statements, etc.A template string corresponds to a semantic
model class, which consists of basic syntax rules.

"""
import traceback

from dataclasses import dataclass, field
from typing import List

@dataclass
class TemplateModel:
    variable: str
    elements_number: str
    filter: str = None
    indicator: str = None


@dataclass
class StringModel:
    strlist: List[str] = field(default_factory=list)

    def search(self, key: str):
        liststr = ''.join(self.strlist)
        index = liststr.find(key)

        return index

    def add(self, string: str):
        self.strlist.append(string)

    def get_string(self):
        return ' '.join(self.strlist)

    def get_no_space_string(self):
        return ''.join(self.strlist)


@dataclass
class StringTemplateModel:
    string: StringModel
    template: TemplateModel

    def get_string(self):
        return self.string.get_string()

    def get_no_space_string(self):
        return self.get_string().replace(' ','')

@dataclass
class MultiTemplateModel:
    models: List[StringModel or TemplateModel] = field(default_factory=list)

    def has_string(self):
        flag = False
        for ele in self.models:
            if isinstance(ele,StringModel):
                flag = True

        return flag

    def get_string(self):
        if self.has_string():
            for ele in self.models:
                if isinstance(ele, StringModel):
                    return ele.get_string()

    def get_no_space_string(self):
        return self.get_string().replace(' ', '')

@dataclass
class LoopModel:
    loop_num: str
    stmt: List[TemplateModel or StringModel or StringTemplateModel
                 or MultiTemplateModel or 'LoopModel'] = field(default_factory=list)


@dataclass
class IfModel:
    condition: str
    stmt: List[TemplateModel or StringModel or StringTemplateModel
                 or LoopModel] = field(default_factory=list)
    else_stmt: List[TemplateModel or StringModel or StringTemplateModel
                 or LoopModel] = field(default_factory=list)


@dataclass
class SemanticModel:
    models: List[TemplateModel or StringModel or StringTemplateModel
                 or LoopModel or IfModel] = field(default_factory=list)
    model_length: int = 0

    def add_model(self, model):
        try:
            self.models.append(model)
            self.model_length += 1
        except Exception as e:
            traceback.print_exc()

    def get_row_number(self):
        pass

    def get_elements_number(self):
        pass