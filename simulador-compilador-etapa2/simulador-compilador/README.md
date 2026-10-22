# Simulador Educacional de Compiladores - Python

## Objetivo
Software educacional para estudantes de compiladores. O usuário escreve (ou escolhe) um programa, solicita a análise e vê a resposta do sistema. Nesta **etapa 2** a aplicação já recebe o código, valida a entrada e se comunica com o backend; as análises léxica, sintática e semântica serão feitas nas próximas etapas.

## Escolha da Linguagem
A linguagem escolhida para análise é o **Python**, devido à sua sintaxe limpa e legibilidade, que reduzem a carga cognitiva de estudantes iniciantes.

Para viabilizar o escopo da ferramenta, o **subconjunto inicial** contempla apenas:
- Declaração e atribuição de variáveis (ex: `x = 10`).
- Operadores aritméticos básicos (`+`, `-`, `*`, `/`).
- Função de saída padrão (`print()`).

Esta delimitação permite construir as fundações da análise léxica e sintática sem introduzir prematuramente a complexidade de blocos de indentação ou estruturas de controle.

## Tecnologias
| Camada | Tecnologia |
|---|---|
| Frontend | HTML, CSS e JavaScript puro, servidos pelo **nginx** |
| Backend | **Python 3.11 + FastAPI** (uvicorn) |
| Testes backend | pytest + httpx (TestClient) |
| Testes frontend | `node:test` (Node 20+), sem dependências externas |
| Orquestração | Docker e Docker Compose |

## Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)
- Para rodar os testes fora do Docker: Python 3.11+ e Node.js 20+

## Como iniciar e encerrar
Na raiz do repositório (onde está o `docker-compose.yml`):
```bash
docker compose up --build -d     # iniciar (ou: docker-compose up --build -d)
docker compose down              # encerrar
```
O backend possui *healthcheck*; o frontend só inicia depois que o backend estiver saudável.

## Como acessar
- Interface web: <http://localhost:8080>
- API (acesso direto, opcional): <http://localhost:8000> (documentação interativa em `/docs`)

O navegador chama `/api/...` no mesmo endereço da página; o **nginx encaminha** essas chamadas ao serviço `backend` pela rede interna do Compose. Assim não há endereços fixos de desenvolvimento no código do navegador.

## A interface
- **Identificação**: nome do sistema e linguagem analisada no topo.
- **Código-fonte**: campo de texto monoespaçado para escrever, colar e editar. O conteúdo é mantido durante toda a interação (inclusive após erros e respostas).
- **Exemplos**: botões que preenchem o campo com um programa pronto, substituindo o conteúdo anterior. O código carregado pode ser editado antes de analisar.
- **Analisar código**: valida a entrada no navegador e envia ao backend.
- **Limpar**: esvazia o campo e restaura a área de resultados.
- **Resultado**: mostra sucesso, erro de entrada (âmbar) ou falha de comunicação/erro inesperado (vermelho).

### Exemplos disponíveis
| Exemplo | Construções demonstradas |
|---|---|
| Atribuição de variável | Atribuição de inteiro e de string; `print()` |
| Operações aritméticas | `+`, `-`, `*`, `/`, precedência e parênteses |
| Expressões encadeadas | Variáveis já definidas usadas em novas expressões |
| Código com erro intencional | Operador sem operando e parêntese aberto (será usado nas etapas de análise) |

## Contrato da API
### `POST /api/analisar`
Requisição (`Content-Type: application/json`):
```json
{ "codigo": "x = 10\nprint(x)" }
```
Resposta de sucesso (`200`):
```json
{ "recebido": true, "mensagem": "Código recebido com sucesso.", "linhas": 2, "caracteres": 15 }
```
Resposta de erro:
```json
{ "recebido": false, "erro": { "tipo": "entrada_vazia", "mensagem": "Informe um código-fonte antes de solicitar a análise." } }
```
| Situação | HTTP | `erro.tipo` |
|---|---|---|
| `codigo` vazio | 422 | `entrada_vazia` |
| `codigo` só com espaços/quebras de linha | 422 | `entrada_somente_espacos` |
| Campo ausente, tipo errado ou JSON malformado | 422 | `requisicao_invalida` |
| `codigo` com mais de 20.000 caracteres | 413 | `entrada_muito_grande` |
| Erro inesperado no servidor | 500 | `erro_interno` (mensagem genérica, sem detalhes internos) |

Outros endpoints: `GET /api/saude` (healthcheck) e `GET /api/hello` (etapa 1, mantido).

O backend **não presume que o código seja válido**: código com erros de sintaxe é recebido normalmente (a análise virá nas próximas etapas). Se o servidor estiver fora do ar, o frontend mostra: *"Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente."*

### Variáveis de ambiente
| Variável | Padrão | Uso |
|---|---|---|
| `CORS_ORIGINS` | `*` | Origens permitidas pelo CORS do backend (separadas por vírgula). |

Nenhuma credencial é necessária ou versionada.

## Estrutura do repositório
```
backend/    main.py (API), validacao.py (regras), tests/ (pytest)
frontend/   index.html, style.css, js/{exemplos,logica,app}.js, nginx.conf, tests/ (node:test)
scripts/    validar_ambiente.sh (teste de implantação/integração)
docs/       testes.md (registro dos testes)
```

## Testes
```bash
# Backend (unitários + endpoints + regressão)
cd backend && pip install -r requirements-dev.txt && python -m pytest -v

# Frontend (lógica, exemplos, HTML e interface com DOM simulado)
cd frontend && npm test

# Implantação + integração real (Docker): sobe tudo e testa via nginx -> backend
bash scripts/validar_ambiente.sh
```
O registro das execuções e resultados está em [`docs/testes.md`](docs/testes.md).

## Limitações conhecidas
- Não há análise léxica, sintática nem semântica: o backend apenas valida e confirma o recebimento.
- Os testes de interface usam um DOM simulado; não há ainda testes *end-to-end* em navegador real (ex.: Playwright).
- O limite de entrada é de 20.000 caracteres.
- Sem realce de sintaxe nem numeração de linhas (opcionais nesta etapa).
