const test = require("node:test");
const assert = require("node:assert/strict");
const { EXEMPLOS } = require("../js/exemplos.js");
const { validarCodigo } = require("../js/logica.js");

test("existem pelo menos três exemplos", () => assert.ok(EXEMPLOS.length >= 3));

test("ids são únicos e todos os campos estão preenchidos", () => {
  const ids = EXEMPLOS.map((e) => e.id);
  assert.equal(new Set(ids).size, ids.length);
  for (const e of EXEMPLOS) {
    for (const campo of ["id", "titulo", "descricao", "codigo"]) {
      assert.equal(typeof e[campo], "string");
      assert.ok(e[campo].trim().length > 0, `${e.id}.${campo} vazio`);
    }
  }
});

test("todo exemplo passa na validação de entrada (inclusive o com erro intencional)", () => {
  for (const e of EXEMPLOS) assert.equal(validarCodigo(e.codigo).valido, true, e.id);
});

test("exemplos fora do erro intencional usam só o subconjunto: atribuição, + - * / e print", () => {
  const permitido = /^\s*(\w+\s*=\s*[^\n]+|print\([^\n]*\))\s*$/;
  for (const e of EXEMPLOS.filter((x) => x.id !== "erro")) {
    for (const linha of e.codigo.split("\n").filter((l) => l.trim())) {
      assert.match(linha, permitido, `${e.id}: "${linha}"`);
      assert.doesNotMatch(linha, /\b(if|for|while|def|import|class)\b/);
    }
  }
});
