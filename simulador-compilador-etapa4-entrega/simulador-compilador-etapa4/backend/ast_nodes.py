"""Nós da Árvore Sintática Abstrata (AST) do subconjunto educacional de Python."""
from dataclasses import dataclass
from typing import Any


@dataclass
class NoAST:
    tipo: str
    valor: Any = None
    filhos: list | None = None
    linha: int | None = None
    coluna: int | None = None
    linha_fim: int | None = None
    coluna_fim: int | None = None

    def para_dict(self):
        return {
            "tipo": self.tipo,
            "valor": self.valor,
            "linha": self.linha,
            "coluna": self.coluna,
            "linha_fim": self.linha_fim,
            "coluna_fim": self.coluna_fim,
            "filhos": [f.para_dict() for f in (self.filhos or [])],
        }
