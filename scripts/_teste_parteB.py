# -*- coding: utf-8 -*-
"""
FASE 5 · Parte B — valida o casamento por chave (mesma regra do js/main.js)
e testa se a anon key consegue APAGAR (para limpar sozinho).
"""
import sys, os, re, json, unicodedata, urllib.request, urllib.error

BASE = r"G:/.shortcut-targets-by-id/18wGiptBKUmAmmkKHgdfu05TU4y_roWC1/BBDPRINT - BACKUP/BBDPRINT/App BBDPRiNT/PROJETOS/Projeto SER Sagi/projeto_SER_Sagi - Hermes"
sys.path.insert(0, os.path.join(BASE, "scripts"))
from publicar import SUPABASE_URL, SUPABASE_ANON_KEY

HEADERS = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"}


def norm(t):
    t = unicodedata.normalize("NFD", (t or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", t))


def buscar(secao):
    url = (f"{SUPABASE_URL}/rest/v1/arquivo?select=id,titulo,imagem_url"
           f"&categoria=eq.Home&secao=eq.{secao}&deleted=eq.false&order=id.asc")
    req = urllib.request.Request(url)
    for k, v in HEADERS.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


# chaves que estao no HTML (lidas do proprio index.html, para nao inventar)
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
BLOCOS = {}
for bloco in ("pilares", "numeros", "como-ajudar"):
    BLOCOS[bloco] = re.findall(
        r'data-secao-img="%s" data-secao-chave="([^"]+)"' % re.escape(bloco), html)

print("=== CASAMENTO CHAVE -> FOTO (como o site faz) ===")
for bloco, chaves in BLOCOS.items():
    itens = buscar(bloco)
    por_chave = {norm(i["titulo"]): i for i in itens}
    print(f"\n  [{bloco}]  {len(itens)} foto(s) publicada(s)")
    for c in chaves:
        item = por_chave.get(norm(c))
        if item:
            print(f"     ✅ {c:20} → foto id {item['id']} ({item['titulo']!r})")
        else:
            print(f"     ⚪ {c:20} → sem foto (card fica como está)")

# ---- teste: a anon key apaga? ----
print("\n=== TESTE: a anon key consegue APAGAR? ===")
ids = [i["id"] for b in BLOCOS for i in buscar(b)]
print(f"  ids de teste a limpar: {ids}")
try:
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/arquivo?id=in.({','.join(map(str, ids))})",
                                 method="DELETE")
    for k, v in HEADERS.items():
        req.add_header(k, v)
    req.add_header("Prefer", "return=minimal")
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"  resposta HTTP {r.status}")
    restantes = [i["id"] for b in BLOCOS for i in buscar(b)]
    print(f"  ainda no banco: {restantes if restantes else 'nenhum ✅'}")
except urllib.error.HTTPError as e:
    print(f"  ❌ HTTP {e.code} — anon key não apaga (precisa de SQL)")
