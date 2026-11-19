"""Testes unitários do scanner léxico."""
from scanner import analisar_lexico


def test_identificadores_palavras_reservadas_e_posicoes():
    r = analisar_lexico("if nome_1 == 12:\n    print(nome_1)")
    assert r["sucesso"] is True
    assert [(t["tipo"], t["lexema"]) for t in r["tokens"][:5]] == [
        ("PALAVRA_RESERVADA", "if"), ("IDENTIFICADOR", "nome_1"),
        ("OPERADOR", "=="), ("LITERAL_INTEIRO", "12"), ("DELIMITADOR", ":")
    ]
    assert (r["tokens"][0]["linha"], r["tokens"][0]["coluna"]) == (1, 1)
    assert (r["tokens"][1]["linha"], r["tokens"][1]["coluna"]) == (1, 4)
    assert (r["tokens"][5]["linha"], r["tokens"][5]["coluna"]) == (2, 5)


def test_inteiros_reais_e_strings():
    r = analisar_lexico('x = 42\ny = 3.14\ns = "oi"')
    assert r["sucesso"] is True
    assert [t["tipo"] for t in r["tokens"] if t["tipo"].startswith("LITERAL")] == [
        "LITERAL_INTEIRO", "LITERAL_REAL", "LITERAL_STRING"
    ]


def test_operadores_compostos_e_delimitadores():
    r = analisar_lexico("a += 1; b != 2 and c <= 3")
    assert r["sucesso"] is True
    assert [t["lexema"] for t in r["tokens"] if t["tipo"] == "OPERADOR"] == ["+=", "!=", "<="]
    assert [t["lexema"] for t in r["tokens"] if t["tipo"] == "DELIMITADOR"] == [";",]


def test_comentarios_e_espacos_sao_ignorados():
    r = analisar_lexico("x = 1 # comentário\n  # só comentário\nprint(x)")
    assert r["sucesso"] is True
    assert [t["lexema"] for t in r["tokens"]] == ["x", "=", "1", "print", "(", "x", ")"]


def test_caractere_invalido_acumula_erro_e_continua():
    r = analisar_lexico("x = @\ny = 2$")
    assert r["sucesso"] is False
    assert [e["lexema"] for e in r["erros"]] == ["@", "$"]
    assert [(e["linha"], e["coluna"]) for e in r["erros"]] == [(1, 5), (2, 6)]
    assert "não reconhecido" in r["erros"][0]["mensagem"]
    assert any(t["lexema"] == "y" for t in r["tokens"])


def test_string_nao_terminada_e_numero_malformado():
    r = analisar_lexico('x = "sem fechar\ny = 123abc')
    assert r["sucesso"] is False
    assert len(r["erros"]) == 2
    assert "string não terminado" in r["erros"][0]["mensagem"]
    assert "numérico malformado" in r["erros"][1]["mensagem"]


def test_token_no_fim_do_arquivo_sem_quebra_de_linha():
    r = analisar_lexico("identificador")
    assert r["sucesso"] is True
    assert r["tokens"] == [{
        "tipo": "IDENTIFICADOR", "lexema": "identificador", "linha": 1, "coluna": 1
    }]


def test_codigo_vazio_espacos_e_comentario_nao_quebram_scanner():
    assert analisar_lexico("") == {"sucesso": True, "tokens": [], "erros": []}
    assert analisar_lexico(" \n\t") == {"sucesso": True, "tokens": [], "erros": []}
    assert analisar_lexico("# comentário") == {"sucesso": True, "tokens": [], "erros": []}


def test_escape_invalido_e_reportado():
    r = analisar_lexico(r's = "oi\q"')
    assert r["sucesso"] is False
    assert any("escape inválida" in e["mensagem"] for e in r["erros"])
