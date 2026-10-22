#!/usr/bin/env bash
# Teste de implantação e integração: constrói, sobe os serviços e verifica
# a comunicação frontend -> nginx -> backend por HTTP real.
# Uso (na raiz do repositório): bash scripts/validar_ambiente.sh
set -u
BASE="http://localhost:8080"
falhas=0; total=0

verifica() {  # descrição, esperado, obtido
  total=$((total+1))
  if [ "$2" = "$3" ]; then echo "  [OK]    $1"; else echo "  [FALHA] $1 (esperado: $2, obtido: $3)"; falhas=$((falhas+1)); fi
}
post() { curl -s -o /tmp/resp.json -w "%{http_code}" -X POST "$BASE/api/analisar" -H 'Content-Type: application/json' -d "$1"; }

echo ">> Construindo e iniciando (docker compose up --build -d --wait)"
docker compose up --build -d --wait || { echo "Falha ao subir os serviços"; docker compose logs --tail=50; exit 1; }

echo ">> Verificações"
verifica "página inicial responde 200"               200 "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/")"
verifica "página contém o título do sistema"          1  "$(curl -s "$BASE/" | grep -c 'Simulador Educacional de Compiladores')"
verifica "backend direto responde /api/saude"         200 "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/api/saude)"
verifica "proxy do nginx: /api/hello (regressão)"     200 "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/api/hello")"
verifica "código válido via proxy"                    200 "$(post '{"codigo":"x = 10"}')"
verifica "resposta tem recebido=true"                 1   "$(grep -c '"recebido":true' /tmp/resp.json)"
verifica "código vazio"                               422 "$(post '{"codigo":""}')"
verifica "somente espaços"                            422 "$(post '{"codigo":"   "}')"
verifica "campo ausente"                              422 "$(post '{}')"
verifica "JSON malformado"                            422 "$(post '{codigo')"
verifica "arquivos JS estáticos servidos"             200 "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/js/app.js")"

echo ">> Resultado: $((total-falhas))/$total verificações aprovadas"
echo ">> Para encerrar: docker compose down"
[ "$falhas" -eq 0 ]
