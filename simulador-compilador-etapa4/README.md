# Simulador Educacional de Compiladores — Python

## Objetivo

Aplicação educacional que recebe um trecho de código de um subconjunto de Python e apresenta sua **análise léxica**, **análise sintática** e **Árvore Sintática Abstrata (AST)**. O simulador não executa o código-fonte nem avalia os resultados das expressões.

O projeto foi desenvolvido em etapas. A Etapa 4 acrescenta o parser e a construção da AST, preservando a análise léxica, a API e a interface das etapas anteriores.

## Escopo da linguagem reconhecida

O scanner identifica categorias léxicas comuns de Python, incluindo:

- palavras reservadas;
- identificadores;
- literais inteiros, reais e strings;
- operadores aritméticos, relacionais, de atribuição e outros operadores;
- delimitadores;
- comentários de linha, que são ignorados;
- espaços em branco e quebras de linha, que não são emitidos como tokens.

Caracteres ou sequências não reconhecidas geram erros léxicos com localização. A análise sintática, por sua vez, aceita o subconjunto educacional descrito abaixo.

### Subconjunto sintático da Etapa 4

O parser é descendente recursivo e analisa cada instrução em uma linha independente. São reconhecidas:

- atribuições simples, no formato `identificador = expressão`;
- chamadas de `print(...)`, com zero ou mais argumentos;
- identificadores e literais inteiros, reais e strings;
- expressões entre parênteses;
- operadores unários `+` e `-`;
- operadores binários `*`, `/`, `%`, `+` e `-`, respeitando a precedência usual.

A gramática completa do subconjunto está em [`docs/gramatica_ebnf.md`](docs/gramatica_ebnf.md).

**Limitações:** o projeto não implementa Python completo. Não são reconhecidos blocos indentados, condicionais, laços, definições de função, listas, dicionários, chamadas genéricas de função ou expressões distribuídas por várias linhas.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Frontend | HTML, CSS e JavaScript puro |
| Servidor da interface e proxy | Nginx |
| Backend | Python 3.11, FastAPI e Uvicorn |
| Análise léxica | Scanner próprio em Python |
| Análise sintática | Parser descendente recursivo em Python |
| AST | Estruturas de nós próprias, serializadas em JSON |
| Testes backend | pytest e httpx / TestClient |
| Testes frontend | Node.js `node:test` |
| Ambiente | Docker Compose |

## Como executar

Pré-requisito: Docker com Docker Compose instalado.

Na pasta que contém `docker-compose.yml`, execute:

```bash
docker compose up --build -d
```

Acesse a interface em:

<http://localhost:8080>

A documentação interativa da API fica disponível em:

<http://localhost:8000/docs>

Para encerrar os serviços:

```bash
docker compose down
```

## Como utilizar

1. Abra a interface no navegador.
2. Escreva um trecho de código no editor ou selecione um exemplo.
3. Clique em **Analisar código**.
4. Consulte a tabela de tokens e os eventuais erros léxicos.
5. Se não houver erros léxicos, consulte o resultado da análise sintática.
6. Quando a estrutura estiver correta, a interface apresenta a AST em formato hierárquico.

**Token** é uma unidade reconhecida pelo scanner; **lexema** é o texto exato encontrado no código. A análise léxica pode reconhecer os tokens de uma entrada que depois seja rejeitada pelo parser por erro sintático.

## API

### `POST /api/analisar`

Recebe um JSON com o campo `codigo`:

```json
{
  "codigo": "x = 10 + 5 * 2"
}
```

A resposta contém os dados da análise léxica (`sucesso`, `tokens` e `erros`) e o campo `analise_sintatica`, com o resultado sintático (`sucesso`, `erros` e `ast`). A análise sintática só é executada quando não há erros léxicos.

Endpoints preservados:

- `GET /api/saude`: verificação de saúde do backend.
- `GET /api/hello`: endpoint mantido para regressão da integração.

## Testes automatizados

Backend:

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest -v
```

Frontend:

```bash
cd frontend
npm test
```

Verificação integrada do ambiente:

```bash
bash scripts/validar_ambiente.sh
```

O registro dos testes automatizados e manuais está em [`docs/testes.md`](docs/testes.md). Os casos manuais estão detalhados em [`docs/casos_de_teste.md`](docs/casos_de_teste.md).

## Estrutura do projeto

```text
simulador-compilador-etapa4/
├── backend/
│   ├── main.py
│   ├── validacao.py
│   ├── scanner.py
│   ├── parser.py
│   ├── ast_nodes.py
│   └── tests/
├── frontend/
│   ├── index.html
│   ├── js/
│   └── tests/
├── docs/
│   ├── arquitetura.md
│   ├── casos_de_teste.md
│   ├── etapa4.md
│   ├── fluxograma.md
│   ├── gramatica_ebnf.md
│   └── testes.md
├── scripts/
├── docker-compose.yml
└── README.md
```

## Documentação complementar

- [`docs/etapa4.md`](docs/etapa4.md): escopo e implementação da Etapa 4.
- [`docs/gramatica_ebnf.md`](docs/gramatica_ebnf.md): gramática formal do subconjunto.
- [`docs/arquitetura.md`](docs/arquitetura.md): componentes e comunicação do sistema.
- [`docs/fluxograma.md`](docs/fluxograma.md): sequência de processamento.
- [`docs/casos_de_teste.md`](docs/casos_de_teste.md): casos de teste manuais.
- [`docs/testes.md`](docs/testes.md): registro das verificações automatizadas e manuais.
