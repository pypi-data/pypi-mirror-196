from tsstp.datatemplate import DataTemplate

def test_search():
    search_template1 = """
    {{ key }} = {{ value }}
    """

    basepath = 'D:\\workspace\\MDI\\datatemplate\\test\\testdata\\'
    text_file = basepath + 'text_file.txt'
    incar = basepath + 'INCAR'
    parser = DataTemplate(search_template1, incar)
    result = parser.search()
    print(f'--result:{result}')

test_search()