/* Regras de validação e comunicação com o backend (sem acesso ao DOM). */
(function (raiz) {
  const MENSAGENS = {
    entradaVazia: "Informe um código-fonte antes de solicitar a análise.",
    apenasEspacos:
      "O código contém apenas espaços em branco. Escreva ao menos uma instrução para solicitar a análise.",
    falhaComunicacao:
      "Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente.",
    erroInesperado:
      "Ocorreu um erro inesperado ao processar o código. Tente novamente em instantes.",
    entradaRejeitada: "O servidor não aceitou o código informado. Revise a entrada e tente novamente.",
  };

  const ESTADOS = {
    SUCESSO: "sucesso",
    ENTRADA_INVALIDA: "entrada_invalida",
    FALHA_COMUNICACAO: "falha_comunicacao",
    ERRO_INESPERADO: "erro_inesperado",
  };

  const URL_ANALISE = "/api/analisar";

  function validarCodigo(codigo) {
    if (typeof codigo !== "string" || codigo.length === 0) {
      return { valido: false, mensagem: MENSAGENS.entradaVazia };
    }
    if (codigo.trim() === "") {
      return { valido: false, mensagem: MENSAGENS.apenasEspacos };
    }
    return { valido: true, mensagem: "" };
  }

  /**
   * Envia o código ao backend e devolve sempre um objeto { estado, mensagem, dados }.
   * Nunca lança exceção: a interface decide o que mostrar a partir de `estado`.
   */
  async function enviarCodigo(codigo, fetchFn, url) {
    const f = fetchFn || (typeof fetch !== "undefined" ? fetch : null);
    const destino = url || URL_ANALISE;

    let resposta;
    try {
      resposta = await f(destino, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codigo }),
      });
    } catch (_) {
      return { estado: ESTADOS.FALHA_COMUNICACAO, mensagem: MENSAGENS.falhaComunicacao, dados: null };
    }

    // Proxy sem backend por trás (nginx devolve 502/503/504): é falha de comunicação.
    if ([502, 503, 504].includes(resposta.status)) {
      return { estado: ESTADOS.FALHA_COMUNICACAO, mensagem: MENSAGENS.falhaComunicacao, dados: null };
    }

    let dados = null;
    try {
      dados = await resposta.json();
    } catch (_) {
      return { estado: ESTADOS.ERRO_INESPERADO, mensagem: MENSAGENS.erroInesperado, dados: null };
    }

    if (resposta.status >= 200 && resposta.status < 300 && dados && dados.recebido === true) {
      return { estado: ESTADOS.SUCESSO, mensagem: dados.mensagem || "Código recebido com sucesso.", dados };
    }

    if (resposta.status >= 400 && resposta.status < 500) {
      const msg = dados && dados.erro && typeof dados.erro.mensagem === "string" ? dados.erro.mensagem : MENSAGENS.entradaRejeitada;
      return { estado: ESTADOS.ENTRADA_INVALIDA, mensagem: msg, dados };
    }

    // 5xx ou resposta fora do contrato: mensagem genérica, sem expor o corpo do servidor.
    return { estado: ESTADOS.ERRO_INESPERADO, mensagem: MENSAGENS.erroInesperado, dados: null };
  }

  const api = { MENSAGENS, ESTADOS, URL_ANALISE, validarCodigo, enviarCodigo };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else raiz.Logica = api;
})(typeof window !== "undefined" ? window : globalThis);
