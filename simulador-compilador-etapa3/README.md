# Simulador Educacional de Compiladores — Python

## Objetivo e escopo da Etapa 3

Aplicação educacional que recebe um trecho de código Python e executa **análise léxica (scanner)**. O scanner percorre os caracteres, agrupa lexemas, classifica tokens e informa a linha e a coluna. Ele **não** executa o código e não verifica se a estrutura sintática está correta.

O subconjunto anterior continua sendo usado nos exemplos (atribuição, expressões aritméticas e `print()`), mas o scanner reconhece também categorias léxicas comuns de Python para permitir experimentação. A análise sintática será desenvolvida na Etapa 4.

## Subconjunto léxico documentado

| Categoria | Regra / exemplos |
|---|---|
| Palavras reservadas | Palavras-chave do Python, como `if`, `else`, `while`, `return`, `def`, `and`, `or`, `not`, `True`, `False` e `None`. São classificadas como `PALAVRA_RESERVADA`. |
| Identificadores | Começam com letra ou `_`; continuam com letras, dígitos ou `_`. Exemplos: `nome`, `_x1`, `resultado2`. |
| Inteiros | Uma sequência de dígitos: `0`, `10`, `2048`. Categoria `LITERAL_INTEIRO`. |
| Reais | Dígitos, ponto e dígitos, por exemplo `3.14`. Categoria `LITERAL_REAL`. |
| Strings | Texto entre aspas simples ou duplas, como `'oi'` e `"Olá"`. Categoria `LITERAL_STRING`. Aspas triplas e strings multilinha não fazem parte do escopo. |
| Operadores aritméticos | `+`, `-`, `*`, `/`, `//`, `%`, `**`. |
| Operadores relacionais | `==`, `!=`, `<`, `<=`, `>`, `>=`. |
| Atribuição e operadores compostos | `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`, `&=`, `|=`, `^=`, `<<=`, `>>=`. |
| Outros operadores reconhecidos | `&`, `|`, `^`, `~`, `<<`, `>>`. |
| Delimitadores | `(`, `)`, `[`, `]`, `{`, `}`, `.`, `,`, `:`, `;`. |
| Comentários | Comentários de linha iniciados por `#`; são ignorados. Python não possui sintaxe específica de comentário de bloco, portanto ela não é implementada. |
| Espaços em branco | Espaços, tabulações, retornos e quebras de linha são ignorados como tokens; linha e coluna são atualizadas. |
| Caracteres/sequências inválidas | Produzem erros léxicos com trecho, linha, coluna e mensagem. O scanner continua para encontrar outros erros quando possível. |

Nomes de tokens usados pela API: `PALAVRA_RESERVADA`, `IDENTIFICADOR`, `LITERAL_INTEIRO`, `LITERAL_REAL`, `LITERAL_STRING`, `OPERADOR` e `DELIMITADOR`. Erros usam `ERRO_LEXICO`.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Frontend | HTML, CSS e JavaScript puro, servido por nginx |
| Backend | Python 3.11, FastAPI e uvicorn |
| Scanner | Módulo Python próprio (`backend/scanner.py`), sem dependência externa |
| Testes backend | pytest + httpx / TestClient |
| Testes frontend | Node.js `node:test`, sem dependências externas |
| Ambiente | Docker Compose |

## Como executar

Pré-requisitos: Docker com Docker Compose. Na raiz do projeto:

```bash
docker compose up --build -d
```

Acesse <http://localhost:8080>. Para encerrar:

```bash
docker compose down
```

A API pode ser acessada diretamente em <http://localhost:8000/docs>. A interface chama `/api/analisar` pela mesma origem e o nginx encaminha a requisição para o backend.

## Como usar

1. Escreva código no editor ou selecione um exemplo.
2. Clique em **Analisar código**.
3. Consulte a tabela de tokens (tipo, lexema, linha e coluna) e a seção de erros léxicos.
4. Para cada erro, confira a linha e coluna indicadas. O código com erro léxico não interrompe a aplicação e os tokens restantes continuam sendo apresentados.

