# Analisador Educacional

Software educacional interativo para apoiar o estudo das análises **sintática e semântica** (precedidas da análise léxica) de compiladores, voltado a estudantes de graduação em Ciência da Computação. A ferramenta busca tornar visíveis as árvores de derivação e as regras semânticas durante a análise de expressões, aproximando a teoria formal da prática.

> **Status:** Etapa 1 — estrutura inicial, ambiente Docker e "Hello, World!".

## Linguagem escolhida e escopo

- **Linguagem analisada:** Python
- **Subconjunto inicial (a ser implementado nas próximas etapas):**
  - números inteiros e decimais;
  - variáveis (identificadores) e atribuição simples, como `x = 5`;
  - operadores aritméticos (`+`, `-`, `*`, `/`) e parênteses;
  - operadores de comparação (`<`, `>`, `<=`, `>=`, `==`, `!=`);
  - estrutura condicional `if` / `else` (em etapa posterior).
- **Por que essa escolha:** Python tem sintaxe legível e é amplamente adotada em disciplinas de base, o que reduz a barreira técnica de entrada e permite focar na complexidade lógica da matéria. Limitar o escopo a expressões e atribuições evita tornar o projeto inviável, e novas construções poderão ser acrescentadas depois.
- **Exemplos de análise previstos:** erros sintáticos (parênteses não fechados, operador sem operando) e semânticos (variável usada antes de ser atribuída, divisão por zero literal).
- **Tecnologia de implementação:** backend em Python (FastAPI) e frontend em HTML/JavaScript.
- 
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
git clone https://github.com/Ttorricelli/analisador-educacional.git
cd analisador-educacional/analisador-educacional/analisador-educacional
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

Checklist executado seguindo os comandos deste README:

- [x] `docker compose up --build` sem erros
- [x] <http://localhost:8080> exibe "Hello, World!"
- [x] `docker compose down` encerra os contêineres
- [x] Testado em: Windows com Docker Desktop 4.95.0

## Solução de problemas

- **Porta em uso:** altere o mapeamento de portas em `docker-compose.yml` (ex.: `"8081:80"`).
- **Página mostra "Erro ao falar com o backend":** veja `docker compose logs backend`.
- **"no configuration file provided":** você está na pasta errada; entre na pasta que contém o `docker-compose.yml`.

## Autor

Tatielly C Leal de Araújo — Professor com acesso ao repositório: `rocha3runo`
