"""Testes unitários das regras de validação."""
import pytest

from validacao import LIMITE_CARACTERES, MSG_SO_ESPACOS, MSG_VAZIO, validar_codigo


def test_codigo_valido_nao_gera_erro():
    assert validar_codigo("x = 10") is None


def test_vazio():
    erro = validar_codigo("")
    assert erro.tipo == "entrada_vazia"
    assert erro.mensagem == MSG_VAZIO
    assert erro.status_http == 422


@pytest.mark.parametrize("texto", [" ", "   ", "\n", "\t", " \n\t \r\n"])
def test_somente_espacos(texto):
    erro = validar_codigo(texto)
    assert erro.tipo == "entrada_somente_espacos"
    assert erro.mensagem == MSG_SO_ESPACOS


def test_limite_exato_e_aceito():
    assert validar_codigo("a" * LIMITE_CARACTERES) is None


def test_acima_do_limite_e_rejeitado():
    erro = validar_codigo("a" * (LIMITE_CARACTERES + 1))
    assert erro.tipo == "entrada_muito_grande"
    assert erro.status_http == 413


def test_codigo_com_erro_de_sintaxe_e_aceito_nesta_etapa():
    # O sistema não pode presumir que o código é válido nem rejeitá-lo por isso.
    assert validar_codigo("x = 10 +\nprint(x") is None
