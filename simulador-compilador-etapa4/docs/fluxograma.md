# Fluxograma do Funcionamento do Simulador

## 1. Descrição do processo

O usuário informa o código-fonte na interface e solicita a análise. O frontend verifica se a entrada está vazia ou contém apenas espaços e, estando válida, envia uma requisição à API.

A API valida a requisição e o conteúdo recebido. Em seguida, o scanner realiza a análise léxica. Se forem encontrados erros léxicos, a API retorna os tokens reconhecidos e os erros, sem executar o parser. Se não houver erros léxicos, os tokens são agrupados por linha e encaminhados ao parser.

O parser reconhece atribuições e chamadas de `print`, verifica as expressões e constrói a representação da AST. A API devolve o resultado ao frontend, que apresenta os tokens, os erros encontrados e, quando a análise sintática é bem-sucedida, a AST.

## 2. Etapas do fluxo

1. Entrada do código-fonte na interface.
2. Validação inicial da entrada pelo frontend.
3. Envio de `POST /api/analisar` para o backend.
4. Validação da requisição e do código pela API.
5. Análise léxica pelo scanner.
6. **Há erros léxicos?**
   - **Sim:** retornar tokens e erros léxicos; não executar o parser.
   - **Não:** agrupar tokens por linha e executar a análise sintática.
7. **A estrutura sintática é válida?**
   - **Sim:** retornar o resultado sintático e a AST.
   - **Não:** retornar os erros sintáticos.
8. Apresentação dos resultados na interface.
9. Encerramento do processo.

## 3. Observação

O parser analisa cada linha como uma instrução independente. Portanto, o subconjunto implementado não permite continuar uma expressão ou instrução na linha seguinte.
