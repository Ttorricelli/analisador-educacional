/* Verificações estáticas do HTML: elementos exigidos pela especificação. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");

test("identifica o sistema e a linguagem escolhida", () => {
  assert.match(html, /<h1 id="titulo-sistema">[^<]*Compiladores/);
  assert.match(html, /id="linguagem">[^<]*Python/);
});

for (const id of ["codigo", "btn-analisar", "btn-limpar", "exemplos", "resultado", "descricao-exemplo"]) {
  test(`contém o elemento #${id}`, () => assert.match(html, new RegExp(`id="${id}"`)));
}

test("campo de código é textarea com rótulo associado", () => {
  assert.match(html, /<textarea[^>]*id="codigo"/);
  assert.match(html, /<label for="codigo"/);
});

test("área de resultados anuncia mudanças a leitores de tela", () => {
  assert.match(html, /id="resultado"[^>]*aria-live="polite"/);
});

test("scripts carregados na ordem correta (dados, lógica, interface)", () => {
  const ordem = [...html.matchAll(/<script src="js\/([\w.]+)"/g)].map((m) => m[1]);
  assert.deepEqual(ordem, ["exemplos.js", "logica.js", "app.js"]);
});

test("não depende de endereço localhost no código do navegador", () => {
  const js = fs.readdirSync(path.join(__dirname, "..", "js"))
    .map((f) => fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8")).join("\n");
  assert.doesNotMatch(html + js, /localhost|127\.0\.0\.1/);
});
