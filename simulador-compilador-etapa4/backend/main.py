"""API do Simulador Educacional de Compiladores (subconjunto de Python).

Recebe e valida o código-fonte, executa a análise léxica e, quando não há
erros léxicos, executa a análise sintática e devolve a AST serializável.
O simulador não executa o programa nem realiza análise semântica.
"""
import logging
import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from validacao import validar_codigo
from scanner import analisar_lexico
from parser import analisar_sintatico

logger = logging.getLogger("simulador")

app = FastAPI(title="Simulador Educacional de Compiladores")

# Em produção o nginx já faz proxy de /api (mesma origem). O CORS continua
# configurável por variável de ambiente para uso em desenvolvimento.
_origens = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origens,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class AnaliseRequest(BaseModel):
    codigo: str


def _erro(status: int, tipo: str, mensagem: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"recebido": False, "erro": {"tipo": tipo, "mensagem": mensagem}},
    )


@app.exception_handler(RequestValidationError)
async def requisicao_invalida(request: Request, exc: RequestValidationError):
    # Não devolvemos exc.errors() para não expor detalhes internos.
    return _erro(
        422,
        "requisicao_invalida",
        'Requisição inválida. Envie um JSON no formato {"codigo": "<texto>"}.',
    )


@app.exception_handler(Exception)
async def erro_inesperado(request: Request, exc: Exception):
    logger.exception("Erro inesperado ao processar %s", request.url.path)
    return _erro(
        500,
        "erro_interno",
        "Ocorreu um erro inesperado ao processar o código. Tente novamente em instantes.",
    )


@app.get("/api/saude")
def saude():
    return {"status": "ok"}


@app.get("/api/hello")
def read_hello():
    # Mantido da etapa 1 (teste de regressão).
    return {"message": "Hello, World! Comunicação Backend -> Frontend funcionando!"}


@app.post("/api/analisar")
def analisar(requisicao: AnaliseRequest):
    erro = validar_codigo(requisicao.codigo)
    if erro:
        return _erro(erro.status_http, erro.tipo, erro.mensagem)

    codigo = requisicao.codigo
    resultado = analisar_lexico(codigo)
    resultado_sintatico = analisar_sintatico(resultado["tokens"]) if resultado["sucesso"] else {"sucesso": False, "erros": [], "ast": None}
    return {
        "recebido": True,
        "mensagem": "Código recebido com sucesso.",
        "linhas": len(codigo.splitlines()),
        "caracteres": len(codigo),
        **resultado,
        "analise_sintatica": resultado_sintatico,
    }
