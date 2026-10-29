# Registro de testes — Etapa 3

Os resultados abaixo correspondem às execuções realizadas no ambiente de desenvolvimento durante a implementação. A validação com Docker deve ser repetida no computador de entrega se o Docker não estiver disponível.

## Execuções

| Módulo | Comando | Resultado observado |
|---|---|---|
| Backend: scanner, validação, API e regressão | `cd backend && python -m pytest -q` | **45 aprovados, 0 reprovados** |
| Frontend: lógica, interface simulada, exemplos, HTML e regressão | `cd frontend && npm test` | **40 aprovados, 0 reprovados** |
| Sintaxe Python | `python -m py_compile backend/*.py backend/tests/*.py` | Executar novamente antes da entrega |
| Integração Docker | `bash scripts/validar_ambiente.sh` | Pendente de confirmação em ambiente com Docker |

## Cobertura acrescentada nesta etapa

- Reconhecimento de palavras reservadas, identificadores, inteiros, reais e strings.
- Operadores simples e compostos, delimitadores, comentários de linha e espaços em branco.
- Linha/coluna dos tokens e erros.
- Caracteres desconhecidos, números malformados, strings não terminadas e escapes inválidos.
- Continuação da análise após erro léxico.
- Resposta estruturada do endpoint, preservação das validações da Etapa 2 e código com erro sintático tokenizado sem parser.
- Exibição de tabela de tokens e de erros com localização na interface.

## Pendências antes da entrega

1. Executar `bash scripts/validar_ambiente.sh` em um ambiente com Docker.
2. Abrir `http://localhost:8080`, analisar um exemplo, editar o código e testar um caractere inválido como `@`.
3. Se qualquer execução apresentar falha, corrigir e atualizar este registro com o resultado real.

Não declarar o teste Docker como aprovado antes de executá-lo.
