from tsstp.internal_ds import SymbolNode,SymbolTable

def test_symbolnode():
    node1 = SymbolNode('string', 'poscar', 'string')
    node2 = SymbolNode('template', 'poscar', list[1, 2, 1, 3, 4])
    node3 = SymbolNode('template', 'xdatacar', 'dhsjak')
    node4 = SymbolNode('template', 'xdatacar', 'dsdsssss')
    node5 = SymbolNode('template', 'poscar', 'dsdsssss')

    symbol_table = SymbolTable()
    symbol_table.add(node1)
    symbol_table.add(node2)
    symbol_table.add(node3)
    symbol_table.add(node4)

    print("symbol table", symbol_table)

    print("lookup", symbol_table.lookup('poscar'))
    print("lookup_template", symbol_table.lookup_template('poscar'))
    print("lookup_template", symbol_table.lookup_template('xdatacar'))
    print("lookup_str", symbol_table.lookup_str('poscar'))

test_symbolnode()