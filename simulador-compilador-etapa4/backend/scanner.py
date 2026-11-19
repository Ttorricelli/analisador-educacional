"""Scanner léxico para o subconjunto educacional de Python."""
from __future__ import annotations

import keyword
from dataclasses import dataclass, asdict


@dataclass
class Token:
    tipo: str
    lexema: str
    linha: int
    coluna: int

    def para_dict(self):
        return asdict(self)


@dataclass
class ErroLexico:
    tipo: str
    lexema: str
    linha: int
    coluna: int
    mensagem: str

    def para_dict(self):
        return asdict(self)


# Python keywords are recognized as reserved words even when the parser is not implemented.
PALAVRAS_RESERVADAS = set(keyword.kwlist) | {"True", "False", "None"}
OPERADORES = (
    "**=", "//=", ">>=", "<<=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=",
    "==", "!=", "<=", ">=", "**", "//", "<<", ">>",
    "+", "-", "*", "/", "%", "=", "<", ">", "&", "|", "^", "~",
)
DELIMITADORES = set("()[]{}.,:;")
_ESCAPE = set("abfnrtv\\'\"")


def analisar_lexico(codigo: str) -> dict:
    """Tokeniza o código e acumula erros léxicos sem interromper a leitura."""
    tokens: list[Token] = []
    erros: list[ErroLexico] = []
    i, linha, coluna = 0, 1, 1
    n = len(codigo)

    def avancar():
        nonlocal i, linha, coluna
        c = codigo[i]
        i += 1
        if c == "\n":
            linha += 1
            coluna = 1
        else:
            coluna += 1
        return c

    def erro(lexema, l, c, mensagem):
        erros.append(ErroLexico("ERRO_LEXICO", lexema, l, c, mensagem))

    while i < n:
        c = codigo[i]
        if c in " \t\r\f\v":
            avancar()
            continue
        if c == "\n":
            avancar()
            continue
        if c == "#":
            while i < n and codigo[i] != "\n":
                avancar()
            continue

        inicio_i, inicio_l, inicio_c = i, linha, coluna

        # Identifiers and reserved words.
        if c == "_" or c.isalpha():
            avancar()
            while i < n and (codigo[i] == "_" or codigo[i].isalnum()):
                avancar()
            lexema = codigo[inicio_i:i]
            tipo = "PALAVRA_RESERVADA" if lexema in PALAVRAS_RESERVADAS else "IDENTIFICADOR"
            tokens.append(Token(tipo, lexema, inicio_l, inicio_c))
            continue

        # Numeric literals: integers and decimal real numbers.
        if c.isdigit():
            while i < n and codigo[i].isdigit():
                avancar()
            tipo = "LITERAL_INTEIRO"
            if i < n and codigo[i] == "." and i + 1 < n and codigo[i + 1].isdigit():
                avancar()
                while i < n and codigo[i].isdigit():
                    avancar()
                tipo = "LITERAL_REAL"
            # A digit sequence immediately followed by identifier characters is malformed.
            if i < n and (codigo[i].isalpha() or codigo[i] == "_"):
                while i < n and (codigo[i].isalnum() or codigo[i] == "_"):
                    avancar()
                lexema = codigo[inicio_i:i]
                erro(lexema, inicio_l, inicio_c, f"Literal numérico malformado: '{lexema}'.")
            else:
                lexema = codigo[inicio_i:i]
                tokens.append(Token(tipo, lexema, inicio_l, inicio_c))
            continue

        # Single- and double-quoted strings. Escapes are scanned but not decoded.
        if c in ("'", '"'):
            aspas = c
            avancar()
            fechado = False
            while i < n:
                atual = codigo[i]
                if atual == aspas:
                    avancar()
                    fechado = True
                    break
                if atual == "\n":
                    break
                if atual == "\\":
                    avancar()
                    if i >= n or codigo[i] == "\n":
                        break
                    escape = codigo[i]
                    if escape not in _ESCAPE and not escape.isdigit() and escape not in "xuUN":
                        # Keep scanning the literal, while reporting its invalid escape.
                        erro("\\" + escape, linha, coluna, f"Sequência de escape inválida: '\\{escape}'.")
                    avancar()
                    continue
                avancar()
            lexema = codigo[inicio_i:i]
            if fechado:
                tokens.append(Token("LITERAL_STRING", lexema, inicio_l, inicio_c))
            else:
                erro(lexema, inicio_l, inicio_c, "Literal de string não terminado antes do fim da linha ou do arquivo.")
            continue

        # Longest match first for compound operators.
        operador = next((op for op in OPERADORES if codigo.startswith(op, i)), None)
        if operador:
            for _ in operador:
                avancar()
            tokens.append(Token("OPERADOR", operador, inicio_l, inicio_c))
            continue

        if c in DELIMITADORES:
            avancar()
            tokens.append(Token("DELIMITADOR", c, inicio_l, inicio_c))
            continue

        avancar()
        erro(c, inicio_l, inicio_c, f"Caractere não reconhecido: '{c}'. Verifique se ele faz parte do subconjunto suportado.")

    return {
        "sucesso": len(erros) == 0,
        "tokens": [t.para_dict() for t in tokens],
        "erros": [e.para_dict() for e in erros],
    }
