/* Exemplos do subconjunto de Python: atribuição, aritmética básica e print(). */
(function (raiz) {
  const EXEMPLOS = [
    {
      id: "atribuicao",
      titulo: "Atribuição de variável",
      descricao: "Declaração e atribuição de variáveis, e saída com print().",
      codigo: "x = 10\nnome = \"Ana\"\nprint(x)\n",
    },
    {
      id: "aritmetica",
      titulo: "Operações aritméticas",
      descricao: "Operadores +, -, * e / com precedência e parênteses.",
      codigo: "a = 10\nb = 5\nresultado = a + b * 2\nmedia = (a + b) / 2\nprint(resultado)\nprint(media)\n",
    },
    {
      id: "expressoes",
      titulo: "Expressões encadeadas",
      descricao: "Uso de variáveis já definidas dentro de novas expressões.",
      codigo: "preco = 100\ndesconto = 15\ntotal = (preco - desconto) / 2\nprint(total)\n",
    },
    {
      id: "erro",
      titulo: "Código com erro intencional",
      descricao: "Operador sem operando e parêntese aberto. Será útil nas etapas de análise.",
      codigo: "x = 10 +\nprint(x\n",
    },
  ];

  if (typeof module !== "undefined" && module.exports) module.exports = { EXEMPLOS };
  else raiz.EXEMPLOS = EXEMPLOS;
})(typeof window !== "undefined" ? window : globalThis);
