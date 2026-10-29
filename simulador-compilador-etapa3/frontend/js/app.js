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

  function mostrarAnaliseLexica(dados) {
    resultado.dataset.estado = dados.sucesso ? "sucesso" : "analise_com_erros";
    resultado.setAttribute("role", "status");
    resultado.replaceChildren();

    const h = document.createElement("h3");
    h.textContent = dados.sucesso ? "Análise léxica concluída" : "Análise léxica concluída com erros";
    const p = document.createElement("p");
    p.textContent = `Foram encontrados ${dados.tokens.length} token(s) e ${dados.erros.length} erro(s) léxico(s).`;
    resultado.append(h, p);

    const explicacao = document.createElement("p");
    explicacao.textContent = "Token é uma unidade reconhecida pelo scanner; lexema é o texto exato encontrado no código.";
    resultado.append(explicacao);

    const subtitulo = document.createElement("h4");
    subtitulo.textContent = "Tokens identificados";
    resultado.append(subtitulo);
    if (!dados.tokens.length) {
      const vazio = document.createElement("p");
      vazio.textContent = "Nenhum token reconhecido.";
      resultado.append(vazio);
    } else {
      const tabela = document.createElement("table");
      tabela.className = "tabela-tokens";
      const thead = document.createElement("thead");
      const linhaCabecalho = document.createElement("tr");
      for (const nome of ["Tipo", "Lexema", "Linha", "Coluna"]) {
        const th = document.createElement("th");
        th.textContent = nome;
        linhaCabecalho.append(th);
      }
      thead.append(linhaCabecalho);
      tabela.append(thead);
      const tbody = document.createElement("tbody");
      for (const token of dados.tokens) {
        const tr = document.createElement("tr");
        for (const valor of [token.tipo, token.lexema, String(token.linha), String(token.coluna)]) {
          const td = document.createElement("td");
          td.textContent = valor;
          tr.append(td);
        }
        tbody.append(tr);
      }
      tabela.append(tbody);
      resultado.append(tabela);
    }

    const errosTitulo = document.createElement("h4");
    errosTitulo.textContent = "Erros léxicos";
    resultado.append(errosTitulo);
    if (!dados.erros.length) {
      const semErros = document.createElement("p");
      semErros.textContent = "Nenhum erro léxico encontrado.";
      resultado.append(semErros);
    } else {
      const lista = document.createElement("ul");
      lista.className = "lista-erros";
      for (const erro of dados.erros) {
        const item = document.createElement("li");
        item.textContent = `Linha ${erro.linha}, coluna ${erro.coluna}: ${erro.mensagem} (trecho: ${erro.lexema})`;
        lista.append(item);
      }
      resultado.append(lista);
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
        if (r.dados && Array.isArray(r.dados.tokens) && Array.isArray(r.dados.erros)) {
          mostrarAnaliseLexica(r.dados);
        } else {
          mostrar("sucesso", "Código recebido", r.mensagem, [
            ["Linhas", String(r.dados.linhas)],
            ["Caracteres", String(r.dados.caracteres)],
          ]);
        }
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
