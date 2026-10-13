# Analisador Educacional

Software educacional para apoiar o estudo das análises **léxica, sintática e semântica** de uma linguagem de programação.

> **Status:** Etapa 1 — estrutura inicial, ambiente Docker e "Hello, World!".

## Linguagem escolhida e escopo

- **Linguagem analisada:** C
- **Subconjunto inicial (a ser implementado nas próximas etapas):**
  - declaração de variáveis dos tipos `int` e `float`;
  - atribuições;
  - operadores aritméticos (`+`, `-`, `*`, `/`) e parênteses;
  - estrutura condicional `if` / `else`;
  - operadores relacionais (`<`, `>`, `<=`, `>=`, `==`, `!=`).
- **Por que essa escolha:** C possui sintaxe pequena e bem definida, tipagem estática e é amplamente usada no ensino de compiladores, o que facilita exemplos claros de erros léxicos, sintáticos e semânticos (ex.: variável não declarada, tipos incompatíveis). Limitar o escopo evita tornar o projeto inviável; novas construções (`while`, `for`, funções) poderão ser acrescentadas depois.

> Ajuste esta seção se você escolher outra linguagem ou subconjunto.

## Arquitetura

```
.
├── backend/              # API em Python (FastAPI)
│   ├── app/main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Interface web estática servida pelo Nginx
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   ├── nginx.conf
│   └── Dockerfile
├── config/               # Arquivos de configuração
├── docs/                 # Documentação adicional
├── docker-compose.yml
└── README.md
```

O navegador acessa o **frontend** (Nginx, porta 8080). O Nginx serve a página e repassa as chamadas `/api/*` ao **backend** (FastAPI, porta 8000) pela rede interna do Compose.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) 24 ou superior
- Docker Compose v2 (`docker compose`) 2.20 ou superior
- Git
- Portas **8080** e **8000** livres

Verifique as versões:

```bash
docker --version
docker compose version
```

## Como executar

```bash
git clone <URL_DO_REPOSITORIO>
cd analisador-educacional
docker compose up --build
```

Depois acesse:

- Interface web: <http://localhost:8080> — deve exibir **Hello, World!**
- API direta: <http://localhost:8000/api/hello>
- Documentação automática da API: <http://localhost:8000/docs>

Para rodar em segundo plano, use `docker compose up --build -d`.

## Como encerrar

```bash
docker compose down
```

Para remover também imagens construídas: `docker compose down --rmi local`.

## Validação de instalação limpa

Checklist executado seguindo apenas este README:

- [ ] `git clone` em uma pasta nova
- [ ] `docker compose up --build` sem erros
- [ ] <http://localhost:8080> exibe "Hello, World!"
- [ ] `docker compose down` encerra os contêineres
- [ ] Testado em: _(sistema operacional / versões do Docker)_

## Solução de problemas

- **Porta em uso:** altere o mapeamento de portas em `docker-compose.yml` (ex.: `"8081:80"`).
- **Página mostra "Erro ao falar com o backend":** veja `docker compose logs backend`.

## Autor

_Seu nome_ — Professor com acesso ao repositório: `rocha3runo`
