import traceback
from dataclasses import dataclass, field
from typing import Any, List


# Constructing symbol tables

@dataclass
class SymbolNode:
    """The dataclass represent each node in the symbol table"""

    type: str
    key: str
    value: Any = None

    def __eq__(self, other):
        return (self.type, self.key) == (other.type, other.key)


@dataclass
class SymbolTable:
    """The dataclass hold data in symbol table, divided into two types of tables,
     one for string tables representing constants str_table,
     and the other for variable tables extracted from templates template_table
     """

    table: List[SymbolNode] = field(default_factory=list)
    template_table: List[SymbolNode] = field(default_factory=list)
    str_table: List[SymbolNode] = field(default_factory=list)

    def add(self, node: SymbolNode):
        """add symbol node into the symbol table"""

        try:
            if node.type == 'string':
                self._add_str(node)
                self.table.append(node)
            elif node.type == 'template':
                if node in self.template_table:
                    index = self.template_table.index(node)
                    table_index = self.table.index(node)
                    del self.template_table[index]
                    del self.table[table_index]
                self.template_table.append(node)
                self.table.append(node)

        except Exception as e:
            traceback.print_exc()

    def add_list(self, nodes:list):
        """add symbol node list into the symbol table"""
        for node in nodes:
            if isinstance(node, SymbolNode):
                self.add(node)
            elif isinstance(node, list):
                self.add_list(node)
            else:
                raise TypeError("SymbolTable has no such type node!")

    def _add_template(self, node: SymbolNode):
        """add template node into the symbol table"""

        self.template_table.append(node)

    def _add_str(self, node: SymbolNode):
        """add string node into the symbol table"""

        self.str_table.append(node)

    def clear(self):
        self.table.clear()
        self.template_table.clear()
        self.str_table.clear()

    def size(self):
        """Length of this symbol table"""

        return len(self.table)

    def is_exist(self, key: str):
        """Determine if a variable existed in the symbol table"""

        exist = False
        for node in self.table:
            if node.key == key:
                exist = True
            else:
                continue
        return exist

    def value_exist(self, value: str):
        """Determine if a SymbolNode's value existed in the symbol table"""

        exist = False
        for node in self.table:
            if node.value == value:
                exist = True
            else:
                continue
        return exist

    def lookup(self, key: str):
        """Search by key for the corresponding node"""

        node = [node for node in self.table if node.key == key]
        return node

    def lookup_template(self, key: str):
        """Search for the existence of the corresponding template variable by the key"""

        node = SymbolNode('template', key)
        index = self.template_table.index(node)

        return self.template_table[index]

    def lookup_str(self, key: str):
        """Search for the existence of the corresponding string constants by the key"""

        node = SymbolNode('string', key)
        index = self.str_table.index(node)

        return self.str_table[index]
