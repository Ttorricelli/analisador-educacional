"""Testes dos endpoints (contrato HTTP) e de regressão da etapa 1."""
import pytest
from fastapi.testclient import TestClient

import main
from validacao import LIMITE_CARACTERES

client = TestClient(main.app)


# ---------- regressão (etapa 1) ----------
def test_hello_continua_funcionando():
    r = client.get("/api/hello")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, World! Comunicação Backend -> Frontend funcionando!"}


def test_saude():
    r = client.get("/api/saude")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_cors_preflight():
    r = client.options(
        "/api/analisar",
        headers={"Origin": "http://localhost:8080", "Access-Control-Request-Method": "POST"},
    )
    assert r.status_code == 200
    assert "access-control-allow-origin" in r.headers


# ---------- requisições válidas ----------
def test_codigo_valido():
    r = client.post("/api/analisar", json={"codigo": "x = 10\nprint(x)"})
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["recebido"] is True
    assert corpo["mensagem"] == "Código recebido com sucesso."
    assert corpo["linhas"] == 2
    assert corpo["caracteres"] == len("x = 10\nprint(x)")


def test_caracteres_especiais():
    codigo = 'texto = "ação ✓ 你好 \\n"  # comentário'
    r = client.post("/api/analisar", json={"codigo": codigo})
    assert r.status_code == 200
    assert r.json()["caracteres"] == len(codigo)


def test_codigo_com_erro_de_sintaxe_e_recebido():
    r = client.post("/api/analisar", json={"codigo": "x = 10 +\nprint(x"})
    assert r.status_code == 200
    assert r.json()["recebido"] is True


def test_limite_exato():
    r = client.post("/api/analisar", json={"codigo": "a" * LIMITE_CARACTERES})
    assert r.status_code == 200


# ---------- entradas inválidas ----------
def _assert_erro(resposta, status, tipo):
    assert resposta.status_code == status
    corpo = resposta.json()
    assert corpo["recebido"] is False
    assert corpo["erro"]["tipo"] == tipo
    assert isinstance(corpo["erro"]["mensagem"], str) and corpo["erro"]["mensagem"]


def test_codigo_vazio():
    r = client.post("/api/analisar", json={"codigo": ""})
    _assert_erro(r, 422, "entrada_vazia")
    assert r.json()["erro"]["mensagem"] == "Informe um código-fonte antes de solicitar a análise."


@pytest.mark.parametrize("texto", ["   ", "\n\n", "\t \n"])
def test_codigo_somente_espacos(texto):
    r = client.post("/api/analisar", json={"codigo": texto})
    _assert_erro(r, 422, "entrada_somente_espacos")


def test_codigo_muito_grande():
    r = client.post("/api/analisar", json={"codigo": "a" * (LIMITE_CARACTERES + 1)})
    _assert_erro(r, 413, "entrada_muito_grande")


@pytest.mark.parametrize(
    "corpo",
    [
        {},                       # campo obrigatório ausente
        {"outro": "x = 1"},       # campo com nome errado
        {"codigo": None},         # nulo
        {"codigo": 123},          # tipo errado
        {"codigo": ["x = 1"]},    # tipo errado
        [],                       # JSON de tipo errado
    ],
)
def test_requisicao_invalida(corpo):
    r = client.post("/api/analisar", json=corpo)
    _assert_erro(r, 422, "requisicao_invalida")


def test_json_malformado():
    r = client.post(
        "/api/analisar", content="{codigo: sem aspas", headers={"Content-Type": "application/json"}
    )
    _assert_erro(r, 422, "requisicao_invalida")


def test_corpo_ausente():
    r = client.post("/api/analisar")
    _assert_erro(r, 422, "requisicao_invalida")


def test_requisicao_invalida_nao_expoe_detalhes_internos():
    r = client.post("/api/analisar", json={"codigo": 123})
    texto = r.text.lower()
    for proibido in ("traceback", "pydantic", "input_value", "/app/"):
        assert proibido not in texto


def test_metodo_nao_permitido():
    assert client.get("/api/analisar").status_code == 405


# ---------- erro inesperado ----------
def test_erro_inesperado_devolve_mensagem_generica(monkeypatch):
    def quebrar(_):
        raise RuntimeError("segredo interno /app/main.py senha=123")

    monkeypatch.setattr(main, "validar_codigo", quebrar)
    seguro = TestClient(main.app, raise_server_exceptions=False)
    r = seguro.post("/api/analisar", json={"codigo": "x = 1"})
    _assert_erro(r, 500, "erro_interno")
    assert "segredo" not in r.text and "senha" not in r.text and "/app/" not in r.text
