/* Testes de interface: executa js/app.js contra um DOM simulado mínimo. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

class El {
  constructor(tag) {
    this.tag = tag; this.children = []; this.listeners = {}; this.attrs = {}; this.dataset = {};
    this.value = ""; this.disabled = false; this.className = ""; this.type = ""; this._text = ""; this._html = "";
    this.focused = false;
  }
  set textContent(v) { this._text = String(v); this.children = []; }
  get textContent() { return this._text + this.children.map((c) => c.textContent).join(""); }
  set innerHTML(v) { this._html = v; this.children = []; this._text = v.replace(/<[^>]+>/g, ""); }
  get innerHTML() { return this._html; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return this.attrs[k]; }
  append(...n) { this.children.push(...n); }
  replaceChildren(...n) { this.children = n; this._text = ""; }
  addEventListener(t, fn) { (this.listeners[t] ||= []).push(fn); }
  async click() { if (this.disabled) return; for (const fn of this.listeners.click || []) await fn(); }
  input(v) { this.value = v; for (const fn of this.listeners.input || []) fn(); }
  focus() { this.focused = true; }
  querySelectorAll(sel) { return sel === "button" ? this.children.filter((c) => c.tag === "button") : []; }
}

function montar(fetchFn) {
  const ids = {};
  for (const id of ["codigo", "btn-analisar", "btn-limpar", "exemplos", "resultado", "descricao-exemplo"]) ids[id] = new El("x");
  ids["btn-analisar"].tag = "button";
  ids.codigo.value = "x = 10\nprint(x)\n";
  ids.resultado.innerHTML = "<p>Texto inicial</p>";
  ids.resultado.dataset.estado = "inicial";
  const document = { getElementById: (i) => ids[i], createElement: (t) => new El(t) };
  const window = { document };
  const ctx = vm.createContext({ window, document, fetch: fetchFn, String, JSON, Error });
  for (const f of ["exemplos.js", "logica.js", "app.js"]) {
    const codigo = fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8");
    vm.runInContext(codigo, ctx, { filename: f });
  }
  return { ids, window };
}

const ok = (corpo, status = 200) => async () => ({ status, json: async () => corpo });
const botoes = (ids) => ids.exemplos.children;

test("renderiza um botão por exemplo", () => {
  const { ids, window } = montar(ok({}));
  assert.equal(botoes(ids).length, window.EXEMPLOS.length);
  assert.ok(botoes(ids).length >= 3);
});

test("cada exemplo, ao ser selecionado, preenche o campo e substitui o conteúdo anterior", async () => {
  const { ids, window } = montar(ok({}));
  for (let i = 0; i < window.EXEMPLOS.length; i++) {
    await botoes(ids)[i].click();
    assert.equal(ids.codigo.value, window.EXEMPLOS[i].codigo);
    assert.equal(ids["descricao-exemplo"].textContent, window.EXEMPLOS[i].descricao);
    assert.equal(botoes(ids)[i].getAttribute("aria-pressed"), "true");
  }
});

test("exemplo carregado pode ser editado e a edição é preservada", async () => {
  const { ids } = montar(ok({}));
  await botoes(ids)[0].click();
  ids.codigo.input("y = 99");
  assert.equal(ids.codigo.value, "y = 99");
  assert.equal(ids["descricao-exemplo"].textContent, "");
  assert.ok(botoes(ids).every((b) => b.getAttribute("aria-pressed") === "false"));
});

test("análise com campo vazio mostra a mensagem e NÃO chama o servidor", async () => {
  let chamadas = 0;
  const { ids } = montar(async () => { chamadas++; return { status: 200, json: async () => ({}) }; });
  ids.codigo.value = "";
  await ids["btn-analisar"].click();
  assert.equal(chamadas, 0);
  assert.equal(ids.resultado.dataset.estado, "entrada_invalida");
  assert.match(ids.resultado.textContent, /Informe um código-fonte antes de solicitar a análise\./);
});

test("análise com apenas espaços mostra orientação e não chama o servidor", async () => {
  let chamadas = 0;
  const { ids } = montar(async () => { chamadas++; });
  ids.codigo.value = "  \n\t ";
  await ids["btn-analisar"].click();
  assert.equal(chamadas, 0);
  assert.match(ids.resultado.textContent, /apenas espaços em branco/);
  assert.equal(ids.codigo.value, "  \n\t ");
});

test("análise bem-sucedida exibe a resposta do backend e preserva o código", async () => {
  const corpo = { recebido: true, mensagem: "Código recebido com sucesso.", linhas: 2, caracteres: 15 };
  const { ids } = montar(ok(corpo));
  await ids["btn-analisar"].click();
  assert.equal(ids.resultado.dataset.estado, "sucesso");
  assert.match(ids.resultado.textContent, /Código recebido com sucesso\./);
  assert.match(ids.resultado.textContent, /2/);
  assert.equal(ids.codigo.value, "x = 10\nprint(x)\n");
  assert.equal(ids["btn-analisar"].disabled, false);
});

test("falha de comunicação mostra mensagem compreensível e reabilita o botão", async () => {
  const { ids } = montar(async () => { throw new TypeError("Failed to fetch"); });
  await ids["btn-analisar"].click();
  assert.equal(ids.resultado.dataset.estado, "falha_comunicacao");
  assert.match(ids.resultado.textContent, /Não foi possível comunicar com o servidor/);
  assert.equal(ids["btn-analisar"].disabled, false);
  assert.equal(ids.codigo.value, "x = 10\nprint(x)\n");
});

test("erro 500 mostra mensagem genérica", async () => {
  const { ids } = montar(ok({ erro: { mensagem: "Traceback interno" } }, 500));
  await ids["btn-analisar"].click();
  assert.equal(ids.resultado.dataset.estado, "erro_inesperado");
  assert.doesNotMatch(ids.resultado.textContent, /Traceback/);
});

test("erro 422 do backend é exibido como entrada inválida", async () => {
  const { ids } = montar(ok({ recebido: false, erro: { tipo: "requisicao_invalida", mensagem: "Requisição inválida." } }, 422));
  await ids["btn-analisar"].click();
  assert.equal(ids.resultado.dataset.estado, "entrada_invalida");
  assert.match(ids.resultado.textContent, /Requisição inválida\./);
});

test("Limpar esvazia o campo e restaura a área de resultados", async () => {
  const { ids } = montar(ok({ recebido: true, linhas: 1, caracteres: 1 }));
  await ids["btn-analisar"].click();
  await ids["btn-limpar"].click();
  assert.equal(ids.codigo.value, "");
  assert.equal(ids.resultado.dataset.estado, "inicial");
  assert.match(ids.resultado.textContent, /Texto inicial/);
});

test("regressão: selecionar exemplo não interfere no envio do código", async () => {
  let corpo;
  const { ids, window } = montar(async (_u, o) => { corpo = JSON.parse(o.body); return { status: 200, json: async () => ({ recebido: true, linhas: 1, caracteres: 1 }) }; });
  await botoes(ids)[1].click();
  await ids["btn-analisar"].click();
  assert.equal(corpo.codigo, window.EXEMPLOS[1].codigo);
});


test("análise léxica exibe a tabela de tokens e a explicação didática", async () => {
  const corpo = {
    recebido: true, sucesso: true, mensagem: "Análise léxica concluída.",
    linhas: 1, caracteres: 6, erros: [],
    tokens: [
      { tipo: "IDENTIFICADOR", lexema: "x", linha: 1, coluna: 1 },
      { tipo: "OPERADOR", lexema: "=", linha: 1, coluna: 3 },
      { tipo: "LITERAL_INTEIRO", lexema: "10", linha: 1, coluna: 5 },
    ],
  };
  const { ids } = montar(ok(corpo));
  await ids["btn-analisar"].click();
  assert.equal(ids.resultado.dataset.estado, "sucesso");
  assert.match(ids.resultado.textContent, /Tokens identificados/);
  assert.match(ids.resultado.textContent, /IDENTIFICADOR/);
  assert.match(ids.resultado.textContent, /LITERAL_INTEIRO/);
  assert.match(ids.resultado.textContent, /lexema/);
});

test("erros léxicos são apresentados com linha, coluna e mensagem", async () => {
  const corpo = {
    recebido: true, sucesso: false, mensagem: "Análise léxica concluída com erros.",
    linhas: 1, caracteres: 5, tokens: [], 
    erros: [{ tipo: "ERRO_LEXICO", lexema: "@", linha: 1, coluna: 5, mensagem: "Caractere não reconhecido: '@'." }],
  };
  const { ids } = montar(ok(corpo));
  await ids["btn-analisar"].click();
  assert.equal(ids.resultado.dataset.estado, "analise_com_erros");
  assert.match(ids.resultado.textContent, /Erros léxicos/);
  assert.match(ids.resultado.textContent, /Linha 1, coluna 5/);
  assert.match(ids.resultado.textContent, /@/);
});
