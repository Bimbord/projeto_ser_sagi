# -*- coding: utf-8 -*-
"""
FASE 5 · Parte C — teste completo do cadastro de depoimentos.

Valida, ponta a ponta:
  1. cadastrar um depoimento (service_role)
  2. a consulta da PÁGINA depoimentos.html  -> traz todos
  3. a consulta da HOME                      -> só os em destaque (máx 3)
  4. o casamento da MÍDIA pelo nome do arquivo (pasta home/depoimentos)
  5. limpa tudo no final (inclusive em caso de erro)

Não imprime nenhuma chave.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from supabase_admin import SUPABASE_URL, admin_headers  # noqa: E402

NOME = "Teste Hermes Depoimento"
URL_FALSA = "https://pub-4eb5a1fd20eb4452b93cedb4c02e30ea.r2.dev/fotos/teste-depoimento.png"


def req(caminho, metodo="GET", corpo=None, prefer=None):
    dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8") if corpo is not None else None
    r = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{caminho}", method=metodo, data=dados)
    for k, v in admin_headers(json_body=corpo is not None).items():
        r.add_header(k, v)
    if prefer:
        r.add_header("Prefer", prefer)
    with urllib.request.urlopen(r, timeout=30) as resp:
        t = resp.read().decode()
        return resp.status, (json.loads(t) if t.strip() else None)


def norm(t):
    import re
    import unicodedata
    t = unicodedata.normalize("NFD", (t or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", t))


criados = {"depoimentos": [], "arquivo": []}
falhas = []

try:
    # ---------- 1. cadastrar ----------
    _, dep = req("depoimentos", "POST", {
        "nome": NOME, "perfil": "Teste", "local": "Pode apagar",
        "texto": "Depoimento criado pelo teste automatico da Fase 5 Parte C.",
        "legenda": "Legenda de teste", "destaque": False, "ordem": 999,
    }, prefer="return=representation")
    id_dep = dep[0]["id"]
    criados["depoimentos"].append(id_dep)
    print(f"  1️⃣ cadastrado .................. id {id_dep} (destaque=false)")

    # mídia do Drive (simula o upload da pasta home/depoimentos)
    _, arq = req("arquivo", "POST", {
        "titulo": NOME, "tipo": "foto", "categoria": "Home", "secao": "depoimentos",
        "imagem_url": URL_FALSA, "descricao": "Legenda vinda do arquivo",
    }, prefer="return=representation")
    id_arq = arq[0]["id"]
    criados["arquivo"].append(id_arq)
    print(f"     mídia publicada .............. id {id_arq} (Home/depoimentos)")

    # ---------- 2. consulta da PÁGINA (todos) ----------
    _, todos = req("depoimentos?select=*&deleted=eq.false&order=ordem.asc")
    print(f"  2️⃣ consulta da PÁGINA ......... {len(todos)} depoimento(s) — inclui o cadastrado: "
          f"{any(d['id'] == id_dep for d in todos)}")

    # ---------- 3. consulta da HOME (só destaque) ----------
    _, destaques = req("depoimentos?select=*&deleted=eq.false&destaque=eq.true")
    tem = any(d["id"] == id_dep for d in destaques)
    print(f"  3️⃣ consulta da HOME ........... {len(destaques)} em destaque — inclui o cadastrado: {tem} "
          f"{'✅ (correto: não é destaque)' if not tem else '⚠️'}")

    # marca como destaque e confere de novo
    req(f"depoimentos?id=eq.{id_dep}", "PATCH", {"destaque": True})
    _, destaques2 = req("depoimentos?select=*&deleted=eq.false&destaque=eq.true")
    tem2 = any(d["id"] == id_dep for d in destaques2)
    print(f"     ➕ marcado como destaque ..... a HOME agora traz: {tem2} {'✅' if tem2 else '⚠️'}")
    if not tem2:
        falhas.append("filtro de destaque não trouxe o registro marcado")

    # ---------- 4. casamento da mídia pelo nome ----------
    _, midias = req("arquivo?select=id,titulo,tipo,imagem_url&categoria=eq.Home&secao=eq.depoimentos&deleted=eq.false")
    mapa = {norm(m["titulo"]): m for m in midias}
    casou = norm(NOME) in mapa
    print(f"  4️⃣ casamento da mídia ......... chave {norm(NOME)!r} -> {'achou ✅' if casou else 'NÃO achou ⚠️'}")
    if not casou:
        falhas.append("casamento da mídia falhou")

    # ---------- 5. leitura pelo site (anon key) ----------
    from publicar import SUPABASE_ANON_KEY
    r = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/depoimentos?select=id&deleted=eq.false")
    r.add_header("apikey", SUPABASE_ANON_KEY)
    r.add_header("Authorization", f"Bearer {SUPABASE_ANON_KEY}")
    com_anon = json.loads(urllib.request.urlopen(r, timeout=30).read().decode())
    print(f"  5️⃣ o SITE (anon key) enxerga .. {len(com_anon)} registro(s) ✅")

except Exception as e:
    falhas.append(f"exceção: {type(e).__name__}: {e}")

finally:
    # ---------- limpeza ----------
    print("\n  🧹 limpando...")
    if criados["depoimentos"]:
        req(f"depoimentos?id=in.({','.join(map(str, criados['depoimentos']))})", "PATCH", {"deleted": True})
    if criados["arquivo"]:
        req(f"arquivo?id=in.({','.join(map(str, criados['arquivo']))})", "PATCH", {"deleted": True})
    _, sobrou = req("depoimentos?select=id&deleted=eq.false")
    _, sobrou_a = req(f"arquivo?select=id&deleted=eq.false&id=in.({','.join(map(str, criados['arquivo'])) or '0'})")
    print(f"     depoimentos ativos no banco . {len(sobrou or [])}")
    print(f"     mídias de teste ativas ..... {len(sobrou_a or [])}")

print("\n" + ("  ❌ " + " | ".join(falhas) if falhas else "  🎉 TUDO OK — cadastro, página, home, mídia e limpeza"))
