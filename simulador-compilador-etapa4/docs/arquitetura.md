# Arquitetura do Sistema

## 1. Visão geral

O simulador utiliza uma arquitetura cliente-servidor. O frontend, desenvolvido em HTML, CSS e JavaScript, comunica-se com uma API FastAPI executada no backend Python.

O Docker Compose define os serviços `frontend` e `backend`. O Nginx serve os arquivos estáticos da interface e encaminha as requisições iniciadas por `/api/` para o serviço backend.

## 2. Componentes

- **Frontend (`frontend/`):** apresenta o editor, exemplos e resultados. `js/logica.js` valida a entrada e envia a requisição; `js/app.js` atualiza a interface com os resultados.
- **Nginx (`frontend/nginx.conf`):** serve a interface e encaminha `/api/` para `http://backend:8000`.
- **API (`backend/main.py`):** valida a requisição, chama o scanner e, se não houver erros léxicos, chama o parser.
- **Validação (`backend/validacao.py`):** verifica as condições de entrada definidas para a API.
- **Scanner (`backend/scanner.py`):** percorre o código-fonte e produz tokens e erros léxicos.
- **Parser (`backend/parser.py`):** agrupa os tokens por linha, reconhece atribuições e chamadas de `print`, analisa expressões e produz erros sintáticos quando necessário.
- **Nós da AST (`backend/ast_nodes.py`):** define a estrutura dos nós e sua conversão para dicionários serializáveis.
- **Docker Compose (`docker-compose.yml`):** configura os serviços, portas, dependência do frontend em relação à saúde do backend e verificações de saúde.

## 3. Fluxo de comunicação e processamento

1. O usuário insere o código na interface e solicita a análise.
2. O JavaScript do frontend envia `POST /api/analisar` com um JSON contendo o campo `codigo`.
3. A API valida a requisição e a entrada.
4. O scanner realiza a análise léxica e retorna tokens e erros.
5. Se houver erro léxico, o parser não é executado.
6. Se a análise léxica não apresentar erros, o parser analisa os tokens agrupados por linha.
7. O parser retorna o resultado sintático e uma AST serializável.
8. A API devolve os resultados em JSON; o frontend apresenta tokens, erros sintáticos e, quando a análise sintática é bem-sucedida, a representação hierárquica da AST.
