"""Analisador sintático descendente recursivo para um subconjunto de Python.

Suporta atribuições, chamadas de print, literais, identificadores e expressões
aritméticas com precedência. Cada instrução deve ocupar uma linha.
"""
from ast_nodes import NoAST

class ErroSintatico(Exception):
    def __init__(self, mensagem, linha, coluna):
        super().__init__(mensagem)
        self.mensagem, self.linha, self.coluna = mensagem, linha, coluna

class ParserLinha:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, lexema=None):
        t = self.atual()
        if t is None:
            ultimo = self.tokens[-1] if self.tokens else {"linha": 1, "coluna": 1}
            raise ErroSintatico(f"Esperado {lexema or 'mais um elemento'}, mas a instrução terminou.", ultimo['linha'], ultimo['coluna'] + 1)
        if lexema is not None and t['lexema'] != lexema:
            raise ErroSintatico(f"Esperado '{lexema}', encontrado '{t['lexema']}'.", t['linha'], t['coluna'])
        self.pos += 1
        return t

    def fator(self):
        t = self.atual()
        if t and t['lexema'] in ('+', '-'):
            op = self.consumir()
            return NoAST('Unario', op['lexema'], [self.fator()], op['linha'])
        if t and t['lexema'] == '(':
            self.consumir('('); no = self.expressao(); self.consumir(')'); return no
        if t and t['tipo'].startswith('LITERAL_'):
            self.consumir(); return NoAST('Literal', t['lexema'], [], t['linha'])
        if t and t['tipo'] == 'IDENTIFICADOR':
            self.consumir(); return NoAST('Identificador', t['lexema'], [], t['linha'])
        if t:
            raise ErroSintatico(f"Elemento inesperado '{t['lexema']}' em uma expressão.", t['linha'], t['coluna'])
        self.consumir('um valor')

    def termo(self):
        no = self.fator()
        while self.atual() and self.atual()['lexema'] in ('*', '/', '%'):
            op = self.consumir(); no = NoAST('Binaria', op['lexema'], [no, self.fator()], op['linha'])
        return no

    def expressao(self):
        no = self.termo()
        while self.atual() and self.atual()['lexema'] in ('+', '-'):
            op = self.consumir(); no = NoAST('Binaria', op['lexema'], [no, self.termo()], op['linha'])
        return no

    def instrucao(self):
        primeiro = self.atual()
        if primeiro is None: return None
        if primeiro['lexema'] == 'print':
            self.consumir('print'); self.consumir('(')
            args = []
            if self.atual() and self.atual()['lexema'] != ')':
                args.append(self.expressao())
                while self.atual() and self.atual()['lexema'] == ',':
                    self.consumir(','); args.append(self.expressao())
            self.consumir(')')
            return NoAST('Chamada', 'print', args, primeiro['linha'])
        if primeiro['tipo'] == 'IDENTIFICADOR':
            nome = self.consumir()
            self.consumir('=')
            return NoAST('Atribuicao', nome['lexema'], [self.expressao()], nome['linha'])
        raise ErroSintatico(f"Instrução não reconhecida iniciada por '{primeiro['lexema']}'.", primeiro['linha'], primeiro['coluna'])

def analisar_sintatico(tokens):
    """Analisa instruções linha a linha e devolve AST serializável e erros."""
    por_linha = {}
    for token in tokens: por_linha.setdefault(token['linha'], []).append(token)
    nos, erros = [], []
    for numero in sorted(por_linha):
        parser = ParserLinha(por_linha[numero])
        try:
            no = parser.instrucao()
            if parser.atual():
                t = parser.atual(); raise ErroSintatico(f"Token inesperado '{t['lexema']}' após o fim da instrução.", t['linha'], t['coluna'])
            if no: nos.append(no)
        except ErroSintatico as exc:
            erros.append({"tipo":"ERRO_SINTATICO", "mensagem":exc.mensagem, "linha":exc.linha, "coluna":exc.coluna})
    arvore = NoAST('Programa', None, nos, 1).para_dict()
    return {"sucesso": not erros, "erros": erros, "ast": arvore}
