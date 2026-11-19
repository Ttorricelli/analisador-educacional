from scanner import analisar_lexico
from parser import analisar_sintatico

def analisar(codigo):
    lexico = analisar_lexico(codigo)
    assert lexico['sucesso']
    return analisar_sintatico(lexico['tokens'])

def test_aceita_atribuicao_e_print():
    r = analisar('x = 10 + 5\nprint(x)')
    assert r['sucesso'] is True
    assert [n['tipo'] for n in r['ast']['filhos']] == ['Atribuicao', 'Chamada']

def test_precedencia_multiplicacao_antes_da_soma():
    r = analisar('resultado = 2 + 3 * 4')
    expr = r['ast']['filhos'][0]['filhos'][0]
    assert expr['tipo'] == 'Binaria' and expr['valor'] == '+'
    assert expr['filhos'][1]['valor'] == '*'

def test_aceita_parenteses():
    assert analisar('x = (2 + 3) * 4')['sucesso'] is True

def test_rejeita_operador_sem_operando():
    r = analisar('x = 10 +')
    assert r['sucesso'] is False
    assert r['erros'][0]['tipo'] == 'ERRO_SINTATICO'

def test_rejeita_print_sem_fechamento():
    assert analisar('print(x')['sucesso'] is False

def test_rejeita_atribuicao_sem_valor():
    assert analisar('x =')['sucesso'] is False

def test_rejeita_tokens_extras():
    assert analisar('x = 1 2')['sucesso'] is False
