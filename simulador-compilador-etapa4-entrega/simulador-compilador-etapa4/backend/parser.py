"""Parser descendente recursivo para o subconjunto educacional de Python.

Cada instrução ocupa uma linha. São aceitas atribuições simples, chamadas
print(...) e expressões aritméticas. O parser consome os tokens do scanner,
sem realizar uma segunda análise léxica.
"""
from ast_nodes import NoAST


class ErroSintatico(Exception):
    def __init__(self, mensagem, linha, coluna, esperado=None, encontrado=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        self.esperado = esperado or []
        self.encontrado = encontrado


class ParserLinha:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _posicao_fim(self):
        if self.tokens:
            ultimo = self.tokens[-1]
            return ultimo["linha"], ultimo["coluna"] + len(ultimo["lexema"])
        return 1, 1

    def consumir(self, lexema=None, esperado=None):
        token = self.atual()
        if token is None:
            linha, coluna = self._posicao_fim()
            descricao = f"'{lexema}'" if lexema else (esperado or "mais um elemento")
            raise ErroSintatico(
                f"Fim inesperado da instrução: era esperado {descricao}.",
                linha, coluna, [lexema or esperado or "expressão"], None,
            )
        if lexema is not None and token["lexema"] != lexema:
            raise ErroSintatico(
                f"Era esperado '{lexema}', mas foi encontrado '{token['lexema']}'.",
                token["linha"], token["coluna"], [lexema], token["lexema"],
            )
        self.pos += 1
        return token

    @staticmethod
    def no(tipo, valor, filhos, inicio, fim=None):
        fim = fim or inicio
        return NoAST(
            tipo, valor, filhos, inicio["linha"], inicio["coluna"],
            fim["linha"], fim["coluna"] + len(fim["lexema"]),
        )

    def primario(self):
        token = self.atual()
        if token is None:
            self.consumir(esperado="literal, identificador ou '('")
        if token["lexema"] == "(":
            inicio = self.consumir("(")
            expressao = self.expressao()
            fim = self.consumir(")")
            # Parênteses organizam a expressão, mas não criam nó próprio na AST.
            expressao.linha = inicio["linha"]
            expressao.coluna = inicio["coluna"]
            expressao.linha_fim = fim["linha"]
            expressao.coluna_fim = fim["coluna"] + 1
            return expressao
        if token["tipo"].startswith("LITERAL_"):
            self.consumir()
            return self.no("Literal", token["lexema"], [], token)
        if token["tipo"] == "IDENTIFICADOR":
            self.consumir()
            return self.no("Identificador", token["lexema"], [], token)
        raise ErroSintatico(
            f"Era esperado um literal, identificador ou '(', mas foi encontrado '{token['lexema']}'.",
            token["linha"], token["coluna"],
            ["literal", "identificador", "("], token["lexema"],
        )

    def fator(self):
        token = self.atual()
        if token and token["lexema"] in ("+", "-"):
            operador = self.consumir()
            filho = self.fator()
            return NoAST("Unario", operador["lexema"], [filho],
                         operador["linha"], operador["coluna"],
                         filho.linha_fim, filho.coluna_fim)
        return self.primario()

    def termo(self):
        no = self.fator()
        while self.atual() and self.atual()["lexema"] in ("*", "/", "%"):
            operador = self.consumir()
            direita = self.fator()
            no = NoAST("Binaria", operador["lexema"], [no, direita],
                       no.linha, no.coluna, direita.linha_fim, direita.coluna_fim)
        return no

    def expressao(self):
        no = self.termo()
        while self.atual() and self.atual()["lexema"] in ("+", "-"):
            operador = self.consumir()
            direita = self.termo()
            no = NoAST("Binaria", operador["lexema"], [no, direita],
                       no.linha, no.coluna, direita.linha_fim, direita.coluna_fim)
        return no

    def instrucao(self):
        primeiro = self.atual()
        if primeiro is None:
            return None
        if primeiro["lexema"] == "print":
            inicio = self.consumir("print")
            self.consumir("(")
            argumentos = []
            if self.atual() and self.atual()["lexema"] != ")":
                argumentos.append(self.expressao())
                while self.atual() and self.atual()["lexema"] == ",":
                    self.consumir(",")
                    argumentos.append(self.expressao())
            fim = self.consumir(")")
            return self.no("Chamada", "print", argumentos, inicio, fim)
        if primeiro["tipo"] == "IDENTIFICADOR":
            nome = self.consumir()
            self.consumir("=", esperado="operador de atribuição '='")
            expressao = self.expressao()
            return NoAST("Atribuicao", nome["lexema"], [expressao],
                         nome["linha"], nome["coluna"],
                         expressao.linha_fim, expressao.coluna_fim)
        raise ErroSintatico(
            f"Instrução não reconhecida: era esperado uma atribuição ou chamada de 'print', mas foi encontrado '{primeiro['lexema']}'.",
            primeiro["linha"], primeiro["coluna"],
            ["identificador", "print"], primeiro["lexema"],
        )


def analisar_sintatico(tokens):
    """Retorna AST somente quando todas as instruções forem sintaticamente válidas.

    A recuperação é feita por linha: um erro não impede o diagnóstico das
    instruções seguintes. Como o scanner não emite tokens de quebra de linha,
    os números de linha originais são usados para separar as instruções.
    """
    por_linha = {}
    for token in tokens:
        por_linha.setdefault(token["linha"], []).append(token)

    nos, erros = [], []
    for numero in sorted(por_linha):
        parser = ParserLinha(por_linha[numero])
        try:
            no = parser.instrucao()
            if parser.atual():
                token = parser.atual()
                raise ErroSintatico(
                    f"Token inesperado '{token['lexema']}' após o fim da instrução.",
                    token["linha"], token["coluna"], ["fim da instrução"], token["lexema"],
                )
            if no:
                nos.append(no)
        except ErroSintatico as exc:
            erros.append({
                "tipo": "ERRO_SINTATICO",
                "mensagem": exc.mensagem,
                "linha": exc.linha,
                "coluna": exc.coluna,
                "esperado": exc.esperado,
                "encontrado": exc.encontrado,
            })

    if erros:
        return {"sucesso": False, "erros": erros, "ast": None}

    ultimo = nos[-1] if nos else None
    arvore = NoAST("Programa", None, nos, 1, 1,
                   ultimo.linha_fim if ultimo else None,
                   ultimo.coluna_fim if ultimo else None).para_dict()
    return {"sucesso": True, "erros": [], "ast": arvore}
