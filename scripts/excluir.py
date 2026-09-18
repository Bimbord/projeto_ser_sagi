# -*- coding: utf-8 -*-
"""
excluir.py — apaga registros das tabelas do site usando a service_role local.

Exemplos
--------
# ver os últimos registros de uma tabela
python scripts/excluir.py --tabela arquivo --listar

# exclusão LÓGICA (marca deleted = true; o site filtra deleted = false)
python scripts/excluir.py --tabela arquivo --ids 36
python scripts/excluir.py --tabela depoimentos --ids 3,4
python scripts/excluir.py --tabela arquivo --categoria Home --secao hero

# exclusão DEFINITIVA (apaga a linha) — use só quando quiser sumir de vez
python scripts/excluir.py --tabela contatos --ids 5 --definitivo

Regras
------
- Sempre confere o resultado depois de apagar (relê o registro).
- Nunca apaga "tudo": exige --ids ou um filtro explícito.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from supabase_admin import SUPABASE_URL, admin_disponivel, admin_headers, INSTRUCOES  # noqa: E402

TABELAS = ["arquivo", "depoimentos", "parceiros", "galeria", "contatos", "newsletter"]


def _req(caminho, metodo="GET", corpo=None):
    url = f"{SUPABASE_URL}/rest/v1/{caminho}"
    dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8") if corpo is not None else None
    req = urllib.request.Request(url, method=metodo, data=dados)
    for k, v in admin_headers(json_body=corpo is not None).items():
        req.add_header(k, v)
    if metodo != "GET":
        req.add_header("Prefer", "return=minimal")
    with urllib.request.urlopen(req, timeout=30) as r:
        texto = r.read().decode()
        return r.status, (json.loads(texto) if texto.strip() else None)


def main():
    ap = argparse.ArgumentParser(description="Apaga registros do site (service_role local).")
    ap.add_argument("--tabela", required=True, choices=TABELAS)
    ap.add_argument("--ids", help="ids separados por vírgula (ex.: 30,31)")
    ap.add_argument("--categoria", help="filtro por categoria")
    ap.add_argument("--secao", help="filtro por secao")
    ap.add_argument("--listar", action="store_true", help="só mostra os últimos registros")
    ap.add_argument("--definitivo", action="store_true", help="apaga a linha (senão marca deleted=true)")
    a = ap.parse_args()

    if not admin_disponivel():
        sys.exit("❌ " + INSTRUCOES)

    # ---- listar ----
    if a.listar:
        _, itens = _req(f"{a.tabela}?select=*&order=id.desc&limit=20")
        if not itens:
            print(f"  (nenhum registro em {a.tabela})")
        for i in itens:
            marca = "🚫" if i.get("deleted") else "  "
            resumo = i.get("titulo") or i.get("nome") or ""
            extra = " · ".join(str(i[c]) for c in ("categoria", "secao") if i.get(c))
            print(f"  {marca} id {i['id']:>3} | {resumo}{' [' + extra + ']' if extra else ''}")
        return

    # ---- montar filtro ----
    if a.ids:
        filtro = "id=in.(" + ",".join(x.strip() for x in a.ids.split(",") if x.strip()) + ")"
    elif a.categoria or a.secao:
        partes = []
        if a.categoria:
            partes.append("categoria=eq." + urllib.parse.quote(a.categoria))
        if a.secao:
            partes.append("secao=eq." + urllib.parse.quote(a.secao))
        filtro = "&".join(partes)
    else:
        sys.exit("❌ informe --ids (ou --categoria/--secao, ou --listar). "
                 "Por segurança não existe 'apagar tudo'.")

    # ---- o que será afetado ----
    try:
        _, alvos = _req(f"{a.tabela}?select=id&{filtro}")
    except urllib.error.HTTPError as e:
        sys.exit(f"❌ não consegui listar: HTTP {e.code}")
    if not alvos:
        sys.exit("  (nada encontrado com esse filtro)")
    ids = [r["id"] for r in alvos]
    print(f"  🎯 {len(ids)} registro(s) em {a.tabela}: {ids}")

    # ---- apagar ----
    try:
        if a.definitivo:
            status, _ = _req(f"{a.tabela}?{filtro}", metodo="DELETE")
            acao = "apagado(s) definitivamente"
        else:
            status, _ = _req(f"{a.tabela}?{filtro}", metodo="PATCH", corpo={"deleted": True})
            acao = "marcado(s) como deleted=true"
    except urllib.error.HTTPError as e:
        corpo = e.read().decode()[:200]
        sys.exit(f"❌ HTTP {e.code}: {corpo}")

    # ---- CONFERIR (a anon key mentia; a service_role não deve mentir, mas confira sempre) ----
    if a.definitivo:
        _, restantes = _req(f"{a.tabela}?select=id&id=in.({','.join(map(str, ids))})")
        ok = len(restantes) == 0
    else:
        _, restantes = _req(f"{a.tabela}?select=id&deleted=eq.false&id=in.({','.join(map(str, ids))})")
        ok = len(restantes) == 0

    print(f"  {'✅' if ok else '⚠️ '} HTTP {status} — {acao}")
    if ok:
        print("  ✅ conferido: não aparecem mais como ativos")
    else:
        print(f"  ⚠️  ainda ativos: {[r['id'] for r in restantes]}")


if __name__ == "__main__":
    main()
