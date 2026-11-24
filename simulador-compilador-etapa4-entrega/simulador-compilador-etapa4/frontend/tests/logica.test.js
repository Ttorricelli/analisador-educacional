const test = require("node:test");
const assert = require("node:assert/strict");
const { validarCodigo, enviarCodigo, MENSAGENS, ESTADOS } = require("../js/logica.js");

const resp = (status, corpo, jsonValido = true) => ({
  status,
  json: async () => { if (!jsonValido) throw new SyntaxError("json"); return corpo; },
});

test("validarCodigo: código válido, com erro de sintaxe e com caracteres especiais", () => {
  assert.equal(validarCodigo("x = 10").valido, true);
  assert.equal(validarCodigo("x = 10 +\nprint(x").valido, true);
  assert.equal(validarCodigo('s = "ação ✓ 你好"').valido, true);
});

test("validarCodigo: vazio", () => {
  for (const v of ["", null, undefined, 42]) {
    const r = validarCodigo(v);
    assert.equal(r.valido, false);
    assert.equal(r.mensagem, "Informe um código-fonte antes de solicitar a análise.");
  }
});

test("validarCodigo: apenas espaços/tabs/quebras de linha", () => {
  for (const v of [" ", "   ", "\n\n", "\t \n "]) {
    const r = validarCodigo(v);
    assert.equal(r.valido, false);
    assert.equal(r.mensagem, MENSAGENS.apenasEspacos);
  }
});

test("enviarCodigo: sucesso envia POST JSON com o campo 'codigo'", async () => {
  let chamada;
  const f = async (url, opts) => {
    chamada = { url, opts };
    return resp(200, { recebido: true, mensagem: "Código recebido com sucesso.", linhas: 1, caracteres: 6 });
  };
  const r = await enviarCodigo("x = 10", f);
  assert.equal(r.estado, ESTADOS.SUCESSO);
  assert.equal(r.mensagem, "Código recebido com sucesso.");
  assert.equal(chamada.url, "/api/analisar");
  assert.equal(chamada.opts.method, "POST");
  assert.equal(chamada.opts.headers["Content-Type"], "application/json");
  assert.deepEqual(JSON.parse(chamada.opts.body), { codigo: "x = 10" });
});

test("enviarCodigo: preserva caracteres especiais no corpo", async () => {
  let corpo;
  const f = async (_u, o) => { corpo = JSON.parse(o.body); return resp(200, { recebido: true }); };
  const texto = 'a = "ação\\n ✓ 你好"\n\t# fim';
  await enviarCodigo(texto, f);
  assert.equal(corpo.codigo, texto);
});

test("enviarCodigo: 4xx do backend vira entrada_invalida com a mensagem do contrato", async () => {
  const f = async () => resp(422, { recebido: false, erro: { tipo: "entrada_vazia", mensagem: "Informe um código-fonte antes de solicitar a análise." } });
  const r = await enviarCodigo("", f);
  assert.equal(r.estado, ESTADOS.ENTRADA_INVALIDA);
  assert.equal(r.mensagem, "Informe um código-fonte antes de solicitar a análise.");
});

test("enviarCodigo: 4xx sem corpo no contrato usa mensagem padrão", async () => {
  const r = await enviarCodigo("x", async () => resp(400, {}));
  assert.equal(r.estado, ESTADOS.ENTRADA_INVALIDA);
  assert.equal(r.mensagem, MENSAGENS.entradaRejeitada);
});

test("enviarCodigo: fetch rejeitado (rede) vira falha_comunicacao", async () => {
  const r = await enviarCodigo("x", async () => { throw new TypeError("Failed to fetch"); });
  assert.equal(r.estado, ESTADOS.FALHA_COMUNICACAO);
  assert.equal(r.mensagem, "Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente.");
});

test("enviarCodigo: 502/503/504 do proxy viram falha_comunicacao", async () => {
  for (const s of [502, 503, 504]) {
    const r = await enviarCodigo("x", async () => resp(s, null, false));
    assert.equal(r.estado, ESTADOS.FALHA_COMUNICACAO);
  }
});

test("enviarCodigo: 500 devolve mensagem genérica e não expõe o corpo", async () => {
  const f = async () => resp(500, { erro: { mensagem: "Traceback /app/main.py senha=123" } });
  const r = await enviarCodigo("x", f);
  assert.equal(r.estado, ESTADOS.ERRO_INESPERADO);
  assert.equal(r.mensagem, MENSAGENS.erroInesperado);
  assert.doesNotMatch(JSON.stringify(r), /Traceback|senha|\/app\//);
});

test("enviarCodigo: resposta 200 que não é JSON vira erro_inesperado", async () => {
  const r = await enviarCodigo("x", async () => resp(200, null, false));
  assert.equal(r.estado, ESTADOS.ERRO_INESPERADO);
});

test("enviarCodigo: 200 fora do contrato (sem recebido=true) vira erro_inesperado", async () => {
  const r = await enviarCodigo("x", async () => resp(200, { qualquer: "coisa" }));
  assert.equal(r.estado, ESTADOS.ERRO_INESPERADO);
});
