"""Nós da Árvore Sintática Abstrata (AST) do subconjunto educacional de Python."""
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class NoAST:
    tipo: str
    valor: Any = None
    filhos: list | None = None
    linha: int | None = None

    def para_dict(self):
        return {"tipo": self.tipo, "valor": self.valor,
                "linha": self.linha,
                "filhos": [f.para_dict() for f in (self.filhos or [])]}