**Token** é a unidade reconhecida pelo scanner; **lexema** é a sequência exata de caracteres que formou aquele token. Um programa pode ser tokenizado mesmo que tenha um erro sintático, porque o parser ainda não faz parte desta etapa.

## Contrato da API

### `POST /api/analisar`

Requisição JSON:

```json
{ "codigo": "x = 10\nprint(x)" }
```

Resposta HTTP `200`, quando não há erros léxicos:

```json
{
  "recebido": true,
  "mensagem": "Código recebido com sucesso.",
  "linhas": 2,
  "caracteres": 15,
  "sucesso": true,
  "tokens": [
    { "tipo": "IDENTIFICADOR", "lexema": "x", "linha": 1, "coluna": 1 },
    { "tipo": "OPERADOR", "lexema": "=", "linha": 1, "coluna": 3 },
    { "tipo": "LITERAL_INTEIRO", "lexema": "10", "linha": 1, "coluna": 5 }
  ],
  "erros": []
}
```

Resposta HTTP `200` com erro léxico para o código `@` (a requisição foi recebida, mas a análise encontrou problema):

```json
{
  "recebido": true,
  "mensagem": "Código recebido com sucesso.",
  "sucesso": false,
  "tokens": [],
  "erros": [
    {
      "tipo": "ERRO_LEXICO",
      "lexema": "@",
      "linha": 1,
      "coluna": 5,
      "mensagem": "Caractere não reconhecido: '@'. Verifique se ele faz parte do subconjunto suportado."
    }
  ]
}
```

O exemplo de erro é ilustrativo; a resposta real também inclui `linhas` e `caracteres`, e mantém todos os tokens que puderam ser reconhecidos.

| Situação | HTTP | Comportamento |
|---|---:|---|
| Análise sem erros léxicos | 200 | `recebido: true`, `sucesso: true`, lista `tokens` e `erros: []` |
| Erros léxicos | 200 | `recebido: true`, `sucesso: false`, tokens encontrados e lista de erros |
| Código vazio ou só espaços | 422 | Contrato de validação mantido da Etapa 2 |
| JSON inválido / `codigo` ausente ou com tipo incorreto | 422 | `erro.tipo: requisicao_invalida` |
| Mais de 20.000 caracteres | 413 | `erro.tipo: entrada_muito_grande` |
| Erro interno inesperado | 500 | Mensagem genérica, sem detalhes internos |

Endpoints preservados: `GET /api/saude` e `GET /api/hello`.

## Testes automatizados

Na raiz do projeto, execute:

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest -v
cd ../frontend
npm test
```

Para verificar a implantação integrada com Docker:

```bash
bash scripts/validar_ambiente.sh
```

O registro das execuções feitas durante a preparação está em [`docs/testes.md`](docs/testes.md). Execute também os comandos no seu ambiente antes de entregar, especialmente o teste de Docker.

## Estrutura principal

```text
backend/
  main.py                 API e endpoints
  validacao.py            validação de entrada da Etapa 2
  scanner.py              análise léxica
  tests/                  testes de API, validação e scanner
frontend/
  index.html              interface
  js/app.js               apresentação dos resultados
  js/logica.js            comunicação com a API
  js/exemplos.js          exemplos de código
  tests/                  testes de frontend e regressão
docs/
  testes.md               registro de testes
scripts/
  validar_ambiente.sh     teste integrado do ambiente
```

## Limitações conhecidas e próximas etapas

- O scanner reconhece tokens; não constrói árvore sintática nem verifica a validade das instruções.
- Strings multilinha/aspas triplas, comentários de bloco, interpolação de strings e todos os detalhes avançados da gramática Python estão fora do escopo.
- O scanner não executa o programa nem avalia expressões.
- A análise sintática (parser) será tratada na Etapa 4.
- Os testes da interface usam DOM simulado; ainda é recomendável realizar um teste manual no navegador com Docker Compose.
