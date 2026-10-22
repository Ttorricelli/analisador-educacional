# Registro de testes - Etapa 2

> Preencha as colunas "Resultado" com a saída real de cada comando na sua máquina.
> Só registre "aprovado" para o que você de fato executou.

## Execuções realizadas durante o desenvolvimento

| Módulo | Tipo | Comando | Resultado |
|---|---|---|---|
| Frontend (lógica, exemplos, HTML, interface com DOM simulado) | Unitário / interface / regressão | `cd frontend && npm test` | **38 aprovados, 0 reprovados** (Node v22.22.2) |
| `backend/validacao.py` | Unitário (verificação manual com Python stdlib; pytest indisponível no ambiente de desenvolvimento) | script ad hoc com `assert` | aprovado |
| Backend (sintaxe) | Estático | `python -m py_compile backend/*.py backend/tests/*.py` | sem erros |
| Backend (endpoints) | Endpoints / regressão | `cd backend && python -m pytest -v` | **PENDENTE: executar localmente** (FastAPI/pytest não puderam ser instalados no ambiente de desenvolvimento, sem acesso à rede) |
| Ambiente Docker | Implantação / integração | `bash scripts/validar_ambiente.sh` | **PENDENTE: executar localmente** (Docker indisponível no ambiente de desenvolvimento) |

## Cobertura
- **Backend (`tests/test_validacao.py`, `tests/test_api.py`)**: código válido, com erro de sintaxe, caracteres especiais, vazio, só espaços, limite de tamanho, campo ausente/nulo/tipo errado, JSON malformado, corpo ausente, método não permitido, erro inesperado sem vazamento de detalhes, CORS, regressão de `/api/hello`.
- **Frontend (`tests/*.test.js`)**: validação de entrada, contrato do POST, tratamento de 4xx/5xx/502-504/falha de rede, mensagens sem vazamento, exemplos (≥3, ids únicos, dentro do subconjunto), seleção/edição/limpeza, preservação do código, elementos exigidos no HTML.
- **Implantação (`scripts/validar_ambiente.sh`)**: build, healthchecks, página servida, proxy `/api`, respostas 200/422 reais.

## Falhas encontradas e correções
- `node --test tests/` não funciona no Node 22 (trata o diretório como módulo) → script `npm test` passou a usar o glob `tests/*.test.js`.
- `httpx >= 0.28` é incompatível com o TestClient do Starlette 0.27 (FastAPI 0.104.1) → `requirements-dev.txt` fixa `httpx==0.27.2`.

## Pendências
- Testes end-to-end em navegador real (Playwright/Cypress).
- Registrar aqui a saída do `pytest` e do `validar_ambiente.sh` após executá-los.
