"""Validações de entrada do código-fonte (regras isoladas, sem dependência do FastAPI)."""
from dataclasses import dataclass
from typing import Optional

LIMITE_CARACTERES = 20_000

MSG_VAZIO = "Informe um código-fonte antes de solicitar a análise."
MSG_SO_ESPACOS = (
    "O código contém apenas espaços em branco. "
    "Escreva ao menos uma instrução para solicitar a análise."
)
MSG_MUITO_GRANDE = (
    f"O código excede o limite de {LIMITE_CARACTERES} caracteres. "
    "Reduza o tamanho do programa e tente novamente."
)


@dataclass(frozen=True)
class ErroEntrada:
    """Descreve por que uma entrada foi rejeitada."""
    tipo: str
    mensagem: str
    status_http: int


def validar_codigo(codigo: str) -> Optional[ErroEntrada]:
    """Retorna None se o código pode ser processado, ou um ErroEntrada."""
    if codigo == "":
        return ErroEntrada("entrada_vazia", MSG_VAZIO, 422)
    if codigo.strip() == "":
        return ErroEntrada("entrada_somente_espacos", MSG_SO_ESPACOS, 422)
    if len(codigo) > LIMITE_CARACTERES:
        return ErroEntrada("entrada_muito_grande", MSG_MUITO_GRANDE, 413)
    return None
