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


def test_ast_guarda_posicoes_de_inicio_e_fim():
    r = analisar("resultado = 2 + 3 * 4")
    atribuicao = r["ast"]["filhos"][0]
    expressao = atribuicao["filhos"][0]
    assert atribuicao["linha"] == 1
    assert atribuicao["coluna"] == 1
    assert atribuicao["linha_fim"] == 1
    assert atribuicao["coluna_fim"] == 22
    assert expressao["tipo"] == "Binaria"
    assert expressao["filhos"][1]["valor"] == "*"


def test_erro_sintatico_informa_esperado_e_encontrado():
    r = analisar("x = 1 + )")
    erro = r["erros"][0]
    assert erro["tipo"] == "ERRO_SINTATICO"
    assert erro["esperado"] == ["literal", "identificador", "("]
    assert erro["encontrado"] == ")"


def test_parser_acumula_erros_em_linhas_independentes():
    r = analisar("x = 1 +\ny = 2 *\nz = 3")
    assert r["sucesso"] is False
    assert len(r["erros"]) == 2
    assert [e["linha"] for e in r["erros"]] == [1, 2]
    assert r["ast"] is None


def test_codigo_vazio_ou_somente_comentarios_produz_programa_vazio():
    assert analisar("# comentário")["ast"]["tipo"] == "Programa"


def test_associatividade_a_esquerda_na_subtracao():
    r = analisar("x = 10 - 3 - 2")
    expr = r["ast"]["filhos"][0]["filhos"][0]
    assert expr["valor"] == "-"
    assert expr["filhos"][0]["tipo"] == "Binaria"
    assert expr["filhos"][0]["valor"] == "-"
