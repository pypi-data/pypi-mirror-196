from pprint import pprint

from tsstp.datatemplate import DataTemplate

def test_match():
    match_template1 = """
    loop
    {{ key }} = {{ value }}
    {{ key1 }} = {{ value1 }}
    {{ key2 }} = {{ value2 }}
    end
    """

    final_energy = """
    Free energy of the ion-electron system (eV)
    {{ separator1 }} ~ n
    alpha Z PSCENC = {{ PSCENC }}
    Ewald energy TEWEN  =  {{ TEWEN }}
    -Hartree energ DENC = {{ DENC }}
    -exchange EXHF = {{ EXHF }}
    -V(xc)+E(xc)  XCENC  = {{ XCENC }}
    PAW double counting  =  {{ PAW }}
    entropy T*S EENTRO = {{ EENTRO }}
    eigenvalues  EBANDS =  {{ EBANDS }}
    atomic energy  EATOM  = {{ EATOM }}
    Solvation  Ediel_sol  = {{ Ediel_sol }}
    {{ separator2 }} ~ n
    free energy  TOTEN  =  {{ TOTEN }} eV
    energy without entropy =  {{ entropy }} energy(sigma->0) =  {{ energy }} 
    """
    basepath = 'D:\\workspace\\MDI\\datatemplate\\test\\testdata\\'
    text_file = basepath + 'text_file.txt'
    outcar = basepath + 'OUTCAR'
    parser = DataTemplate(final_energy, outcar)

    result = parser.match()
    print(f'--result:{result}')

test_match()