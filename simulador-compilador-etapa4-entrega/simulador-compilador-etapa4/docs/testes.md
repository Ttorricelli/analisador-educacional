# Registro de testes — Etapas 3 e 4

## Testes automatizados

O registro de execução automatizada disponível nesta versão do projeto apresenta:

| Módulo | Comando | Resultado registrado |
|---|---|---|
| Backend: scanner, validação, API, parser e AST | `cd backend && python -m pytest -q` | **60 aprovados, 0 reprovados** |
| Frontend: lógica, interface simulada, exemplos, HTML e regressão | `cd frontend && npm test` | **42 aprovados, 0 reprovados** |

**Total registrado: 102 testes automatizados aprovados.**

Os testes da Etapa 4 verificam, entre outros aspectos, posições dos nós, precedência,
associatividade, campos `esperado`/`encontrado`, acumulação de erros em linhas
distintas, retorno de `ast: null` em caso de erro sintático e apresentação da AST e
dos diagnósticos na interface.

## Testes manuais da interface

Os sete cenários abaixo foram executados na interface e confirmados como aprovados:

| ID | Cenário | Resultado | Status |
|---|---|---|---|
| CT01 | Programa com atribuições, operações e chamada de `print` | Código aceito e AST gerada | Aprovado |
| CT02 | Expressão incompleta (`x = 10 +`) | Erro sintático identificado | Aprovado |
| CT03 | Expressão com parênteses (`x = (10 + 5) * 2`) | AST respeita o agrupamento dos parênteses | Aprovado |
| CT04 | Parêntese de fechamento ausente em atribuição | Erro sintático identificado | Aprovado |
| CT05 | Parêntese de fechamento ausente em chamada de `print` | Erro sintático identificado | Aprovado |
| CT06 | Operador em posição inválida (`x = * 5`) | Erro sintático identificado | Aprovado |
| CT07 | Precedência de multiplicação sobre adição (`x = 10 + 5 * 2`) | AST representa a multiplicação como subexpressão da adição | Aprovado |

**Total: 7 cenários manuais aprovados.**

## Verificação integrada com Docker

Foi executado:

```bash
docker compose up --build -d
```

Na saída apresentada, a imagem foi construída, o contêiner do backend ficou com
estado `Healthy` e o contêiner do frontend iniciou (`Started`). A interface foi
acessada em `http://localhost:8080` e utilizada para executar os cenários manuais.

Para encerrar os serviços:

```bash
docker compose down
```

## Observações

- Os resultados documentam as execuções e confirmações realizadas durante a
  validação. O ambiente pode variar entre computadores.
- Os testes manuais e a verificação Docker devem ser repetidos caso haja alterações
  no código ou na configuração.
- O simulador implementa somente o subconjunto didático de Python descrito em
  `gramatica_ebnf.md`; não se propõe a reconhecer a linguagem Python completa.
