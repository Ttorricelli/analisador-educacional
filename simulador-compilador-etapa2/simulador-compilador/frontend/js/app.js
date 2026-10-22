/* Ligação entre o DOM e as regras de js/logica.js. */
(function () {
  const { validarCodigo, enviarCodigo, ESTADOS } = window.Logica;

  const campo = document.getElementById("codigo");
  const botaoAnalisar = document.getElementById("btn-analisar");
  const botaoLimpar = document.getElementById("btn-limpar");
  const listaExemplos = document.getElementById("exemplos");
  const resultado = document.getElementById("resultado");
  const descricaoExemplo = document.getElementById("descricao-exemplo");

  const TEXTO_INICIAL = resultado.innerHTML;

  function mostrar(estado, titulo, mensagem, detalhes) {
    resultado.dataset.estado = estado;
    resultado.setAttribute("role", estado === "sucesso" || estado === "carregando" ? "status" : "alert");
    resultado.replaceChildren();
    const h = document.createElement("h3");
    h.textContent = titulo;
    const p = document.createElement("p");
    p.textContent = mensagem;
    resultado.append(h, p);
    if (detalhes) {
      const dl = document.createElement("dl");
      for (const [rotulo, valor] of detalhes) {
        const dt = document.createElement("dt");
        dt.textContent = rotulo;
        const dd = document.createElement("dd");
        dd.textContent = valor;
        dl.append(dt, dd);
      }
      resultado.append(dl);
    }
  }

  function selecionarExemplo(exemplo, botao) {
    campo.value = exemplo.codigo;
    descricaoExemplo.textContent = exemplo.descricao;
    for (const b of listaExemplos.querySelectorAll("button")) {
      b.setAttribute("aria-pressed", String(b === botao));
    }
    campo.focus();
  }

  for (const exemplo of window.EXEMPLOS) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "exemplo";
    b.dataset.exemplo = exemplo.id;
    b.setAttribute("aria-pressed", "false");
    b.textContent = exemplo.titulo;
    b.addEventListener("click", () => selecionarExemplo(exemplo, b));
    listaExemplos.append(b);
  }

  // Editar o texto desfaz a associação visual com o exemplo escolhido.
  campo.addEventListener("input", () => {
    for (const b of listaExemplos.querySelectorAll("button")) b.setAttribute("aria-pressed", "false");
    descricaoExemplo.textContent = "";
  });

  botaoLimpar.addEventListener("click", () => {
    campo.value = "";
    descricaoExemplo.textContent = "";
    for (const b of listaExemplos.querySelectorAll("button")) b.setAttribute("aria-pressed", "false");
    resultado.dataset.estado = "inicial";
    resultado.setAttribute("role", "status");
    resultado.innerHTML = TEXTO_INICIAL;
    campo.focus();
  });

  botaoAnalisar.addEventListener("click", async () => {
    const codigo = campo.value;
    const validacao = validarCodigo(codigo);
    if (!validacao.valido) {
      mostrar("entrada_invalida", "Entrada inválida", validacao.mensagem);
      campo.focus();
      return;
    }

    botaoAnalisar.disabled = true;
    mostrar("carregando", "Enviando", "Enviando o código para o servidor...");
    try {
      const r = await enviarCodigo(codigo);
      if (r.estado === ESTADOS.SUCESSO) {
        mostrar("sucesso", "Código recebido", r.mensagem, [
          ["Linhas", String(r.dados.linhas)],
          ["Caracteres", String(r.dados.caracteres)],
          ["Análise", "As análises léxica, sintática e semântica ainda não estão disponíveis."],
        ]);
      } else if (r.estado === ESTADOS.ENTRADA_INVALIDA) {
        mostrar("entrada_invalida", "Entrada inválida", r.mensagem);
      } else if (r.estado === ESTADOS.FALHA_COMUNICACAO) {
        mostrar("falha_comunicacao", "Servidor indisponível", r.mensagem);
      } else {
        mostrar("erro_inesperado", "Erro inesperado", r.mensagem);
      }
    } finally {
      botaoAnalisar.disabled = false;
    }
  });
})();
