const el = document.getElementById("mensagem");

fetch("/api/hello")
  .then((res) => {
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  })
  .then((data) => {
    el.textContent = data.message;
  })
  .catch((err) => {
    el.textContent = "Erro ao falar com o backend: " + err.message;
    el.classList.add("erro");
  });
